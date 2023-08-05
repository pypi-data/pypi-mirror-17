# -*- coding: utf-8 -*-
# -- This file is part of the Apio project
# -- (C) 2016 FPGAwars
# -- Author Jesús Arroyo
# -- Licence GPLv2

import click

from apio.managers.project import Project

# Python3 compat
try:
    unicode = str
except NameError:  # pragma: no cover
    pass


@click.command('init')
@click.pass_context
@click.option('-s', '--scons', is_flag=True,
              help='Create default SConstruct file.')
@click.option('-b', '--board', type=unicode, metavar='BOARD',
              help='Create init file with the selected board.')
@click.option('--project-dir', type=unicode, metavar='PATH',
              help='Set the target directory for the project')
def cli(ctx, board, scons, project_dir):
    """Manage apio projects."""

    if scons:
        Project().create_sconstruct(project_dir)
    elif board:
        Project().create_ini(board, project_dir)
    else:
        click.secho(ctx.get_help())
