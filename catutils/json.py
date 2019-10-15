#!/usr/bin/python3
"""
BSD 2-Clause License

Copyright (c) 2019, wenqian
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import re
from typing import List

# 不处理，直接赋值的属性类型
__NO_HANDLE_TYPE__ = [str, float, int, dict]


def __need_jsonify(attr_name: str,
                   include_pattern: str = None,
                   include_attrs: List[str] = None,
                   exclude_pattern: str = None,
                   exclude_attrs: List[str] = None):
    """判断属性是否需要被json化"""

    if include_attrs is not None:
        if attr_name in include_attrs:
            return True
        else:
            return False
    if include_pattern is not None:
        if re.match(include_pattern, attr_name):
            return True
        else:
            return False
    if exclude_pattern is not None:
        return not re.match(exclude_pattern, attr_name)
    if exclude_attrs is not None:
        return attr_name not in exclude_attrs
    return True


def __unfold_json_dict(json_dict: dict):
    """将字典中所有可以被json化的对象json化"""
    unfold_json_dict = {}

    for key, value in json_dict.items():
        unfold_json_dict[key] = __get_json_val(value)

    return unfold_json_dict


def __unfold_list(li: list):
    """将列表中所有可以被json化的对象json化"""
    unfold_list = []

    for obj in li:
        unfold_list.append(__get_json_val(obj))

    return unfold_list


def __is_base_type(obj):
    """判断obj是否需要处理后赋值"""
    return type(obj) in __NO_HANDLE_TYPE__


def __get_json_val(value):
    """处理value为json数据

    有4种情况：

    1 - value类型在`__NO_HANDLE_TYPE__`中，直接返回
    2 - value类型为tuple，转换为list后交给`__unfold_list`处理
    3 - value类型为list，交给`__unfold_list`处理
    4 - value为其它类型，如果有`jsonify`方法(说明它也被`@json_class`注释过)，
        则调用`jsonify()`后返回。否则转换为`str`后返回。

    - `__NO_HANDLE_TYPE__` 表示该类型不用经过json化处理，是基本类型，其它叫做复杂类型，需要额外处理为json。
    - `__unfold_xxx()` 方法负责将可迭代对象中那些隐性的复杂类型处理为json数据。

    Args:
        value: 需要处理为json数据的目标

    Returns:
        json数据，表现为字典，列表或基本类型

    """
    if value is None:
        return ''

    if __is_base_type(value):
        return value
    elif type(value) == tuple:
        return __unfold_list(list(value))
    elif type(value) == list:
        return __unfold_list(value)
    else:
        if hasattr(value, 'jsonify'):
            return value.jsonify()
        else:
            return jsonify(value)


def jsonify(obj, **kwargs):
    # 需要被json化的属性-值
    json_dict = {}

    # 取出属性，使用正则过滤掉那些魔法方法和函数
    # 同时将那些callable的属性过滤掉（它们是方法，不应该被json化）
    attr_names = [attr_name for attr_name in dir(obj)
                  if not re.match('__.+__', attr_name) and
                  not hasattr(getattr(obj, attr_name), '__call__')]

    for attr_name in attr_names:
        if __need_jsonify(attr_name, **kwargs):
            json_dict[attr_name] = getattr(obj, attr_name)

    return __unfold_json_dict(json_dict)


def json_class(rewrite_str_method=False,  **kwargs):

    def json_class_decorator(cls: object):

        def __jsonify(self):
            return jsonify(self, **kwargs)

        cls.jsonify = __jsonify

        if rewrite_str_method:
            cls.__str__ = lambda self: str(self.jsonify())

        return cls

    return json_class_decorator
