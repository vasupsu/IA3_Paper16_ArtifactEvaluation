#
# Copyright (c) 2017 cTuning foundation.
# See CK COPYRIGHT.txt for copyright details.
#
# SPDX-License-Identifier: BSD-3-Clause.
# See CK LICENSE.txt for licensing details.
#
# Convert raw output to CK format
#
# Developer(s):
#   - Grigori Fursin, cTuning foundation, 2017
#

import json
import os
import re
import struct


# Dummy (just for example)
def ck_preprocess(i):
    ck=i['ck_kernel']
    rt=i['run_time']

    meta=i['meta']
    env=i['env']

    return {'return':0}

# Postprocess stdout/stderr and convert to CK format (dummy)
def ck_postprocess(i):
    ck=i['ck_kernel']
    rt=i['run_time']
    env=i['env']
    deps=i['deps']

    raw_input('xyz')

    return {'return':0}

# Do not add anything here!
