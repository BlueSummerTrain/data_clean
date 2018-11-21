#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 根据关键字匹配清洗数据
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from random import shuffle
import re

# Original_corpus_dir = '/home/lj/data_clean/air_tickets.data/'
# #Original_corpus_in = '/home/wyy/cls-nlp/cls_scene/corpus/'
# Original_corpus_out = '/home/lj/data_clean/out_air_tickets'
input_dir = '/home/lj/data_clean/air_tickets.data/'
out_dir_1 = '/home/lj/data_clean/out_air_tickets1/'
out_dir_2 = '/home/lj/data_clean/out_air_tickets2/'
import random
import linecache

def get_data_item(line_num, path):
    while True:
        i = random.randint(0, line_num)
        name_line = linecache.getline(path, i)
        if name_line != '':
            break
    return name_line.strip().decode('utf-8')

def write_data_to_txt(data, file_dir, mode='a'):
    """
    :param file_dir: 
    :return: 
    """
    try:
        import os
        dirs, file_name = os.path.split(file_dir)
        if not os.path.isdir(dirs):
            os.makedirs(dirs)
        fp = open(file_dir, mode)
        for item in data:
            item = str(item)
            item = item.replace(' ', '')
            fp.write(item + "\n")
        fp.close()
        print "write %d into %s" % (len(data), file_dir)
    except IOError:
        print("fail to open file")

def write_data_to_txt2(data, file_dir, mode='w'):
    """
    :param file_dir:
    :return:
    """
    try:
        import os
        dirs, file_name = os.path.split(file_dir)
        if not os.path.isdir(dirs):
            os.makedirs(dirs)
        fp = open(file_dir, mode)
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
        line = ''.join(line).replace(" ", "")
        if '' != line:
            data_list.append(line)
    return data_list


def get_repeat_item(input_1, input_2):
    ret_list = list((set(input_1).union(set(input_2)))
                    ^ (set(input_1) ^ set(input_2)))
    return ret_list


def check_repeat(input_file_path, check_dir, out_file_name = None):
    sens = read_data_from_txt(input_file_path)
    all_repeat_item = []
    for parent, dirnames, filenames in os.walk(check_dir):
        for filename in filenames:
            file_path = os.path.join(parent, filename)
            if file_path != input_file_path:
                #print file_path
                check_sens = read_data_from_txt(file_path)
                ret_list = get_repeat_item(sens, check_sens)
                # if len(ret_list) == 0:
                #     print filename + " is clean!"
                # else:
                if len(ret_list) != 0:
                    print file_path
                    print filename + ",find repeat items ,ret_list len::%d" % len(ret_list)
                    all_repeat_item.extend(ret_list)
                    for item in ret_list:
                        print item

    write_data_to_txt(all_repeat_item, out_file_name,"a")


def check_file(input_file_path):
    sens = read_data_from_txt(input_file_path)
    _sens = list(set(sens))

    ori_len = len(sens)
    print os.path.basename(input_file_path) + ",length: %d" % ori_len
    write_data_to_txt(_sens, input_file_path)


def check_dir(input_dir):
    for parent, dirnames, filenames in os.walk(input_dir):
        for filename in filenames:
            file_path = os.path.join(parent, filename)
            check_file(file_path)


def get_samples_from_file(file_dir, samples_name, sentence_max_length=20, nums=20000):
    sentences = read_data_from_txt(file_dir)
    shuffle(sentences)
    samples = []
    for i in range(len(sentences)):
        if len(sentences[i]) < sentence_max_length:
            if len(samples) < nums:
                samples.append(sentences[i])
            else:
                break

    write_data_to_txt(samples, samples_name)


def filter_file_with_keyword(sentences, keyword, out_dir):

    filter_sens = []
    for sen in sentences:
        if sen.find(keyword) == -1:
            filter_sens.append(sen)

    # return filter_sens
    write_data_to_txt(filter_sens, out_dir)


