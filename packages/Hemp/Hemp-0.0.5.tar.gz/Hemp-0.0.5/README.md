# Hemp

Tools for Fabric

## Installation

`pip install hemp`

## Usage

Hemp executable wraps Fabric and performs some subtle actions, like, loading default tasks and configuration files before
Fabric executed. The command line interface is not any different than Fabric itself, so, running your tasks
as usual and replacing `fab` with `hemp` should work out of the box.

## Differences from Fabric

### Fabfile location

By default, Fabric will load `fabfile.py` from current working directory or any of the parent directories.
Hemp extends this functionality to include `fabfile.py` located in `$HOME` of the current user.

This allows you to define your custom tasks in one file, and use them without specifying the file location specifically.