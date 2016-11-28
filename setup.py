from setuptools import setup, find_packages

setup(
    name='bigjobbies',
    packages=find_packages(),
    install_requires=[
        'docker-py',
        'flask',
        'lxml',
        'markdown',
        'python-dateutil',
    ],
)
