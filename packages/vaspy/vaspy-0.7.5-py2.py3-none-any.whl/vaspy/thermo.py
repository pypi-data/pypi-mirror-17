# -*- coding:utf-8 -*-
"""
=====================================================================
Provide energy-related file class which do operations on these files.
=====================================================================
Written by PytLab <shaozhengjiang@gmail.com>, August 2015
Updated by PytLab <shaozhengjiang@gmail.com>, August 2015
==============================================================

"""
import re

import numpy as np
import matplotlib.pyplot as plt

from vaspy import VasPy


class OsziCar(VasPy):
    def __init__(self, filename='OSZICAR'):
        """
        Create a OSZICAR file class.

        Example:

        >>> a = OsziCar(filename='OSZICAR')

        Class attributes descriptions
        =======================================================================
          Attribute      Description
          ============  =======================================================
          filename       string, name of the file the direct coordiante data
                         stored in
          vars           list of strings, 每次迭代得到的数据
          esort()        method, 对数据进行排序
          plot()         method, 对数据绘图
          ============  =======================================================
        """
        VasPy.__init__(self, filename)

        #set regex patterns
        float_regex = r'[\+|-]?\d*\.\d*(?:[e|E][\+|-]?\d+)?'
        eq_regex = r'\s*([\w|\d|\s]+)\=\s*(' + float_regex + r')\s*'
        split_regex = r'^\s*(\d+)\s*((' + eq_regex + r')+)$'  # 将step和其余部分分开

        self.eq_regex = re.compile(eq_regex)
        self.split_regex = re.compile(split_regex)

        self.load()

    def match(self, line):
        "匹配每一步迭代的数据"
        m = self.split_regex.search(line)
        if m:
            #get step
            step = int(m.group(1))
            #get other data
            resid = m.group(2)
            eq_tuples = self.eq_regex.findall(resid)  # list of tuples
            names, numbers = zip(*eq_tuples)
            #remove space in names
            names = [name.replace(' ', '') for name in names]
            #convert string to float
            numbers = [float(number) for number in numbers]
            eq_tuples = [('step', step)] + zip(names, numbers)
            return eq_tuples
        else:
            return None

    def load(self):
        "加载文件数据信息"
        with open(self.filename, 'r') as f:
            content = ''
            for line in f:
                eq_tuples = self.match(line)
                if eq_tuples:  # if matched
                    if not hasattr(self, 'vars'):
                        self.vars, numbers = zip(*eq_tuples)
                    for name, number in eq_tuples:
                        if not hasattr(self, name):
                            setattr(self, name, [number])
                        else:
                            getattr(self, name).append(number)
                    content += line
            self.content = content
            #convert list to numpy array
            for var in self.vars:
                data = getattr(self, var)
                setattr(self, var, np.array(data))

        return

    def esort(self, var, n, reverse=False):
        '''
        进行数据var排序, 获取排序后的前n个值.

        Example:
        >>> esort('E0', 10, reverse=True)

        Parameters
        ----------
        var: string, data to be sorted.

        n: int, top numbers of sorted data.

        '''
        zipped = zip(getattr(self, var), self.step)  # (E0, step)
        dtype = [('var', float), ('step', int)]
        zipped = np.array(zipped, dtype=dtype)
        srted = np.sort(zipped, order='var')

        if reverse:
            return srted[-n:]
        else:
            return srted[:n]

    def plot(self, var, mode='show'):
        "绘制不同变量随step的变化曲线"
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.set_ylabel(var)
        ax.set_xlabel('step')
        ax.plot(self.step, getattr(self, var), linewidth=2.5)
        if mode == 'show':
            plt.show()
        elif mode == 'save':
            fname = "%s_vs_%s.png" % (var, 'step')
            fig.savefig(fname)
        else:
            raise ValueError('Unrecognized show mode parameter : ' + mode)

        return fig
