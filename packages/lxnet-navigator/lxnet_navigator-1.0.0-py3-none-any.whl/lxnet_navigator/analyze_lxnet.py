"""
lxnet-navigator | analyze_lxnet.py
Last Updated: 2022-11-19
수정자: 이웅성

description:
- 렉스넷 버전 업데이트를 위한 함수들의 모음이다.
"""

import ndjson
import pandas as pd
import numpy as np
from tqdm import tqdm

import lxnet_navigator.convert_lxnet

# 필요에 따라 path 수정
LXNET_PATHS = {
    'Dictionary': '../lxnet_v.1.0.1_json/lxnet_dictionary_v.1.0.1.json',
    'Example': '../lxnet_v.1.0.1_json/lxnet_example_v.1.0.1.json',
    'Difficulty': '../lxnet_v.1.0.1_json/lxnet_difficulty_v.1.0.1.json',
    'Mapper': '../lxnet_v.1.0.1_json/sensekey_map_v.1.0.1.json'
}

def see_shape(LXNET_PATHS):
    for key, LXNET_PATH in LXNET_PATHS.items():
        data = convert_lxnet.ndjson_to_pd(LXNET_PATH)
        print("\n"+"-~"*10+f"{key}"+"~-"*10)
        print(f"\n{key} - shape")
        print(data.shape)
        print(f"\n{key} - columns")
        print(data.columns)
        print(f"\n{key} - sample")
        print(data.head(5))

def check_if_all_sense_keys_are_contained(LXNET_PATHS):
    all_sensekeys = convert_lxnet.give_sensekey_mapper(f"{LXNET_PATHS['Mapper']}").keys()
    lxnet_dictionary = convert_lxnet.ndjson_to_pd(f"{LXNET_PATHS['Dictionary']}")
    lxnet_difficulty = convert_lxnet.ndjson_to_pd(f"{LXNET_PATHS['Mapper']}")

    all_sensekeys = list(all_sensekeys)

    lxnet_dictionary_sensekeys = lxnet_dictionary['sense_key'].values
    lxnet_difficulty_sensekeys = lxnet_difficulty['sense_key'].values

    miss_flag_dictionary = False
    for sense_key in tqdm(all_sensekeys):
        if sense_key not in lxnet_dictionary_sensekeys:
            miss_flag_dictionary = True
    
    miss_flag_difficulty = False
    for sense_key in tqdm(all_sensekeys):
        if sense_key not in lxnet_difficulty_sensekeys:
            miss_flag_difficulty = True

    print(miss_flag_dictionary)
    print(miss_flag_difficulty)

if __name__ == "__main__":
    #see_shape(LXNET_PATHS)
    check_if_all_sense_keys_are_contained(LXNET_PATHS)