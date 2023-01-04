"""
People and Roots of People Extractor

Allows for checking if a word processed by Stanza refers to a person.

Requires that `OpenWordnet-PT` be installed within the Python
environment you are running this script in.

This file can be imported as a module and contains the following
functions:

    * check_refers_to_person - returns the bool value refering to whether the word passed as argument refers to a person or not
    * get_roots_of_people_and_people - returns two lists: one with the words in a Stanza parsed sentence that refer to people; other with their respective heads in the sentence

"""


import re 
import wn, wn.taxonomy

def check_refers_to_person(word):
    pessoa = wn.synsets('pessoa', pos='n')[0]
    # we check with the lemmatized form because wn is not complete with gender and number
    for w in wn.synsets(word.lemma):  # checking all synsets (we need to do this, the first one might not refer to a person but the next ones might)
        try:
            wn.taxonomy.shortest_path(w, pessoa)  # checking for the existence of a path between the word and the concept of person
            #print(word, "É pessoa\n")
            return True
        except:
            #print(word, "NÃO É pessoa\n")
            continue
    return False


def get_roots_of_people_and_people(sentence):
    r = []
    p = []
    proper_nouns = []
    for word in sentence.words:
        # proper nouns always refer to people
        if word.upos == "PROPN":
            r.append(word.head)
            p.append(word.id)
            proper_nouns.append(word.id)
        elif word.upos == "NOUN" and check_refers_to_person(word):
            r.append(word.head)
            p.append(word.id)
        # assume the personal pronouns always refer to people
        elif word.upos == "PRON" and re.search("PronType=Prs", word.feats):
            r.append(word.head)
            p.append(word.id)
    return r, p, proper_nouns