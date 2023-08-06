'''
Commands for work with python packages source code.
'''


from os import (
    environ as env,
    path
)

from shutil import rmtree
from duty import duty
import yaml


__all__ = [
    'install',
    'uninstall'
]


@duty
def install(ctx):
    '''
    Install the current package locality from source.
    '''

    env['CI_PIPELINE_IID'] = '0'
    env['BUILD_SUFFIX'] = 'dev'

    with open('./setup.yml', 'r', encoding='utf-8') as vars_file:
        conf = yaml.safe_load(vars_file)

    install_cmd = ''.join(
        [
            'pip3.10 install --force-reinstall --no-build-isolation --user ./dist/',
            f'{conf["NAMESPACE"].replace(".", "-")}-{conf["VERSION"]}.{env["BUILD_SUFFIX"]}0.tar.gz; ',
        ]
    )

    try:
        ctx.run('python3 -m build --no-isolation .', title='Building')
        ctx.run(install_cmd, title='Installing')
    finally:
        rmtree(f'{conf["NAMESPACE"].replace(".", "_")}.egg-info', ignore_errors=True)
        rmtree(f'{path.join(env["PWD"], "dist")}', ignore_errors=True)


@duty
def uninstall(ctx):
    '''
    Uninstalling current package from an activate environment.
    '''

    with open('./setup.yml', 'r', encoding='utf-8') as vars_file:
        conf = yaml.safe_load(vars_file)

    package = conf['NAMESPACE'].replace('.', '-')
    ctx.run(f'pip3 uninstall {package}', title='Uninstalling')
