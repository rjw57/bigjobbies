import os
import shutil
import tempfile

from dateutil.parser import parse as date_parse
from flask import abort, request, render_template, jsonify, current_app

from .app import app
from . import sge

def log_path(job_number):
    log_dir = current_app.config['LOG_DIR']
    path  = os.path.join(log_dir, '{}.log'.format(job_number))
    if os.path.exists(path):
        return path
    else:
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        log_dir = current_app.config['LOG_DIR']
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        job_env = {
            'GIT_REPO': request.values['gitrepo'],
            'GIT_BRANCH': request.values.get('gitbranch', ''),
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
            job_num, job_name = sge.qsub(job_path, qsub_args)
        return render_template('submitted.html', job_num=job_num)
    return render_template('index.html')

@app.route('/qstat')
def qstat():
    qstat_out = sge.qstat()

    running_jobs = []
    for queue in qstat_out['job_info']['queue_info']['Queue-List']:
        job_list = queue.get('job_list', None)
        if job_list is None:
            continue
        if job_list.get('@state') != 'running':
            continue
        running_jobs.append(dict(
            queue=queue['name']['$'],
            number=job_list['JB_job_number']['$'],
            state='running',
            owner=job_list['JB_owner']['$'],
            start_time=date_parse(job_list['JAT_start_time']['$']),
        ))

    def parse_job(job):
        return dict(
            number=job['JB_job_number']['$'],
            state=job['@state'],
            owner=job['JB_owner']['$'],
            sub_time=date_parse(job['JB_submission_time']['$']),
            has_log=log_path(job['JB_job_number']['$']) is not None,
        )

    jobs = [
        parse_job(j)
        for j in qstat_out['job_info']['job_info']['job_list']
    ]

    return render_template('qstat.html', jobs=jobs, running_jobs=running_jobs)

@app.route('/log/<int:job_number>')
def log(job_number):
    path = log_path(job_number)
    if path is None:
        abort(404)

    with open(path) as f:
        log_text = f.read()

    return render_template('log.html', job_number=job_number, log_text=log_text)

@app.route('/api/qstat')
def api_qstat():
    return jsonify(sge.qstat())
