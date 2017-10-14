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
#    ck.out ('in ck_postprocess pword2vec')
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
            os.rename (vectors_file, 'pword2vec.words')
#            ck.out('python '+ph_path+' hyperwords/text2numpy.py '+os.getcwd()+'/pword2vec.words')
            ret=subprocess.Popen (['python',ph_path+'hyperwords/text2numpy.py',os.getcwd()+'/pword2vec.words'], stdout=subprocess.PIPE)
#            ck.out('python ' + ph_path+'hyperwords/ws_eval.py'+ ' embedding'+' pword2vec '+ph_path+'testsets/ws/ws353.txt')
            ret1=subprocess.Popen (['python', ph_path+'hyperwords/ws_eval.py', 'embedding', 'pword2vec', ph_path+'testsets/ws/ws353.txt'], stdout=subprocess.PIPE)
            eval_op = ret1.communicate()[0]
#            ck.out (eval_op)
            cc['ws']=eval_op.split (' ')[2].strip()
#            ck.out ('python '+ ph_path+'hyperwords/analogy_eval.py'+ ' embedding'+ ' pword2vec '+ ph_path+'testsets/analogy/google.txt')
            ret2=subprocess.Popen (['python', ph_path+'hyperwords/analogy_eval.py', 'embedding', 'pword2vec', ph_path+'testsets/analogy/google.txt'], stdout=subprocess.PIPE)
            eval_op = ret2.communicate()[0]
#            ck.out (eval_op)
            cc['wa']=eval_op.split (' ')[2].strip()
            ck.out (cc['ws'].strip()+'-'+cc['wa'].strip())

    # Load output as list.
    r=ck.load_text_file({'text_file':'pWord2Vec_time','split_to_list':'yes'})
    if r['return']>0: return r
#    ck.out (r['string'])
    r1=r['lst'][0].split(' ')
    cc['execution_time']=r1[1]
    cc['create_in_m']=r1[5]
    cc['create_out_m']=r1[7]
    cc['sgd_time']=r1[3]
    cc['update_min']=r1[9]
    cc['update_mout']=r1[11]
    cc['overhead']=r1[13]

    return {'return':0, 'characteristics':cc}
