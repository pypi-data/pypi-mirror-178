# -*- coding: UTF-8 -*-
"""
lxnet-navigator | create_lxnet.py
Last Updated: 2022-11-06
수정자: 이웅성

description:
- 렉스넷 (LXNET) 1.0.0 개발을 위해 사용된 코드이며, 워드넷 3.0을 렉스넷 형태로 바꾸어준다.
- 구체적인 내재화 과정 및 과정 상의 판단 등은 사내 컨플루언스 참고 https://lxper.atlassian.net/l/cp/a8JdwmnA
"""
import time
from collections import defaultdict
import random
import string

import ndjson
import pandas as pd
import spacy
from spacy.matcher import Matcher
from nlprule import Tokenizer, Rules
from tqdm import tqdm
tokenizer = Tokenizer.load("en")
rules = Rules.load("en", tokenizer)

NLP = spacy.load('en_core_web_sm', disable = ['parser','ner'])
PLACEHOLDER = {'PLACEHOLDER': 'PLACEHOLDER'}
LXNET_PATHS = {
    'Dictionary': 'lxnet_dictionary_v.1.0.0.json',
    'Example_Sentences': 'lxnet_example_v.1.0.0.json',
    'Difficulty': 'lxnet_difficulty_v.1.0.0.json',
    'Mapper': 'sensekey_map_v.1.0.0.json',
    'Original_DB': "original_DB_map_v.1.0.0.json"
}

"""
locate_elements_from_WN_data_line (function)

description:
워드넷 data 파일에는 ready_to_hand(p)와 같은 단어들이 있는데, (p)를 제거하는 역할을 한다. 이외 bracket안에 있는것은 두 단계까지 제거 가능하다.

input:
    word (str) -> a word from WN data file
        example) ready_to_hand(p)

output:
    corrected_word (str)
"""
def bracket_remover(word):
    corrected_word = ''
    skip1 = 0
    skip2 = 0
    for i in word:
        if i == '[':
            skip1 += 1
        elif i == '(':
            skip2 += 1
        elif i == ']' and skip1 > 0:
            skip1 -= 1
        elif i == ')'and skip2 > 0:
            skip2 -= 1
        elif skip1 == 0 and skip2 == 0:
            corrected_word += i
    return corrected_word



"""
locate_elements_from_WN_data_line (function)

description:
워드넷 data 파일의 한 줄에서, 필요한 요소들을 뽑아서 return한다.

input:
    line (str) -> a line from WN data file
        example) 13260190 21 n 07 return 0 issue 0 take 0 takings 0 proceeds 0 yield 0 payoff 2 006 @ 13255145 n 0000 + 01629000 v 0602 + 02209745 v 0303 + 01629000 v 0103 ~ 13296270 n 0000 ~ 13296460 n 0000 | the income or profit arising from such transactions as the sale of land or other property; "the average return was about 5%"  \n

output:
    wn_sense_id (int)
    words (list) -> for multi-words, underscore (_) is replaced with a space
    pos (str)
    hypernyms_wn_sense_ids (list)
    hyponyms_wn_sense_ids (list)
    enDef (str)
    example_sentences (list)
"""
def locate_elements_from_WN_data_line(
    WN_data_line: str
    ) -> tuple[int, list, list, list, str, list]:

    WN_data_line = WN_data_line.strip()

    # wn_sense_id
    wn_sense_id = WN_data_line.split("|")[0].split(" ")[0]
    
    # words
    n_of_words_in_synset = int(WN_data_line.split("|")[0].split(" ")[3], base=16)
    words = []
    for idx in range(0, n_of_words_in_synset):
        word = WN_data_line.split("|")[0].split(" ")[4 + 2*idx] # identify word
        corrected_word = bracket_remover(word)
        corrected_word = corrected_word.replace("_", " ")
        words.append(corrected_word)

    # pos
    pos = WN_data_line.split("|")[0].split(" ")[2]
    if pos == 'n':
        pos = 'noun'
    elif pos == 'v':
        pos = 'verb'
    elif pos == 'a' or pos == 's':
        pos = 'adj'
    elif pos == 'r':
        pos = 'adv'

    # antonyms
    antonyms_wn_sense_ids = []
    if "!" in WN_data_line:
        n_of_antonyms_in_synset = len(WN_data_line.split("|")[0].split("! ")[1:])
        for span in WN_data_line.split("|")[0].split("! ")[1:]:
            antonyms_wn_sense_ids.append(span.split(" ")[0])

    # hypernyms
    hypernyms_wn_sense_ids = []
    if "@" in WN_data_line:
        n_of_hypernyms_in_synset = len(WN_data_line.split("|")[0].split("@ ")[1:])
        for span in WN_data_line.split("|")[0].split("@ ")[1:]:
            hypernyms_wn_sense_ids.append(span.split(" ")[0])

    # hyponyms
    hyponyms_wn_sense_ids = []
    if "~" in WN_data_line:
        n_of_hyponyms_in_synset = len(WN_data_line.split("|")[0].split("~ ")[1:])
        for span in WN_data_line.split("|")[0].split("~ ")[1:]:
            hyponyms_wn_sense_ids.append(span.split(" ")[0])

    # enDef
    enDef = WN_data_line.split("|")[1].split('"')[0]

    # example_sentences
    if '"' in WN_data_line.split("|")[1]: # if WN_data_line has example_sentences
        example_sentences = WN_data_line.split("|")[1].split('"')[1:-1] 
        for example_sentence in example_sentences:
            if len(example_sentence) < 5: # 짧은 example sentence는 제거
                example_sentences.remove(example_sentence)
                continue
    else:
        example_sentences = []
    
    return wn_sense_id, words, pos, antonyms_wn_sense_ids, hypernyms_wn_sense_ids, hyponyms_wn_sense_ids, enDef, example_sentences