def remove_repeat(input_file_path, check_dir):
    sens = read_data_from_txt(input_file_path)

    for parent, dirnames, filenames in os.walk(check_dir):
        for filename in filenames:
            file_path = os.path.join(parent, filename)
            if file_path != input_file_path:
                print file_path
                check_sens = read_data_from_txt(file_path)
                ret_list = get_repeat_item(sens, check_sens)
                if len(ret_list) == 0:
                    print filename + " is clean!"
                else:
                    print filename + ",find repeat items ,ret_list len::%d" % len(ret_list)
                    sens = list(set(sens) - set(ret_list))
    write_data_to_txt(sens, input_file_path)


def remove_repeat_in_dir(input_file_path, check_dir):
    sens = read_data_from_txt(input_file_path)

    for parent, dirnames, filenames in os.walk(check_dir):
        for filename in filenames:
            file_path = os.path.join(parent, filename)
            if file_path != input_file_path:
                print file_path
                check_sens = read_data_from_txt(file_path)
                print("check_sens len: ", len(check_sens))
                ret_list = get_repeat_item(sens, check_sens)
                if len(ret_list) == 0:
                    pass
                    # print filename + " is clean!"
                else:
                    # print file_path
                    print filename + ",find repeat items ,ret_list len::%d" % len(ret_list)
                    clean_sens = list(set(check_sens) - set(ret_list))
                    print("sens len: ", len(clean_sens))
                    write_data_to_txt(clean_sens, file_path, "w")


def clean_corpus(input_file_path, out_dir):
    sens = read_data_from_txt(input_file_path)
    clean_sens = []
    for sen in sens:
        _sen = ''.join(re.findall(u'[\u4e00-\u9fff]+', sen))
        if _sen != '' and len(_sen) < 32:
            clean_sens.append(_sen)
    print len(sens)
    print len(clean_sens)
    clean_sens = list(set(clean_sens))
    print len(clean_sens)
    # for sen in clean_sens:
    #     #print sen
    #     #$print len(sen)
    shuffle(clean_sens)
    write_data_to_txt(clean_sens, out_dir)


def clean_repeats_in_dir(input_dir):

    for parent, dirnames, filenames, in os.walk(input_dir):

        for filename in filenames:
            file_path = os.path.join(parent, filename)
            check_repeat(file_path, input_dir, 'd.txt')

air_tickets_keyword = ['定', '预定', '机票', '航班', '飞机']

video_keyword = ['看', '片', '秀', '剧', '集', '期', '季', '部', '放映', '电影', '电视', '视频',
                 '节目', '相声', '小品', '动画', '动漫', '杂技', '魔术', '综艺', '卡通', '直播', '演的',
                 '主角', '高清的', '480p的', '720p的', '超清', '演出的', '演', '字幕', '拍的', '上映',
                 '1080p', '标清', 'mv']

music_keyword = ['听', '歌', '曲', '音乐', '首', '乐队', '唱', '专辑']

multi_keyword = ['的呢', '的']


def filter_dir_with_keywords(input_dir, keywords, out_dir_1, out_dir_2):

    # for parent, dirnames, filenames in os.walk(input_dir):
        # for filename in filenames:
        #     file_path = os.path.join(parent, filename)
            sens = read_data_from_txt(input_dir)
            media_sens = []
            video_sens = []
            for _sen in sens:
                is_media = True
                i = 0
                while is_media:
                    if i >= len(air_tickets_keyword):
                        break
                    if _sen.find(air_tickets_keyword[i]) != -1:
                        # if _sen.endswith(keywords[i]):
                        is_media = False
                    i += 1
                if is_media:
                    media_sens.append(_sen)
                else:
                    video_sens.append(_sen)
            write_data_to_txt(media_sens, out_dir_1+0)
            write_data_to_txt(video_sens, out_dir_2+1)


def remove_repeat_in_sens(input_file_path):
    """if sen is abcabc clean it be abc"""
    sens = read_data_from_txt(input_file_path)
    clean_sens = []
    for sen in sens:
        repeat_index = len(sen)/2
        if sen[:repeat_index] == sen[repeat_index:]:
            clean_sens.append(sen[:repeat_index])
        else:
            clean_sens.append(sen)

    write_data_to_txt(clean_sens, input_file_path)


