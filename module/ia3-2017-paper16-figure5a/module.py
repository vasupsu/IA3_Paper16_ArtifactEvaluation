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
    result = [{'threads' :[1, 4, 8, 16],
    'pword2vec' : [0, 0, 0, 0],
    'word2vec' : [0, 0, 0, 0],
    'pSGNScc' : [0, 0, 0, 0]},
     {'threads' :[1, 4, 8, 16],
    'pword2vec' : [0, 0, 0, 0],
    'word2vec' : [0, 0, 0, 0],
    'pSGNScc' : [0, 0, 0, 0]}]

    cmd=json.dumps(result, indent=2)
#    ck.out (cmd)
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
    ck.out('Compile word2vec ...')
    ck.out('')

    r=ck.access({'action':'compile',
                 'module_uoa':cfg['module_deps']['program'],
                 'data_uoa':cfg['programs_uoa']['word2vec'],
                 'deps':cdeps,
                 'speed':'yes'})
    if r['return']>0: return r

    ck.out('')
    ck.out('Compile pword2vec ...')
    ck.out('')

    r=ck.access({'action':'compile',
                 'module_uoa':cfg['module_deps']['program'],
                 'data_uoa':cfg['programs_uoa']['pword2vec'],
                 'deps':cdeps,
                 'speed':'yes'})
    if r['return']>0: return r

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

    data_no = 0
    for ds in datasets:
        dataset_uid=ds['data_uid']
        dataset_name=ds.get('meta',{}).get('env',{}).get('CK_ENV_DATASET_WORDSNAME','')
        ck.out('---------------------------------------------')
        ck.out('Run with data set: '+dataset_name+' ('+dataset_uid+')')
        ck.out('---------------------------------------------')
        if (dataset_name=="1b" ):
            data_no = 1
        else:
            data_no = 0
        run_no = 0
        for threads in result[0]['threads']:
            if (threads < 16):
                run_no = run_no + 1
                continue
#            ck.out ("Threads "+str(threads))

    
            preset_deps={}
            preset_deps['dataset-words']=dataset_uid # force using this env
            ck.out('\t------------------------------')
            ck.out('\tRun Word2Vec using '+str(threads)+' threads')
            ck.out('\t------------------------------')
    
#            if (data_no==0):
            if (data_no==0):
                r=ck.access({'action':'run',
                        'module_uoa':cfg['module_deps']['program'],
                        'data_uoa':cfg['programs_uoa']['word2vec'],
                        'env':{'CK_THREADS':threads},
                        'preset_deps':preset_deps})
            else:
                r=ck.access({'action':'run',
                        'module_uoa':cfg['module_deps']['program'],
                        'data_uoa':cfg['programs_uoa']['word2vec'],
                        'env':{'CK_WINDOW':'5', 'CK_SIZE':'300', 'CK_THREADS':threads, 'CK_ITER':'1', 'CK_MIN_COUNT':'2'},
                        'preset_deps':preset_deps})
            if r['return']>0: return r
   
            ch=r.get('characteristics',{})
            if ch.get('run_success','')!='yes':
                return {'return':1, 'error':'execution failed ('+ch.get('fail_reason','')+')'}
   
            result[data_no]['word2vec'][run_no] = ch.get('execution_time','')
            if (data_no==0):
                result[data_no]['word2vec'][run_no] = result[data_no]['word2vec'][run_no]/10
            cmd=json.dumps(ch, indent=2)
#            ck.out(cmd)
   
            ck.out('\n\t------------------------------')
            ck.out('\tRun pWord2Vec using '+str(threads)+' threads')
            ck.out('\t------------------------------')
            if (data_no==0):
                r=ck.access({'action':'run',
                        'module_uoa':cfg['module_deps']['program'],
                        'data_uoa':cfg['programs_uoa']['pword2vec'],
                        'env':{'CK_THREADS':threads},
                        'preset_deps':preset_deps})
            else:
                r=ck.access({'action':'run',
                        'module_uoa':cfg['module_deps']['program'],
                        'data_uoa':cfg['programs_uoa']['pword2vec'],
                        'env':{'CK_WINDOW':'5', 'CK_SIZE':'300', 'CK_THREADS':threads, 'CK_ITER':'1', 'CK_MIN_COUNT':'2', 'CK_BATCH_SIZE':'11'},
                        'preset_deps':preset_deps})
            if r['return']>0: return r
    
            ch=r.get('characteristics',{})
            if ch.get('run_success','')!='yes':
                return {'return':1, 'error':'execution failed ('+ch.get('fail_reason','')+')'}
    
            result[data_no]['pword2vec'][run_no] = ch.get('execution_time','')
            if (data_no==0):
                result[data_no]['pword2vec'][run_no] = result[data_no]['pword2vec'][run_no]/10
            cmd=json.dumps(ch, indent=2)
