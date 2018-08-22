# Быстренько обучаем модель и анализируем входной текст
import numpy as np
import pandas as pd
import math
import nltk
from sklearn import linear_model
import re
import pymystem3
from collections import defaultdict
import statistics
from sklearn.model_selection import train_test_split
from nltk.tokenize import sent_tokenize

def load_dictionaries():
    global m
    m = pymystem3.Mystem(entire_input=False,disambiguation=True)

    global ridge
    ridge = linear_model.Ridge(alpha=0.1)

    global features
    features = pd.read_csv("data/list_of_features_1207.csv")

    global columns_needed
    columns_needed = ['inA2', 'kellyC2', 'simple850', 'simple1000', 'simple2000', 'dale3000','infr1000', 'infr3000', 
                    'infr5000', 'infr10000','lex_abstract','formula_smog', 'mean_len_word', 'median_len_word',
                    'median_len_sentence', 'mean_len_sentence', 'percent_of_long_words', 'mean_punct_per_sentence', 
                    'median_punct_per_sentence', 'tt_ratio', 'contentPOS', 'kotoryi/words', 'modal_verbs', 
                    'conj_adversative', 'kotoryi/sentences', 'passive', 'A', 'ADV', 'ADVPRO', 'ANUM', 'APRO', 
                    'COM', 'CONJ', 'INTJ', 'NUM', 'PART', 'PR', 'S', 'SPRO', 'V', 'наст', 'непрош', 'прош', 
                    'вин', 'дат', 'им', 'пр', 'род', 'твор', 'ед', 'мн', 'деепр', 'изъяв', 'инф', 'пов', 'прич', 'кр', 
                    'полн', 'притяж', '1-л', '2-л', '3-л', 'жен', 'муж', 'сред', 'несов', 'сов', 'действ', 'страд', 'неод', 
                    'од', 'нп', 'пе']

    ## словники ##
    slovnik_A1 = open('data/new_vocab_a1.txt','r', encoding = 'utf_8').readlines()
    global slovnik_A1_list
    slovnik_A1_list = [f.replace('\n','') for f in slovnik_A1]
    slovnik_A2 = open('data/new_vocab_a2.txt','r', encoding = 'utf_8').readlines()
    global slovnik_A2_list
    slovnik_A2_list = [f.replace('\n','') for f in slovnik_A2]
    slovnik_B1 = open('data/new_vocab_b1.txt','r', encoding = 'utf_8').readlines()
    global slovnik_B1_list
    slovnik_B1_list = [f.replace('\n','') for f in slovnik_B1]
    slovnik_B2 = open('data/new_vocab_b2.txt','r', encoding = 'utf_8').readlines()
    global slovnik_B2_list
    slovnik_B2_list = [f.replace('\n','') for f in slovnik_B2]
    slovnik_C1 = open('data/new_vocab_c1.txt','r', encoding = 'utf_8').readlines()
    global slovnik_C1_list
    slovnik_C1_list = [f.replace('\n','') for f in slovnik_C1]


    ## списки kelly ##
    kelly_A1 = open('data/kelly_a1.txt','r', encoding = 'utf_8').readlines()
    global kelly_A1_list
    kelly_A1_list = [f.replace('\n','') for f in kelly_A1]
    kelly_A2 = open('data/kelly_a2.txt','r', encoding = 'utf_8').readlines()
    global kelly_A2_list
    kelly_A2_list = [f.replace('\n','') for f in kelly_A2]
    kelly_B1 = open('data/kelly_b1.txt','r', encoding = 'utf_8').readlines()
    global kelly_B1_list
    kelly_B1_list = [f.replace('\n','') for f in kelly_B1]
    kelly_B2 = open('data/kelly_b2.txt','r', encoding = 'utf_8').readlines()
    global kelly_B2_list
    kelly_B2_list = [f.replace('\n','') for f in kelly_B2]
    kelly_C1 = open('data/kelly_c1.txt','r', encoding = 'utf_8').readlines()
    global kelly_C1_list
    kelly_C1_list = [f.replace('\n','') for f in kelly_C1]
    kelly_C2 = open('data/kelly_c2.txt','r', encoding = 'utf_8').readlines()
    global kelly_C2_list
    kelly_C2_list = [f.replace('\n','') for f in kelly_C2]

    ## Списки частотных слов ##
    fr_100 = open('data/fr_100.txt','r', encoding = 'utf_8').readlines()
    global fr_100_list
    fr_100_list = [f.replace('\n','') for f in fr_100]
    fr_300 = open('data/fr_300.txt','r', encoding = 'utf_8').readlines()
    global fr_300_list
    fr_300_list = [f.replace('\n','') for f in fr_300]
    fr_500 = open('data/fr_500.txt','r', encoding = 'utf_8').readlines()
    global fr_500_list
    fr_500_list = [f.replace('\n','') for f in fr_500]
    fr_1000 = open('data/fr_1000.txt','r', encoding = 'utf_8').readlines()
    global fr_1000_list
    fr_1000_list = [f.replace('\n','') for f in fr_1000]
    fr_3000 = open('data/fr_3000.txt','r', encoding = 'utf_8').readlines()
    global fr_3000_list
    fr_3000_list = [f.replace('\n','') for f in fr_3000]
    fr_5000 = open('data/fr_5000.txt','r', encoding = 'utf_8').readlines()
    global fr_5000_list
    fr_5000_list = [f.replace('\n','') for f in fr_5000]
    fr_10000 = open('data/fr_10000.txt','r', encoding = 'utf_8').readlines()
    global fr_10000_list
    fr_10000_list = [f.replace('\n','') for f in fr_10000]

    fr_more_than_5 = open('data/fr_more_than_5ipm.txt', 'r', encoding ='utf_8').readlines()
    global fr_more_than_5list
    fr_more_than_5list = [f.replace('\n', '') for f in fr_more_than_5]

    fr_spoken = open('data/fr_spoken.txt', 'r', encoding ='utf_8').readlines()
    global fr_spoken_list
    fr_spoken_list = [f.replace('\n', '') for f in fr_spoken]

    ##Списки слов
    simple_russian_850 = open('data/SimpleRussian850.txt', 'r', encoding ='utf_8').readlines()
    global simple_russian_850_list
    simple_russian_850_list = [f.replace('\n', '') for f in simple_russian_850]

    simple_russian_1000 = open('data/simple_russian.txt', 'r', encoding ='utf_8').readlines()
    global simple_russian_1000_list
    simple_russian_1000_list = [f.replace('\n', '') for f in simple_russian_1000]

    simple_russian_2000 = open('data/SimpleRussian2000.txt', 'r', encoding ='utf_8').readlines()
    global simple_russian_2000_list
    simple_russian_2000_list = [f.replace('\n', '') for f in simple_russian_2000]

    brown_russian_10000 = open('data/Brown10000.txt', 'r', encoding ='utf_8').readlines()
    global brown_russian_10000_list
    brown_russian_10000_list = [f.replace('\n', '') for f in brown_russian_10000]

    dale_russian_3000 = open('data/DaleRussian3000.txt', 'r', encoding ='utf_8').readlines()
    global dale_russian_3000_list
    dale_russian_3000_list = [f.replace('\n', '') for f in dale_russian_3000]


    ##семантические списки##
    lex_abstract = open('data/lex_abstract.txt','r', encoding = 'utf_8').readlines()
    global lex_abstract_list
    lex_abstract_list = [f.replace('\n','') for f in lex_abstract]

    global modal_words
    modal_words = ['хочется','нужно','надо','кажется','казаться','пожалуй','хотеть','должный',
                        'хотеться']

    global gram_features
    gram_features = ['A', 'ADV', 'ADVPRO', 'ANUM', 'APRO', 'COM', 'CONJ', 'INTJ', 'NUM', 'PART',
    'PR', 'S', 'SPRO', 'V', 'непрош', 'прош', 'им', 'пр', 'род', 'твор', 'деепр', 'изъяв','инф', 'пов', 'прич', 'кр', 'полн', 'притяж', '1-л', 
    'сред', 'несов', 'сов', 'действ', 'страд', 'неод', 'од']


