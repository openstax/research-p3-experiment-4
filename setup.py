import codecs

from setuptools import find_packages, setup


def parse_reqs(req_path='./requirements.txt'):
    """Recursively parse requirements from nested pip files."""
    install_requires = []
    with codecs.open(req_path, 'r') as handle:
        # remove comments and empty lines
        lines = (line.strip() for line in handle
                 if line.strip() and not line.startswith('#'))

        for line in lines:
            # check for nested requirements files
            if line.startswith('-r'):
                # recursively call this function
                install_requires += parse_reqs(req_path=line[3:])

            else:
                # add the line as a new requirement
                install_requires.append(line)

    return install_requires


setup(
    long_description="",
    name="openstax-p3-exp-4",
    version="0.0.3",
    author="m1yag1",
    author_email="mike.arbelaez@rice.edu",
    py_modules=[],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "alembic==0.9.3",
        "aniso8601==1.2.1",
        "Babel==2.4.0",
        "bcrypt==3.1.3",
        "beautifulsoup4==4.6.0",
        "blinker==1.4",
        "boto==2.48.0",
        "cffi==1.10.0",
        "click==6.7",
        "coverage==4.4.1",
        "croniter==0.3.17",
        "cssselect==1.0.1",
        "factory-boy==2.8.1",
        "fake-factory==9999.9.9",
        "Faker==0.7.18",
        "Flask==0.12.2",
        "Flask-BabelEx==0.9.3",
        "Flask-Login==0.4.0",
        "Flask-Mail==0.9.1",
        "Flask-Principal==0.4.0",
        "Flask-Security==3.0.0",
        "Flask-SQLAlchemy==2.2",
        "Flask-Webpack==0.1.0",
        "Flask-WTF==0.14.2",
        "functools32>=3.2",
        "gunicorn==19.7.1",
        "inflection==0.3.1",
        "ipaddress==1.0.18",
        "itsdangerous==0.24",
        "Jinja2==2.9.6",
        "jsonschema==2.6.0",
        "logger==1.4",
        "lxml==3.8.0",
        "Mako==1.0.7",
        "Markdown==2.6.8",
        "MarkupSafe==1.0",
        "mirakuru==0.8.2",
        "numpy==1.13.1",
        "pandas==0.20.3",
        "passlib==1.7.1",
        "path.py==10.3.1",
        "pathlib==1.0.1",
        "port-for==0.4",
        "psutil==5.2.2",
        "psycopg2==2.7.3",
        "py==1.4.34",
        "pycparser==2.18",
        "pymlconf==0.7.3",
        "pyquery==1.2.17",
        "python-dateutil==2.6.1",
        "python-editor==1.0.3",
        "pytz==2017.2",
        "PyYAML==3.12",
        "redis==2.10.5",
        "rq==0.8.0",
        "rq-scheduler==0.7.0",
        "scipy==0.19.1",
        "six==1.10.0",
        "speaklater==1.3",
        "SQLAlchemy==1.1.12",
        "transitions==0.5.3",
        "ua-parser==0.7.3",
        "waitress==1.0.2",
        "WebOb==1.7.3",
        "WebTest==2.0.27",
        "Werkzeug==0.12.2",
        "WTForms==2.1"
    ],
    zip_safe=False,
    tests_require=[
        'pytest',
    ],
    extras_require=
    {
        'dev': [
            'pytest==3.1.3',
            'pytest-postgresql==1.3.0',
            'pytest-runner==2.11.1',
            'pytest-cov==2.5.1',
        ]
    },
    setup_requires=[
        'pytest-runner',
    ]
)
