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
from gn_grammar import pron_and_dets, adpos, m_to_f_adpos, m_to_f_pron_and_dets, f_to_m_adpos, f_to_m_pron_and_dets, gn_nouns_non_people, gn_adjectives, semi_gn_nouns
from termination_switchers import e_termination_neutralizer, a_to_o_termination_switcher, o_to_a_termination_switcher

# Estes casos referem-se a pessoas:
# 'ele lembra-mo' é equivalente a 'ele lembra-me ele'
# 'vou vê-la' é equivalente a 'vou ver ela'
def neutralize_hyphenated(word_parent_text):
    if word_parent_text.endswith(('mo', 'ma')):
        return word_parent_text[:-1] + 'e'
    elif word_parent_text.endswith(('mos', 'mas')):
        return word_parent_text[:-2] + 'es'
    elif word_parent_text.endswith(('lo', 'la')):
        return word_parent_text[:-1] + 'e'
    elif word_parent_text.endswith(('los', 'las')):
        return word_parent_text[:-2] + 'es'
    elif word_parent_text.endswith(('lho', 'lha')):
        return word_parent_text[:-1] + 'e'
    elif word_parent_text.endswith(('lhos', 'lhas')):
        return word_parent_text[:-2] + 'es'
    elif word_parent_text.endswith(('o', 'a')):
        return word_parent_text[:-1] + 'e'
    else:
        return word_parent_text

def neutralize(word, people, roots_of_people, proper_nouns, omit_dets, check_alt, multi_tokens, gender_neutral_people, gn_keep, verbs_with_aux):
    res = ""

    # deal with multi-word tokens: we check the grammar for ADP and ignore PRON
    if word.upos == "ADP":

        # we are keeping the gender of the alternative gender neutral term
        if word.head in gn_keep:
            res = word.parent.text

        # changing to a gender-neutral term
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

            # can be a case where the ADP is non-gendered, such as 'com' (ex: Ele dormiu com a mulher.)
            else:
                res = word.text

        # usual neutralization
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

            # uma mulher -> uma pessoa
            if gender_neutral_people[word.head] == "F" and word.text.lower() in f_to_m_pron_and_dets: 
                # nothing changes
                res = word.text
                if omit_dets and word.head in proper_nouns and word.text.lower() in ["o", "os", "a", "as"]:
                    res = "[omitted]"
            # uma mulher -> um indivíduo
            elif gender_neutral_people[word.head] == "M" and word.text.lower() in f_to_m_pron_and_dets: 
                res = f_to_m_pron_and_dets.get(word.text.lower())
                if omit_dets and word.head in proper_nouns and word.text.lower() in ["o", "os", "a", "as"]:
                    res = "[omitted]"

            # um homem -> uma pessoa
            elif gender_neutral_people[word.head] == "F" and word.text.lower() in m_to_f_pron_and_dets: 
                res = m_to_f_pron_and_dets.get(word.text.lower())
                if omit_dets and word.head in proper_nouns and word.text.lower() in ["o", "os", "a", "as"]:
                    res = "[omitted]"

            # um homem -> um indivíduo
            elif gender_neutral_people[word.head] == "M" and word.text.lower() in m_to_f_pron_and_dets: 
                # nothing changes
                res = word.text
                if omit_dets and word.head in proper_nouns and word.text.lower() in ["o", "os", "a", "as"]:
                    res = "[omitted]"
            else:
                #res = "[Unknown]"
                res = word.text

        # usual neutralization
        elif word.head in people and word.head not in gn_nouns_non_people:
            if word.text.lower() in pron_and_dets: 
                res = pron_and_dets.get(word.text.lower())
                if omit_dets and word.head in proper_nouns and word.text.lower() in ["o", "os", "a", "as"]:
                    res = "[omitted]"
            # an attempt at neutralizing determinants that may have escaped the grammar
            else:
                res = e_termination_neutralizer(word, check_alt)

        # neutralization not needed
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

        # neutralization not needed
        else:
            res = word.text


    # specific case for proper nouns
    elif word.upos == "PROPN":
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
    elif word.upos in ["ADJ", "NUM"]:

        # gender neutral adjectives are nor changed
        if word.text in gn_adjectives:
            res = word.text

        # adjectives of gender neutral alternative nouns should agree with the respective gender
        elif word.head in gender_neutral_people:
            if gender_neutral_people[word.head] == "F":
                res = o_to_a_termination_switcher(word)
            elif gender_neutral_people[word.head] == "M":
                res = a_to_o_termination_switcher(word)
            else:
                #res = "[Unknown]"
                res = word.text

        # no changes: pessoa boa -> pessoa boa
        elif word.head in gn_keep:
            res = word.text

        # usual neutralization
        elif word.id in roots_of_people or word.head in people or word.id in people or word.head in roots_of_people:
            res = e_termination_neutralizer(word, check_alt)

        # not to neutralize
        else: 
            res = word.text

    elif word.upos == "VERB":
        # verbs are not usually gendered, with the exception of some main verbs that require an aux verb
        if word.id not in verbs_with_aux:
            res = word.text
        else:
            # gerúndio
            if word.text.endswith(('ando', 'endo', 'indo')):
                res = word.text

            # particípio
            # malcriado -> malcriade
            elif word.text.endswith(('ido', 'ado')):
                res = word.text[:-1] + 'e'
            # malcriada -> malcriade
            elif word.text.endswith(('ida', 'ada')):
                res = word.text[:-1] + 'e'

            # most cases end up here i guess 
            else:
                res = word.text

    else:
        #res = "[Unknown]"
        res = word.text


    # Capitalization
    if word.text[0].isupper():
        return res[:1].upper() + res[1:]
    else:
        return res