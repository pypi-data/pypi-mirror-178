from setuptools import setup, find_packages

setup(
    name='dictogc',
    version='0.0.7',
    packages=find_packages(),
    url='https://bitbucket.org/submax82/dictogc/src/master/',
    license='GPL',
    author='massimo',
    author_email='massimo.cavalleri@gmail.com',
    description='sync dipendentincloud.it timesheet with google calendar',
    install_requires=[
        'requests',
        'gcsa',
        'appdirs',
        'python-dateutil'
    ],
    entry_points={
        'console_scripts': [
            'dictogc=dictogc.dictogc:main',
        ],
    }
)
