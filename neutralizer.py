"""
Neutralizer

"""
from gn_grammar import pron_and_dets

# for nouns and adjectives
def e_termination_neutralizer(word):
    if word.text.endswith('o') or word.text.endswith('a'):
        return word.text[:-1] + 'e'
    if word.text.endswith('os') or word.text.endswith('as'):
        return word.text[:-2] + 'es'

    return word.text


def neutralize(word, people, roots_of_people, omit_dets):
    res = ""
    if word.upos == "DET":
        if word.head in people:
            if word.text.lower() in pron_and_dets: 
                res = pron_and_dets.get(word.text.lower())
                if omit_dets and word.text.lower() in ["o", "os", "a", "as"]:
                    res = "[omitted]"
            else:
                res = e_termination_neutralizer(word)

        else:
            res = word.text

    elif word.upos == "PRON":
        if word.head in roots_of_people:
            if word.text.lower() in pron_and_dets: 
                res = pron_and_dets.get(word.text.lower())
            else:
                res = e_termination_neutralizer(word)
        else:
            res = word.text


    # specific case for proper nouns
    elif word.upos == "PROPN":
        #roots_of_people.append(word.head)
        res = word.text


    # wordnet checks if the noun refers to a person
    elif word.upos == "NOUN":
        if word.id in people:
            res = e_termination_neutralizer(word)
        else:
            res = word.text

    elif word.upos == "ADJ":
        if word in roots_of_people:
            res = e_termination_neutralizer(word)
        else: 
            res = word.text

    else:
        res = "[Unknown]"

    if word.text[0].isupper():
        return res[:1].upper() + res[1:]
    else:
        return res