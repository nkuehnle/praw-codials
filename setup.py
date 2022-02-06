'''
Install script for PRAW-CoDiaLS
'''
from setuptools import setup, find_packages

with open('README.md', 'r') as readme_file:
    long_description = readme_file.read()

setup(
    name='praw-codials',
    version='1.0.0',
    description='PRAW-Powered COmmunity & DomaIn tArgeted Link Scraper',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Neil Kuehnle',
    author_email='nkuehnle1191@gmail.com',
    license='MIT',
    url='https://github.com/nkuehnle/praw-codials',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Adaptive Technologies'
    ],
    keywords=['reddit', 'webscraper', 'command-line'],
    packages=find_packages(),
    install_requires=['praw', 'pandas', 'pyaml'],
    python_requires='~=3.6 ',
    scripts=['bin/praw-codials'],
)