"""
break_into_separate_instances (function)

description:
locate_elements_from_WN_data_line의 output 한 세트에서, 여러 단어가 포함된 synset을 여러 개의 dictionary로 나누어 list 하나로 return한다.

input:
    wn_sense_id (int)
    words (list)
    pos (str)
    antonyms_wn_sense_ids (list)
    hypernyms_wn_sense_ids (list)
    hyponyms_wn_sense_ids (list)
    enDef (str)
    example_sentences (list)

output:
    separated_instances (list)
"""
def break_into_separate_instances(
    wn_sense_id: int, 
    words: list, 
    pos: str, 
    antonyms_wn_sense_ids: str,
    hypernyms_wn_sense_ids: list, 
    hyponyms_wn_sense_ids: list,
    enDef: str, 
    example_sentences: list
    ) -> list:
    separated_instances = []
    for word in words:
        words_copy = words.copy()
        words_copy.remove(word)
        separated_instances.append(
            {
                "wn_sense_id" : wn_sense_id,
                "word" : word,
                "pos" : pos,
                "synonyms" : words_copy,
                "antonyms_wn_sense_ids" : antonyms_wn_sense_ids,
                "hypernyms_wn_sense_ids" : hypernyms_wn_sense_ids,
                "hyponyms_wn_sense_ids" : hyponyms_wn_sense_ids,
                "enDef" : enDef,
                "example_sentences" : example_sentences
            }
        )
    
    return separated_instances



"""
create_spacy_pattern_for_matching (function)

description:
단어를 받아서 그에 해당하는 spacy matcher pattern을 뽑아준다. Multi-word와 Single-word 모두 프로세스 가능하다. Multi-word 의 경우, 두 단어가 붙어 있는 것에 한해서 매칭 가능하다 (가능 예시: He "gets off". 불가능 예시: He wanted to "get" her "off".).

input:
    word (str)

output:
    spacy_pattern (list)
"""
def create_spacy_pattern_for_matching(
    word: str
    ) -> list:
    spacy_pattern = []
    for component_word in word.split(" "):
        spacy_pattern.append(
            {"LEMMA" : component_word}
        )

    return spacy_pattern



