'''
Commands for manipulating a virtual environments.
'''

# pylint: disable=missing-module-docstring

from duty import duty


__all__ = [
    'init',
    'activate',
    'freeze'
]


@duty
def init(ctx, name: str = 'dev'):
    '''
    Initialize environment in .venv/{name}. Default name=dev. You can use ```duty init name```

    Args:
        venv: Name of your virtual environment.
    '''

    ctx.run(f'python3.10 -m venv .venv/{name}', title='Make venv')
    ctx.run(f'. .venv/{name}/bin/activate', title='Activate')
    ctx.run('pip3 install --upgrade pip', title='Upgrade pip')
    ctx.run('pip3 install --upgrade wheel pylint isort ipykernel', title='Base install')
    ctx.run(f'pip3 install --upgrade -r .venv/{name}.req', title='Installing requirements')
    ctx.run(f'pip3 freeze > .venv/{name}.req', title=f'Upgrade {name}.req file')


@duty
def activate(ctx, name: str = 'dev'):
    '''
    Activate environment from .venv/{name}. Default name=dev. You can use ```duty activate name```

    Args:
        venv: Name of your virtual environment.
    '''

    ctx.run(f'. .venv/{name}/bin/activate', title='Activating')


@duty
def freeze(ctx, name: str = 'dev'):
    '''
    Freeze current environment to .venv/{name}.req. Default name=dev. You can use ```duty freeze name```

    Args:
        venv: Name of your virtual environment.
    '''

    ctx.run(f'pip3 freeze > .venv/{name}.req', title='Freeze environment')
