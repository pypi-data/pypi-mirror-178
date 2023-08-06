#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@ Author: stephen.wan
@ Date: 2022-11-08 17:35
@ Email: stephen.wan@colourdata.com.cn
@ LastEditors: stephen.wan
@ LastEditTime: 2022-11-08 17:35
@ ProjectName: YiliEcommerceNewProductProject
@ Description: to do
"""
import os


def get_base_file(name=None):
    base_path = os.path.dirname(os.path.abspath(name))
    return base_path


if __name__ == '__main__':
    print(get_base_file(__file__))