def get_gr_info(element):
    gr_info = element.get('analysis')[0]['gr']
    gr_info = gr_info.replace(',', '<b>')
    gr_info = gr_info.replace('=', '<b>')
    gr_info = gr_info.split('<b>')
    return gr_info

# считаем слоги и буквы
def count_syllables(element):
    i_text = element.get('text')
    i_text_syl_counter = 0
    syllables = ['а', 'е', 'ё', 'и', 'о', 'у', 'ы', 'ь']
    for ii in i_text:
        if ii in syllables:
            i_text_syl_counter += 1
    if i_text_syl_counter == 0:
        i_text_syl_counter += 1
    number_of_syllables_list.append(i_text_syl_counter)
    words_length_list.append(len(i_text))
    if i_text_syl_counter >= 4:
        long_words_list.append(i_text_syl_counter)
    return True

#чистимся от имен, гео объектов и бастардов
def clean_from_name_geo_bastard(element):
    whole_lemmas_list.append(element.get('analysis')[0]['lex'])
    gr_info = element.get('analysis')[0]['gr']
    if 'qual' in element.get('analysis')[0]:
        if element.get('analysis')[0]['qual'] == 'bastard':
            bastard_list.append(element.get('text'))
    if (gr_info.find('имя') > 0 or gr_info.find('гео') > 0):
        geo_imen_list.append(element.get('analysis')[0]['lex'])
    if (gr_info.find('фам') > 0 or gr_info.find('отч') > 0):
        geo_imen_list.append(element.get('analysis')[0]['lex'])
    if (element.get('analysis')[0]['lex'] == 'но' or
        element.get('analysis')[0]['lex'] == 'а' or
        element.get('analysis')[0]['lex'] == 'однако' or
        element.get('analysis')[0]['lex'] == 'зато'):
        conj_adversative_list.append(element.get('analysis')[0]['lex'])
    if (element.get('analysis')[0]['lex'] in modal_words):
        modal_words_list.append(element.get('analysis')[0]['lex'])
    if element.get('analysis')[0]['lex'] == 'который':
        count_kotoryi.append(element.get('analysis')[0]['lex'])
    return True

