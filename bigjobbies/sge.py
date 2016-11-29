import re
import subprocess

from lxml import objectify

class SGEError(RuntimeError):
    pass

def qstat():
    return objectify.fromstring(subprocess.check_output([
        'qstat', '-u', '*', '-f', '-s', 'prsz', '-xml'
    ]))

QSUB_PATTERN = re.compile(r'Your job ([0-9]+) \("([^"]*)"\) has been submitted')

def qsub(job_script, name=None, extra_args=[]):
    if name is None:
        name = job_script

    # Sanitise name (see sge_types(1) for "name")
    name = re.sub(r'(\\n)|(\\t)|(\\r)|[/:@\\\*\?]', '_', name)

    sub_output = subprocess.check_output(
        ['qsub'] + extra_args + ['-N', name, job_script]
    ).decode('utf8')

    m = QSUB_PATTERN.search(sub_output)
    if not m:
        raise SGEError('unknown output from qsub: {}'.format(sub_output))

    g = m.groups()
    return int(g[0]), g[1]

def qdel(job_number, extra_args=[]):
    subprocess.check_call(['qdel'] + extra_args + [str(int(job_number))])

