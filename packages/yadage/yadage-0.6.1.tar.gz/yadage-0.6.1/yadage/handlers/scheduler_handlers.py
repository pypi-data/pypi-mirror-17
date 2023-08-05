import logging
import utils
import jsonpointer
import itertools
import copy
import jq
import jsonpath_rw

from yadage.yadagestep import yadagestep, initstep, outputReference
from yadage.yadagemodels import jsonStage
import  packtivity.statecontexts.poxisfs_context as statecontext

log = logging.getLogger(__name__)

handlers, scheduler = utils.handler_decorator()

# A scheduler does the following things:
#   - attached new nodes to the DAG
# - for each added step
#     - the step is given a name
#     - the step attributes are determined using the scheduler spec and context
#     - a list of used inputs (in the form of [stepname,outputkey,index])


def pointerize(jsondata, asref=False, stepid=None):
    '''
    a helper method that replaces leaf nodes in a JSON object with
    a outputReference objects (~ a JSONPath) pointing to that leaf position
    useful to track access to leaf nodes later on.
    '''
    allleafs = jq.jq('leaf_paths').transform(jsondata, multiple_output=True)
    leafpointers = [jsonpointer.JsonPointer.from_parts(x).path for x in allleafs]
    jsondata_proxy = copy.deepcopy(jsondata)
    for leaf in leafpointers:
        x = jsonpointer.JsonPointer(leaf)
        x.set(jsondata_proxy, outputReference(stepid, x) if asref else x.path)
    return jsondata_proxy


def select_reference(step, selection):
    '''
    resolves a jsonpath selection and returns JSONPointerized matches
    '''
    log.debug('selecting output from step %s',step)
    pointerized = pointerize(step.result, asref=True, stepid=step.identifier)
    matches = jsonpath_rw.parse(selection).find(pointerized)
    if not matches:
        log.error('no matches found for selection %s in result %s', selection, step.result)
        raise RuntimeError('no matches found in reference selection')

    if len(matches) > 1:
        log.error('found multiple matches to query: %s within result: %s\n \ matches %s', selection, step.result, matches)
        raise RuntimeError('multiple matches in result jsonpath query')
    return matches[0].value


def combine_outputs(outputs, flatten, unwrapsingle):
    combined = []
    for reference in outputs:
        if type(reference)==list:
            if flatten:
                for elementref in reference:
                    combined+=[elementref]
            else:
                combined+=[reference]
        else:
            combined+=[reference]
    if len(combined)==1 and unwrapsingle:
        combined = combined[0]
    return combined

def select_steps(stage,query):
    return stage.view.getSteps(query)


def select_outputs(steps,selection,flatten,unwrapsingle):
    return combine_outputs(map(lambda s: select_reference(s, selection), steps), flatten, unwrapsingle)


def resolve_reference(stage,selection):
    '''resolves a output reference by selecting the stage and stage outputs'''
    log.debug('resolving selection %s',selection)
    if type(selection) is not dict:
        return None
    else:
        steps = select_steps(stage, selection['stages'])
        log.debug('selected steps %s',steps)
        outputs = select_outputs(steps,
                                 selection['output'],
                                 selection.get('flatten', False),
                                 selection.get('unwrap', False))
        log.debug('selected outputs %s',outputs)
        return outputs


def select_parameter(stage,parameter):
    if type(parameter) is not dict:
        value = parameter
    else:
        value = resolve_reference(stage,parameter)
    return value


def finalize_value(stage,step,value,context):
    '''
    finalize a value by recursively resolving references and
    interpolating with the context when necessary
    '''
    if type(value)==outputReference:
        step.used_input(value)
        v = value.pointer.resolve(stage.view.dag.getNode(value.stepid).result)
        return finalize_value(stage,step,v,context)
    if type(value)==list:
        return [finalize_value(stage,step,x,context) for x in value]
    if type(value) in [str,unicode]:
        return value.format(**context)
    return value

