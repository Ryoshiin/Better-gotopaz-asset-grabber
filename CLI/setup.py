from setuptools import setup, find_packages

setup(
    name='GotoDL',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'requests',
        'google_play_scraper',
    ],
    entry_points={
        'console_scripts': [
            'gotodl=gotodl.main:main',
        ],
    },
)
