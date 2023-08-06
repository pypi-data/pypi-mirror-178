from setuptools import setup, find_packages
import os
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='maskurl',
    packages=find_packages(),
    include_package_data=True,
    version="1.0.1",
    description='Python maskurl project.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='ITSN0B1T4',
    author_email='toxinum.org@gmail.com',
    install_requires=['requests'],

  
    keywords=["PYTHON PROJECT", "ITSN0B1T4", "MASKURL", "PISHING URL", "URL SHORTNER"],
    classifiers=[
            'Development Status :: 4 - Beta',
            'Intended Audience :: Developers',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3',
            'Operating System :: OS Independent',
            'Environment :: Console',
    ],
    
    license='MIT',
    entry_points={
            'console_scripts': [
                'maskurl = maskurl.maskurl:maskurl',
            ],
    },
    python_requires='>=3.9.5'
)