def finalize_input(stage,step,json,context):
    '''
    evaluate final values of parameters by either resolving a
    reference to a upstream output or evaluating a static
    reference from the template (possibly string-interpolated)
    '''

    context = context.copy()
    context['workdir'] = context['readwrite'][0]
    result = {}
    for k,v in json.iteritems():
        if type(v) is not list:
            result[k] = finalize_value(stage,step,v,context)
        else:
            result[k] = [finalize_value(stage,step,element,context) for element in v]

    return result

def step_or_init(name,spec,context):
    if 'step' in spec:
        stepcontext = statecontext.make_new_context(name,context)
        return yadagestep(name = name, spec = spec['step'], context = stepcontext)
    elif 'workflow' in spec:
        return initstep('init {}'.format(name))


def addStepOrWorkflow(name,stage,step,spec):
    if type(step)==initstep:
        newcontext = statecontext.make_new_context(name,stage.context)
        subrules = [jsonStage(yml,newcontext) for yml in spec['workflow']['stages']]
        stage.addWorkflow(subrules, initstep = step)
    else:
        stage.addStep(step)

def get_parameters(spec):
    return {x['key']:x['value']for x in spec['parameters']}

@scheduler('singlestep-stage')
def singlestep_stage(stage,spec):
    '''
    a simple state that adds a single step/workflow. The node is attached
    to the DAG based on used upstream outputs
    '''
    log.debug('scheduling singlestep stage with spec:\n%s',spec)


    parameters = {
        k:select_parameter(stage,v) for k,v in get_parameters(spec).iteritems()
    }

    step = step_or_init(name = stage.name, spec = spec, context = stage.context)

    ctx = step.context if hasattr(step,'context') else stage.context
    finalized = finalize_input(stage,step,parameters,ctx)

    addStepOrWorkflow(stage.name,stage,step.s(**finalized),spec)

def scatter(parameters,scatter):
    commonpars = parameters.copy()
    to_scatter = {}
    for scatpar in scatter['parameters']:
        to_scatter[scatpar] = commonpars.pop(scatpar)

    singlesteppars=[]
    if scatter['method']=='zip':
        keys, zippable = zip(*[(k,v) for i,(k,v) in enumerate(to_scatter.iteritems())])

        for zipped in zip(*zippable):
            individualpars = dict(zip(keys,zipped))
            pars = commonpars.copy()
            pars.update(**individualpars)
            singlesteppars += [pars]

    if scatter['method']=='cartesian':
        for what in itertools.product(*[to_scatter[k] for k in scatter['parameters']]):
            individualpars = dict(zip(scatter['keys'],what))
            pars = commonpars.copy()
            pars.update(**individualpars)
            singlesteppars += [pars]
    return singlesteppars

@scheduler('multistep-stage')
def multistep_stage(stage,spec):
    '''
    a stage that attaches an array of nodes to the DAG. The number of nodes
    is determined by a scattering recipe. Currently two algs are supported
    'zip': one or more arrays of length n are iterated through in lock-step.
           n nodes are added to the DAG where the  parameters values are set to
           the values in the iteration
    'cartesian': a cartesian product of a number of arrays (possibly different sizes)
                 adds n1 x n2 x ... nj nodes.
    Nodes are attached to the DAG based on used upstream inputs
    '''
    log.debug('scheduling multistep stage with spec:\n%s',spec)
    parameters = {
        k:select_parameter(stage,v) for k,v in get_parameters(spec).iteritems()
    }
    singlesteppars = scatter(parameters,spec['scatter'])
    for i,pars in enumerate(singlesteppars):
        singlename = '{}_{}'.format(stage.name,i)
        step = step_or_init(name = singlename, spec = spec, context = stage.context)
        ctx = step.context if hasattr(step,'context') else stage.context
        ctx = ctx.copy()
        ctx.update(index = i)
        finalized = finalize_input(stage,step,pars,ctx)
        addStepOrWorkflow(singlename,stage,step.s(**finalized),spec)
