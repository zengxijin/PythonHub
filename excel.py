#coding=utf-8
"""
Created on 2018-6-21 10:30:47
@author: xijin.zeng
"""
from pyexcel_xls import save_data
from pyexcel_xls import get_data
from collections import OrderedDict


# get the number index from alphabet column name
def get_index_by_col(column_index):
    if len(column_index) == 1:  # A-Z => total columns 26
        return ord(column_index) - 64 - 1
    if len(column_index) == 2:  # AA - ZZ => total columns 26 + 26*26
        return 26*(ord(column_index[0]) - 64) + ord(column_index[-1]) - 64 - 1


def save_to_file(sheet_data, sheet_name, file_name):
    file_data = OrderedDict()
    file_data.update({sheet_name: sheet_data})
    save_data(file_name, file_data)


# usage:
# x_start_col: x param start column in excel
# x_end_col: x param end column in excel
# x_file_path: x param excel file path
# x_sheet_name: specific sheet name of x param file in excel
# x_join_col: x param column for join
# x_header_index: x header column index
# y_file_path: y param excel file path
# y_join_col: y param column for join
# y_output_cols: after join output columns, list values, example:['A','B']
# y_header_index: y header column index
def extract_xy(x_start_col, x_end_col, x_file_path, x_sheet_name, x_join_col, x_header_index,
               y_file_path, y_join_col, y_output_cols, y_header_index):

    x_sheet_name_decode = x_sheet_name.decode('utf-8')  # for Chinese sheet name

    x_file_data = get_data(x_file_path)
    y_file_data = get_data(y_file_path)

    join_data_buffer = []

    # process x file
    x_sheet_data = x_file_data.items()[0][1]  # default to get the first sheet
    if x_sheet_name_decode is not '':
        x_sheet_data = x_file_data[x_sheet_name_decode]
    x_header = x_sheet_data[x_header_index - 1]

    x_join_index = get_index_by_col(x_join_col)
    y_join_index = get_index_by_col(y_join_col)

    x_start_index = get_index_by_col(x_start_col)
    x_end_index = get_index_by_col(x_end_col)

    # process y file
    y_sheet_data = y_file_data.items()[0][len(y_file_data)]
    y_data = y_sheet_data[1:len(y_sheet_data)]  # exclude header
    y_header = y_sheet_data[y_header_index - 1]

    xy_header = x_header[x_start_index:x_end_index + 1]
    for h in y_output_cols:
        h_index = get_index_by_col(h)
        xy_header.append(y_header[h_index])

    join_data_buffer.append(xy_header)

    for y_row in y_data:
        for x_row in x_sheet_data:
            if len(x_row) >= (x_join_index+1):
                if len(y_row) >= (y_join_index+1):
                    val_src = x_row[x_join_index]
                    val_dst = y_row[y_join_index]
                    if val_src == val_dst:
                        print 'match src:' + val_src + ' dst:' + val_dst
                        x_row_clone = x_row[x_start_index:x_end_index + 1]
                        for y_output_col in y_output_cols:
                            y_output_index = get_index_by_col(y_output_col)
                            if len(y_row) >= (y_output_index+1):
                                y_val = y_row[y_output_index]
                                x_row_clone.append(y_val)
                            else:
                                x_row_clone.append(u'')  # if y_row have no y value
                        # watch out!
                        join_data_buffer.append(x_row_clone)
                else:
                    print "couldn't to find y join value, target index:" + y_join_index
                    print "length:" + str(len(y_row))
                    print y_row
            else:
                print "couldn't to find x join value, target index:" + str(x_join_index)
                print "length:" + str(len(x_row))
                print x_row

    print 'total size: %s' % len(join_data_buffer)

    return join_data_buffer


