from setuptools import setup, find_packages
import os
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='shurl',
    packages=find_packages(),
    include_package_data=True,
    version="1.0.0",
    description='URL shortener and Masking!',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='CyberSH',
    author_email='cybershbd@gmail.com',
    #install_requires=[],

  
    keywords=["cybershbd","cyber sh","sh url","shurl","shurl shortener","shurl masking","url shortener","url masking"],
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
                'shurl = shurl.shurl:shurl',
            ],
    },
    python_requires='>=3.9.5'
)
