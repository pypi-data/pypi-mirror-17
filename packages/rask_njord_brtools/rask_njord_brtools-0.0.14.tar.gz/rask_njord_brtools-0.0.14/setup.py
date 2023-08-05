import os
from setuptools import find_packages,setup
from subprocess import check_output

f_version = os.path.join(os.path.dirname(__file__), 'version.py')

def git_version():
    try:
        v = check_output(['git','describe','--tags']).rstrip().split('-')
        v = '%s.%s' % (v[0],v[1])

        f_v = open(f_version,'w')
        f_v.write(v)
        f_v.close()
    except:
        v = open(f_version,'r').read()
    return v

setup(
    description='Rask BRTools Client',
    install_requires=[
        'rask',
    ],
    license='https://gitlab.com/vikingmakt/rask_njord_brtools/raw/master/LICENSE',
    maintainer='Umgeher Torgersen',
    maintainer_email='me@umgeher.org',
    name='rask_njord_brtools',
    packages=find_packages(),
    url='https://gitlab.com/vikingmakt/rask_njord_brtools',
    version=git_version()
)
