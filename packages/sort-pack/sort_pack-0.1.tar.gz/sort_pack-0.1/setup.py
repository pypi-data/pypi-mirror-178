from os import path
from setuptools import setup, find_packages
from sort_pack import about


try:
    current_path = path.abspath(path.dirname(__file__))
except NameError:
    current_path = None


try:
    with open(path.join(current_path, 'README.md'), encoding='utf-8') as f:
        description = f.read()
except FileNotFoundError:
    description = ''


setup(
    name=about.__title__,
    version=about.__version__,
    license='MIT License',
    author=about.__author__,
    author_email=about.__email__,
    description='Merge sort',
    long_description=description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    python_requires='>=3.5',
    install_requires=[],
    entry_points={
        'console_scripts': [
            'main=sort_pack:main',
            'sort_list=sort_pack.sort_counting:sort_list',
        ],
    },
)