import pandas as pd
import sys
import os
import pprint
import xlrd

data_file_loc = './../data'
data_file_name = 'gartner.xlsm'
data_file_path = data_file_loc + '/' + data_file_name
data_file_loc = './../data/gartner'

# def f2():
#
#     count = 0
#     purge_nl = '_x000D_'
#     with open(data_file_path, 'r') as inp:
#         inp_line = inp.readline()
#         while inp_line:
#             count += 1
#             if count == 1:
#                 # first line is blank
#                 continue
#
#             line = inp.readline()
#             line = line.replace(purge_nl, '')
#
#             line = line.lstrip(";-.,!")
#             line = line.rstrip(";-.,!/\n")
#
#             if len(line) == 0:
#                 continue
#             line = line.decode("utf8")
#             line = line.encode('ascii', 'ignore')
#             print line
#             # line = textacy.preprocess.fix_bad_unicode(line, normalization='NFC')




def clean_text(text):
    comma = ','
    new_line ='/\n'
    ret_char='/\r'
    comma_replacement = ' && '
    text = text.replace(ret_char, comma_replacement)
    text = text.replace(comma, comma_replacement)
    text = text.replace(new_line, comma_replacement)
    text = text.replace('/\t', ' ')
    text = text.lstrip(";-.,!")
    text = text.rstrip(";-.,!/\n")
    text = text.encode('ascii', 'ignore')
    return text


def f3():
    name_col = 1
    col_dict = {
        'name' : 1,
        'text1': 2,
        'text2': 6,
        'text3': 7,
        'text4': 8,
        'instance': 12
    }
    workbook = xlrd.open_workbook(data_file_path)
    worksheet = workbook.sheet_by_index(2)
    # data  starts at line 2
    cur_line = 2
    data_dict = {}
    line_count = 1
    while True:
        dict = {}
        try:
            class_name = worksheet.cell(cur_line, name_col).value
            cur_line+=1
            for key,val in col_dict.iteritems():
                data = clean_text(worksheet.cell(cur_line, val).value)
                dict[key] =  data
            data_dict[line_count] = dict
            line_count+=1
        except:
            break

    # Create data-frame!
    df = pd.DataFrame(columns=col_dict.keys())

    for line_num,data in data_dict.iteritems():
        d = {}
        for _a,_b in data.iteritems() :
            d[_a] = [_b]
        _df = pd.DataFrame(d)
        df = df.append(_df,ignore_index=True)

    df = df.reset_index()
    op_file_name ='gartner_clean.csv'
    op_file_path = data_file_loc + '/' + op_file_name
    df.to_csv(op_file_path,index=True)
    return

f3()

# # ----------------------------------------------- #
# def f1():
#     purge_nl = '_x000D_'
#     delim = '^'
#     max_delim_count = 4
#     comma = ','
#     comma_replacement = ' && '
#     count = 0
#     line_list = {}
#     line_count = 0
#     prev_delim_count = 0
#
#     with open(data_file_path, 'r') as inp :
#
#         inp_line = inp.readline()
#         while inp_line:
#             print 'current line count ', line_count
#             count += 1
#             if count == 1:
#                 # first line is blank
#                 continue
#
#             line = inp.readline()
#             line = line.replace('purge_nl', '')
#             line = line.lstrip(":;-.,!")
#             line = line.rstrip(":;-.,!/\n")
#
#             if len(line)==0 :
#                 continue
#             delim_count = line.count(delim)
#             line = line.replace(comma , comma_replacement)
#             print 'delim count ', delim_count
#             print line
#
#             if delim_count < max_delim_count :
#                 if prev_delim_count + delim_count == max_delim_count :
#                     # Seems this line completes the record!
#                     line_list[line_count] = line.replace(delim, ',')
#                     line_count += 1
#                     prev_delim_count = 0
#                 else :
#                     # start of a new record, that can be completed in the next few lines
#                     if prev_delim_count == 0 :
#                         line_list[line_count] = ""
#
#                     # 2 cases :
#                     # 1. prev_delim_count = 0  - simple case
#                     # 2. prev_delim_count > 0 && < 4
#                     prev_delim_count += delim_count
#                     line_list[line_count] = line_list[line_count] + line
#             else :
#                 # got a complete line!!
#                 line_list[line_count] = line.replace(delim, ',')
#                 line_count += 1
#                 prev_delim_count = 0
#
#
#
#             if line_count > 545:
#                 break
#                 # f = raw_input('strike a key! ')
#
#     pprint.pprint(line_list)
#
#
#
