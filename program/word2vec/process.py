#
# Postprocessing program and converting
# raw output to the CK timing format.
#

import json
import os
import re

def ck_postprocess(i):

    ck=i['ck_kernel']

    cc={}
    # Path to hyperwords
    ph=deps['tool-hyperwords']
    ph_env=ph.get('dict',{}).get('env',{})

    ph_path=ph_env.get('CK_ENV_TOOL_HYPERWORDS_LIB','')

    ck.out('path to hyperwords: '+ph_path)
    ck.out ('in ck_postprocess word2vec')
    # Load output as list.
    r=ck.load_text_file({'text_file':'word2vec_time','split_to_list':'yes'})
    if r['return']>0: return r
#    ck.out (r['string'])
    r1=r['lst'][0].split(' ')
    cc['execution_time']=r1[0]

    return {'return':0, 'characteristics':cc}
