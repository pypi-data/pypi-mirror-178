#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
"""
    # @Time : 2021/4/13 9:26 
    # @Author : JunJie Duan
    # @Version：V 0.1
    # @File : pandas_sql.py
"""

import os, re
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

from copy import deepcopy

"""
字段: xxx, *
表名: xxx
链接方式: left right inner outer
链接表名: xxx
链接条件: =, !=, >, <, >=, <=, in (不使用恒等时 多对多查询会可能会出现多个重复值)
宽表条件: =, !=, >, <, >=, <=, in
特殊条件:groupby, oderby, limit
其他
    字段聚合：max, min, avg, std count
    字段类型：str, int, float,  date, datetime
"""

class ElementTools(object):

    Element_Compile = r'select (.*) from (.*) where (.*?);$'
    Element_Compile2 = r'select (.*) from (.*?) (.*?);$'
    Element_MultiTab_Compile = r'select (.*?) from (.*) (.{4,5})+ join (.*?) ON'
    Element_MultiTab_Compile2 = f'(.*?) where (.*)'

    Func_Compile = r'(.*)\((.*)\)'
    Where_Compile = r'(.*?) (and|or) '
    In_Compile = r'(.*)(in)(.*?)(\))'
    Compare_Compile = r'(.*?)([><=!]+)(.*?) '
    Like_Compile = r"like (.*?) (.*?) "

    Group_Compile = r"group by (.*?) |group by (.*);"
    Oderby_Compile = r"oder by (.*?) (.*?) |oder by (.*?) (.*);|oder by (.*?) (.*)"
    Limit_Compile = r"limit (.*)"

    Child_Tab_Compile = '\((.*)\) (.*)'

    @staticmethod
    def get_table_name(x):
        name = str(x).strip(' ')
        return name

    @staticmethod
    def str_join(join, strs):
        if isinstance(join, str):
            if isinstance(strs, Iterable):
                strs = join.join(strs)
        return strs

    @staticmethod
    def sub_space_str(strs):
        return re.sub(' +', ' ', strs)

    @staticmethod
    def printf(value, color=None, bgcolor=None):
        '\033[0;33;5m warning:`{}` not support aggregation \033[0m'
        colors = {'red': 31, 'yellow': 33, 'green': 32, 'blue': 34, 'violet': 35, 'gray': 37}
        color = colors.get(color)
        color = color if color else 30
        bgcolor = colors.get(bgcolor)
        bgcolor = bgcolor + 10 if bgcolor else 10
        m = 5 if bgcolor > 10 or color > 30 else 0
        color_format = f"\033[{bgcolor};{color};{m}m{value}\033"
        print(color_format)

    @staticmethod
    def get_elements(sql):
        """ 解析出sql中包含的条件元素 """
        elements = {}
        multitabs = False
        try:

            sql = sql if sql.endswith(';') else sql + ";"
            sql = ElementTools.sub_space_str(sql)
            if 'JOIN' in sql.upper():
                multitabs = True
                elements_tuple = re.findall(ElementTools.Element_MultiTab_Compile, sql, re.M | re.I)[0]
                keys = ['field', 'tab', 'join_type', 'join_tab']
                elements = dict(zip(keys, elements_tuple))
                end_sql = sql.split('ON')[-1]

                if 'WHERE' in end_sql.upper():
                    elements_tuple = re.findall(ElementTools.Element_MultiTab_Compile2, sql, re.M | re.I)[0]
                    keys = ['field', 'tab', 'join_type', 'join_tab', 'join_on', 'where']
                    elements.update({'join_on': elements_tuple[0], 'where': elements_tuple[1]})
                else:
                    elements.update({'join_on': end_sql, 'where': ''})

            elif 'WHERE' in sql.upper():
                get_elements = re.search(ElementTools.Element_Compile, sql, re.M | re.I)
                name = get_elements.group(2)
                elements['field'] = get_elements.group(1)
                elements['name'] = re.sub(' +', ' ', name.replace('as', ' '))
                elements['where'] = get_elements.group(3)
            else:
                get_elements = re.search(ElementTools.Element_Compile2, sql.replace(';', ' ;'), re.M | re.I)
                name = get_elements.group(2)
                elements['field'] = get_elements.group(1)
                elements['name'] = re.sub(' +', ' ', name.replace('as', ' '))
                elements['where'] = get_elements.group(3)
        except Exception as e:
            raise RuntimeError('sql error! `%s`' % sql)
        return elements, multitabs

    @staticmethod
    def get_file_columns(path, encoding='utf-8'):
        """ 读取表字段 """
        columns = []
        try:
            columns = pd.read_csv(path, nrows=0, encoding=encoding).columns.tolist()
        except FileNotFoundError as e:
            raise FileNotFoundError('No such table in: `%s`' % path)
        return columns

    @staticmethod
    def get_file_datas(path, header='infer', names=None, usecols=None, skiprows=None, nrows=None, encoding='utf-8'):
        """ 读取表字段 """
        datas = pd.DataFrame()
        try:
            datas = pd.read_csv(path, header=header, names=names, usecols=usecols, skiprows=skiprows, nrows=nrows,
                                encoding=encoding)
        except FileNotFoundError as e:
            raise FileNotFoundError('No such table in: `%s`' % path)
        return datas

    @staticmethod
    def get_col_back_tab(col, tab_columns):
        """ 根据列名返回列所属表 """
        col = str(col).strip()
        tab, name = None, None
        if '.' in col:
            tab, name = col.split('.')
            columns = tab_columns.get(tab)
            if columns is None or name not in columns:
                print('Warning:=> `%s` not in now table, but in `%s`' % (name, tab))
        else:
            for k, v in tab_columns.items():
                if col in v:
                    tab, name = k, col
                    continue
            if name is None:
                raise ValueError('`%s` not in table' % col)
        return tab, name

    @staticmethod
    def fromat_field(fields, tab_columns):
        """ 解析查询字段 """
        """
            1. x.xx
            2. xx
            3. func(xx)
            4. xx xx

            单字段结构:{
                'col':'xxx'
                ,'as':'xxx'
                ,'func':'xxx'
            }
        """

        fields = fields.replace('as ', '').split(',')
        field_dict = {}
        for line in fields:
            line = line.strip()
            field = dict.fromkeys(['col', 'as', 'func'])
            tab, col = None, None
            as_ = line.split(' ')
            field['as'] = None if len(as_) == 1 else as_[-1]
            if '*' in line:
                if '.' in line:
                    tab, names = line.split('.')
                    names = tab_columns.get(tab)
                else:
                    for tab, item in tab_columns.items():
                        tab, names = tab, item
                        break
                for name in names:
                    field.update({'col': name})
                    flag = field_dict.get(tab)
                    if flag is not None:
                        field_dict[tab].append(deepcopy(field))
                    else:
                        field_dict[tab] = [deepcopy(field)]
                continue

            if "(" in line:
                match = re.search(ElementTools.Func_Compile, line)
                field['func'] = match.group(1)
                line = match.group(2)

            tab, col = ElementTools.get_col_back_tab(line, tab_columns)
            field['col'] = col

            flag = field_dict.get(tab)
            if flag is not None:
                field_dict[tab].append(deepcopy(field))
            else:
                field_dict[tab] = [deepcopy(field)]

        return field_dict

    @staticmethod
    def fromat_where(where, tab_columns):
        """ 解析查询规则 """

        result = {
            'wheres': {
                'where': None
                , 'like_where': []
                , 'other': {}
            }
            , 'columns': {}
            , 'type_transition': []
        }

        """ 1.解析每一组规则 """
        where = where.replace('1=1', '').replace('AND','and').replace('OR','or')

        if 'and' in where or 'or' in where:
            wheres = re.findall(ElementTools.Where_Compile, where)
            end_where = ' '.join(wheres[-1])
            end_where = where[where.index(end_where) + len(end_where):].strip()
        else:
            wheres = []
            end_where = where

        if 'in' in end_where.lower():
            in_rule = re.findall(ElementTools.In_Compile, end_where, re.M | re.I)
            if in_rule and isinstance(in_rule, list):
                *start, end = in_rule[0]
                end_rule = (" ".join(start) + end, '')
                wheres.append(end_rule)
        if 'like' in end_where.lower():
            if not end_where.endswith(' '):
                end_where += " "
            like_rule = re.findall(ElementTools.Like_Compile, end_where, re.M | re.I)
            if like_rule and isinstance(like_rule, list):
                like_rule = " ".join(like_rule[0])
                like_rule = ('like ' + like_rule, '')
                wheres.append(like_rule)
        else:
            end_rule = re.findall(ElementTools.Compare_Compile, end_where, re.M | re.I)
            if end_rule and isinstance(end_rule, list):
                rule_ = end_rule[0][1]
                end_where_temp = end_where.replace(rule_ + ' ', rule_)
                end_rule = re.findall(ElementTools.Compare_Compile, end_where_temp, re.M | re.I)
                end_rule = (" ".join(end_rule[0]), '')
                wheres.append(end_rule)

        """ 2.规则合并 """
        new_wheres = []
        for i, line in enumerate(wheres):
            # print(line)
            """ 
                记录所有字段名
                是否包含类型转换
            """
            rule, logstic = line
            # print('rule1:`%s`'%rule)

            ''' 2.1记录需要转换的类型 '''
            if '::' in rule:
                start, end = rule.lower().split('::')
                start = start.replace('(', '')
                start = start.split(' ')[-1] if ' ' in start else start
                tab, name = ElementTools.get_col_back_tab(start, tab_columns)
                t_type = {
                    'table_name': tab
                    , 'column': name
                    , 'type': ''
                }
                as_type = ''
                if end.startswith('int'):
                    as_type = 'int'
                elif end.startswith('float'):
                    as_type = 'float'
                elif end.startswith('str'):
                    as_type = 'str'
                elif end.startswith('date'):
                    as_type = 'date'
                elif end.startswith('datetime'):
                    as_type = 'datetime'
                else:
                    raise RuntimeError('不支持！ 该类型转换：`%s`' % rule)
                # 将字符串中的转换语句清除
                t_type['type'] = as_type
                rule = rule.replace('::' + as_type, '')
                # 修改原始where条件
                wheres[i] = (rule, logstic)
                result['type_transition'].append(deepcopy(t_type))

            """ 2.2替换=为==  并记录字段名称 """
            if 'in' in rule:
                in_temp = re.findall(ElementTools.In_Compile, rule, re.M | re.I)
                col = in_temp[0][0].replace('(', '')
                tab, name = ElementTools.get_col_back_tab(col, tab_columns)
            elif 'like' in rule:
                if not rule.endswith(' '):
                    rule += " "
                like_temp = re.findall(ElementTools.Like_Compile, rule, re.M | re.I)
                col = like_temp[0][0].replace('(', '')
                tab, name = ElementTools.get_col_back_tab(col, tab_columns)
            else:
                if not rule.endswith(' '):
                    rule += " "
                compare_temp = re.findall(ElementTools.Compare_Compile, rule, re.M | re.I)
                k, v, var = compare_temp[0]
                if v == '=':
                    rule = rule.replace('=', '==')
                col = k.replace('(', '')
                tab, name = ElementTools.get_col_back_tab(col, tab_columns, re.M | re.I)
            # 将表的别名去掉
            rule = rule.replace(col, name + " ")
            rule = ElementTools.sub_space_str(rule)
            columns = result['columns']
            columns_flag = columns.get(tab)
            if columns_flag is not None:
                columns[tab].append(name)
            else:
                columns[tab] = [name]

            """ 2.3 生成新规则条件 """
            if rule.strip()[0] == '(':
                continue
            elif rule.strip()[-1] == ')' and '(' in wheres[i - 1][0].strip()[0]:
                rule = ' '.join(wheres[i - 1]) + ' ' + rule
            rule_logstic = rule + " " + logstic + " "
            # print('rule:`%s`'%rule)
            if 'like' in rule_logstic.lower():
                # print('\033[0;33;5min_like:%s\033[0m'%rule_logstic)
                result['wheres']['like_where'].append(rule_logstic)
                continue
            new_wheres.append(rule_logstic)
        new_wheres = ElementTools.sub_space_str(''.join(new_wheres))
        result['wheres']['where'] = (new_wheres)

        """ 3.特殊规则 """
        columns = result['columns']
        if 'oder' in end_where.lower():
            oder_by = re.findall(ElementTools.Oderby_Compile, end_where, re.M | re.I)
            print(oder_by, end_where)
            k = [i for i in oder_by[0] if i != '']
            if len(k) == 1:
                k, sc = k[0], 'ase'
            else:
                k, sc = k
            tab, name = ElementTools.get_col_back_tab(k, tab_columns)
            result['wheres']['other'].update({'oderby': {
                'key': name
                , 'var': sc
            }})
            columns_flag = columns.get(tab)
            if columns_flag is not None:
                columns[tab].append(name)
            else:
                columns[tab] = [name]

        if 'group' in end_where.lower():
            group_by = re.findall(ElementTools.Group_Compile, end_where, re.M | re.I)
            group_by = ''.join(group_by[0])
            tab, name = ElementTools.get_col_back_tab(group_by, tab_columns)
            result['wheres']['other'].update({'groupby': name})
            columns_flag = columns.get(tab)
            if columns_flag is not None:
                columns[tab].append(name)
            else:
                columns[tab] = [name]

        if 'limit' in end_where.lower():
            limit = re.findall(ElementTools.Limit_Compile, end_where, re.M | re.I)
            result['wheres']['other'].update({'limit': limit})

        return result


