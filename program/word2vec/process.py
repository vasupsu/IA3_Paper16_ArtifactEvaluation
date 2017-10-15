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

#    ck.out ('in ck_postprocess word2vec')
#    cmd=json.dumps(, indent=2)
    cc={}
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
            os.rename (vectors_file, 'word2vec.words')
            ret=subprocess.Popen (['python',ph_path+'hyperwords/text2numpy.py',os.getcwd()+'/word2vec.words'], stdout=subprocess.PIPE)
            ck.out (ret.communicate()[0])
            ret1=subprocess.Popen (['python', ph_path+'hyperwords/ws_eval.py', 'embedding', 'word2vec', ph_path+'testsets/ws/ws353.txt'], stdout=subprocess.PIPE)
            eval_op = ret1.communicate()[0].split()

            token_no = 0
            for token in eval_op:
                if (token.strip()=="word2vec"):
                    cc['ws']=float(eval_op[token_no + 1].strip())
                token_no = token_no + 1
            ret2=subprocess.Popen (['python', ph_path+'hyperwords/analogy_eval.py', 'embedding', 'word2vec', ph_path+'testsets/analogy/google.txt'], stdout=subprocess.PIPE)
            eval_op = ret2.communicate()[0].split()
            token_no = 0
            for token in eval_op:
                if (token.strip()=="word2vec"):
                    cc['wa']=float(eval_op[token_no + 1].strip())
                token_no = token_no + 1
#            ck.out (cc['ws']+'-'+cc['wa'])

    # Load output as list.
    r=ck.load_text_file({'text_file':'word2vec_time','split_to_list':'yes'})
    if r['return']>0: return r
    r1=r['lst'][0].split(' ')
    cc['execution_time']=float(r1[0])
    if (os.path.isfile(vectors_file)):
        os.remove(vectors_file) 
    if (os.path.isfile('word2vec.words')):
        os.remove('word2vec.words')
        os.remove('word2vec.words.npy')
    return {'return':0, 'characteristics':cc}
