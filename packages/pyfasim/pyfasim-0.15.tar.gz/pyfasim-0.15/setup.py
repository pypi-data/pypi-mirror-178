from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='pyfasim',
    version='0.15',
    description='Python Finite Automata Simulator',
    keywords='deterministic non-determistic finite automata pushdown turing',
    author='Samy Zafrany',
    #url='https://www.samyzaf.com/afl/pyfasim.html',
    author_email='sz@samyzaf.com',
    license='MIT',
    packages=['pyfasim'],
    install_requires=['automata-lib'],
    zip_safe=False,
)