"""
remove_example_sentences_without_target_words (function)

description:
워드넷 예문은 synset 별로 주어지는데, 따라서 synset의 각 단어를 하나 씩의 행으로 만들면 어떤 예문에는 그 행의 단어가 아예 없을 수 있다. 아예 없는 단어는 예문에서 제외한다.

input:
    separated_instances (list)

output:
    removed_instances (list)
"""
def remove_example_sentences_without_target_words(
    separated_instances: list
    ) -> list :
    removed_instances = []

    for separated_instance in separated_instances:
        removed_example_sentences = []

        synonyms = separated_instance['synonyms'].copy()
        synonyms.append(separated_instance['word'])
        all_words_with_same_meaning = synonyms

        for example_sentence in separated_instance['example_sentences']:
            doc = NLP(example_sentence)
            spacy_pattern = create_spacy_pattern_for_matching(separated_instance['word'])
            matcher = Matcher(NLP.vocab)
            matcher.add("id", [spacy_pattern])
            matches = matcher(doc)

            # GRAMMAR CHECK 
            example_sentence = rules.correct(example_sentence)

            if len(matches) >= 1: #매치가 있을 경우애
                if " " not in separated_instance['word']:
                    match_id, start, end = matches[0]
                    removed_example_sentences.append(
                        {
                            'example_sentence': example_sentence,
                            'target_word_location': (
                                doc[start:end].start_char, doc[start:end].end_char
                                ),
                            'specific_location': [
                                (doc[start:end].start_char, doc[start:end].end_char)
                            ],
                            'source': 'wordnet3.0'
                        }
                    )
                elif " " in separated_instance['word']:
                    match_id, start, end = matches[0]
                    words_list = separated_instance['word'].split(" ")
                    locations = []
                    for word in words_list:
                        spacy_pattern = create_spacy_pattern_for_matching(word)
                        matcher = Matcher(NLP.vocab)
                        matcher.add("id", [spacy_pattern])
                        matches = matcher(doc)
                        location_match_id, location_start, location_end = matches[0]
                        locations.append(
                            (
                            doc[location_start:location_end].start_char, 
                            doc[location_start:location_end].end_char
                            )
                        )

                    removed_example_sentences.append(
                        {
                            'example_sentence': example_sentence,
                            'target_word_location': (
                                doc[start:end].start_char, doc[start:end].end_char
                                ),
                            'specific_location': locations,
                            'source': 'wordnet3.0'
                        }
                    )
            else:
                continue
        
        removed_instances.append(
            {
                "wn_sense_id" : separated_instance['wn_sense_id'],
                "word" : separated_instance['word'],
                "pos" : separated_instance['pos'],
                "synonyms" : separated_instance['synonyms'],
                "antonyms_wn_sense_ids" : separated_instance['antonyms_wn_sense_ids'],
                "hypernyms_wn_sense_ids" : separated_instance['hypernyms_wn_sense_ids'],
                "hyponyms_wn_sense_ids" : separated_instance['hyponyms_wn_sense_ids'],
                "enDef" : separated_instance['enDef'],
                "example_sentences" : removed_example_sentences
            }
        )

    return removed_instances



"""
change_wn_sense_ids_to_wn_sense_keys (function)

description:
워드넷 기준 Sense ID들을 워드넷 기준 Sense Key로 바꾸어준다. 지금까지는 Synonyms, Antonyms, Hypernyms, Hyponyms가 워드넷 Sense ID 로 기록되었지만, 이 평션을 거치면 이제 워드넷 Sense Key으로 바뀌어 처리되기 시작한다.

input:
    removed_instances (list)
    id_key_mapper (obj)

output:
    changed_instances (list)
"""
def change_wn_sense_ids_to_wn_sense_keys(
    removed_instances: list,
    id_key_mapper: object
    ) -> list :
    changed_instances = []

    for removed_instance in removed_instances:
        changed_synonyms = []
        changed_antonyms = []
        changed_hypernyms = []
        changed_hyponyms = []

        wn_sense_id = removed_instance['wn_sense_id']

        # word
        word = removed_instance['word']
        possible_wn_sense_keys =\
            id_key_mapper.loc[id_key_mapper["wn_sense_id"] == int(wn_sense_id)]
        possible_wn_sense_keys = possible_wn_sense_keys['wn_sense_key'].tolist()
        
        for possible_wn_sense_key in possible_wn_sense_keys:
            if possible_wn_sense_key.split("%")[0].replace("_"," ") ==\
                word.lower():
                wn_sense_key = possible_wn_sense_key
        
        # synonym
        synonyms = removed_instance['synonyms'].copy()
        if len(synonyms) >= 1:
            for synonym in synonyms:
                for possible_wn_sense_key in possible_wn_sense_keys:
                    if possible_wn_sense_key.split("%")[0].replace("_"," ") ==\
                        synonym.lower():
                        synonym_wn_sense_key = possible_wn_sense_key
                        changed_synonyms.append(synonym_wn_sense_key)

        # antonym
        antonyms_wn_sense_ids = removed_instance['antonyms_wn_sense_ids'].copy()
        if len(antonyms_wn_sense_ids) >= 1:
            for antonyms_wn_sense_id in antonyms_wn_sense_ids:
                possible_wn_sense_keys =\
                    id_key_mapper.loc[id_key_mapper["wn_sense_id"] ==\
                        int(antonyms_wn_sense_id)]
                possible_wn_sense_keys =\
                    possible_wn_sense_keys['wn_sense_key'].tolist()
                for possible_wn_sense_key in possible_wn_sense_keys:
                    changed_antonyms.append(possible_wn_sense_key)

        # hypernym
        hypernyms_wn_sense_ids = removed_instance['hypernyms_wn_sense_ids'].copy()
        if len(hypernyms_wn_sense_ids) >= 1:
            for hypernyms_wn_sense_id in hypernyms_wn_sense_ids:
                possible_wn_sense_keys =\
                    id_key_mapper.loc[id_key_mapper["wn_sense_id"] ==\
                        int(hypernyms_wn_sense_id)]
                possible_wn_sense_keys =\
                    possible_wn_sense_keys['wn_sense_key'].tolist()
                for possible_wn_sense_key in possible_wn_sense_keys:
                    changed_hypernyms.append(possible_wn_sense_key)
        
        # hyponym
        hyponyms_wn_sense_ids = removed_instance['hyponyms_wn_sense_ids'].copy()
        if len(hyponyms_wn_sense_ids) >= 1:
            for hyponyms_wn_sense_id in hyponyms_wn_sense_ids:
                possible_wn_sense_keys =\
                    id_key_mapper.loc[id_key_mapper["wn_sense_id"] ==\
                        int(hyponyms_wn_sense_id)]
                possible_wn_sense_keys =\
                    possible_wn_sense_keys['wn_sense_key'].tolist()
                for possible_wn_sense_key in possible_wn_sense_keys:
                    changed_hyponyms.append(possible_wn_sense_key)

        changed_instances.append(
            {
                "word" : str(removed_instance['word']),
                "pos" : str(removed_instance['pos']),
                "wn_sense_key" : str(wn_sense_key),
                "synonyms" : changed_synonyms , #list
                "antonyms" : changed_antonyms , #list
                "hypernyms" : changed_hypernyms, #list
                "hyponyms" : changed_hyponyms , #list
                "enDef" : removed_instance['enDef'],
                "example_sentences" : removed_instance['example_sentences']
            }
        )

    return changed_instances



