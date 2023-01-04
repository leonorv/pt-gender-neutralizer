"""
Gender Neutralizer

Replaces the binary-gendered pronouns of entities in a given text by a neutral form.

"""
import argparse
import stanza
from prp_extractor import check_refers_to_person, get_roots_of_people_and_people
from neutralizer import neutralize, e_termination_neutralizer

# ARGUMENT PARSING
parser = argparse.ArgumentParser()
parser.add_argument('filename')
args = parser.parse_args()
with open(args.filename) as file:
    file_content = open(args.filename).read()

# CREATING PIPELINE
nlp = stanza.Pipeline(lang="pt", processors = 'tokenize,mwt,pos,lemma,depparse')
doc = nlp(file_content)

print("\nWelcome to Gender Neutralizer!\n")
print("Gender Neutralizer assumes that the input text is written in a binary-gendered portuguese. It will attempt to replace the pronouns of any binary-gendered entity with a desired gender neutral form.")
print("Currently, Gender Neutralizer only supports a neutral form with an -e termination. Gender neutralizer uses the gender neutral neopronoun éle.")
print("Do you wish to omit determinants that precede proper nouns? This is recommended for legibility. (y/n)")
omit_dets = input()
# INPUT CHECK
while omit_dets not in ('y', 'n'):
    print("Please input y/n")
    omit_dets = input()

omit_dets = (omit_dets == 'y')

print("Do you wish to check already existent gender-neutral alternatives to words? (y/n)")
check_alt = input()
# INPUT CHECK
while check_alt  not in ('y', 'n'):
    print("Please input y/n")
    check_alt  = input()

check_alt  = (check_alt  == 'y')




# CREATING NEW STRING
res = ""
for sentence in doc.sentences:
    roots_of_people, people, proper_nouns = get_roots_of_people_and_people(sentence)
    for word in sentence.words:
        if word.upos in ["DET","PRON", "ADJ", "NOUN", "PROPN"]:
            neutral_word = neutralize(word, people, roots_of_people, proper_nouns, omit_dets, check_alt)
            if neutral_word != "[omitted]":
                res += (neutral_word + " ")
        elif word.upos == "PUNCT":
            res = res[:-1]
            res += (word.text + " ")
        else:
            res += (word.text + " ")
  

print("\nEXTRAS: Token features as provided by stanza")
print(*[f'word: {word.text}\tupos: {word.upos}\txpos: {word.xpos}\tfeats: {word.feats if word.feats else "_"}' for sent in doc.sentences for word in sent.words], sep='\n')


print("\nEXTRA: Dependency parsing")
print(*[f'id: {word.id}\tword: {word.text}\thead id: {word.head}\thead: {sent.words[word.head-1].text if word.head > 0 else "root"}\tdeprel: {word.deprel}' for sent in doc.sentences for word in sent.words], sep='\n')


print("\nORIGINAL INPUT TEXT:")
print(file_content)
print("\nRESULT:")
print(res)



