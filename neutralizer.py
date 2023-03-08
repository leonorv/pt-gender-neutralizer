"""
Neutralizer

Rewrites a binary-gendered term as gender neutral. It can check already existing alternative terms in the grammar or rewrite using gender-neutral language.

Requires the gn_grammar module as the gender neutral grammar rules to follow.

This file can be imported as a module and contains the following
functions:
    - Auxiliary functions:
    * e_termination_neutralizer - applies rules for rewriting gendered terms (-o and -a) to neutral (-e or -u)
    * o_to_a_termination_switcher - switches a terms's termination from masculine (-o) to feminine (-a)
    * a_to_o_termination_switcher - switches a terms's termination from feminine (-a) to masculine (-o)

    - Main function:
    * neutralize - applies the previous functions, as well as the gender neutral grammars, as necessary in order to rewrite terms as gender neutral; requires information from PaRP

"""
from gn_grammar import pron_and_dets, semi_gn_alternatives, truly_gn_alternatives, adpos, m_to_f_adpos, m_to_f_pron_and_dets, f_to_m_adpos, f_to_m_pron_and_dets, gn_nouns_non_people, gn_adjectives, semi_gn_nouns

# for nouns and adjectives
def e_termination_neutralizer(word, check_alt):
    # check if word already has a gender neutral alternative
    if check_alt:
        if word.text in semi_gn_alternatives.keys():
            return semi_gn_alternatives[word.text]
        elif word.text in truly_gn_alternatives.keys():
            return truly_gn_alternatives[word.text][0]
    # -co/-ca/-que
    if word.text.endswith('co') or word.text.endswith('ca'):
        return word.text[:-2] + 'que'
    elif word.text.endswith('cos') or word.text.endswith('cas'):
        return word.text[:-2] + 'ques'
    # -ço/-ça/-ce
    elif word.text.endswith('ço') or word.text.endswith('ça'):
        return word.text[:-2] + 'ce'
    elif word.text.endswith('ços') or word.text.endswith('ças'):
        return word.text[:-2] + 'ces'
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
        return word.text[:-1] + 'es'
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

def o_to_a_termination_switcher(word):
    # -co/-ca/-que
    if word.text.endswith('co'):
        return word.text[:-1] + 'a'
    elif word.text.endswith('cos'):
        return word.text[:-2] + 'as'
    # -ço/-ça/-ce
    elif word.text.endswith('ço'):
        return word.text[:-1] + 'a'
    elif word.text.endswith('ços'):
        return word.text[:-2] + 'as'
    # -go/-ga/-gue
    elif word.text.endswith('go'):
        return word.text[:-1] + 'a'
    elif word.text.endswith('gos'):
        return word.text[:-2] + 'as'
    # -nho/-nha/-nhe
    elif word.text.endswith('nho'):
        return word.text[:-1] + 'a'
    elif word.text.endswith('nhos'):
        return word.text[:-2] + 'as'
    # -ão/-ã/-ae
    elif word.text.endswith('ão'):
        return word.text[:-1]
    elif word.text.endswith('ãos'):
        return word.text[:-2] + 's'
    # -tor/-triz/-tore
    elif word.text.endswith('tor'):
        return word.text[:-2] + 'riz'
    elif word.text.endswith('tores'):
        return word.text[:-4] + 'rizes'
    # -r/-ra/-re
    elif word.text.endswith('r'):
        return word.text + 'a'
    elif word.text.endswith('ros'):
        return word.text[:-2] + 'as'
    # -l/-la/-le
    elif word.text.endswith('l'):
        return word.text + 'a'
    elif word.text.endswith('les'):
        return word.text[:-2] + 'as'
    # -z/-za/-ze
    elif word.text.endswith('z'):
        return word.text + 'a'
    elif word.text.endswith('zas'):
        return word.text[:-2] + 'as'
    # -u/-ua/-ue 
    elif word.text.endswith('u'):
        return word.text + 'a'
    elif word.text.endswith('us'):
        return word.text[:-1] + 'as'
    # -e/-e
    elif word.text.endswith('e'):
        return word.text
    elif word.text.endswith('es'):
        return word.text
    # -ês/-esa/-ese
    elif word.text.endswith('ês'):
        return word.text[:-2] + 'esa'
    elif word.text.endswith('eses'):
        return word.text[:-2] + 'as'
    # -ois/-uas/-ues
    elif word.text.endswith('ois'):
        return word.text[:-3] + 'uas'
    # -om
    elif word.text.endswith('om'):
        return word.text[:-1] + 'a'
    elif word.text.endswith('ons'):
        return word.text[:-2] + 'as'
    # generic
    elif word.text.endswith('o'):
        return word.text[:-1] + 'a'
    elif word.text.endswith('os'):
        return word.text[:-2] + 'as'

    return word.text

