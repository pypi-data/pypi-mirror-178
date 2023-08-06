# -*- coding: utf-8 -*-
"""
Created on 2022 년 9월 7일

made by HN Park
"""


from PyQt5.QtWidgets import *
import os
import itertools as it

def list_chunk(lst, n):
    return [lst[i:i + n] for i in range(0, len(lst), n)]

def open_info():
    ip_add_folder = os.getcwd()
    file_list = os.listdir(ip_add_folder)

    IPCon_idx = []
    query_list = {}
    field_names = {}
    cnt_question = {}
    col_index = []
    type_index = []
    only_cols = []

    for i in range(0, file_list.__len__()):
        if file_list[i] == 'resource':
            with open(ip_add_folder + "\\" + file_list[i] + "\\" + "Migr_Info.ini", 'r') as FileObj:
                srccontent = FileObj.read()
                jlist = srccontent.split('\n')
                jlist = list(filter(None, jlist))  # 빈 문자열 제거cd

                for match in jlist:
                    if "Table" in match:
                        Tables_idx = jlist.index(match)
                    elif "col" in match:
                        col_index.append(jlist.index(match))
                    elif "type" in match:
                        type_index.append(jlist.index(match))
                    elif "IPCon" in match:
                        IPCon_idx = jlist.index(match)
                        db_ip = jlist[IPCon_idx+1:len(jlist)+1]
                    else:
                        pass
                eq_dic = dict()
                for idx in jlist[IPCon_idx+1:len(jlist)+1]:
                    eq_key = idx.split(',')[0]
                    eq_val = idx.split(',')[1]
                    eq_dic[eq_key] = eq_val

                for idx in range(len(col_index)):
                    log_col = jlist[col_index[idx]].split('=')[0].strip().replace('col_','')  # Table 다음라인_col
                    log_val = jlist[col_index[idx]].split('=')[1].strip().replace(" ", "").split(',')

                    type_val = jlist[type_index[idx]].split('=')[1].strip().replace(" ", "").split(',')
                    only_cols.append(jlist[col_index[idx]].split('=')[1].strip().replace(" ", "").split(','))
                    tmplist = list(it.chain(*zip(log_val, type_val)))
                    query_list[log_col] = tmplist

                for k, v in query_list.items():
                    list_chunked = list_chunk(v, 2)
                    tmp_field_names = [' '.join(d) for d in list_chunked]
                    field_names[k] = ','.join(tmp_field_names)
                    print(field_names)

                    p = []
                    for jdx in range(len(tmp_field_names)):
                        p.append('?')
                    cnt_question[k + '_cnt'] = (','.join(p))
                print('Migr_info.ini cleasing done')
            return query_list, field_names, cnt_question, only_cols, eq_dic


def dataframe_table_viewer(df, table):
    df_row_name = list(df.index)
    df_col_name = list(df.columns)

    table.clear()
    table.setRowCount(len(df_row_name))
    table.setColumnCount(len(df_col_name))
    table.setHorizontalHeaderLabels(df_col_name)

    for i in range(len(df_row_name)):
        for j in range(len(df_col_name)):
            item = str(df.iloc[i, j])
            table.setItem(i, j, QTableWidgetItem(item))

