import os
from setuptools import setup, find_packages


def read_content(filename):
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)) as f:
        content = f.read()

    return content


def get_version():
    global_names = {}
    exec(
        read_content('minesweeper/version.py'),
        global_names
    )
    return global_names['__version__']


setup(
    name='ascii-minesweeper',
    version=get_version(),
    description='An interactive minesweeper game for your terminal.',
    long_description=read_content('README.md'),
    long_description_content_type='text/markdown',
    author='Nathaniel Young',
    author_email='',
    maintainer='Nathaniel Young',
    maintainer_email='',
    url='https://github.com/nyoungstudios/ascii-minesweeper',
    license='MIT',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'minesweeper = minesweeper.play:main',
            'ascii-minesweeper = minesweeper.play:main'
        ]
    },
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Games/Entertainment :: Puzzle Games',
        'Topic :: Terminals'
    ],
    keywords='minesweeper ascii ascii-art terminal game python',
    setup_requires=['numpy'],
    install_requires=['numpy']
)
