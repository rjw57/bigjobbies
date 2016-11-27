import os
import shutil
import tempfile
import subprocess
from xml.etree.ElementTree import fromstring

from flask import current_app
from xmljson import badgerfish as bf

from . import sge

def gpuinfo():
    return bf.data(fromstring(subprocess.check_output([
        'nvidia-smi', '-q', '-x'])))

def submitjob(gitrepo, **kwargs):
    log_dir = current_app.config['LOG_DIR']
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    job_env = {
        'GIT_REPO': gitrepo,
        'GIT_BRANCH': kwargs.get('gitbranch', ''),
    }

    qsub_args = [
        '-e', os.path.join(log_dir, '$JOB_ID.log'),
        '-o', os.path.join(log_dir, '$JOB_ID.log'),
    ]

    for k, v in job_env.items():
        qsub_args.extend([
            '-v', '{}={}'.format(k, v),
        ])

    js = current_app.open_resource('scripts/container-job.sh')
    td = tempfile.TemporaryDirectory(prefix='bigjobbies')
    with js as js, td as td:
        job_path = os.path.join(td, 'job.sh')
        with open(job_path, 'wb') as f:
            shutil.copyfileobj(js, f)
        return sge.qsub(job_path, qsub_args)

