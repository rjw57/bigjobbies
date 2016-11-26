# Useful information

This page documents some important information on the container.

## Overview

## Directories

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

