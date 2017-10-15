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
    result = [{
    'pword2vec' : [0, 0],
    'word2vec' : [0, 0],
    'pSGNScc' : [0, 0]},
    {
    'pword2vec' : [0, 0],
    'word2vec' : [0, 0],
    'pSGNScc' : [0, 0]}]

    cmd=json.dumps(result, indent=2)
#    ck.out (cmd)
    o=i.get('out','') # if con, then console output

    ck.out('Reproducing results for Table 2 ...')

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
        ck.out('\n---------------------------------------------')
        ck.out('Run with data set: '+dataset_name+' ('+dataset_uid+')')
        ck.out('---------------------------------------------')
        if (dataset_name=="1b" ):
            data_no = 1
#            continue
        else:
            data_no = 0
 
        run_no = 0
        threads = 16

        preset_deps={}
        preset_deps['dataset-words']=dataset_uid # force using this env

        ck.out('\n\t----------------------------------')
        ck.out('\tRunning Word2Vec using '+str(threads)+' threads')
        ck.out('\t----------------------------------')

        if (data_no==0):
            r=ck.access({'action':'run',
                    'module_uoa':cfg['module_deps']['program'],
                    'data_uoa':cfg['programs_uoa']['word2vec'],
                    'env':{'CK_THREADS':threads, 'CK_OUTPUT':'word2vec_text8.txt'},
                    'preset_deps':preset_deps})
        else:
            r=ck.access({'action':'run',
                    'module_uoa':cfg['module_deps']['program'],
                    'data_uoa':cfg['programs_uoa']['word2vec'],
                    'env':{'CK_WINDOW':'5', 'CK_SIZE':'300', 'CK_THREADS':threads, 'CK_ITER':'1', 'CK_MIN_COUNT':'2', 'CK_OUTPUT':'word2vec_1b.txt'},
                    'preset_deps':preset_deps})
        if r['return']>0: return r

        ch=r.get('characteristics',{})
        if ch.get('run_success','')!='yes':
            return {'return':1, 'error':'execution failed ('+ch.get('fail_reason','')+')'}

        result[data_no]['word2vec'][0] = ch.get('ws','')
        result[data_no]['word2vec'][1] = ch.get('wa','')
#        cmd=json.dumps(ch, indent=2)
#        ck.out(cmd)

        ck.out('\n\t----------------------------------')
        ck.out('\tRunning pWord2Vec using '+str(threads)+' threads')
        ck.out('\t----------------------------------')

        if (data_no==0):
            r=ck.access({'action':'run',
                    'module_uoa':cfg['module_deps']['program'],
                    'data_uoa':cfg['programs_uoa']['pword2vec'],
                    'env':{'CK_THREADS':threads, 'CK_OUTPUT':'pword2vec_text8.txt'},
                    'preset_deps':preset_deps})
        else:
            r=ck.access({'action':'run',
                    'module_uoa':cfg['module_deps']['program'],
                    'data_uoa':cfg['programs_uoa']['pword2vec'],
                    'env':{'CK_WINDOW':'5', 'CK_SIZE':'300', 'CK_THREADS':threads, 'CK_ITER':'1', 'CK_MIN_COUNT':'2', 'CK_BATCH_SIZE':'11', 'CK_OUTPUT':'pword2vec_1b.txt'},
                    'preset_deps':preset_deps})
        if r['return']>0: return r

        ch=r.get('characteristics',{})
        if ch.get('run_success','')!='yes':
            return {'return':1, 'error':'execution failed ('+ch.get('fail_reason','')+')'}

        result[data_no]['pword2vec'][0] = ch.get('ws','')
        result[data_no]['pword2vec'][1] = ch.get('wa','')
#        cmd=json.dumps(ch, indent=2)
#        ck.out(cmd)

        ck.out('\n\t----------------------------------')
        ck.out('\tRunning pSGNScc using '+str(threads)+' threads')
        ck.out('\t----------------------------------')

        if (data_no==0):
            r=ck.access({'action':'run',
                    'module_uoa':cfg['module_deps']['program'],
                    'data_uoa':cfg['programs_uoa']['pSGNScc'],
                    'env':{'CK_THREADS':threads, 'CK_OUTPUT':'pSGNScc_text8.txt'},
                    'preset_deps':preset_deps})
        else:
            r=ck.access({'action':'run',
                    'module_uoa':cfg['module_deps']['program'],
                    'data_uoa':cfg['programs_uoa']['pSGNScc'],
                    'env':{'CK_WINDOW':'5', 'CK_SIZE':'300', 'CK_THREADS':threads, 'CK_ITER':'1', 'CK_MIN_COUNT':'2', 'CK_BATCH_SIZE':'11', 'CK_OUTPUT':'pSGNScc_1b.txt'},
                    'preset_deps':preset_deps})
        if r['return']>0: return r

        ch=r.get('characteristics',{})
        if ch.get('run_success','')!='yes':
            return {'return':1, 'error':'execution failed ('+ch.get('fail_reason','')+')'}

#        cmd=json.dumps(ch, indent=2)
#        ck.out(cmd)
        result[data_no]['pSGNScc'][0] = ch.get('ws','')
        result[data_no]['pSGNScc'][1] = ch.get('wa','')
    
#        data_no = data_no + 1
#    cmd=json.dumps(result, indent=2)
#    ck.out(cmd)
    print "\n==================================================="
    print "           Table 2: Comparing Accuracy"
    print "==================================================="
    print "{:<12}\t{:<15}\t{:<15}".format('','Similarity','Analogy')
    print "{:<12}\t{:<5}\t{:<5}\t{:<5}\t{:<5}".format('','text8','1B','text8','1B')
    print "==================================================="
    print "{:<12}\t{:.3f}\t{:.3f}\t{:.3f}\t{:.3f}".format('Word2Vec', result[0]['word2vec'][0], result[1]['word2vec'][0], result[0]['word2vec'][1], result[1]['word2vec'][1])
    print "{:<12}\t{:.3f}\t{:.3f}\t{:.3f}\t{:.3f}".format('pWord2Vec',result[0]['pword2vec'][0], result[1]['pword2vec'][0], result[0]['pword2vec'][1], result[1]['pword2vec'][1])
    print "{:<12}\t{:.3f}\t{:.3f}\t{:.3f}\t{:.3f}".format('pSGNScc',result[0]['pSGNScc'][0], result[1]['pSGNScc'][0], result[0]['pSGNScc'][1], result[1]['pSGNScc'][1])
    print ""

    return {'return':0}
