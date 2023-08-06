'''
'''

from os import environ as env

from duty import duty


__all__ = [
    'mkdocs',
    'login2gcp'
]


@duty
def mkdocs(ctx):
    '''
    Build & Serv the [MkDocs Documentation](https://www.mkdocs.org/) on 0.0.0.0:8008.
    '''

    ctx.run(
        'mkdocs build --config-file .mkdocs.yml --site-dir .html',
        title='Building documentation'
    )

    ctx.run(
        '. .venv/dev/bin/activate && mkdocs serve --config-file .mkdocs.yml --dev-addr 0.0.0.0:8008',
        title='Serving on http://localhost:8008/'
    )


@duty
def login2gcp(ctx):
    '''
    Login to Google Cloud Platform.
    Tried to read project_id from $GCP_PROJECT
    '''

    ctx.run(
        'gcloud beta auth login --update-adc --enable-gdrive-access --add-quota-project-to-adc --brief',
        title='Login'
    )

    project = env.get('GCP_PROJECT', None) or input('Please enter GCP project id: ')
    ctx.run(
        f'gcloud config set project {project}',
        title='Set project'
    )