##подсчет грам. информации##
def count_gram(element):
    gr_info = element.get('analysis')[0]['gr']
    gr_info = gr_info.replace(',','<b>')
    gr_info = gr_info.replace('=','<b>')
    gr_info = gr_info.split('<b>')
    for i in gram_features:
        if i in gr_info:
            dict_of_features[i] += 1
    if 'S' in gr_info:
        noun_list.append(element.get('analysis')[0]['lex'])
    if 'S' in gr_info or 'V' in gr_info or 'A' in gr_info or 'ADV' in gr_info:
        count_content_pos.append(element.get('analysis')[0]['lex'])
    return True

def count_passive_form(element):
    if element[0].get('analysis') and element[1].get('analysis'):
        element0_gr = get_gr_info(element[0])
        element1_gr = get_gr_info(element[1])
        if element[0].get('analysis')[0]['lex'] == 'быть' and 'прош' in element0_gr:
            if 'прич' in element1_gr:
                count_passive.append(element[1].get('text'))
    return True

##считаем пунктуацию по предложениям##
def punctuation_per_sentence(element):
    list_punctuation_score = []
    punctuation = [',','-',':',';','—']
    for i in sentences:
        counter = 0
        for ii in i:
            if ii in punctuation:
                counter += 1
        list_punctuation_score.append(counter)
    return list_punctuation_score

## Вычисляем процент слов из разных словников и частотных списков ##
def percent_of_known_words(element, list_of_words):
    known_words = [w for w in element if w in list_of_words]
    unknown_words = [f for f in element if f not in list_of_words]
    percent = len(known_words)/len(element)
    #print('Известные слова: ', known_words)
    #print('Незнакомые слова: ', unknown_words)
    return percent


##общий цикл просмотра анализа слов##
def gram_analyze(element):
    for i in element:
        count_syllables(i)
        if len(i.get('analysis')) > 0:
            clean_from_name_geo_bastard(i)
            count_gram(i)
    return True