def a_to_o_termination_switcher(word):
    # -co/-ca/-que
    if word.text.endswith('ca'):
        return word.text[:-1] + 'o'
    elif word.text.endswith('cas'):
        return word.text[:-2] + 'os'
    # -ço/-ça/-ce
    elif word.text.endswith('ça'):
        return word.text[:-1] + 'o'
    elif word.text.endswith('ças'):
        return word.text[:-2] + 'os'
    # -go/-ga/-gue
    elif word.text.endswith('ga'):
        return word.text[:-1] + 'o'
    elif word.text.endswith('gas'):
        return word.text[:-2] + 'os'
    # -nho/-nha/-nhe
    elif word.text.endswith('nha'):
        return word.text[:-1] + 'o'
    elif word.text.endswith('nhas'):
        return word.text[:-2] + 'os'
    # -ão/-ã/-ae
    elif word.text.endswith('ã'):
        return word.text + 'o'
    elif word.text.endswith('ãs'):
        return word.text[:-1] + 'os'
    # -tor/-triz/-tore
    elif word.text.endswith('triz'):
        return word.text[:-3] + 'or'
    elif word.text.endswith('trizes'):
        return word.text[:-5] + 'ores'
    # -r/-ra/-re
    elif word.text.endswith('ra'):
        return word.text[:-1]
    elif word.text.endswith('ras'):
        return word.text[:-2] + 'os'
    # -l/-la/-le
    elif word.text.endswith('la'):
        return word.text[:-1]
    elif word.text.endswith('las'):
        return word.text[:-2] + 's'
    # -z/-za/-ze
    elif word.text.endswith('za'):
        return word.text[:-1]
    elif word.text.endswith('zas'):
        return word.text[:-2] + 'es'
    # -u/-ua/-ue 
    elif word.text.endswith('ua'):
        return word.text[:-1]
    elif word.text.endswith('uas'):
        return word.text[:-2] + 's'
    # -e/-e
    elif word.text.endswith('e'):
        return word.text
    elif word.text.endswith('es'):
        return word.text
    # -ês/-esa/-ese
    elif word.text.endswith('esa'):
        return word.text[:-3] + 'ês'
    elif word.text.endswith('esas'):
        return word.text[:-2] + 'es'
    # -ois/-uas/-ues
    elif word.text.endswith('uas'):
        return word.text[:-3] + 'ois'
    # -om
    #elif word.text.endswith('a'):
    #    return word.text[:-1] + 'om'
    #elif word.text.endswith('as'):
    #    return word.text[:-2] + 'ons'
    # generic
    elif word.text.endswith('a'):
        return word.text[:-1] + 'o'
    elif word.text.endswith('as'):
        return word.text[:-2] + 'os'

    return word.text