"""
add_grade_frequency_and_KoDef (function)

description:
렉스넷이 존재하기 전에 관리하던 기존 DB에서 KoDef와 grade를 가져온다. 또한, example_sentences 수에 따른 frequency를 기록한다.

input:
    changed_instances: list
    original_db: object

output:
    added_instances: list
"""
def add_grade_frequency_and_KoDef(
    changed_instances: list,
    original_db: object
    ) -> list :
    added_instances = []

    for changed_instance in changed_instances:
        KoDef = original_db.loc[
            original_db['wn_sense_key'] == changed_instance['wn_sense_key']
            ]['KoDef'].values
        if len(KoDef) == 1:
            KoDef = KoDef[0]
            KoDef = str(KoDef)
            KoDef = KoDef.replace("<U>","")
            KoDef = KoDef.replace("<C>","")
            KoDef = KoDef.strip()
        else:
            KoDef = None

        grade = original_db.loc[
            original_db['wn_sense_key'] == changed_instance['wn_sense_key']
            ]['grade'].values
        if len(grade) == 1:
            grade = grade[0]
            grade = str(grade)
        else:
            grade = None

        priority = original_db.loc[
            original_db['wn_sense_key'] == changed_instance['wn_sense_key']
            ]['priority'].values
        if len(priority) == 1:
            priority = priority[0]
            priority = int(priority)
        else:
            priority = None
        
        original_db_en_def = original_db.loc[
            original_db['wn_sense_key'] == changed_instance['wn_sense_key']
            ]['original_db_en_def'].values
        if len(original_db_en_def) == 1:
            original_db_en_def = original_db_en_def[0]
            original_db_en_def = str(original_db_en_def)
        else:
            original_db_en_def = None

        EnDef = changed_instance['enDef'].replace(";","")
        EnDef = EnDef.strip()

        added_instances.append(
            {
                "word" : changed_instance['word'] ,
                "pos" : changed_instance['pos'] ,
                "priority" : priority ,
                "wn_sense_key" : changed_instance['wn_sense_key'] ,
                "synonyms" : changed_instance['synonyms'] ,
                "antonyms" : changed_instance['antonyms'] ,
                "hypernyms" : changed_instance['hypernyms'] ,
                "hyponyms" : changed_instance['hyponyms'] ,
                "grade" : grade ,
                "frequency" : str(len(changed_instance['example_sentences'])) ,
                "ko_def" : KoDef ,
                "en_def" : EnDef ,
                "original_db_en_def" : original_db_en_def,
                "example_sentences" : changed_instance['example_sentences']
            }
        )

    return added_instances



