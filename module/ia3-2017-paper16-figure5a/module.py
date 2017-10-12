#
# Collective Knowledge ()
#
# 
# 
#
# Developer: 
#

cfg={}  # Will be updated by CK (meta descripti:0 on of this module)
work={} # Will be updated by CK (temporal data)
ck=None # Will be updated by CK (initialized CK kernel) 

# Local settings

##############################################################################
# Initialize module

def init(i):
    """

    Input:  {}

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """
    return {'return':0}

##############################################################################
# TBD: action description

def run_expt(i):
    """
    Input:  {
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    ck.out('Reproducing results for Figure 5a ...')

    r=ck.access({'action':'load',
                 'module_uoa':cfg['module_deps']['program'],
                 'data_uoa':cfg['programs_uoa']['pword2vec']})
    if r['return']>0: return r

    deps=r['dict']['compile_deps']
    ii={'action':'resolve',
        'module_uoa':cfg['module_deps']['env'],
        'deps':deps}
    rx=ck.access(ii)
    if rx['return']>0: return rx

    r=ck.access({'action':'compile',
                 'module_uoa':cfg['module_deps']['program'],
                 'data_uoa':cfg['programs_uoa']['pword2vec'],
                 'deps':deps,
                 'speed':'yes'})
    if r['return']>0: return r

    oo=[]
    r=ck.access({'action':'run',
                     'module_uoa':cfg['module_deps']['program'],
                     'data_uoa':cfg['programs_uoa']['pword2vec'],
                     'env':{'CK_OUTPUT':'vectors.txt'},
                     'out':oo})
    if r['return']>0: return r
    import json
    cmd=json.dumps(oo, indent=2)
    ck.out('ooooo:' +cmd)
    return {'return':0}
