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

    o=i.get('out','') # if con, then console output

    ck.out('Reproducing results for Figure 5a ...')

    ck.out('')
    ck.out('Read program meta ...')

    r=ck.access({'action':'load',
                 'module_uoa':cfg['module_deps']['program'],
                 'data_uoa':cfg['programs_uoa']['pword2vec']})
    if r['return']>0: return r

    prog_meta=r['dict']

    ck.out('')
    ck.out('Resolve compile dependencies ...')

    cdeps=prog_meta['compile_deps']
    ii={'action':'resolve',
        'module_uoa':cfg['module_deps']['env'],
        'deps':cdeps}
    rx=ck.access(ii)
    if rx['return']>0: return rx

    ck.out('')
    ck.out('Compile pword2vec ...')
    ck.out('')

    r=ck.access({'action':'compile',
                 'module_uoa':cfg['module_deps']['program'],
                 'data_uoa':cfg['programs_uoa']['pword2vec'],
                 'deps':cdeps,
                 'speed':'yes'})
    if r['return']>0: return r

#   import json
#    cmd=json.dumps(oo, indent=2)
#    ck.out('ooooo:' +cmd)
    # Get env UOA of installed packages
    ck.out('')
    ck.out('Get installed datasets ...')

    r=ck.access({'action':'search',
                 'module_uoa':cfg['module_deps']['env'],
                 'tags':'dataset,words',
                 'add_meta':'yes'})
    if r['return']>0: return r
    datasets=r['lst']

    for ds in datasets:
        dataset_uid=ds['data_uid']

        dataset_name=ds.get('meta',{}).get('env',{}).get('CK_ENV_DATASET_WORDSNAME','')

        ck.out('')
        ck.out('Run with data set: '+dataset_name+' ('+dataset_uid+')')
        ck.out('')

        preset_deps={}
        preset_deps['dataset-words']=dataset_uid # force using this env

        r=ck.access({'action':'run',
                    'module_uoa':cfg['module_deps']['program'],
                    'data_uoa':cfg['programs_uoa']['pword2vec'],
                    'env':{'CK_OUTPUT':'vectors.txt'},
                    'preset_deps':preset_deps})
        if r['return']>0: return r

    return {'return':0}
