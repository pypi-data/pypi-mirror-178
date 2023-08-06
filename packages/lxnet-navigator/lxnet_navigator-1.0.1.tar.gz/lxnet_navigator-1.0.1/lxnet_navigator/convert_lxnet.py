# -*- coding: UTF-8 -*-
"""
lxnet-navigator | convert_lxnet.py
Last Updated: 2022-11-06
수정자: 이웅성

description:
- 기본적으로 ndjson 포맷인 렉스넷을 여러 다른 포맷으로 변환시켜주는 함수들의 모음이다.
"""
from collections import defaultdict

import ndjson
import pandas as pd

def ndjson_to_pd(path: str):
    with open(path, encoding='utf-8') as f:	
        data = ndjson.load(f)													
        data = pd.DataFrame(data)

    return data

def save_csv_from_ndjson(path: str, save_path: str):
    with open(path, encoding='utf-8') as f:	
        data = ndjson.load(f)													
        data = pd.DataFrame(data)
        data.to_csv(f"{save_path}.csv", index=False)

def save_ndjson_from_pd(df: object, save_path: str):
    df.to_json(f'{save_path}.json', orient="records", lines=True)

def give_sensekey_mapper(lxnet_mapper_path: str):
    sensekey_mapper_df = ndjson_to_pd(lxnet_mapper_path)
    sensekey_mapper = sensekey_mapper_df.set_index('sense_key')['wn_sense_key'].to_dict()

    return sensekey_mapper

def lxnet_dictionary_to_wordnet_dictionary(lxnet_paths: dict, save_path: str):
    sensekey_mapper = give_sensekey_mapper(lxnet_paths['Mapper'])
    lxnet_dictionary = ndjson_to_pd(f"{lxnet_paths['Dictionary']}")
    lxnet_dictionary = lxnet_dictionary.to_dict('records')
    new_dictionary = []

    for row in lxnet_dictionary:
        new_sense_key = sensekey_mapper[row['sense_key']][0]
        relation_dictionary = defaultdict(list)
        for relation in ['synonyms','antonyms','hypernyms','hyponyms']:
            for sense_key in row[relation]:
                new_sense_key_ = sensekey_mapper[sense_key][0]
                relation_dictionary[relation].append(new_sense_key_)
        
        new_row = {
            'word': row['word'],
            'pos' : row['pos'],
            'sense_key': new_sense_key,
            'en_def': row['en_def'],
            'synonyms': relation_dictionary['synonyms'],
            'antonyms': relation_dictionary['antonyms'],
            'hypernyms': relation_dictionary['hypernyms'],
            'hyponyms': relation_dictionary['hyponyms'],
        }
        new_dictionary.append(new_row)
    df = pd.DataFrame(new_dictionary)
    save_ndjson_from_pd(df, save_path)
    