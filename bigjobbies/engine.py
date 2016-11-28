import getpass
import os
import shutil
import subprocess
import tempfile

import docker
from flask import current_app
from lxml import objectify

from . import sge

def image_tags():
    return ['{}:{}'.format(current_app.config['IMAGE_PREFIX'], n) for n in [
        'cuda',
    ]]

def gpuinfo():
    return objectify.fromstring(subprocess.check_output([
        'nvidia-smi', '-q', '-x']))

def submitjob(script, name=None, job_env={}):
    if name is None:
        name = script

    log_dir = current_app.config['LOG_DIR']
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    qsub_args = [
        '-e', os.path.join(log_dir, '$JOB_ID.log'),
        '-o', os.path.join(log_dir, '$JOB_ID.log'),
    ]

    for k, v in job_env.items():
        qsub_args.extend([
            '-v', '{}={}'.format(k, v),
        ])

    js = current_app.open_resource(os.path.join('scripts', script))
    td = tempfile.TemporaryDirectory(prefix=current_app.config['APP_PREFIX'])
    with js as js, td as td:
        job_path = os.path.join(td, 'job.sh')
        with open(job_path, 'wb') as f:
            shutil.copyfileobj(js, f)
        return sge.qsub(job_path, name=name, extra_args=qsub_args)

def docker_images():
    """Get a set of docker image dicts (see docker-py) which correspond to this
    app. Returns only images which are tagged with IMAGE_TAG.

    """
    cli = docker.Client()
    tag = current_app.config['IMAGE_TAG']
    tag_set = set(image_tags())
    return [im for im in cli.images()
            if tag in im.get('RepoTags', [])]

def missing_images():
    """Return a sequence of image tags which are missing. (I.e. they have not
    yet been built.)

    """
    all_tags = []
    for im in docker_images():
        all_tags.extend(im.get('RepoTags', []))
    return set(image_tags()).difference(all_tags)
