# Useful information

This page documents some important information on the container.

## Overview

The lab GPU server provides a facility whereby compute jobs can be submitted to
a queue and run "fairly" such that each user can get a fair slice of the
resource. Usually a user specifies the requirements for a job, for example that
it should use two CPUs and 4GB of memory, and the job scheduler arranges for the
job to be run when the resources are available.

Unfortunately there's not much in the way of enforcement. Usually this is not a
problem but it is very easy to inadvertently use the wrong GPU when running a
job. A modern solution to this problem is the <em>container</em>. This is a way
by which a job may be "isolated" from the main compute environment and run in
it's own environment. Usefully for our needs, the container can arrange for all
but the correct GPU to be "hidden" to guard against inadvertent use of the wrong
GPU.

## Repository driven job specification

If you've used services such as <a href="https://travis-ci.org">Travis CI</a>,
you'll be familiar with the workflow: you give a cloud server the location of
your git repository, the server clones the latest version of your code and runs
a script corresponding to your test suite. Our system is similar: jobs are no
longer specified as <tt>.sh</tt> files. Instead you simply point the job
scheduler to your git repository and you code is cloned and run for you.

Unlike Travis CI and the like, this server allows for some access to local
files. This allows you to store shared datasets, persist output and to clone
from git repositories which are hosted within the yoshi scratch space and not in
the cloud.

## Directories

The containers have some restricted access to the local filesystem by way of a
few well-known directories:

<table class="bordered">
  <thead><th>Path</th><th>Descriptions</th></thead>
  <tbody>
    <tr>
      <td style="vertical-align: top"><tt>/repo</tt></td>
      <td>
        The specified git repository is cloned to this directory. This directory
        exists only as long as the container runs so don't save output data to
        this directory. Use <tt>/workspace</tt> for output data.
      </td>
    </tr>
    <tr>
      <td style="vertical-align: top"><tt>/workspace</tt></td>
      <td>
        The user's private workspace. The container is given full read and
        write permissions within this directory. On yoshi, this directory
        is mapped to <tt>/scratch/$USER</tt>.
    </tr>
    <tr>
      <td style="vertical-align: top"><tt>/data</tt></td>
      <td>
        Shared data storage. The container is only given read access to this
        directory. It is intended to store datasets but not output. On yoshi,
        this directory is mapped to <tt>/scratch</tt>.
      </td>
    </tr>
  </tbody>
</table>

