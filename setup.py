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
    install_requires=parse_reqs(),
    zip_safe=False,
    tests_require=[
        'pytest',
    ],
    setup_requires=[
        'pytest-runner',
    ]
)