class Dsql(ElementTools):

    def __init__(self, path, file_type, multitabs=False, encoding='utf-8'):
        """
            根据给定的本地路径以sql语言读取数据
        :param path: 文件路径
        :param file_type: 文件类型（csv,excel）
        :param multitabs: 是否多表  目前最多支持两张表联查
        :param encoding: 文件编码格式
        """
        self.path = path
        self.file_type = file_type
        self.encoding = encoding
        self.multitabs = multitabs
        self.datas = {}
        self.tabs_columns = {}
        self.columns_tbas = {}
        self.columns_index = {}

    def set_elements(self, sql):
        """ 解析出sql中包含的条件元素 """
        elements, multitabs = self.get_elements(sql)

        self.elements = elements
        self.multitabs = multitabs
        return self.elements

    def set_tabs_columns(self, names):
        """ 读取表字段 """
        tabs_columns = {}
        names = names if isinstance(names, list) else [names]
        for name in names:
            path = os.path.join(self.path, name + '.' + self.file_type)
            tabs_columns[name] = self.get_file_columns(path, self.encoding)
        self.tabs_columns.update(tabs_columns)
        return self.tabs_columns

    def set_fromat_field(self):
        """ 格式化表头 """
        field = self.elements.get('field')
        self.my_fromat_field = self.fromat_field(field, self.tabs_columns)

    def set_format_where(self):
        """  格式化规则条件 """
        where = self.elements.get('where')
        self.my_fromat_where = self.fromat_where(where, self.tabs_columns)

    def set_columns_index(self):
        """ 找到需要读的表及必要字段索引  """
        columns_tbas = {}
        columns_index = {}
        for k, v in self.my_fromat_field.items():
            where_columns = self.my_fromat_where.get('columns').get(k)
            columns = [i.get('col') for i in v]
            if where_columns is not None:
                columns = where_columns + columns
            columns = list(set(columns))
            indexs = [self.tabs_columns.get(k).index(col) for col in columns]
            columns_tbas[k] = columns
            columns_index[k] = indexs
        self.columns_tbas.update(columns_tbas)
        self.columns_index.update(columns_index)

    def to_type_transition(self):
        """ 类型转换 """
        type_transition = self.my_fromat_where.get('type_transition')
        for item in type_transition:
            tab = item.get('table_name')
            col = item.get('column')
            tp = item.get('type').lower()
            data = self.datas[tab]
            # print(data.info())
            # print(tab,col,tp)
            if tp == 'date':
                data[col] = data[col].astype('datetime64').dt.date
            if tp == 'datetime':
                data[col] = data[col].astype('datetime64')
            if tp in ['int', 'float', 'str']:
                data[col] = data[col].astype(tp)
                # print(self.datas[tab].info())

    def func_tool(self, name, key_map=None, is_group=False):
        """ 分组聚合 """

        if key_map is None:
            key_map = self.my_fromat_field.get(name)

        def inner(x):
            if is_group:
                y = pd.Series()
            else:
                y = x
            for k_mp in key_map:
                col = k_mp.get('col')
                as_ = k_mp.get('as')
                func = k_mp.get('func')
                func =  func.lower() if func else None

                name = col
                # name = func+f'({col})' if func else col
                as_ = as_ if as_ else name

                if func == 'min':
                    y[as_] = x[col].min()
                elif func == 'max':
                    y[as_] = x[col].max()
                elif func == 'avg':
                    y[as_] = x[col].mean()
                elif func == 'std':
                    y[as_] = x[col].std()
                else:
                    """  """
                    if not is_group:
                        y[as_] = x[col].values
                    # print('\033[0;33;5m warning:`%s` not support aggregation \033[0m'%col)
            return y

        return inner

    def to_where_query(self, name):

        # print(self.datas)
        # print(self.my_fromat_where)
        """
        fromat结构：{
            'wheres':{
                'where':'xxx'
                ,'like_where':[]
                ,'other':{
                    'oderby':{
                        'key':''
                         'var':''
                    }
                    ,'groupby':'x'
                    ,'limit':[]
                }
            }
            ,'columns':{[]}
            ,'type_transition':[{
                'table_name':''
                ,'column':''
                ,'type':''
            }]
        }
        """
        # 1.类型转换
        self.to_type_transition()

        # 2.where条件
        data = deepcopy(self.datas.get(name))
        wheres = self.my_fromat_where.get('wheres')
        where = wheres.get('where')
        like_where = wheres.get('like_where')
        other = wheres.get('other')

        if where:
            # 存在BUG 避免:结尾的条件尽量不要包含like（like语句尽量在结尾前）
            # print(where)
            where = where.strip()
            if where.endswith('and'):
                where = where[:-3]
            elif where.endswith('or'):
                where = where[:-3]
            data = data.query(where)
        if like_where:
            # print(like_where)
            for like_rule in like_where:
                like_rule = re.findall(self.Like_Compile, like_rule)
                col, like = like_rule[0]

                d_type = data[col].dtype
                if d_type != object:
                    raise RuntimeError(' `%s` is `%s` type not use like!' % (col, d_type))

                like = like.replace('%', '.*').replace('_', '.{1}')
                # print(data.shape)
                # display(data)
                # print(data.info())
                data = data[data[col].str.contains(like, regex=True)]
                # print(data.shape)

        if other:
            by = other.get('groupby')
            oderby = other.get('oderby')
            limit = other.get('limit')
            #  {'oderby': {'key': 'flow', 'var': 'limit'}, 'groupby': 'gnbid', 'limit': ['5']}
            if by:
                if ',' in by:
                    by = by.split(',')
                warning = '\033[0;33;5m warning:`{}` not support aggregation \033[0m'
                key_map = self.my_fromat_field.get(name)
                [print(warning.format(line.get('col'))) for line in key_map if line.get('func') is None]
                data = data.groupby(by).apply(self.func_tool(name, is_group=True)).reset_index()
            else:
                agg_func = self.func_tool(name, is_group=False)
                data = agg_func(x=data)

            if oderby:

                key = oderby.get('key')
                var = oderby.get('var')
                if var.lower() == 'desc':
                    data = data.sort_values(key, ascending=False)
                else:
                    # 默认升序
                    data = data.sort_values(key)

            if limit:
                limit = limit[0].split(',')
                if len(limit) == 2:
                    start, end = limit
                    start, end = int(start), int(end)
                else:
                    start, end = None, int(limit[0])
                data = data.iloc[start:end]
        else:
            agg_func = self.func_tool(name, is_group=False)

            data = agg_func(x=data)
        data.reset_index(drop=True, inplace=True)
        return data

    def set_datas(self, name, inplace=True):
        """ 当没有where条件时 或特殊条件 仅包含limit时只根据limit读取数据 """
        """
        存在问题  多表与单表混合 

        """
        flag = False
        datas = pd.DataFrame()
        if inplace:
            """ 当该表数据 已存在时将不再读取  """
            if self.datas.get(name) is not None:
                return self.datas
        path = os.path.join(self.path, name + '.' + self.file_type)
        if self.my_fromat_where['wheres'].get('where') == '':
            other = self.my_fromat_where['wheres'].get('other')
            limit = other.get('limit')
            if len(other) == 1 and limit is not None:
                limit = limit[0].split(',')
                if len(limit) == 2:
                    start, end = limit
                    start, end = int(start), int(end)
                else:
                    start, end = None, int(limit[0])
                # 根据limit读取数据
                # print(start,end)

                indexs = pd.Series(index=self.columns_index.get(name), data=self.columns_tbas.get(name)).sort_index()
                usecols, names = indexs.index.tolist(), indexs.values.tolist()

                datas = self.get_file_datas(path, header=0, names=names, usecols=usecols, skiprows=start, nrows=end,
                                            encoding=self.encoding)
                # print('data :%s'%str(datas.shape))
                flag = True
        if not flag:
            # print(self.columns_index.get(name))
            datas = self.get_file_datas(path, usecols=self.columns_index.get(name), skiprows=None, nrows=None,
                                        encoding=self.encoding)
        # print('data :%s'%str(datas.shape))
        self.datas.update({name: deepcopy(datas)})
        return self.datas

    def set_child_tab(self, tab):

        tab_sql_info = re.findall(self.Child_Tab_Compile, tab)
        tab_sql, tab_name = tab_sql_info[0]
        # print('-------------------')
        # print(tab_sql)
        # print(tab_name)
        tab_name = tab_name.replace('as', '').strip()
        # print('===================')
        dsql = Dsql(self.path, self.file_type, self.multitabs, self.encoding)
        tab_data = dsql.query(tab_sql)

        columns = tab_data.columns.tolist()
        index = list(range(len(columns)))
        self.datas.update({tab_name: tab_data})
        self.tabs_columns.update({tab_name: columns})  # 在单表查询中的源表字段
        self.columns_tbas.update({tab_name: columns})
        self.columns_index.update({tab_name: index})
        # display(self.datas)

    def is_in_child_tab(self, tab, join_tab):
        """ 检查子语句 """

        wait_load_data = {}
        for tab in [tab, join_tab]:
            if 'select' in tab:
                self.set_child_tab(tab)
            else:
                # 解析表字段

                name = self.sub_space_str(tab.replace('as', ' ')).split(' ')
                if len(name) > 1:
                    name, asname = name
                else:
                    name, asname = name[0], name[0]
                # 1.读取非子语句表头
                self.set_tabs_columns(name)
                # 2.修改key为别名
                self.tabs_columns[asname] = self.tabs_columns.pop(name)
                # 3.将表加入呆加载信息
                wait_load_data.update({name: asname})
        return wait_load_data

    def to_join(self):
        """
        数据连接
        只支持and条件
            规则只能 =
        """
        join_type = self.elements.get('join_type')
        join_on = self.elements.get('join_on')

        ons = join_on.replace('AND', 'and').replace(';', '').split('and')
        on_dict = {}
        for line in ons:
            if not line.endswith(' '):
                line += " "
            rule = re.findall(self.Compare_Compile, line)
            k, r, v = rule[0]
            if r == '=':
                tab, name = k.strip().split('.')
                join_tab, join_name = v.strip().split('.')
                if tab == join_tab:
                    raise ValueError('join error `%s`' % line.strip())
                tab_names = on_dict.get(tab)
                join_names = on_dict.get(tab)
                if tab_names is not None and join_names is not None:
                    on_dict[tab].append(name)
                    on_dict[join_tab].append(join_name)
                else:
                    on_dict[tab] = [name]
                    on_dict[join_tab] = [join_name]
            else:
                raise ValueError('join error! `%s`' % r)

        table_a, table_b = on_dict.items()
        a_name, a_columns = table_a
        b_name, b_columns = table_b
        join_type = join_type.strip().lower()
        table_a = self.datas.get(a_name)
        table_b = self.datas.get(b_name)

        data = pd.DataFrame()
        if join_type in {'left', 'right', 'outer', 'inner'}:
            data = pd.merge(table_a, table_b, how=join_type, left_on=a_columns, right_on=b_columns,
                            suffixes=('^x', 'x^'))
            data.columns = data.columns.map(lambda x: x.replace('^x', '').replace('x^', ''))
        else:
            raise RuntimeError(' join type error!')
        return data

    def query(self, sql):
        """
        根据sql语句读取数据

        :param sql: sql语句
        :return: dataframe
        """
        # 仅支持单表 双表联查

        self.set_elements(sql)
        #print(self.elements)
        #print('^' * 100)
        data = pd.DataFrame()
        if self.multitabs:
            # print('yes')
            # 1.是否包含子表
            tab = self.elements.get('tab')
            join_tab = self.elements.get('join_tab')

            # 2.是否包含子语句
            wait_load_data = self.is_in_child_tab(tab, join_tab)

            # 3.解析规则
            # print('*'*30)
            self.set_fromat_field()
            # print("fromat_field: %s"%self.my_fromat_field)
            self.set_format_where()
            # print("fromat_where: %s"%self.my_fromat_where)
            self.set_columns_index()
            # print("columns_index: %s"%self.columns_index)
            # print("columns_tbas: %s"%self.columns_tbas)

            #  4.读取待加载数据
            for name, asname in wait_load_data.items():
                self.set_datas(name)
                self.datas[asname] = self.datas.pop(name)
            # print(self.datas)
            #  on 语句执行 join
            join_data = self.to_join()
            self.datas['join_data'] = join_data
            field_a, field_b = self.my_fromat_field.values()
            self.my_fromat_field['join_data'] = field_a + field_b
            # 执行规则
            join_data = self.to_where_query('join_data')
            return join_data
        else:
            # print('****non****')
            name = self.get_table_name(self.elements.get('name'))
            name = name.replace('as', ' ').split(' ')
            if len(name) > 1:
                name, asname = name
            else:
                name, asname = name[0], name[0]
            # print("table name:'%s'" % name)
            tabs_columns = self.set_tabs_columns(name)
            # print("tab columns:'%s'" % tabs_columns)
            self.set_fromat_field()
            # print("fromat_field: %s"%self.my_fromat_field)
            self.set_format_where()
            # print("fromat_where: %s"%self.my_fromat_where)
            self.set_columns_index()
            # print("columns_index: %s"%self.columns_index)
            # print("columns_tbas: %s"%self.columns_tbas)
            self.set_datas(name)
            data = self.to_where_query(name)
        return data


if __name__ == '__main__':
    """ 
    sql = "select cellid, cellname, flow, max(flow) flow_max, avg(flow) flow_std from A as a  where cellid in (1,2,3) " \
          "and cellid in (1,4,3) and lon >= 116.5 and like cellname RBJ60% and flow::int>170"
    data = Dsql(path=r'F:\ipython_notebook\tools\datas', file_type='csv').query(sql=sql)
    print(data)
    """