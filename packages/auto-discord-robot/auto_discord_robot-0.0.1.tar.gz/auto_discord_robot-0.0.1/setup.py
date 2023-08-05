#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/11/24 下午2:36
# @Author  : Xsu
# @File    : setup.py

import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="auto_discord_robot",
  version="0.0.1",
  author="Xsu",
  author_email="bbworktime@gmail.com",
  description="A small example package for discord",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/Web3-Base-Installation/auto-discord-robot.git",
  packages=setuptools.find_packages(),
  classifiers=[
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: MIT License",
  "Operating System :: OS Independent",
  ],
)