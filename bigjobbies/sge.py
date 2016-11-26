import re
import subprocess
from xml.etree.ElementTree import fromstring

from xmljson import badgerfish as bf

class SGEError(RuntimeError):
    pass

def qstat():
    xml = fromstring(subprocess.check_output([
        'qstat', '-u', '*', '-f', '-s', 'prsz', '-xml'
    ]))
    return bf.data(xml)

QSUB_PATTERN = re.compile(r'Your job ([0-9]+) \("([^"]*)"\) has been submitted')

def qsub(job_script, extra_args=[]):
    sub_output = subprocess.check_output(
        ['qsub'] + extra_args + [job_script]
    ).decode('utf8')

    m = QSUB_PATTERN.search(sub_output)
    if not m:
        raise SGEError('unknown output from qsub: {}'.format(sub_output))

    g = m.groups()
    return int(g[0]), g[1]

