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

    ck.out('TBD: action description')

    ck.out('')
    ck.out('Command line: ')
    ck.out('')

    import json
    cmd=json.dumps(i, indent=2)

    ck.out(cmd)
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

    r=ck.access({'action':'run',
                     'module_uoa':cfg['module_deps']['program'],
                     'data_uoa':cfg['programs_uoa']['pword2vec'],
                     'env':{'CK_OUTPUT':'vectors.txt'}})
    if r['return']>0: return r
    cmd=json.dumps(r, indent=2)
    ck.out(cmd)
    return {'return':0}
