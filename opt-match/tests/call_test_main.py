import os, sys
from os.path import join
ROOT_DIR = os.path.abspath(os.curdir)
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)
    sys.path.append(join(ROOT_DIR, 'optmatch'))
import subprocess as sp
script = join(ROOT_DIR, 'optmatch','tests', 'call_test.py')

sp.call(['python', script, '10'])