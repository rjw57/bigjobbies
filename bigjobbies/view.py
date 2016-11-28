import datetime
import itertools
import os

from dateutil.parser import parse as date_parse
from flask import (
    abort, request, render_template, current_app, Markup,
    redirect, flash, url_for, Response
)
import markdown

from .app import app
from . import sge
from . import engine

def log_path(job_number):
    log_dir = current_app.config['LOG_DIR']
    path  = os.path.join(log_dir, '{}.log'.format(job_number))
    if os.path.exists(path):
        return path
    else:
        return None

@app.route('/')
def index():
    return redirect(url_for('submit'))

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    missing = engine.missing_images()
    if len(missing) > 0:
        return render_template('needimage.html', missing=missing)

    image = [im for im in engine.docker_images()
             if any(t.endswith(':cuda') for t in im.get('RepoTags', []))][0]

    if request.method == 'POST':
        job_num, job_name = engine.submitjob(
            script='container-job.sh',
            name='Container job from {}'.format(request.values['gitrepo']),
            job_env={
                'GIT_REPO': request.values['gitrepo'],
                'GIT_BRANCH': request.values.get('gitbranch', ''),
                'CONTAINER_TAG': image['Id'],
            }
        )

        flash('Job #{} submitted'.format(job_num))
        return redirect(url_for('qstat'))
    return render_template('submit.html')

@app.route('/images')
def images():
    return render_template(
        'images.html', images=engine.docker_images(),
        fromtimestamp=datetime.datetime.fromtimestamp)

@app.route('/images/build', methods=['POST'])
def build_images():
    if request.method != 'POST':
        abort(403) # Forbidden

    job_num, job_name = engine.submitjob(
        script='build-containers.sh',
        name=r'Build container images',
        job_env={
            'CONTAINER_DIR': os.path.join(app.root_path, 'docker'),
            'IMAGE_TAG': current_app.config['IMAGE_TAG'],
            'IMAGE_PREFIX': current_app.config['IMAGE_PREFIX'],
        },
    )

    flash('Job #{} submitted'.format(job_num))
    return redirect(url_for('qstat'))

@app.route('/images/delete', methods=['POST'])
def delete_images():
    if request.method != 'POST':
        abort(403) # Forbidden

    engine.delete_images()
    return redirect(url_for('images'))

def parse_qstat():
    qstat_out = sge.qstat()

    running_jobs = []
    for queue in qstat_out.queue_info['Queue-List']:
        try:
            job_list = queue.job_list
        except AttributeError:
            continue
        if job_list is None or job_list.get('state', '') != 'running':
            continue
        running_jobs.append(dict(
            queue=queue.name,
            number=job_list.JB_job_number,
            name=job_list.JB_name,
            state='running',
            owner=job_list.JB_owner,
            start_time=date_parse(job_list.JAT_start_time.text),
        ))

    def parse_job(job):
        return dict(
            number=job.JB_job_number,
            state=job.get('state'),
            owner=job.JB_owner,
            name=job.JB_name,
            sub_time=date_parse(job.JB_submission_time.text),
            has_log=log_path(job.JB_job_number) is not None,
        )

    jobs = [
        parse_job(j)
        for j in qstat_out.job_info.job_list
    ]

    return dict(jobs=jobs, running_jobs=running_jobs)

@app.route('/qstat')
def qstat():
    return render_template('qstat.html', **parse_qstat())

@app.route('/qstat/update')
def qstat_update():
    return render_template('qstat_dynamic.html', **parse_qstat())

@app.route('/gpuinfo')
def gpuinfo():
    return render_template(
        'gpuinfo.html', smi=engine.gpuinfo())

@app.route('/gpuinfo/update')
def gpuinfo_update():
    return render_template(
        'gpuinfo_dynamic.html', smi=engine.gpuinfo())

PREFIXES = {
    'O:': 'stdout', 'E:': 'stderr', 'I:': 'info', 'C:': 'command',
    'S:': 'section',
}

@app.route('/log/<int:job_number>')
def log(job_number):
    path = log_path(job_number)
    if path is None:
        abort(404)

    sections = []
    current_section = dict(blocks=[], title='Log', line_count=0)
    current_section_title = ''
    with open(path) as f:
        line_prefix = lambda l: l[:2] if l[:2] in PREFIXES else ''
        for k, lines in itertools.groupby(f, line_prefix):
            lines = [l[len(k):].rstrip() for l in lines]
            if PREFIXES.get(k) == 'section':
                if len(current_section['blocks']) > 0:
                    sections.append(current_section)
                current_section = dict(
                    blocks=[], title=''.join(lines).strip(), line_count=0)
            else:
                current_section['blocks'].append(
                    dict(type=PREFIXES.get(k), text=lines))
                current_section['line_count'] += len(lines)
    if len(current_section['blocks']) > 0:
        sections.append(current_section)

    return render_template(
        'log.html', job_number=job_number, sections=sections)

@app.route('/log/<int:job_number>/raw')
def log_raw(job_number):
    path = log_path(job_number)
    if path is None:
        abort(404)
    with open(path) as f:
        return Response(f.read(), mimetype='text/plain')

@app.route('/help')
def info():
    with current_app.open_resource('markdown/info.md') as f:
        content = Markup(markdown.markdown(f.read().decode('utf8')))
    return render_template('markdown.html', content=content)
