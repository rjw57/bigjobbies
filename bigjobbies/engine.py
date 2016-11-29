import collections
import getpass
import os
import shutil
import subprocess
import tempfile

import docker
from flask import current_app
from lxml import objectify

from . import sge

JobSpec = collections.namedtuple(
    'JobSpec', 'id description job_script image_subtype')

JOB_SPECS = [
    JobSpec('cpu_only', 'CPU only', 'cpu-job.sh', 'cpu'),
    JobSpec('gpu_cuda', 'CUDA (GPU)', 'cuda-job.sh', 'cuda'),
]

IMAGE_SUB_TYPES = list(set([js.image_subtype for js in JOB_SPECS]))

def gpuinfo():
    return objectify.fromstring(
        subprocess.check_output(['nvidia-smi', '-q', '-x']))

def submitjob(script, name=None, job_env={}):
    if name is None:
        name = script

    log_dir = os.path.join(
        current_app.instance_path, current_app.config['LOG_DIR'])
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
    app. Returns only images which are marked as worker images.

    """
    cli = docker.Client()
    worker_label = '{}worker'.format(current_app.config['LABEL_NS'])
    user_label = '{}user'.format(current_app.config['LABEL_NS'])
    def is_our_image(im):
        labels = im.get('Labels', {})
        if labels is None or worker_label not in labels:
            return False
        if labels.get(user_label) != getpass.getuser():
            return False
        tag_prefix = '{}/{}:'.format(
            current_app.config['APP_PREFIX'], getpass.getuser())
        return any(t.startswith(tag_prefix) for t in im.get('RepoTags', []))
    return [im for im in cli.images() if is_our_image(im)]

def delete_images():
    cli = docker.Client()
    for im_id in [im['Id'] for im in docker_images()]:
        cli.remove_image(im_id, noprune=False, force=True)

def missing_images():
    """Return a sequence of image tags which are missing. (I.e. they have not
    yet been built.)

    """
    all_types = []
    type_label = '{}type'.format(current_app.config['LABEL_NS'])
    for im in docker_images():
        labels = im.get('Labels', {})
        if labels is None or type_label not in labels:
            continue
        all_types.append(labels[type_label])
    return list(set(IMAGE_SUB_TYPES).difference(all_types))
