from setuptools import setup, find_packages

setup(
    name='bigjobbies',
    packages=find_packages(),
    install_requires=[
        'flask',
        'markdown',
        'python-dateutil',
        'xmljson',
    ],
)