def clean_sens_repeat_in_dir(input_dir):

    for parent, dirnames, filenames, in os.walk(input_dir):

        for filename in filenames:
            file_path = os.path.join(parent, filename)
            remove_repeat_in_sens(file_path)


def lower_sens_in_dir(input_dir):
    for parent, dirnames, filenames, in os.walk(input_dir):
        for filename in filenames:
            clean_sens = []
            file_path = os.path.join(parent, filename)
            sens = read_data_from_txt(file_path)
            sens = list(set(sens))
            for sen in sens:
                clean_sens.append(sen.strip().lower())
            write_data_to_txt(clean_sens, file_path)


def filter_sens_with_length(input_dir, sens_length, out_dir):
    out_sens = []
    for parent, dirnames, filenames, in os.walk(input_dir):
        for filename in filenames:

            file_path = os.path.join(parent, filename)
            sens = read_data_from_txt(file_path)
            sens = list(set(sens))
            for sen in sens:
                if len(sen) <= sens_length:
                    out_sens.append(sen)

    write_data_to_txt(out_sens, out_dir)

def generate_neg_samples(input_file, vocab_path,out_dir):
    sens = read_data_from_txt(input_file)
    neg_sens = []
    for sen in sens:
        print sen
        for i in range(random.randint(1,10)):
            neg_sen = ''
            neg_length = random.randint(4,8)
            word_1 = sen[0]
            if len(sen) ==2:
                word_2 = sen[1]
            index_1 = random.randint(0,neg_length-1)
            index_2 = random.randint(0,neg_length-1)
            for i in range(neg_length):
                neg_sen += get_data_item(2000,vocab_path)
            neg_sen = list(neg_sen)
            neg_sen[index_1] = word_1
            if len(sen) ==2:
                neg_sen[index_2] = word_2
            neg_sen = ''.join(neg_sen)
            print neg_sen
            neg_sens.append(neg_sen)

    write_data_to_txt(neg_sens,out_dir)

def check_repeat_self_repeat(inputname, repeat):
    sens1 = read_data_from_txt(inputname)
    print "sens1",len(sens1)
    sens2 = read_data_from_txt(repeat)
    print "sens2",len(sens2)
    sens3 = [ i for i in sens1 if i not in sens2 ]
    print "sens1 - sens2",len(sens3)
    write_data_to_txt(sens3, inputname, "w")

def check_repeat_self1(Original_corpus_dir):
    for parent, dirnames, filenames in os.walk(Original_corpus_dir):
        for filename in filenames:
            file_path = os.path.join(parent, filename)
            sens = read_data_from_txt(file_path)
            print "oldlen",len(sens)
            sens = list(set(sens))
            print "newlen",len(sens)
            write_data_to_txt(sens, file_path.replace('corpus', 'corpus_clean'),"a")
            #write_data_to_txt(sens, file_path, "w")
def check_repeat_self2(Original_corpus_dir):
    for parent, dirnames, filenames in os.walk(Original_corpus_dir):
        for filename in filenames:
            file_path = os.path.join(parent, filename)
            sens = read_data_from_txt(file_path)
            print "oldlen",len(sens)
            sens = list(set(sens))
            print "newlen",len(sens)
            #write_data_to_txt(sens, file_path.replace('corpus', 'corpus_clean'),"a")
            write_data_to_txt(sens, file_path, "w")
def sort_self(Original_corpus_in):
    for parent, dirnames, filenames in os.walk(Original_corpus_in):
        for filename in filenames:
            file_path = os.path.join(parent, filename)
            sens = read_data_from_txt(file_path)
            sens.sort()
            write_data_to_txt(sens, file_path, "w")

