"""
lxnet-navigator | convert_lxnet.py
Last Updated: 2022-11-06
수정자: 이웅성

description:
- 기본적으로 ndjson 포맷인 렉스넷을 여러 다른 포맷으로 변환시켜주는 함수들의 모음이다.
"""

import ndjson
import pandas as pd

def ndjson_to_pd(path: str):
    with open(path, encoding='utf-8') as f:	
        data = ndjson.load(f)													
        data = pd.DataFrame(data)

    return data

def save_csv_from_ndjson(path: str):
    with open(path, encoding='utf-8') as f:	
        data = ndjson.load(f)													
        data = pd.DataFrame(data)
        data.to_csv(f"{path[:-5]}.csv", index=False)

def save_ndjson_from_pd(df: object, save_path: str):
    df.to_json(f'{save_path}.json', orient="records", lines=True)

def give_sensekey_mapper(lxnet_mapper_path: str):
    sensekey_mapper_df = ndjson_to_pd(lxnet_path)
    sensekey_mapper = sensekey_mapper_df.set_index('sense_key')['wn_sense_key'].to_dict()

    return sensekey_mapper

def lxnet_dictionary_to_wordnet_dictionary(lxnet_paths: dict):
    sensekey_mapper = give_sensekey_mapper(give_sensekey_mapper['Mapper'])