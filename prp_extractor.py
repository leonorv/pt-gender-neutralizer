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

import wn, wn.taxonomy
from gn_grammar import gn_nouns_non_people, truly_gn_alternatives, truly_gn_terms, pronouns_that_are_always_people

def check_refers_to_person(word):
    # Checks if noun is not a person (but wordnet tags as such)
    if word.text in gn_nouns_non_people: 
        return False
    # Checks if noun is already gender-neutral
    elif word.text in truly_gn_alternatives.keys():
        return True

    pessoa = wn.synsets('pessoa', pos='n')[0]

    # Case where word does not exist in the wordnet - we neutralize it, fuck it
    if len(wn.synsets(word.lemma)) == 0:
        return True

    # We check with the lemmatized form because wn is not complete with gender and number
    for i, w in enumerate(wn.synsets(word.lemma)):  # checking all synsets (we need to do this, the first one might not refer to a person but the next ones might)
        # If the synset is not in the first 2 positions we give up (otherwise we would get a lot of false positives)
        if i >= 2:
            return False
        try:
            wn.taxonomy.shortest_path(w, pessoa)  # Checking for the existence of a path between the word and the concept of person
            #print(word, "É pessoa\n")

            # We are capping the maximum size of the path to 6.
            if len( wn.taxonomy.shortest_path(w, pessoa)) > 6:
                return False
            return True
        
        except:
            #print(word, "NÃO É pessoa\n")
            continue
    return False


def get_roots_of_people_and_people(sentence):
    r = []
    p = []
    gn_p = {}
    gn_keep = []
    proper_nouns = []
    for word in sentence.words:
        # proper nouns always refer to people
        if word.upos == "PROPN":
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