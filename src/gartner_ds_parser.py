import pandas as pd
import sys
import os
import pprint
import xlrd
import textacy
from spacy.language import Language
import spacy
# Set up english as the language for the text
lang = spacy.load('en_core_web_sm')

# --------------------- #
# SET (True) this flag to have the input file processed
# UNSET if already done (False)
TO_PROCESS = False
# --------------------- #


# Global variables #
data_file_loc = './../data/gartner'
data_file_name = 'gartner.xlsm'
data_file_path = data_file_loc + '/' + data_file_name
clean_file_name = 'gartner_clean.csv'

# ------------- Methods ------------------ #

def get_feed_template():
    dict = {
        'class': None,
        'hyponym': None,
        'text': None
    }
    return dict


def get_gartner_data_columns():
    col_dict = {
        'name': 1,
        'text1': 2,
        'text2': 6,
        'text3': 7,
        'text4': 8,
        'instance': 12
    }
    return col_dict


def clean_text(text):
    comma = ','
    new_line = '/\n'
    ret_char = '/\r'
    comma_replacement = ' && '
    text = text.replace(ret_char, comma_replacement)
    text = text.replace(comma, comma_replacement)
    text = text.replace(new_line, comma_replacement)
    text = text.replace('/\t', ' ')
    text = text.lstrip(";-.,!")
    text = text.rstrip(";-.,!/\n")
    text = text.encode('ascii', 'ignore')
    return str(text)



def process_assc_text(text):
    text = text.replace("\'", ' ')
    text = text.replace('"', ' ')
    text = text.replace(' && ', ' ')
    text = text.replace('\t', ' ')
    text = text.replace('\r\n', ' ')
    text = textacy.preprocess.normalize_whitespace(text)
    text = textacy.preprocess.remove_accents(text)
    text = textacy.preprocess.replace_urls(text,' ')

    doc = textacy.doc.Doc(content=text,lang=lang)
    itr_named_ent = textacy.extract.named_entities(doc)
    itr_words = textacy.extract.words(doc)
    itr_noun_chunks = textacy.extract.noun_chunks(doc)

    named_entities = []
    noun_chunks = []
    words = []

    for i in itr_named_ent:
        named_entities.append(i)

    for i in itr_noun_chunks:
        noun_chunks.append(str(i))

    for i in itr_words:
        words.append(str(i))

    text_dict = {
        'named_entities' : named_entities,
        'noun_chunks' : noun_chunks,
        'words' : words
    }

    return text_dict


def clean_gartner_data():
    if not TO_PROCESS:
        return

    global clean_file_name
    global data_file_loc
    global data_file_name
    name_col = 1
    col_dict = get_gartner_data_columns()
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
            cur_line += 1
            for key, val in col_dict.iteritems():
                data = clean_text(worksheet.cell(cur_line, val).value)
                dict[key] = data
            data_dict[line_count] = dict
            line_count += 1
        except:
            break

    # Create data-frame!
    df = pd.DataFrame(columns=col_dict.keys())

    for line_num, data in data_dict.iteritems():
        d = {}
        for _a, _b in data.iteritems():
            d[_a] = [_b]
        _df = pd.DataFrame(d)
        df = df.append(_df, ignore_index=True)

    df = df.reset_index()
    clean_file_path = data_file_loc + '/' + clean_file_name
    df.to_csv(clean_file_path, index=False)
    pprint.pprint(df)
    return

# This function provides data to the seed graph #
def gen_data_to_feed():
    global data_file_loc
    global clean_file_name
    cleaned_file_path = data_file_loc + '/' + clean_file_name
    df = pd.read_csv(cleaned_file_path, index_col=0)

    for i, row in df.iterrows():
        dict = get_feed_template()
        dict['class'] = row['name']
        dict['hyponym'] = str(row['instance']).split(';')
        text = ' '.join([str(row['text1']), str(row['text2']), str(row['text3']), str(row['text4'])])

        dict['text'] = process_assc_text(text)
        yield dict


# --------------------- Call methods! ---------------------- #
clean_gartner_data()

# for i in gen_data_to_feed():
#     print i
