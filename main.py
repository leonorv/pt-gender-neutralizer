"""
Gender Neutralizer

Replaces the binary-gendered pronouns of entities in a given text by a neutral form.
It is completely rule-based.

"""
import argparse
import stanza
from prp_extractor import get_roots_of_people_and_people
from neutralizer import neutralize
from gn_grammar import adpos, gn_auxiliary_verbs

#
# ARGUMENT PARSING
#
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input_file", required=True)
parser.add_argument("-o", "--output_file", required=True)
args = parser.parse_args()
with open(args.input_file) as file:
    file_content = open(args.input_file).read()
f = open(args.output_file, "w")

#
# STANZA MODELS
#
processor_dict = {
    "tokenize" : "bosque",
    "mwt" : "bosque",
    "pos" : "gsd",
    "lemma" : "bosque",
    "depparse" : "bosque"
}

spanish_processor_dict = {
    "tokenize" : "ancora",
    "mwt" : "ancora",
    "ner" : "CoNLL02"
}

#
# STANZA PIPELINE
#
nlp = stanza.Pipeline(lang="pt", processors = processor_dict)
doc = nlp(file_content)

#
# STANZA PIPELINE FOR NER (SPANISH)
#

nlp_ner = stanza.Pipeline(lang="es", processors = spanish_processor_dict)
doc_ner = nlp_ner(file_content)


print("\nWelcome to Gender Neutralizer!\n")
print("Gender Neutralizer assumes that the input text is written in a binary-gendered portuguese. It will attempt to replace the pronouns of any binary-gendered entity with a desired gender neutral form.")
print("Currently, Gender Neutralizer only supports a neutral form with an -e termination. Gender neutralizer uses the gender neutral neopronoun elu.")

print("Do you wish to omit determinants that precede proper nouns? This is recommended for legibility. (y/n)")
omit_dets = input()

#
# INPUT CHECK
#
while omit_dets not in ('y', 'n'):
    print("Please input y/n")
    omit_dets = input()
omit_dets = (omit_dets == 'y')

print("Do you wish to check already existent gender-neutral alternatives to words? (y/n)")
check_alt = input()

#
# INPUT CHECK
#
while check_alt  not in ('y', 'n'):
    print("Please input y/n")
    check_alt  = input()
check_alt  = (check_alt  == 'y')

#
# Extra prints
#
print("\nEXTRAS: Token features as provided by stanza")
print(*[f'word: {word.text}\tupos: {word.upos}\txpos: {word.xpos}\tfeats: {word.feats if word.feats else "_"}' for sent in doc.sentences for word in sent.words], sep='\n')


print("\nEXTRA: Dependency parsing")
print(*[f'id: {word.id}\tword: {word.text}\thead id: {word.head}\thead: {sent.words[word.head-1].text if word.head > 0 else "root"}\tdeprel: {word.deprel}' for sent in doc.sentences for word in sent.words], sep='\n')


ner_proper_nouns = []
for sentence in doc_ner.sentences:
    for token in sentence.tokens:
        if "PER" in token.ner:
            ner_proper_nouns.append(token.text)

#print(*[f'token: {token.text}\tner: {token.ner}' for sent in doc_ner.sentences for token in sent.tokens], sep='\n')


#
# CREATING NEW STRING
#
for sentence in doc.sentences:
    res = ""
    multi_tokens = {}
    verbs_with_aux = []

    #
    # 1. Get info from PaRP
    #
    roots_of_people, people, proper_nouns, gender_neutral_people, gn_keep = get_roots_of_people_and_people(sentence, ner_proper_nouns)

    for word in sentence.words:

        #
        # 2. Main verbs with auxiliary verbs that require neutralization. There are some that do not require neutralization (stored in gn_auxiliary verbs)
        #
        if word.upos == "AUX" and word.text not in gn_auxiliary_verbs:
            if word.head == word.id + 1 and sentence.words[word.head-1].upos == "VERB":
                verbs_with_aux.append(word.head)

        # 
        # 3. Dealing with multi-word tokens (eg. pela, dele, etc...)
        #
        if word.parent.text != word.text:

            # MWT first token can be ADP, AUX, or VERB
            if word.upos in ["ADP", "AUX", "VERB"]:

                # Checks if it's an hifenated mwt
                if '-' in word.parent.text:
                    res += (word.parent.text + " ")
                    continue


                # terms in apos require neutralization
                elif word.parent.text in adpos.keys():
                    multi_tokens[word.id] = word.parent.text
                # terms not in adpos are left alone - this is a bit on uncharted territory
                else:
                    res += (word.parent.text + " ")
                    continue

            # MWT second token can be PRON or DET (ou NOUN/X for accomodating stanza errors)
            elif word.upos in ["PRON", "DET", "NOUN", "X"]:

                # Checks if it's an hifenated mwt
                if '-' in word.parent.text:
                    res += ""
                    continue

                # CONVENTION: second token key is an empty string, meaning it should be ignored in the neutralizer
                if word.parent.text in adpos.keys():
                    multi_tokens[word.id] = ""
                # terms not in adpos are left alone - this is a bit on uncharted territory
                else:
                    res += ""
                    continue
        

        # 
        # 4. Send necessary terms to the Neutralizer, along with info from PaRP and stuff from the filters 2. and 3. 
        #
        if word.upos in ["DET","PRON", "ADJ", "NOUN", "PROPN", "ADP", "AUX", "NUM", "VERB"]:
            neutral_word = neutralize(word, people, roots_of_people, proper_nouns, omit_dets, check_alt, multi_tokens, gender_neutral_people, gn_keep, verbs_with_aux)
            # MWT spacing 
            if (word.upos in ["PRON", "DET", "VERB"] and word.id in multi_tokens.keys()):
                res += neutral_word
            # Not MWT cases
            elif neutral_word != "[omitted]":
                res += (neutral_word + " ")
        elif word.upos == "PUNCT":
            res = res[:-1]
            res += (word.text + " ")
        else:
            res += (word.text + " ")
        #print(res)

    # adding a new line for each sentence
    print(sentence.text, "->", res)
    f.write(res)
    f.write('\n')
    #res += "\n"

        

#print("\nORIGINAL INPUT TEXT:")
#print(file_content)
#print("\nRESULT:")
#print(res)
#f.write(res)
#
f.close()