dirlist = []
def getnameanddirlist(Original_corpus_out):
    for parent, dirnames, filenames in os.walk(Original_corpus_out):
        label = parent[parent.rfind('/') + 1:]
        print(label)
        for filename in filenames:
            #file_path = os.path.join(parent, filename)
            dirlist.append(label + '/' +filename)
            #print(file_path)
if __name__ == '__main__':
    # check_repeat_self1(Original_corpus_in)
    # sort_self(Original_corpus_out)
    # getnameanddirlist(Original_corpus_out)
    # for filename in dirlist:
    #   check_repeat(Original_corpus_out + filename, Original_corpus_out, Original_corpus_dir + 'repeat.data')
    # check_repeat_self2(Original_corpus_dir)
	filter_dir_with_keywords(input_dir, air_tickets_keyword, out_dir_1, out_dir_2)

    # for filename in dirlist:
    #     check_repeat_self_repeat(Original_corpus_out + filename, Original_corpus_dir + 'repeat.data')
    # remove_repeat_in_dir(Original_corpus_dir + 'repeat.data', Original_corpus_out)
    #check_file(Original_corpus_dir+ 'tv_control/tv_ui.data')
    # check_file('./disaster_warn.data')
    # check_dir(Original_corpus_dir+'image_scene_interactive/')
    # get_samples_from_file('./_unuse_music_on_demand.data',
    #                       './music_20000.data')
    # check_file('./music_20000.data')
    # filter_file_with_keyword('./music_20000.data','唱')
    # check_file('./918/corpus_918.data')
    #remove_repeat('./918/corpus_918.data', Original_corpus_dir)
    # clean_corpus('./109/chat.data','./109/clean_chat.data')
    #filter_file_with_keyword('./109/chat_unknow.data', '鸡', './109/chat_un.data')
   # clean_corpus('./109/chat_un.data','./109/chat1.data')
    #check_repeat(Original_corpus_dir+'multi-turn_dialogue/multi-turn_dialogue.data', Original_corpus_dir+'tv_control/', './tv_control&mul.repeats')
    #check_repeat(Original_corpus_dir+'multi-turn_dialogue/multi-turn_dialogue.data', Original_corpus_dir+'chat/', './chat&mul.repeats')
    # remove_repeat_in_dir('./chat&mul.repeats',Original_corpus_dir+'chat/')
    # remove_repeat_in_dir('./household&mul.repeats',Original_corpus_dir+'household_appliance_control/')
    # remove_repeat_in_dir('./tv_control&mul.repeats',Original_corpus_dir+'tv_control/')
    #check_repeat(Original_corpus_dir+'multi-turn_dialogue/multi-turn_dialogue.data', Original_corpus_dir+'app_control/', './app_control&mul.repeats')
    # remove_repeat_in_dir('./app_control&mul.repeats',Original_corpus_dir+'app_control/')
    #check_repeat(Original_corpus_dir+'multi-turn_dialogue/multi-turn_dialogue.data', Original_corpus_dir+'weather/', './weather&mul.repeats')
    # remove_repeat_in_dir('./weather&mul.repeats',Original_corpus_dir+'weather/')
    # check_dir('./corpus/')
    # clean_repeats_in_dir('./corpus/')

    #filter_dir_with_keywords('./1031/media/', multi_keyword, './media/', './mul/')
    #filter_dir_with_keywords('./video', video_keyword, './media/', './clean_video/')
    #filter_dir_with_keywords('./1031/media/', video_keyword, './1031/media/', './1031/video/')
    #check_repeat('./1101/app_control/app_control.data', './1101/tv_control/','./1101/repeats.data')
    #remove_repeat_in_dir('./1103/error_sentences.txt',
    #                     '/home/lee/workspace/cls-nlp_git/cls-nlp/cls_scene/corpus_new/')
    # remove_repeat_in_sens('./1103/error_sentences.txt')
    # clean_sens_repeat_in_dir('./1103/out_linan/')
    # lower_sens_in_dir('./corpus/')
    #filter_sens_with_length(Original_corpus_dir,2,'./sens.data')
    #generate_neg_samples('./sens.data', './vocab','./negs.data')
