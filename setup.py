from setuptools import setup, find_packages

setup(
    name='bigjobbies',
    packages=find_packages(),
    install_requires=[
        'docker-py',
        'flask',
        'future',
        'lxml',
        'markdown',
        'psutil',
        'pyjwt',
        'python-dateutil',
    ],
    package_data={
        'bigjobbies': [
            'docker/*/*', 'scripts/*', 'templates/*', 'templates/*/*',
            'markdown/*',
        ],
    },
)
