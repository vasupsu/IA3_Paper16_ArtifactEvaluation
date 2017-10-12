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
    ck.out ('in ck_postprocess pSGNScc')
    # Load output as list.
    r=ck.load_text_file({'text_file':'pWord2Vec_time','split_to_list':'yes'})
    if r['return']>0: return r
    ck.out (r['string'])
    r1=r['lst'][0].split(' ')
    cc['execution_time']=r1[1]
    cc['create_in_m']=r1[5]
    cc['create_out_m']=r1[7]
    cc['sgd_time']=r1[3]
    cc['update_min']=r1[9]
    cc['update_mout']=r1[11]
    cc['overhead']=r1[13]

    print json.dumps(cc, indent=2)
#            break

#    if len(cc)==0:
#       return {'return':1, 'error':'couldn\'t parse time in stdout'}

    return {'return':0, 'characteristics':cc}

# Do not add anything here!