###Начало цикла анализа этого текста
def start(this_text):
    load_dictionaries()

    global sentences
    sentences = sent_tokenize(this_text)
    whole_analyzed_text = m.analyze(this_text) #весь текст одним списком
    analyzed_bigrams = list(nltk.bigrams(whole_analyzed_text)) ## биграммочки
    global whole_lemmas_list
    whole_lemmas_list = []
    global noun_list
    noun_list = []
    global bastard_list
    bastard_list = []
    global geo_imen_list
    geo_imen_list = []
    global conj_adversative_list
    conj_adversative_list = [] #противительные союзы
    modal_words_list = []
    global words_length_list
    words_length_list = []
    global number_of_syllables_list
    number_of_syllables_list = []
    global long_words_list
    long_words_list = [] #слова более чем 4 слога
    global count_kotoryi
    count_kotoryi = []
    global count_content_pos
    count_content_pos = []
    count_passive = []

    ##СОЗДАЕМ СЛОВАРЬ СО ВСЕМИ ДАННЫМИ ИЗ ТЕКСТА##
    global dict_of_features
    dict_of_features = defaultdict(int)

    for i in gram_features:
        dict_of_features[i] = 0
    
    ##запускаем функцию со всеми грам. анализами##
    gram_analyze(whole_analyzed_text)

    for i in analyzed_bigrams:
        count_passive_form(i)

    ##меняем значения в словаре с простых счетчиков на процент встречаемости в тексте##
    for i in gram_features:
        dict_of_features[i] = dict_of_features[i] / len(whole_lemmas_list)

    clean_lemmas_list = [f for f in whole_lemmas_list if f not in geo_imen_list and f not in bastard_list]
    noun_unic_list = list(set(noun_list)) #список уникальный сущ.

    all_words = len(whole_analyzed_text)
    all_sentences = len(sentences)
    all_syllables = sum(number_of_syllables_list)
    all_letters = sum(words_length_list)
    long_words = len(long_words_list)
    all_len_words = [len(f) for f in whole_lemmas_list]
    all_len_sentences = [len(f.split(' ')) for f in sentences]

    #цифры про текст
    dict_of_features['words'] = (len(whole_analyzed_text)) #всего слов в тексте
    dict_of_features['sentences'] = (len(sentences)) #всего предложений в тексте
    dict_of_features['mean_len_word'] = (sum(words_length_list))/all_words #средняя длина слова в тексте
    dict_of_features['median_len_word'] = statistics.median(all_len_words)
    dict_of_features['median_len_sentence'] = statistics.median(all_len_sentences)
    dict_of_features['mean_len_sentence'] = all_words/all_sentences # средняя длина предложения в тексте
    dict_of_features['mean_len_word_in_syllables'] = all_syllables/all_words
    dict_of_features['percent_of_long_words'] = long_words/all_words

    #type-token ratio - number of types and the number of tokens - lexical variety
    dict_of_features['tt_ratio'] = len(whole_lemmas_list)/len(set(whole_lemmas_list))

    ## Среднее количество модальных глаголов и противительных союзов на предложение
    dict_of_features['conj_adversative'] = len(conj_adversative_list)/all_sentences
    dict_of_features['modal_verbs'] = len(modal_words_list)/all_words
    dict_of_features['kotoryi/words'] = len(count_kotoryi)/len(whole_lemmas_list)
    dict_of_features['kotoryi/sentences'] = len(count_kotoryi)/all_sentences
    dict_of_features['contentPOS'] = len(count_content_pos)/len(whole_lemmas_list)
    dict_of_features['passive'] = len(count_passive)

    ##формулы читабельности (адаптированные, из Бегтина)##
    dict_of_features['formula_smog'] = (30*(long_words/all_sentences))**0.5

    ##Доля слов, входящих в лексические минимумы##
    dict_of_features['inA1'] = percent_of_known_words(clean_lemmas_list,slovnik_A1_list)
    dict_of_features['inA2'] = percent_of_known_words(clean_lemmas_list,slovnik_A2_list)
    dict_of_features['inB1'] = percent_of_known_words(clean_lemmas_list,slovnik_B1_list)
    dict_of_features['inB2'] = percent_of_known_words(clean_lemmas_list,slovnik_B2_list)
    dict_of_features['inC1'] = percent_of_known_words(clean_lemmas_list,slovnik_C1_list)

    ##Доля слов, входящих в списки Kelly ##
    dict_of_features['kellyA1'] = percent_of_known_words(clean_lemmas_list,kelly_A1_list)
    dict_of_features['kellyA2'] = percent_of_known_words(clean_lemmas_list,kelly_A2_list)
    dict_of_features['kellyB1'] = percent_of_known_words(clean_lemmas_list,kelly_B1_list)
    dict_of_features['kellyB2'] = percent_of_known_words(clean_lemmas_list,kelly_B2_list)
    dict_of_features['kellyC1'] = percent_of_known_words(clean_lemmas_list, kelly_C1_list)
    dict_of_features['kellyC2'] = percent_of_known_words(clean_lemmas_list, kelly_C2_list)

    ##Доля слов, входящих в частотные списки##
    dict_of_features['infr100'] = percent_of_known_words(clean_lemmas_list,fr_100_list)
    dict_of_features['infr300'] = percent_of_known_words(clean_lemmas_list,fr_300_list)
    dict_of_features['infr500'] = percent_of_known_words(clean_lemmas_list,fr_500_list)
    dict_of_features['infr1000'] = percent_of_known_words(clean_lemmas_list,fr_1000_list)
    dict_of_features['infr3000'] = percent_of_known_words(clean_lemmas_list,fr_3000_list)
    dict_of_features['infr5000'] = percent_of_known_words(clean_lemmas_list,fr_5000_list)
    dict_of_features['infr10000'] = percent_of_known_words(clean_lemmas_list,fr_10000_list)
    dict_of_features['infr_more_than_5'] = percent_of_known_words(clean_lemmas_list, fr_more_than_5list)
    dict_of_features['infr_spoken'] = percent_of_known_words(clean_lemmas_list, fr_spoken_list)


    ##Доля слов, которую покрывает Simple Russian
    dict_of_features['simple850'] = percent_of_known_words(clean_lemmas_list, simple_russian_850_list)
    dict_of_features['simple1000'] = percent_of_known_words(clean_lemmas_list, simple_russian_1000_list)
    dict_of_features['simple2000'] = percent_of_known_words(clean_lemmas_list, simple_russian_2000_list)
    dict_of_features['dale3000'] = percent_of_known_words(clean_lemmas_list, dale_russian_3000_list)
    dict_of_features['brown10000'] = percent_of_known_words(clean_lemmas_list, brown_russian_10000_list)

    ##Доля абстрактных/конкретных сущ от всех сущ##
    dict_of_features['lex_abstract'] = percent_of_known_words(noun_unic_list,lex_abstract_list)

    ##Доля названий и бастардов##
    dict_of_features['lex_names_and_geo'] = len(geo_imen_list)
    dict_of_features['lex_bastards'] = len(bastard_list)


    ## Среднее количество модальных глаголов и противительных союзов на предложение
    dict_of_features['conj_adversative'] = len(conj_adversative_list)/len(sentences)
    dict_of_features['modal_verbs'] = len(modal_words_list)/all_words
    dict_of_features['kotoryi/words'] = len(count_kotoryi)/len(whole_lemmas_list)
    dict_of_features['kotoryi/sentences'] = len(count_kotoryi)/len(sentences)
    dict_of_features['contentPOS'] = len(count_content_pos)/len(whole_lemmas_list)

    ##грам. значения на предложение##
    dict_of_features['median_punct_per_sentence'] = statistics.median((punctuation_per_sentence(sentences)))#медианное пунктуации на предложение
    dict_of_features['mean_punct_per_sentence'] = sum(punctuation_per_sentence(sentences))/len(sentences)

    #for i in dict_of_features:
        #print(i, '---', "{0:.2f}".format(dict_of_features[i]))
    
    whole_analyzed_text.clear()
    analyzed_bigrams.clear()

    ##из словаря признаков делаем список##

    features_for_test_text = []
    for ii in columns_needed:
        features_for_test_text.append(dict_of_features[ii])#словарь с признаками.
    test_features_array = np.array(features_for_test_text)
    test_features_array = test_features_array.reshape(1, -1)

    x_train, y_train = features[columns_needed], features['level']
    
    #Основная функция, где обучаем модель на полученных признаках и делаем предсказание
    def fit_and_predict(y):
        ridge.fit(x_train,y_train)
        prediction = ridge.predict(y)
        return prediction
        
    prediction = fit_and_predict(test_features_array)

    interpreter = [("A0, самое начало",-10,0.2),
                ("A1",0.2,1),
                ("начало A2", 1, 1.3), 
                ("середина A2", 1.3, 1.6),
                ("конец A2", 1.6, 2),
                ("начало B1", 2, 2.3), 
                ("середина B1", 2.3, 2.6),
                ("конец B1", 2.6, 3),
                ("начало B2", 3, 3.3), 
                ("середина B2", 3.3, 3.6),
                ("конец B2", 3.6, 4),
                ("начало C1", 4, 4.3), 
                ("середина C1", 4.3, 4.6),
                ("конец C1", 4.6, 5),
                ("C2, уровень носителя", 5, 6), 
                ("ой-ой-ой, этот текст сложный даже для носителя", 6, 20)]
                
    #принимает на вход уровень текста и выдает статистику.
    def tell_me_about_text(element):
        level_int = int(round(list(element)[0])) #округленное до целых уровень, чтобы потом анализировать по средним значениям для этого уровня
        if level_int > 7:
            level_int = 7
        level_comment = ''
        for i in interpreter:
            if i[1] < element < i[2]:
                level_comment = i[0]

        #создаем словарь и будем в него все складывать
        data_about_text = defaultdict(int)
        data_about_text['level_number'] = '%.2f' %element
        data_about_text['level_comment'] = level_comment
        
        
        ##Ищем средние значения по уровням
        f_by_levels = [features.iloc[:,:][features["level"] == 0], 
                    features.iloc[:,:][features["level"] == 1], 
                    features.iloc[:,:][features["level"] == 2],
                    features.iloc[:,:][features["level"] == 3],
                    features.iloc[:,:][features["level"] == 4],
                    features.iloc[:,:][features["level"] == 5],
                    features.iloc[:,:][features["level"] == 6]]
                    
        slovnik_by_levels = [slovnik_A1_list,slovnik_A2_list,slovnik_B1_list,slovnik_B2_list, slovnik_C1_list]
        kelly_by_levels = [kelly_A1_list,kelly_A2_list,kelly_B1_list,kelly_B2_list, kelly_C1_list]

        reading_speed_learn = [10,30,50,50,100,120,120,120]
        reading_speed_watch = [20,50,100,300,400,500,500,500]
        
        ## Начинаем анализ
        #Слов в тексте
        data_about_text['words'] = dict_of_features['words']
        
        #Изучающее чтение текста должно занять... мин		
        data_about_text['reading_for_detail_speed'] = int(dict_of_features['words']/reading_speed_learn[level_int])
        
        #Просмотровое чтение текста должно занять...мин
        data_about_text['skim_reading_speed'] = int(dict_of_features['words']/reading_speed_watch[level_int])
        
        #Средняя длина предложения
        data_about_text['mean_sentence_length'] = '%.2f' % dict_of_features['mean_len_sentence']
        
        # норма для этого уровня
        data_about_text['norm_sentence_length'] = int(np.mean(f_by_levels[level_int]['mean_len_sentence']))
        
        # слишком длинное предложение, лучше разбить на несколько
        data_about_text['too_long_sentence'] = [f for f in sentences if (len(f.split(' '))-( np.mean(f_by_levels[level_int]['mean_len_sentence']) + 10) > 0)]
        
        # можем работать с лексическими списками только до 4 уровня, дальше их не существует
        if level_int < 4:
        
            # новые частотные слова (объяснить в первую очередь):
            data_about_text['new_and_frequent'] = set([f for f in clean_lemmas_list if f not in slovnik_by_levels[(level_int-1)] and f in slovnik_by_levels[level_int] and f in fr_3000_list])
            
            # нет в словнике есть в келли
            data_about_text['not_in_kelly'] = set([f for f in clean_lemmas_list if f not in slovnik_by_levels[level_int] and f in kelly_by_levels[level_int] and f in fr_3000_list])
            
            # низкочастотные слова, которых нет в минимуме (возможно, стоит заменить на синоним): 			
            data_about_text['no_minimum_no_frequent'] = set([f for f in clean_lemmas_list if f not in slovnik_by_levels[level_int] and f not in fr_10000_list ])
            
            #Неизвестные, но достаточно частотные слова 
            data_about_text['no_minimum_frequent'] = set([f for f in clean_lemmas_list if f not in slovnik_by_levels[4] and f in fr_10000_list ])
            
            #Эти слова я не понял, может, опечатка? 
            data_about_text['bastards'] = set(bastard_list)
            
            #Имена собственные 
            data_about_text['names_and_geo'] = set(geo_imen_list)
            
            return data_about_text

    data = tell_me_about_text(prediction)
    
    return data