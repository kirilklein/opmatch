from setuptools import setup, find_packages

setup(
    name='opmatch',
    version='0.1.1.dev0',
    author="Kiril Klein",
    author_email="kikl@di.ku.dk",
    description="A small package to perform optimal matching based on propensity scores.",
    packages=find_packages(),
    url="https://github.com/kirilklein/opt-match",
    license='MIT',
    long_description=open('README.md').read(),
)