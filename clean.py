#!/usr/bin/env python
# -*- coding: utf-8 -*-
#按照关键字匹配清洗数据
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import random
import linecache
def get_data_item(line_num, path):
	while True:
		i = random.randint(0, line_num)
		name_line = linecache.getline(path, i)
		if name_line != '':
			break
	return name_line.strip().decode('utf-8')


def write_data_to_txt(data, file_dir):
	"""
	:param file_dir:
	:return:
	"""
	try:
		import os
		dirs, file_name = os.path.split(file_dir)
		if not os.path.isdir(dirs):
			os.makedirs(dirs)
		fp = open(file_dir, "w")
		for item in data:
			item = str(item)
			item = item.replace(' ', '')
			fp.write(item + "\n")
		fp.close()
		print "write %d into %s" % (len(data), file_dir)
	except IOError:
		print("fail to open file")


def read_data_from_txt(file_dir):
	"""
	:param file_dir:
	:return:
	"""
	data_list = []
	lines = open(file_dir, 'r').readlines()
	for line in lines:
		line = line.decode('utf-8').split('\n')
		if '' in line:
			line.remove('')
		line = ''.join(line)
		data_list.append(line)
	return data_list


def split_data_with_keyword(keyword, na_data_file, lf_data_file, out_dir):

	na_data = read_data_from_txt(na_data_file)
	lf_data = read_data_from_txt(lf_data_file)
	datas = []
	for i in range(len(na_data)):
		datas.append((na_data[i], lf_data[i]))

	filter_na_datas = []

	for item in datas:
		if item[1].find(keyword) != -1:
			filter_na_datas.append(item[0])

	write_data_to_txt(filter_na_datas, out_dir+keyword+'.data')






def generate_sentences_UI_control(na_data_file='train_tickets.data'):




	ui_data = read_data_from_txt(na_data_file)
	ui_data_0 = []
	ui_data_1 = []
	ui_data_2 = []
	ui_data_3 = []
	ui_data_4 = []
	ui_data_5 = []
	ui_data_6 = []
  
	for sen in ui_data:

		if sen.find('订') != -1:

			ui_data_0.append(sen)
		elif sen.find('预订') != -1:

			ui_data_0.append(sen)
		elif sen.find('火车票') != -1:

			ui_data_0.append(sen)
		elif sen.find('动车票') != -1:

			ui_data_0.append(sen)
		elif sen.find('高铁票') != -1:

			ui_data_0.append(sen)
		elif sen.find('动车') != -1:

			ui_data_0.append(sen)
		elif sen.find('火车') != -1:

			ui_data_0.append(sen)
		elif sen.find('高铁') != -1:

			ui_data_0.append(sen)
		elif sen.find('车票') != -1:

			ui_data_0.append(sen)
		elif sen.find('硬座') != -1:

			ui_data_0.append(sen)
		elif sen.find('硬座票') != -1:

			ui_data_0.append(sen)
		elif sen.find('动卧票') != -1:

			ui_data_0.append(sen)
		elif sen.find('软卧票') != -1:

			ui_data_0.append(sen)
		elif sen.find('车次') != -1:

			ui_data_0.append(sen)
		else:
			ui_data_1.append(sen)
	print("ui_data_0 length::", len(ui_data_0))
	print("ui_data_1 lenght::", len(ui_data_1))
	# print("ui_data_2 lenght::", len(ui_data_2))
	# print("ui_data_3 lenght::", len(ui_data_3))
	# print("ui_data_4 lenght::", len(ui_data_4))
	# print("ui_data_5 lenght::", len(ui_data_5))


	write_data_to_txt(ui_data_0,'./out_train_tickets/0.data')
	write_data_to_txt(ui_data_1, './out_train_tickets/1.data')
	# write_data_to_txt(ui_data_2, './out/2.data')
	# write_data_to_txt(ui_data_3, './out/3.data')
	# write_data_to_txt(ui_data_4, './out/4.data')
	# write_data_to_txt(ui_data_5, './out/5.data')
if __name__ == '__main__':
	generate_sentences_UI_control()
