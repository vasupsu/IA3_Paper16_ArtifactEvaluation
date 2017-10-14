#
# Postprocessing program and converting
# raw output to the CK timing format.
#

import json
import os
import re
from shutil import copyfile
import subprocess

def ck_postprocess(i):

    ck=i['ck_kernel']
    env=i['env']
    deps=i['deps']

    cc={}
#    ck.out ('in ck_postprocess pSGNScc')
    # Path to hyperwords
    ph=deps['tool-hyperwords']
    ph_env=ph.get('dict',{}).get('env',{})
    ph_path=ph_env.get('CK_ENV_TOOL_HYPERWORDS_LIB','')
    ph_path = ph_path+'/'
    vectors_file=env.get('CK_OUTPUT',{});
    if (vectors_file != "vectors.txt"):
        if not (os.path.isfile(ph_path+'hyperwords/docopt.py')):
            if (os.path.isfile('../docopt.py')):
                copyfile ('../docopt.py', ph_path+'hyperwords/docopt.py')
            else:
                ck.out ('docopt.py not present')
        if (os.path.isfile(ph_path+'hyperwords/docopt.py')):
            os.rename (vectors_file, 'pSGNScc.words')
            ret=subprocess.Popen (['python',ph_path+'hyperwords/text2numpy.py',os.getcwd()+'/pSGNScc.words'], stdout=subprocess.PIPE)
            ck.out (ret.communicate()[0])
            ret1=subprocess.Popen (['python', ph_path+'hyperwords/ws_eval.py', 'embedding', 'pSGNScc', ph_path+'testsets/ws/ws353.txt'], stdout=subprocess.PIPE)
            eval_op = ret1.communicate()[0].split()
            token_no = 0
            for token in eval_op:
                if (token.strip()=="pSGNScc"):
                    cc['ws']=eval_op[token_no + 1].strip()
                token_no = token_no + 1
            
            ret2=subprocess.Popen (['python', ph_path+'hyperwords/analogy_eval.py', 'embedding', 'pSGNScc', ph_path+'testsets/analogy/google.txt'], stdout=subprocess.PIPE)
            eval_op = ret2.communicate()[0].split()
            token_no = 0
            for token in eval_op:
                if (token.strip()=="pSGNScc"):
                    cc['wa']=eval_op[token_no + 1].strip()
                token_no = token_no + 1
            ck.out (cc['ws']+"-"+cc['wa'])

    # Load output as list.
    r=ck.load_text_file({'text_file':'pSGNScc_time','split_to_list':'yes'})
    if r['return']>0: return r
    r1=r['lst'][0].split(' ')
    cc['execution_time']=float(r1[1])
    cc['create_in_m']=float(r1[5])
    cc['create_out_m']=float(r1[7])
    cc['sgd_time']=float(r1[3])
    cc['update_min']=float(r1[9])
    cc['update_mout']=float(r1[11])
    cc['overhead']=float(r1[13])
    cc['avg_windows']=float(r1[15])
    if (os.path.isfile(vectors_file)):
        os.remove(vectors_file)
    if (os.path.isfile('pSGNScc.words')):
        os.remove('pSGNScc.words')
        os.remove('pSGNScc.words.npy')

    return {'return':0, 'characteristics':cc}
