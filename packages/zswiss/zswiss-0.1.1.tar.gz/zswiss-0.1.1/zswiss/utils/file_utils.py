#!/usr/bin/env python
# coding=utf8

import os


def load_to_list(paths, deduplicate=False, appendix=None, recurse=False):
    """
    将指定路径下的文件，按行读入到list中。
    注意：不会进一步递归处理子文件夹!即，如果p是paths中的一个路径，p是一个文件夹，那么只会处理p里面的文件，而p里的文件夹会被忽略。
    :param recurse: 是否递归读取, 默认为不递归
    :param paths: 单个路径、或是可迭代的路径集合
    :param deduplicate: 元素是否去重, 默认不去重
    :param appendix: 识别的文件后缀, 仅读取指定后缀的文件
    :return:
    """
    if isinstance(paths, str):
        t = [paths]
        paths = t

    content_lst = []
    already_set = set()

    while paths:
        p = paths.pop(0)
        if os.path.isdir(p):
            for fn in os.listdir(p):
                fn_full = os.path.join(p, fn)
                if os.path.isfile(fn_full):
                    if (appendix is not None and fn.endswith(appendix)) or appendix is None:
                        with open(fn_full, 'r') as ifile:
                            for line in ifile:
                                content = line.strip()
                                if deduplicate:
                                    if content not in already_set:
                                        content_lst.append(content)
                                        already_set.add(content)
                                else:
                                    content_lst.append(content)
                else:
                    if recurse:
                        paths.append(fn_full)
        else:
            if (appendix is not None and p.endswith(appendix)) or appendix is None:
                with open(p, 'r') as ifile:
                    for line in ifile:
                        content = line.strip()
                        if deduplicate:
                            if content not in already_set:
                                content_lst.append(content)
                                already_set.add(content)
                        else:
                            content_lst.append(content)

    return content_lst


def load_to_set(paths, appendix=None, recurse=False):
    """
    将指定路径下的文件，按行读入到list中。
    注意：不会进一步递归处理子文件夹!即，如果p是paths中的一个路径，p是一个文件夹，那么只会处理p里面的文件，而p里的文件夹会被忽略。
    :param recurse: 是否递归读取，默认为不递归
    :param paths: 单个路径、或是可迭代的路径集合
    :param appendix: 识别的文件后缀, 仅读取指定后缀的文件
    :return:
    """
    if isinstance(paths, str):
        t = [paths]
        paths = t

    content_set = set()
    while paths:
        p = paths.pop(0)
        if os.path.isdir(p):
            for fn in os.listdir(p):
                fn_full = os.path.join(p, fn)
                if os.path.isfile(fn_full):
                    if (appendix is not None and fn.endswith(appendix)) or appendix is None:
                        with open(fn_full, 'r') as ifile:
                            for line in ifile:
                                content = line.strip()
                                content_set.add(content)
                else:
                    if recurse:
                        paths.append(fn_full)
        else:
            if (appendix is not None and p.endswith(appendix)) or appendix is None:
                with open(p, 'r') as ifile:
                    for line in ifile:
                        content = line.strip()
                        content_set.add(content)

    return content_set
