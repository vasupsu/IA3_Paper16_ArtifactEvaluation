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

    import json
    result = {'T' :[100000, 500000, 1000000, 2000000],
    'execution_time' : [0, 0, 0, 0],
    'overhead' : [0, 0, 0, 0],
    'avg_wins' : [0, 0, 0, 0]}

    cmd=json.dumps(result, indent=2)
#    ck.out (cmd)
    o=i.get('out','') # if con, then console output

    ck.out('Reproducing results for Table 3a ...')

    ck.out('')
    ck.out('Read program meta ...')

    r=ck.access({'action':'load',
                 'module_uoa':cfg['module_deps']['program'],
                 'data_uoa':cfg['programs_uoa']['pSGNScc']})
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
    ck.out('Compile pSGNScc ...')
    ck.out('')

    r=ck.access({'action':'compile',
                 'module_uoa':cfg['module_deps']['program'],
                 'data_uoa':cfg['programs_uoa']['pSGNScc'],
                 'deps':cdeps,
                 'speed':'yes'})
    if r['return']>0: return r

    # Get env UOA of installed packages
    ck.out('')
    ck.out('Get installed datasets ...')

    r=ck.access({'action':'search',
                 'module_uoa':cfg['module_deps']['env'],
                 'tags':'dataset,words',
                 'add_meta':'yes'})
    if r['return']>0: return r
    datasets=r['lst']

    threads=16
    for ds in datasets:
        dataset_uid=ds['data_uid']
        dataset_name=ds.get('meta',{}).get('env',{}).get('CK_ENV_DATASET_WORDSNAME','')
    
        if (dataset_name!="1b"):
            continue
        run_no = 0
        for T in result['T']:
#            ck.out ("T "+str(T))

            preset_deps={}
            preset_deps['dataset-words']=dataset_uid # force using this env
    
            ck.out('\n\t----------------------------------------------------------')
            ck.out('\tRunning pSGNScc using '+str(threads)+' threads, T='+str(T)+' on dataset ' + dataset_name)
            ck.out('\t----------------------------------------------------------')

            r=ck.access({'action':'run',
                        'module_uoa':cfg['module_deps']['program'],
                        'data_uoa':cfg['programs_uoa']['pSGNScc'],
                        'env':{'CK_WINDOW':'5', 'CK_SIZE':'300', 'CK_THREADS':threads, 'CK_ITER':'1', 'CK_MIN_COUNT':'2', 'CK_BATCH_SIZE':'11', 'CK_T':T},
                        'preset_deps':preset_deps})
            if r['return']>0: return r
    
            ch=r.get('characteristics',{})
            if ch.get('run_success','')!='yes':
                return {'return':1, 'error':'execution failed ('+ch.get('fail_reason','')+')'}
    
            cmd=json.dumps(ch, indent=2)
#            ck.out(cmd)
            result['execution_time'][run_no] = ch.get('execution_time','')
            result['overhead'][run_no] = ch.get('overhead','')
            result['avg_wins'][run_no] = ch.get('avg_windows','')
            run_no = run_no + 1

    cmd=json.dumps(result, indent=2)
#    ck.out(cmd)
    print "\n==================================================="
    print "           Table 3a: Performance impact of T"
    print "==================================================="
    print "{:<20}\t{:<30}".format('','Value of T')
    print "{:<20}\t{:<5}\t{:<5}\t{:<5}\t{:<5}".format('','100K','500K','1M','2M')
    print "{:<20}\t{:.3f}\t{:.3f}\t{:.3f}\t{:.3f}".format('Time per epoch(s)', result['execution_time'][0], result['execution_time'][1], result['execution_time'][2], result['execution_time'][3])
    print "{:<20}\t{:.3f}\t{:.3f}\t{:.3f}\t{:.3f}".format('Index time(s)',result['overhead'][0], result['overhead'][1], result['overhead'][2], result['overhead'][3])
    print "{:<20}\t{:.3f}\t{:.3f}\t{:.3f}\t{:.3f}".format('Avg. Rel Windows',result['avg_wins'][0], result['avg_wins'][1], result['avg_wins'][2], result['avg_wins'][3])
    print ""

    return {'return':0}