#            ck.out(cmd)
    
            ck.out('\n\t------------------------------')
            ck.out('\tRun pSGNScc using '+str(threads)+' threads')
            ck.out('\t------------------------------')
            if (data_no==0):
                r=ck.access({'action':'run',
                        'module_uoa':cfg['module_deps']['program'],
                        'data_uoa':cfg['programs_uoa']['pSGNScc'],
                        'env':{'CK_THREADS':threads},
                        'preset_deps':preset_deps})
            else:
                r=ck.access({'action':'run',
                        'module_uoa':cfg['module_deps']['program'],
                        'data_uoa':cfg['programs_uoa']['pSGNScc'],
                        'env':{'CK_WINDOW':'5', 'CK_SIZE':'300', 'CK_THREADS':threads, 'CK_ITER':'1', 'CK_MIN_COUNT':'2', 'CK_BATCH_SIZE':'11'},
                        'preset_deps':preset_deps})
            if r['return']>0: return r
    
            ch=r.get('characteristics',{})
            if ch.get('run_success','')!='yes':
                return {'return':1, 'error':'execution failed ('+ch.get('fail_reason','')+')'}
    
            cmd=json.dumps(ch, indent=2)
#            ck.out(cmd)
            result[data_no]['pSGNScc'][run_no] = ch.get('execution_time','')
            if (data_no==0):
                result[data_no]['pSGNScc'][run_no] = result[data_no]['pSGNScc'][run_no]/10
    
            run_no = run_no + 1
#        data_no = data_no + 1
    cmd=json.dumps(result, indent=2)
#    ck.out(cmd)
    print "\n======================================================="
    print "              Data to verify Figure 5C"
    print "======================================================="
    print "text8 dataset"
    print "============="
    print "{:<17}\t\t{:<20}".format(' ','Number of cores')
    print "{:<17}\t{:2d}\t{:2d}\t{:2d}\t{:2d}".format('',1,4,8,16)
    print "{:<17}\t{:.2f}\t{:.2f}\t{:.2f}\t{:.2f}".format('Word2Vec',result[0]['word2vec'][0], result[0]['word2vec'][1], result[0]['word2vec'][2], result[0]['word2vec'][3])
    print "{:<17}\t{:.2f}\t{:.2f}\t{:.2f}\t{:.2f}".format('pWord2Vec',result[0]['pword2vec'][0], result[0]['pword2vec'][1], result[0]['pword2vec'][2], result[0]['pword2vec'][3])
    print "{:<17}\t{:.2f}\t{:.2f}\t{:.2f}\t{:.2f}".format('pSGNScc',result[0]['pSGNScc'][0], result[0]['pSGNScc'][1], result[0]['pSGNScc'][2], result[0]['pSGNScc'][3])
    print "============="
    print "1B dataset"
    print "============="
    print "{:<17}\t\t{:<20}".format(' ','Number of cores')
    print "{:<17}\t{:2d}\t{:2d}\t{:2d}\t{:2d}".format('',1,4,8,16)
    print "{:<17}\t{:.2f}\t{:.2f}\t{:.2f}\t{:.2f}".format('Word2Vec',result[1]['word2vec'][0], result[1]['word2vec'][1], result[1]['word2vec'][2], result[1]['word2vec'][3])
    print "{:<17}\t{:.2f}\t{:.2f}\t{:.2f}\t{:.2f}".format('pWord2Vec',result[1]['pword2vec'][0], result[1]['pword2vec'][1], result[1]['pword2vec'][2], result[1]['pword2vec'][3])
    print "{:<17}\t{:.2f}\t{:.2f}\t{:.2f}\t{:.2f}".format('pSGNScc',result[1]['pSGNScc'][0], result[1]['pSGNScc'][1], result[1]['pSGNScc'][2], result[1]['pSGNScc'][3])

    return {'return':0}
