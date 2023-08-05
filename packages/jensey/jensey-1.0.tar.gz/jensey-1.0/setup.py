from setuptools import setup

setup(
    name='jensey',
    author='Gao Tianchi',
    author_email='6159984@gmail.com',
    version='1.0',
    description='Imitate Shakespeare quote.',
    url='https://sdfgsad.com',
    install_requires=['setuptools', ],
    packages=['jensey'],
    entry_points={
        'console_scripts': ['shakespeare = jensey:hello_shakespeare']
    }
)