def start_extract_and_join(x_start_col, x_end_col, x_file_path, x_sheet_name, x_join_col, x_header_index,
                           y_file_path, y_join_col, y_output_cols, y_header_index,
                           sheet_name, file_name):
    data = extract_xy(x_start_col, x_end_col, x_file_path, x_sheet_name, x_join_col, x_header_index,
                      y_file_path, y_join_col, y_output_cols, y_header_index)
    if len(data) > 0:
        save_to_file(data, sheet_name, file_name)
        print "join finished, join total rows: %s, output file: %s" % (len(data), file_name)
    else:
        print "warn: no data match join, process finished"


# demo
if __name__ == '__main__':
    # -------------------信用-------------------
    # ZRobot信用
    start_extract_and_join('E', 'U', r'jd-hits.xlsx', '信用', 'C', 2,
                             r'mapping.xlsx', 'C', ['D', 'E', 'F'], 1,
                             "Sheet0", "credit_zrobot_data.xlsx")

    # 小白信用
    start_extract_and_join('V', 'AB', r'jd-hits.xlsx', '信用', 'C', 2,
                           r'mapping.xlsx', 'C', ['D', 'E', 'F'], 1,
                           "Sheet0", "credit_xiaobai_data.xlsx")

    # 金融画像
    start_extract_and_join('AC', 'AG', r'jd-hits.xlsx', '信用', 'C', 2,
                              r'mapping.xlsx', 'C', ['D', 'E', 'F'], 1,
                                  "Sheet0", "credit_fin_profile_data.xlsx")

    # 网购画像
    start_extract_and_join('AH', 'AQ', r'jd-hits.xlsx', '信用', 'C', 2,
                           r'mapping.xlsx', 'C', ['D', 'E', 'F'], 1,
                           "Sheet0", "credit_online_shopping_data.xlsx")
    # 消费画像
    start_extract_and_join('AR', 'BD', r'jd-hits.xlsx', '信用', 'C', 2,
                           r'mapping.xlsx', 'C', ['D', 'E', 'F'], 1,
                           "Sheet0", "credit_consume_profile_data.xlsx")

    # -------------------营销-------------------
    # 基本画像
    start_extract_and_join('D', 'G', r'jd-hits.xlsx', '营销', 'C', 2,
                           r'mapping.xlsx', 'C', ['D', 'E', 'F'], 1,
                           "Sheet0", "promotion_basic_profile_data.xlsx")

    # 需求画像
    start_extract_and_join('H', 'M', r'jd-hits.xlsx', '营销', 'C', 2,
                           r'mapping.xlsx', 'C', ['D', 'E', 'F'], 1,
                           "Sheet0", "promotion_demand_profile_data.xlsx")

    # 营销画像
    start_extract_and_join('N', 'U', r'jd-hits.xlsx', '营销', 'C', 2,
                           r'mapping.xlsx', 'C', ['D', 'E', 'F'], 1,
                           "Sheet0", "promotion_profile_data.xlsx")

    # -------------------反欺诈-------------------
    # 黑名单—Zrobot
    start_extract_and_join('D', 'F', r'jd-hits.xlsx', '反欺诈', 'C', 2,
                           r'mapping.xlsx', 'C', ['D', 'E', 'F'], 1,
                           "Sheet0", "antifraud_blacklist_zrobot_data.xlsx")
    # 黑名单—天机
    start_extract_and_join('L', 'N', r'jd-hits.xlsx', '反欺诈', 'C', 2,
                           r'mapping.xlsx', 'C', ['D', 'E', 'F'], 1,
                           "Sheet0", "antifraud_blacklist_tianji_data.xlsx")
    # 欺诈评分
    start_extract_and_join('O', 'P', r'jd-hits.xlsx', '反欺诈', 'C', 2,
                           r'mapping.xlsx', 'C', ['D', 'E', 'F'], 1,
                           "Sheet0", "antifraud_score_data.xlsx")
    # 手机号画像
    start_extract_and_join('Q', 'S', r'jd-hits.xlsx', '反欺诈', 'C', 2,
                           r'mapping.xlsx', 'C', ['D', 'E', 'F'], 1,
                           "Sheet0", "antifraud_phone_profile_data.xlsx")