#!/usr/bin/env python
#-*- coding:utf-8 -*-
import os 
from setuptools import setup, find_packages

MAJOR =0
MINOR =7
PATCH =3
VERSION = f"{MAJOR}.{MINOR}.{PATCH}"

def get_install_requires():
    reqs = [
            'pandas>=0.18.0',
            'requests>=2.0.0',
			'toml>=0.10' ,
			'pyzstd >=0.15',
			'numpy>=1.9.2'
            ]
    return reqs
setup(
	name = "dbpystream",
	version = VERSION,
    author ="songroom",
    author_email = "rustroom@163.com",
    long_description_content_type="text/markdown",
	url = 'https://github.com/songroom2016/dbpystream.git',
	long_description = open('README.md',encoding="utf-8").read(),
    python_requires=">=3.6",
    install_requires=get_install_requires(),
	packages = find_packages(),
 	license = 'Apache',
   	classifiers = [
       'License :: OSI Approved :: Apache Software License',
       'Natural Language :: English',
       'Operating System :: OS Independent',
       'Programming Language :: Python',       
       'Programming Language :: Python :: 3.6',
       'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    #package_data={'': ['*.csv', '*.txt','.toml']} #这个很重要
    package_data={'dbpy_new': ['./dbpystream/method.toml']},
    include_package_data=True
    #include_package_data = True ,
    #data_files=[('dbpystream', ['./my_package/data_files/my_data_file.csv'./method.toml'])] # 指定文件夹dbpystream下，指定文件
    # 每一个(directory, files)对儿指定了安装时文件的存储路径，和文件目前存储的位置
)