"""
map_and_create_example_sentences_database (function)

description:
예문들에 대해서는 다른 데이터베이스에 저장하고, 그 예문 키를 매핑한다.

input:
    preprocessed_instances: list

output:
    example_mapped_instances: list
"""
def map_and_create_example_sentences_database(
    preprocessed_instances: list
    ) -> list :
    example_mapped_instances = []
    example_sentences_list = []

    id_num = 0
    for preprocessed_instance in preprocessed_instances:
        preprocessed_instance_example_id = []
        for example_sentence in preprocessed_instance['example_sentences']:
            id_num += 1
            example_id = f'exmp%wordnet%{id_num}'
            location_dict_list = []
            for specific_location in example_sentence["specific_location"]:
                location_dict = {
                    'type': 'voca',
                    'start': specific_location[0],
                    'end': specific_location[1]
                }
                location_dict_list.append(location_dict)
            example_id_dictionary = {
                'example_id': example_id,
                'start': example_sentence["target_word_location"][0],
                'end': example_sentence["target_word_location"][1],
                'locations': location_dict_list
            }
            preprocessed_instance_example_id.append(example_id_dictionary)
            example_sentences_list.append(
                {   
                    'example_id': example_id,
                    'sentence': example_sentence["example_sentence"],
                    'source': 'wordnet3.0'
                }
            )
        example_mapped_instances.append(
            {
                "word" : preprocessed_instance['word'] ,
                "pos" : preprocessed_instance['pos'] ,
                "priority" : preprocessed_instance['priority'] ,
                "wn_sense_key" : preprocessed_instance['wn_sense_key'] ,
                "synonyms" : preprocessed_instance['synonyms'] ,
                "antonyms" : preprocessed_instance['antonyms'] ,
                "hypernyms" : preprocessed_instance['hypernyms'] ,
                "hyponyms" : preprocessed_instance['hyponyms'] ,
                "grade" : preprocessed_instance['grade'] ,
                "frequency" : preprocessed_instance['frequency'] ,
                "ko_def" : preprocessed_instance['ko_def'] ,
                "en_def" : preprocessed_instance['en_def'] ,
                "original_db_en_def" : preprocessed_instance['original_db_en_def'],
                "example_sentences" : preprocessed_instance_example_id
            }
        )
            
    df = pd.DataFrame(example_sentences_list)
    with open(LXNET_PATHS['Example_Sentences'], 'w', encoding='utf-8') as file:
        df.to_json(file, orient="records", lines=True, force_ascii = False)

    return example_mapped_instances



"""
give_lxnet_sensekey (function)

description:
렉스넷 센스키를 만들고 부여하는 최초의 펑션이다. 워드넷 센스키와 렉스넷 센스키의 매핑 관계를 따로 파일로 저장해놓는다. 기존 렉스퍼 어휘 DB도 정제하여 저장해놓는다.

input:
    id_key_mapper: object,
    example_mapped_instances: list

output:
    lxnet_sensekey_instances: list
"""
def give_lxnet_sensekey (
    id_key_mapper: object,
    example_mapped_instances: list
    ) -> list :
    lxnet_sensekey_instances = []
    lx_sense_key_list = []
    lx_sense_key_map = []
    random.seed(10)
    letters = string.ascii_lowercase
    original_db_instances = []

    for example_mapped_instance in example_mapped_instances:
        wn_sense_key = example_mapped_instance['wn_sense_key']

        possible_wn_sense_keys =\
            id_key_mapper.loc[id_key_mapper["wn_sense_key"] == wn_sense_key]
        possible_wn_sense_keys = possible_wn_sense_keys['ranking'].values
        wordnet_priority = possible_wn_sense_keys[0]

        lx_sense_key =\
            f"voca%{example_mapped_instance['word'].replace(' ','_')}%{example_mapped_instance['pos']}%{wordnet_priority}"

        assert lx_sense_key not in lx_sense_key_list

        lx_sense_key_list.append(lx_sense_key)
        lx_sense_key_map.append(
            {
                "sense_key" : lx_sense_key, 
                "wn_sense_key" : example_mapped_instance['wn_sense_key']
            }
        )
        if example_mapped_instance['grade'] is not None:
            original_db_instances.append(
                {
                    "wn_sense_key" : example_mapped_instance['wn_sense_key'] ,
                    "grade" : example_mapped_instance['grade'],
                    "ko_def" : example_mapped_instance['ko_def'],
                    "en_def" : example_mapped_instance['original_db_en_def'],
                }
            )
        lxnet_sensekey_instances.append(
            {
                "word" : example_mapped_instance['word'] ,
                "pos" : example_mapped_instance['pos'] ,
                "priority" : int(wordnet_priority) ,
                "lx_sense_key" : str(lx_sense_key) ,
                "wn_sense_key" : example_mapped_instance["wn_sense_key"],
                "synonyms" : example_mapped_instance['synonyms'] ,
                "antonyms" : example_mapped_instance['antonyms'] ,
                "hypernyms" : example_mapped_instance['hypernyms'] ,
                "hyponyms" : example_mapped_instance['hyponyms'] ,
                "grade" : None ,
                "frequency" : example_mapped_instance['frequency'] ,
                "ko_def" : None ,
                "en_def" : example_mapped_instance['en_def'] ,
                "example_sentences" : example_mapped_instance['example_sentences']
            }
        )
    
    df = pd.DataFrame(lx_sense_key_map)
    with open(LXNET_PATHS['Mapper'], 'w', encoding='utf-8') as file:
        df.to_json(file, orient="records", lines=True, force_ascii = False)

    df = pd.DataFrame(original_db_instances)
    with open(LXNET_PATHS['Original_DB'], 'w', encoding='utf-8') as file:
        df.to_json(file, orient="records", lines=True, force_ascii = False)

    return lxnet_sensekey_instances
        
        

