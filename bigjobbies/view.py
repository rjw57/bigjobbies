import itertools
import os

from dateutil.parser import parse as date_parse
from flask import (
    abort, request, render_template, current_app, Markup, jsonify
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

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        job_num, job_name = engine.submitjob(
            gitrepo=request.values['gitrepo'], **request.values
        )
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

@app.route('/help')
def info():
    with current_app.open_resource('markdown/info.md') as f:
        content = Markup(markdown.markdown(f.read().decode('utf8')))
    return render_template('markdown.html', content=content)

@app.route('/api/qstat')
def api_qstat():
    return jsonify(sge.qstat())

@app.route('/api/gpuinfo')
def api_gpuinfo():
    return jsonify(engine.gpuinfo())
