"""
People and Roots of People Extractor

Allows for checking if a word processed by Stanza refers to a person.

This file can be imported as a module and contains the following
functions:

    * check_refers_to_person - returns the bool value refering to whether the word passed as argument refers to a person or not
    * get_roots_of_people_and_people - returns five lists: 
        - words in a Stanza parsed sentence that refer to people; 
        - their respective heads in the sentence;
        - ids of proper nouns;
        - nouns that have an already existing gender-neutral alternative (gn_keep)
        - nouns that are already gender-neutral (gn_p)


"""
import nltk
from nltk.corpus import wordnet as wn
from gn_grammar import gn_nouns_non_people, truly_gn_alternatives, truly_gn_terms, pronouns_that_are_always_people, nouns_that_are_always_people

def check_refers_to_person(word):
    # Checks if noun is not a person (but wordnet tags as such)
    if word.text in gn_nouns_non_people: 
        return False
    # Checks if noun is already gender-neutral
    elif word.text in truly_gn_alternatives.keys():
        return True
    
    # Case where word does not exist in the wordnet - we check our own list
    if len(wn.synsets(word.lemma, lang="por")) == 0 and word in nouns_that_are_always_people:
        #print(word, "NÃO CONHECEMOS MAS É PESSOA\n")
        return True
    
    for i, syn in enumerate(wn.synsets(word.lemma, lang="por")):
        # we only check the first 2 synsets
        if i > 2:
            return False
        if syn.lexname() == "noun.person":
            #print(word, "É pessoa\n")
            return True
        
    #print(word, "NAO É pessoa\n")
    return False
        
        


        


def get_roots_of_people_and_people(sentence, ner_proper_nouns):
    r = []
    p = []
    gn_p = {}
    gn_keep = []
    proper_nouns = []
    for word in sentence.words:
        # proper nouns always refer to people
        if word.upos == "PROPN" and word.text in ner_proper_nouns:
            r.append(word.head)
            p.append(word.id)
            proper_nouns.append(word.id)
        # nouns have to refer to people
        elif word.upos == "NOUN" and check_refers_to_person(word):
            r.append(word.head)
            p.append(word.id)
        # pronouns have to belong to pronouns_that_are_always_people
        elif word.upos == "PRON" and word.text.lower() in pronouns_that_are_always_people: 
            r.append(word.head)
            p.append(word.id)

        # if we can find a gender neutral version of the word
        if word.text in truly_gn_alternatives.keys():
            # gn_p contains the id for the gn term as key and the respective gender as value (neutralizer needs it)
            gn_p[word.id] = truly_gn_alternatives[word.text][1]
        elif word.text in truly_gn_terms:
            # terms that are to keep non-neutralized
            gn_keep.append(word.id)
        
    return r, p, proper_nouns, gn_p, gn_keep