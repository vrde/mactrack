from setuptools import setup, find_packages

setup(
    name='mactrack',
    version='0.1.0',
    description='How surveillance works, chapter 1: tracking smartphones.',
    url='https://github.com/vrde/mactrack/',
    author='vrde',
    author_email='',
    license='MIT',

    packages=find_packages(),
    install_requires=[
        'python-dateutil',
        'coloredlogs'
    ],

    entry_points={
        'console_scripts': [
            'mactrack=mactrack.commands:main'
        ],
    }
)

