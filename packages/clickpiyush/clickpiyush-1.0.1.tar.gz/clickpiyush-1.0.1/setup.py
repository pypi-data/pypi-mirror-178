from setuptools import setup

setup(
    name='clickpiyush',
    version='1.0.1',
    author="Piyush Goyani",
    author_email="thesourcepedia@gmail.com",
    license='MIT',
    description="CLI tool to describe Piyush Goyani's resume aka Resume Explainer.",
    long_description="CLI tool to describe Piyush Goyani's resume aka Resume Explainer made with Click.",
    keywords='cli piyush goyani thesourcepedia resume cv',
    url='https://github.com/piyush-multiplexer/click-piyush',
    py_modules=['clickpiyush'],
    install_requires=['Click', ],
    entry_points={
        'console_scripts': [
            'clickpiyush = clickpiyush:cli'
        ]
    },

)
