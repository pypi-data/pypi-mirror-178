# -*- coding: UTF-8 -*-
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

import lxnet_navigator.convert_lxnet as converter

def see_shape(lxnet_paths):
    for key, lxnet_path in lxnet_paths.items():
        data = converter.ndjson_to_pd(lxnet_path)
        print("\n"+"-~"*10+f"{key}"+"~-"*10)
        print(f"\n{key} - shape")
        print(data.shape)
        print(f"\n{key} - columns")
        print(data.columns)
        print(f"\n{key} - sample")
        print(data.head(5))

def check_if_all_sense_keys_are_contained(lxnet_paths):
    all_sensekeys = converter.give_sensekey_mapper(f"{lxnet_paths['Mapper']}").keys()
    lxnet_dictionary = converter.ndjson_to_pd(f"{lxnet_paths['Dictionary']}")
    lxnet_difficulty = converter.ndjson_to_pd(f"{lxnet_paths['Mapper']}")

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