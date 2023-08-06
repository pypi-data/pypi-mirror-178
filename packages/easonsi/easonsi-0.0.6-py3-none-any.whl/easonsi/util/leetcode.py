import typing
from typing import List, Optional, Tuple
import copy
from copy import deepcopy, copy
import collections
from collections import deque, defaultdict, Counter, OrderedDict, namedtuple
import math
from math import sqrt, ceil, floor, log, log2, log10, exp, sin, cos, tan, asin, acos, atan, atan2, hypot, erf, erfc, inf, nan
import bisect
from bisect import bisect_right, bisect_left
import heapq
from heapq import heappush, heappop, heapify, heappushpop
import functools
from functools import lru_cache, reduce, partial # cache
# cache = partial(lru_cache, maxsize=None)
# cache for Python 3.9, equivalent to @lru_cache(maxsize=None)
import itertools
from itertools import product, permutations, combinations, combinations_with_replacement, accumulate
import string
from string import ascii_lowercase, ascii_uppercase
# s = ""
# s.isdigit, s.islower, s.isnumeric
import operator
from operator import add, sub, xor, mul, truediv, floordiv, mod, neg, pos # 注意 pow 与默认环境下的 pow(x,y, MOD) 签名冲突
import sys, os
# sys.setrecursionlimit(10000)
import re

# https://github.com/grantjenks/python-sortedcontainers
import sortedcontainers
from sortedcontainers import SortedList, SortedSet, SortedDict
# help(SortedDict)
# import numpy as np
from fractions import Fraction
from decimal import Decimal

# from structures import ListNode, TreeNode, linked2list, list2linked

# def testClass(inputs):
#     # 用于测试 LeetCode 的类输入
#     s_res = [None] # 第一个初始化类, 一般没有返回
#     methods, args = [eval(l) for l in inputs.split('\n')]
#     class_name = eval(methods[0])(*args[0])
#     for method_name, arg in list(zip(methods, args))[1:]:
#         r = (getattr(class_name, method_name)(*arg))
#         s_res.append(r)
#     return s_res




# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


""" 解析LC格式的树结构
关联: 0297. 二叉树的序列化与反序列化 #hard
参见 [LeetCode 序列化二叉树的格式](https://support.leetcode-cn.com/hc/kb/article/1567641/)
"""
def parseLCBinaryTree(data):
    """ 解析形如 '[1,2,3,null,null,4,5]' 这样的LC树结构 """
    if data == "[]": return None
    data = data[1:-1].split(",")
    n = len(data)
    root = TreeNode(int(data[0]))
    idx = 1
    q = deque([root])
    while q:
        node = q.popleft()
        if idx >= n: break
        lv = data[idx]; idx+=1
        if lv!='null':
            l = TreeNode(int(lv))
            node.left = l; q.append(l)
        if idx >= n: break
        rv = data[idx]; idx+=1
        if rv!='null':
            r = TreeNode(int(rv))
            node.right = r; q.append(r)
    return root

def printLCBinaryTree(root):
    """ 打印形如 '[1,2,3,null,null,4,5]' 这样的LC树结构 """
    if not root: return "[]"
    q = deque([root])
    res = []
    while q:
        node = q.popleft()
        if node:
            res.append(str(node.val))
            q.append(node.left)
            q.append(node.right)
        else:
            res.append("null")
    # 删除最后的可能多余的null
    while res[-1] == "null":
        res.pop()
    return f"[{','.join(res)}]"
