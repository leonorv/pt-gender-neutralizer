"""
Neutralizer

"""
from gn_grammar import pron_and_dets, gn_alternatives, adpos

# for nouns and adjectives
def e_termination_neutralizer(word, check_alt):
    # check if word already has a gender neutral alternative
    if check_alt and word.text in gn_alternatives.keys():
        return gn_alternatives[word.text]
    # -co/-ca/-que
    elif word.text.endswith('co') or word.text.endswith('ca'):
        return word.text[:-2] + 'que'
    elif word.text.endswith('cos') or word.text.endswith('cas'):
        return word.text[:-2] + 'ques'
    # -go/-ga/-gue
    elif word.text.endswith('go') or word.text.endswith('ga'):
        return word.text[:-1] + 'ue'
    elif word.text.endswith('gos') or word.text.endswith('gas'):
        return word.text[:-2] + 'ues'
    # -nho/-nha/-nhe
    elif word.text.endswith('nho') or word.text.endswith('nha'):
        return word.text[:-1] + 'e'
    elif word.text.endswith('nhos') or word.text.endswith('nhas'):
        return word.text[:-2] + 'es'
    # -ão/-ã/-ae
    elif word.text.endswith('ão'):
        return word.text[:-1] + 'e'
    elif word.text.endswith('ã'):
        return word.text + 'e'
    elif word.text.endswith('ãos'):
        return word.text[:-1] + 'es'
    elif word.text.endswith('ãs'):
        return word.text + 'es'
    # -ona/-one
    elif word.text.endswith('ona'):
        return word.text[:-1] + 'e'
    elif word.text.endswith('onas'):
        return word.text[:-1] + 'es'
    # -oa/-oe
    elif word.text.endswith('oa'):
        return word.text[:-1] + 'e'
    elif word.text.endswith('oas'):
        return word.text[:-2] + 'es'
    # -tor/-triz/-tore
    elif word.text.endswith('tor'):
        return word.text + 'e'
    elif word.text.endswith('triz'):
        return word.text[:-3] + 'ore'
    elif word.text.endswith('tores'):
        return word.text
    elif word.text.endswith('trizes'):
        return word.text[:-5] + 'ores'
    # -r/-ra/-re
    elif word.text.endswith('r'):
        return word.text + 'e'
    elif word.text.endswith('ra'):
        return word.text[:-1] + 'e'
    elif word.text.endswith('res'):
        return word.text
    elif word.text.endswith('ras'):
        return word.text[:-2] + 'es'
    # -l/-la/-le
    elif word.text.endswith('l'):
        return word.text + 'e'
    elif word.text.endswith('la'):
        return word.text[:-1] + 'e'
    elif word.text.endswith('les'):
        return word.text
    elif word.text.endswith('las'):
        return word.text[:-2] + 'es'
    # -z/-za/-ze
    elif word.text.endswith('z'):
        return word.text + 'e'
    elif word.text.endswith('za'):
        return word.text[:-1] + 'e'
    elif word.text.endswith('zes'):
        return word.text
    elif word.text.endswith('zas'):
        return word.text[:-2] + 'es'
    # -u/-ua/-ue 
    elif word.text.endswith('u'):
        return word.text + 'e'
    elif word.text.endswith('ua'):
        return word.text[:-1] + 'e'
    elif word.text.endswith('us'):
        return word.text[:-1] + 'es'
    elif word.text.endswith('uas'):
        return word.text[:-2] + 'es'
    # -e/-e
    elif word.text.endswith('e'):
        return word.text
    elif word.text.endswith('es'):
        return word.text
    # -ês/-esa/-ese
    elif word.text.endswith('ês'):
        return word.text[:-2] + 'ese'
    elif word.text.endswith('esa'):
        return word.text[:-1] + 'e'
    elif word.text.endswith('eses'):
        return word.text
    elif word.text.endswith('esas'):
        return word.text[:-2] + 'es'
    # -ois/-uas/-ues
    elif word.text.endswith('ois'):
        return word.text[:-3] + 'ues'
    elif word.text.endswith('uas'):
        return word.text[:-2] + 'es'
    # -om
    elif word.text.endswith('om'):
        return word.text[:-1] + 'e'
    elif word.text.endswith('ons'):
        return word.text[:-2] + 'es'
    # generic
    elif word.text.endswith('o') or word.text.endswith('a'):
        return word.text[:-1] + 'e'
    elif word.text.endswith('os') or word.text.endswith('as'):
        return word.text[:-2] + 'es'

    return word.text


def neutralize(word, people, roots_of_people, proper_nouns, omit_dets, check_alt, multi_tokens):
    res = ""

    # deal with multi-word tokens: we check the grammar for ADP and ignore PRON
    if word.upos == "ADP":
        if word.id in multi_tokens.keys() and multi_tokens[word.id] in adpos.keys():
            res = adpos[multi_tokens[word.id]]
        else:
            res = word.text

    elif word.upos == "DET":
        if word.head in people:
            if word.text.lower() in pron_and_dets: 
                res = pron_and_dets.get(word.text.lower())
                if omit_dets and word.head in proper_nouns and word.text.lower() in ["o", "os", "a", "as"]:
                    res = "[omitted]"
            else:
                res = e_termination_neutralizer(word, check_alt)

        else:
            res = word.text

    elif word.upos == "PRON":

        # deal with mwt: ignore pron
        if word.id in multi_tokens.keys() and multi_tokens[word.id] == "":
            res = ""

        elif word.id in people:
            if word.text.lower() in pron_and_dets: 
                res = pron_and_dets.get(word.text.lower())
            else:
                # attempt to neutralize pronouns that are not in the grammar
                res = e_termination_neutralizer(word, check_alt)
        else:
            res = word.text


    # specific case for proper nouns
    elif word.upos == "PROPN":
        #roots_of_people.append(word.head)
        res = word.text


    # wordnet checks if the noun refers to a person
    elif word.upos == "NOUN":
        if word.id in people:
            res = e_termination_neutralizer(word, check_alt)
        else:
            res = word.text

    elif word.upos == "ADJ":
        if word.id in roots_of_people or word.head in roots_of_people or word.head in people or word.id in people:
            res = e_termination_neutralizer(word, check_alt)
        else: 
            res = word.text

    else:
        res = "[Unknown]"

    if word.text[0].isupper():
        return res[:1].upper() + res[1:]
    else:
        return res