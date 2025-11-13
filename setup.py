from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='todo-list-manager',
    version='1.0.0',
    author='Giorgi Zautashvili',
    author_email='giorgi.zautashvili@promptrun.ai',
    description='A simple CLI-based todo list manager with SQLite storage',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/todo-list-manager',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Office/Business :: Scheduling',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    python_requires='>=3.7',
    install_requires=[
        'click>=8.0.0',
        'tabulate>=0.9.0',
    ],
    entry_points={
        'console_scripts': [
            'todo=src.client:cli',
        ],
    },
)
