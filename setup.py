from setuptools import setup, find_packages

setup(
    name="pulse-app",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'requests',
        'beautifulsoup4',
        'urllib3',
    ],
)
