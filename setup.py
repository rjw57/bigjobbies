from setuptools import setup, find_packages

setup(
    name='bigjobbies',
    packages=find_packages(),
    install_requires=[
        'docker-py',
        'flask',
        'lxml',
        'markdown',
        'psutil',
        'python-dateutil',
    ],
    package_data={
        'bigjobbies': [
            'docker/*/*', 'scripts/*', 'templates/*', 'templates/*/*',
            'markdown/*',
        ],
    },
)