"""
replace_everything_into_lx_sense_key (function)

description:
앞서 매핑 된 렉스넷 센스키를 기준으로, 나머지 워드넷 센스키도 바꾼다

input:
    lxnet_sensekey_instances: list

output:
    replaced_instances: list
"""
def replace_everything_into_lx_sense_key(
    lxnet_sensekey_instances: list
    ) -> list:
    replaced_instances = []

    with open(LXNET_PATHS['Mapper'], encoding='utf-8') as f:
        sensekey_map = pd.read_json(f, lines=True)							

    for lxnet_sensekey_instance in lxnet_sensekey_instances:
        type_dict = defaultdict(list)
        for type_word in ["synonyms","antonyms","hypernyms","hyponyms"]:
            to_search = lxnet_sensekey_instance[type_word]
            for item in to_search:
                lx_sense_key_of_item =\
                    sensekey_map.loc[sensekey_map["wn_sense_key"] == item]["sense_key"].values

                if len(lx_sense_key_of_item) == 1:
                    lx_sense_key_of_item = lx_sense_key_of_item[0]
                    type_dict[type_word].append(str(lx_sense_key_of_item))

        replaced_instances.append(
            {
                "word" : lxnet_sensekey_instance['word'] ,
                "pos" : lxnet_sensekey_instance['pos'] ,
                "priority" : lxnet_sensekey_instance['priority'] ,
                "lx_sense_key" : lxnet_sensekey_instance['lx_sense_key'] ,
                "wn_sense_key" : lxnet_sensekey_instance["wn_sense_key"],
                "synonyms" : type_dict['synonyms'] ,
                "antonyms" : type_dict['antonyms'] ,
                "hypernyms" : type_dict['hypernyms'] ,
                "hyponyms" : type_dict['hyponyms'] ,
                "grade" : lxnet_sensekey_instance['grade'] ,
                "frequency" : lxnet_sensekey_instance['frequency'] ,
                "ko_def" : lxnet_sensekey_instance['ko_def'] ,
                "en_def" : lxnet_sensekey_instance['en_def'] ,
                "example_sentences" : lxnet_sensekey_instance['example_sentences']
            }
        )

    def turn_to_list(x):
        return [x]

    sensekey_map['wn_sense_key'] = sensekey_map['wn_sense_key'].apply(turn_to_list)
    df = pd.DataFrame(sensekey_map)
    with open(LXNET_PATHS['Mapper'], 'w', encoding='utf-8') as file:
        df.to_json(file, orient="records", lines=True, force_ascii = False)
        
    return replaced_instances
            


"""
map_and_create_difficulty_database (function)

description:
렉스넷 난이도 DB를 따로 만들고, 렉스넷 딕셔너리에서는 난이도 행을 제거한다.

input:
    replaced_instances: list

output:
    difficulty_mapped_instances: list
"""
def map_and_create_difficulty_database(
    replaced_instances: list
    ) -> list :
    difficulty_mapped_instances = []
    difficulty_list = []

    id_num = 0
    for replaced_instance in replaced_instances:
        difficulty_dictionary = {
            'sense_key': replaced_instance['lx_sense_key'],
            'grade': None,
            'frequency': {
                'global': {
                    'count': replaced_instance['frequency']
                }
            }
        }
        difficulty_list.append(difficulty_dictionary)

        difficulty_mapped_instances.append(
            {
                "word" : replaced_instance['word'] ,
                "pos" : replaced_instance['pos'] ,
                "priority" : replaced_instance['priority'] ,
                "sense_key" : replaced_instance['lx_sense_key'] ,
                "synonyms" : replaced_instance['synonyms'] ,
                "antonyms" : replaced_instance['antonyms'] ,
                "hypernyms" : replaced_instance['hypernyms'] ,
                "hyponyms" : replaced_instance['hyponyms'] ,
                "ko_def" : replaced_instance['ko_def'] ,
                "en_def" : replaced_instance['en_def'] ,
                "example_sentences" : replaced_instance['example_sentences']
            }
        )
            
    df = pd.DataFrame(difficulty_list)
    with open(LXNET_PATHS['Difficulty'], 'w', encoding='utf-8') as file:
        df.to_json(file, orient="records", lines=True, force_ascii = False)

    return difficulty_mapped_instances
        


