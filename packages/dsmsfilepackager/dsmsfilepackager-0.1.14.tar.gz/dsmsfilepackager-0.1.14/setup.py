from setuptools import setup

setup(
    name='dsmsfilepackager',
    version='0.1.14',
    author='Chris Horsley',
    author_email='chris.horsley@csirtfoundry.com',
    packages=['dsmsfilepackager'],
    scripts=[],
    url='http://bitbucket.org/dsms/dsmsfilepackager/',
    license='LICENSE.txt',
    description='',
    long_description=open('README').read(),
    install_requires=[
        "sftpsyncer==0.1.12",
        "python-magic"
    ],
)
