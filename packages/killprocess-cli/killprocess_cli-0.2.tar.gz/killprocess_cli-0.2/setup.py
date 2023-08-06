from setuptools import setup, find_packages

setup(
    name='killprocess_cli',
    version='0.2',
    description='Kills Process using grep',
    url='http://github.com/tushark39',
    author='Tushar Pandey',
    author_email='tushark39@gmail.com',
    license='MIT',
    install_requires=[],
    packages=find_packages(),
    entry_points={
        'console_scripts' : [
            'killprocess = killprocess_cli.__init__:main'
        ]
    }
)
