import os
import sys

from setuptools import setup


reqs = []
if [sys.version_info[0], sys.version_info[1]] < [2, 7]:
    reqs.append("simplejson>=2.0.9")

setup(
    name='avk-django-datadog',
    version='0.1.0.8',
    packages=[
        'datadog',
        'datadog.middleware'
    ],
    include_package_data=True,
    license='BSD',
    description=(
        'Simple Django middleware for submitting timings and exceptions to'
        ' Datadog.'),
    author='Conor Branagan',
    author_email='conor.branagan@gmail.com',
    url='https://github.com/conorbranagan/django-datadog',
    install_requires=reqs.extend([
        'dogapi==1.2.1'
    ])
)
