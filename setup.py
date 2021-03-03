from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name='dchelp',
    version='0.1',
    description='docker-compose wrappers',
    long_description=readme(),
    url='https://github.com/smokehill/dchelp',
    author='Valera Padolochniy',
    author_email='valera.padolochniy@gmail.com',
    license='MIT',
    packages=['dchelp'],
    entry_points={
        'console_scripts': ['dchelp=dchelp.main:main'],
    },
    classifiers=[
        'Environment :: Console',
        'License :: OSI Approved :: MIT',
        'Programming Language :: Python :: 2.7',
    ],
)