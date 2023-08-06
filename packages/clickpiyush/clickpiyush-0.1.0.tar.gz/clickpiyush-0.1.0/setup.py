from setuptools import setup

setup(
    name='clickpiyush',
    version='0.1.0',
    author="Piyush Goyani",
    author_email="thesourcepedia@gmail.com",
    license='MIT',
    description="CLI tool to describe Piyush Goyani's resume aka Resume Explainer.",
    keywords='cli piyush goyani thesourcepedia resume cv',
    py_modules=['clickpiyush'],
    install_requires=['Click', ],
    entry_points={
        'console_scripts': [
            'clickpiyush = clickpiyush:cli'
        ]
    }
)