def neutralize(word, people, roots_of_people, proper_nouns, omit_dets, check_alt, multi_tokens, gender_neutral_people, gn_keep, passive_verbs):
    res = ""

    # deal with multi-word tokens: we check the grammar for ADP and ignore PRON
    if word.upos == "ADP":

        if word.head in gn_keep:
            res = word.parent.text

        elif word.head in gender_neutral_people:
            # na mulher -> na pessoa
            if gender_neutral_people[word.head] == "F" and word.parent.text.lower() in f_to_m_adpos: 
                # nothing changes
                res = word.parent.text
            # na mulher -> no [palavra neutra masculina]
            elif gender_neutral_people[word.head] == "M" and word.parent.text.lower() in f_to_m_adpos: 
                res = f_to_m_adpos.get(word.parent.text.lower())

            # no homem -> na pessoa
            elif gender_neutral_people[word.head] == "F" and word.parent.text.lower() in m_to_f_adpos: 
                res = m_to_f_adpos.get(word.parent.text.lower())

            # no homem -> no [palavra neutra masculina]
            elif gender_neutral_people[word.head] == "M" and word.parent.text.lower() in m_to_f_adpos: 
                # nothing changes
                res = word.parent.text
            else:
                res = "[Unknown]"


        elif (word.head in people or word.id in people) and word.id in multi_tokens.keys() and multi_tokens[word.id] in adpos.keys():
            res = adpos[multi_tokens[word.id]]
        else:
            res = word.parent.text

    # deal with multi-word tokens: we check the grammar for ADP and ignore PRON
    elif word.upos == "AUX":
        if word.head in gn_keep:
            res = word.parent.text
        elif (word.head in people or word.id in people) and word.id in multi_tokens.keys() and multi_tokens[word.id] in adpos.keys():
            res = adpos[multi_tokens[word.id]]
        else:
            res = word.parent.text

    elif word.upos == "DET":
        # deal with mwt: ignore pron
        if word.id in multi_tokens.keys() and multi_tokens[word.id] == "":
            res = ""

        # no changes: uma pessoa -> uma pessoa
        elif word.head in gn_keep:
            res = word.text

        # deal with the gender_neutral_people drama
        elif word.head in gender_neutral_people.keys():
            #res = word.text

            # uma mulher -> uma pessoa
            if gender_neutral_people[word.head] == "F" and word.text.lower() in f_to_m_pron_and_dets: 
                # nothing changes
                res = word.text
                if omit_dets and word.head in proper_nouns and word.text.lower() in ["o", "os", "a", "as"]:
                    res = "[omitted]"
            # uma mulher -> um [palavra neutra masculina]
            elif gender_neutral_people[word.head] == "M" and word.text.lower() in f_to_m_pron_and_dets: 
                res = f_to_m_pron_and_dets.get(word.text.lower())
                if omit_dets and word.head in proper_nouns and word.text.lower() in ["o", "os", "a", "as"]:
                    res = "[omitted]"

            # um homem -> uma pessoa
            elif gender_neutral_people[word.head] == "F" and word.text.lower() in m_to_f_pron_and_dets: 
                res = m_to_f_pron_and_dets.get(word.text.lower())
                if omit_dets and word.head in proper_nouns and word.text.lower() in ["o", "os", "a", "as"]:
                    res = "[omitted]"

            # um homem -> um [palavra neutra masculina]
            elif gender_neutral_people[word.head] == "M" and word.text.lower() in m_to_f_pron_and_dets: 
                # nothing changes
                res = word.text
                if omit_dets and word.head in proper_nouns and word.text.lower() in ["o", "os", "a", "as"]:
                    res = "[omitted]"
            else:
                res = "[Unknown]"


        elif word.head in people and word.head not in gn_nouns_non_people:
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

        # if head of the pronoun is not a person then we do not change it
        elif word.id in people or word.head in people:
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
        if word.id in gn_keep:
            res = word.text
        elif word.text in semi_gn_nouns:
            res = word.text
        elif word.id in people:
            res = e_termination_neutralizer(word, check_alt)
        else:
            res = word.text

    # we do not wish to neutralize gender neutral adjectives
    elif word.upos in ["ADJ", "NUM"] and word.text not in gn_adjectives:
        if word.head in gender_neutral_people:
            #res = word.text
            if gender_neutral_people[word.head] == "F":
                res = o_to_a_termination_switcher(word)
            elif gender_neutral_people[word.head] == "M":
                res = a_to_o_termination_switcher(word)
            else:
                Exception("Grammatical gender for the word " + word.text + " not found.")

        # no changes: pessoa boa -> pessoa boa
        elif word.head in gn_keep:
            res = word.text

        elif word.id in roots_of_people or word.head in people or word.id in people or word.head in roots_of_people:
            res = e_termination_neutralizer(word, check_alt)
        else: 
            res = word.text

    elif word.upos == "VERB":
        if word.id not in passive_verbs:
            res = word.text
        else:
            # gerundio
            if word.text.endswith(('ando', 'endo', 'indo')):
                res = word.text

            # particípio
            # malcriado -> malcriade
            elif word.text.endswith(('ido', 'ado')):
                res = word.text[:-1] + 'e'
            # malcriada -> malcriade
            elif word.text.endswith(('ida', 'ada')):
                res = word.text[:-1] + 'e'

            else:
                res = word.text


    elif word.text in gn_adjectives:
        res = word.text

    else:
        res = "[Unknown]"

    if word.text[0].isupper():
        return res[:1].upper() + res[1:]
    else:
        return res