"""
load_necessary_resources (function)

description:
data 파일과 같이 큰 리소스를 제외한, 나머지 리소스들은 여기서 통합적으로 로드한다.

input:
    None

output:
    id_key_mapper: object
    original_db: object
"""
def load_necessary_resources() -> tuple[object, object, object]:
    id_key_mapper =\
        pd.read_csv(f'resources/wn_sense_ids_to_wn_sense_keys.txt', sep=" ", header=None)
    id_key_mapper.columns = ["wn_sense_key", "wn_sense_id", "ranking", "1"]

    original_db =\
        pd.read_csv('resources/original_db.csv', sep=",", header=None)
    original_db.columns = ["0", "1", "priority", "3", "grade", "KoDef","original_db_en_def", "wn_sense_key", "8", "9", "10", "11", "12", "13", "14", "15"]

    return id_key_mapper, original_db



"""
create_lxnet_from_WN (function)

description:
워드넷 파일들을 LXNET으로 만든다 (this is the only function that has to be called).

input:
    None

output:
    None
"""
def create_lxnet_from_WN():
    id_key_mapper, original_db = load_necessary_resources()
    preprocessed_instances = []
    start_time = time.time()

    for pos in tqdm(['verb','adj','adv','noun']):
        count = 0
        with open(f'resources/wordnet3.0_db/data.{pos}', 'r') as pos_file:
            while True:
                count += 1

                WN_data_line = pos_file.readline()

                # skip license statement
                if count < 30:
                    continue
                
                # detect last WN_data_line
                if not WN_data_line:
                    if pos == 'adj':
                        assert count == 18186, "wrong adj data file"
                    elif pos == 'adv':
                        assert count == 3651, "wrong adv data file"
                    elif pos == 'noun':
                        assert count == 82145, "wrong noun data file"
                    elif pos == 'verb':
                        assert count == 13797, "wrong verb data file"
                    break
                    
                wn_sense_id, words, pos, antonyms_wn_sense_ids, hypernyms_wn_sense_ids, hyponyms_wn_sense_ids, enDef, example_sentences =\
                    locate_elements_from_WN_data_line(WN_data_line)

                separated_instances =\
                    break_into_separate_instances(wn_sense_id, words, pos, antonyms_wn_sense_ids, hypernyms_wn_sense_ids, hyponyms_wn_sense_ids, enDef, example_sentences)

                removed_instances =\
                    remove_example_sentences_without_target_words(separated_instances)
                
                changed_instances =\
                    change_wn_sense_ids_to_wn_sense_keys(removed_instances, id_key_mapper)

                added_instances =\
                    add_grade_frequency_and_KoDef(changed_instances, original_db)

                preprocessed_instances.extend(added_instances)

                #if count >= 100:
                #    break

    mapped_instances =\
        map_and_create_example_sentences_database(preprocessed_instances)
    print(f"mapped_instances time: {time.time()-start_time}")
    lxnet_sensekey_instances =\
        give_lxnet_sensekey(id_key_mapper, mapped_instances)
    print(f"lxnet_sensekey_instances time: {time.time()-start_time}")
    replaced_instances =\
        replace_everything_into_lx_sense_key(lxnet_sensekey_instances)
    print(f"replaced_instances time: {time.time()-start_time}")
    difficulty_mapped_instances =\
        map_and_create_difficulty_database(replaced_instances)
    print(f"difficulty_mapped_instances time: {time.time()-start_time}")
    df = pd.DataFrame(difficulty_mapped_instances )
    with open(LXNET_PATHS['Dictionary'], 'w', encoding='utf-8') as file:
        df.to_json(file, orient="records", lines=True, force_ascii = False)
    print(f"save time: {time.time()-start_time}")
    print("SUCCESS!")

if __name__ == '__main__':
    create_lxnet_from_WN()



"""
inflate_with_example_sentences_semcor_and_omsti (function)

description:
SemCor와 Omsti 데이터셋에서 추가 예문을 가져오고, 예문의 갯수에 따른 Priority를 매기고 frequency도 기록한다. semcor+omsti.data.xml 데이터셋은 한 번에 불러오기 너무 사이즈가 크기 때문에, 따로 코드 상에 저장해두지 않고, 새로운 인스턴스마다 다시 찾는 과정을 실시한다. 시간은 느리겠지만, 이런 방식으로 코드를 짜야 렉스퍼 서버 다운을 방지 할 수 있다.

input:
    added_instances: list,
    raganato_gold: object

output:
    inflated_instances: list
"""
def inflate_with_example_sentences_semcor_and_omsti(
    added_instances: list,
    raganato_gold: object
    ) -> list:
    inflated_instances = []

    for added_instance in added_instances:
        locations = raganato_gold.loc[
            raganato_gold['wn_sense_key'] == added_instance['wn_sense_key']
            ]['location'].values
        found_example_sentences = []
        if len(locations) >= 1: #해당 센스키가 출현한 위치들을 찾는다
            for location in locations: #위치마다 예문을 가져온다
                sentence_location = ".".join(location.split(".")[0:2])
                instance_location = location
                if len(instance_location) == 14: 
                    current_corpus = "semcor"
                elif len(instance_location) == 23: 
                    current_corpus = "omsti"
                found_flag = False
                found_example_sentence = ""
                #'resources/WSD_Training_Corpora/SemCor+OMSTI/semcor+omsti.data.xml'
                with open(f'resources/WSD_Training_Corpora/SemCor/semcor.data.xml', 'r') as data_file:
                    #count = 10000
                    while True:
                        #count += 1
                        #print(count)
                        data_line = data_file.readline()
                        if data_line.strip() ==\
                            f'<sentence id="{sentence_location}">':
                            found_flag = True
                            #print(sentence_location)
                            #print(data_line)
                            #print("found start of sentence")
                            continue
                        if found_flag == True:
                            if f'<instance id="{instance_location}">' in data_line.strip():
                                #print(instance_location)
                                #print(data_line)
                                #print("found instance")
                                word = data_line.split(">")[1].replace('</instance','')
                                found_example_sentence += word
                                found_example_sentence += ' '
                            elif data_line.strip() == "</sentence>":
                                break
                            else:
                                word = data_line.split(">")[1].replace('</wf','')
                                word = word.replace('</instance','')
                                # basic preprocessing
                                word = word.replace("&apos;","'")
                                if "&amp;" in word: 
                                    word = ""
                                found_example_sentence += word
                                found_example_sentence += ' '

                doc = NLP(found_example_sentence)
                spacy_pattern = create_spacy_pattern_for_matching(added_instance['word'])
                matcher = Matcher(NLP.vocab)
                matcher.add("id", [spacy_pattern])
                matches = matcher(doc)

                # GRAMMAR CHECK
                found_example_sentence = rules.correct(found_example_sentence)

                if len(matches) >= 1: #매치가 있을 경우애
                    match_id, start, end = matches[0]
                    found_example_sentences.append(
                        {
                            'example_sentence': found_example_sentence,
                            'target_word_location': (
                                doc[start:end].start_char, doc[start:end].end_char
                                ),
                            'source': current_corpus
                        }
                    )
                else:
                    continue
        
        inflated_example_sentences = added_instance['example_sentences'].copy()
        inflated_example_sentences.extend(found_example_sentences)

        frequency = len(inflated_example_sentences)

        inflated_instances.append(
            {
                "word" : added_instance['word'] ,
                "pos" : added_instance['pos'] ,
                "synonyms" : added_instance['synonyms'] ,
                "antonyms" : added_instance['antonyms'] ,
                "hypernyms" : added_instance['hypernyms'] ,
                "hyponyms" : added_instance['hyponyms'] ,
                "grades" : added_instance["grades"] ,
                "frequencies" : [
                    {
                        "frequency": frequency,
                        "source": "LXNET_v.1.0.0"
                    }
                ] ,
                "KoDefs" : added_instance["KoDefs"] ,
                "EnDefs" : added_instance["EnDefs"] ,
                "example_sentences" : inflated_example_sentences
            }
        )

    return inflated_instances

"""
load_necessary_resources (function)

description:
data 파일과 같이 큰 리소스를 제외한, 나머지 리소스들은 여기서 통합적으로 로드한다.

input:
    None

output:
    id_key_mapper: object
    original_db: object
    raganato_gold: object
"""
def load_necessary_resources() -> tuple[object, object, object]:
    id_key_mapper =\
        pd.read_csv(f'resources/wn_sense_ids_to_wn_sense_keys.txt', sep=" ", header=None)
    id_key_mapper.columns = ["wn_sense_key", "wn_sense_id", "0", "1"]

    original_db =\
        pd.read_csv('resources/original_db.csv', sep=",", header=None)
    original_db.columns = ["0", "1", "2", "3", "grade", "KoDef","6", "wn_sense_key", "8", "9", "10", "11", "12", "13", "14", "15"]
    # 'resources/WSD_Training_Corpora/SemCor+OMSTI/semcor+omsti.gold.key.txt'
    raganato_gold =\
        pd.read_csv(f'resources/WSD_Training_Corpora/SemCor/semcor.gold.key.txt', sep=" ", header=None, error_bad_lines=False)
    raganato_gold.columns = ["location", "wn_sense_key"]

    return id_key_mapper, original_db, raganato_gold