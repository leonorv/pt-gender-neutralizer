"""
Gender Neutralizer

Replaces the binary-gendered pronouns of entities in a given text by a neutral form.

"""
import argparse
import stanza
import re 
import wn, wn.taxonomy

def check_refers_to_person(word):
    pessoa = wn.synsets('pessoa', pos='n')[0]
    for w in wn.synsets(word.text):  # checking all synsets (we need to do this, the first one might not refer to a person but the next ones might)
        try:
            wn.taxonomy.shortest_path(w, pessoa)  # checking for the existence of a path between the word and the concept of person
            return True
        except:
            return False
    return False


def get_roots_of_people_and_people(sentence):
    r = []
    p = []
    for word in sentence.words:
        # proper nouns always refer to people
        if word.upos == "PROPN":
            r.append(word.head)
            p.append(word.id)
        elif word.upos == "NOUN" and check_refers_to_person(word):
            r.append(word.head)
            p.append(word.id)
        # assume the personal pronouns always refer to people
        elif word.upos == "PRON" and re.search("PronType=Prs", word.feats):
            r.append(word.head)
            p.append(word.id)
    return r, p

# for nouns and adjectives (?)
def e_termination_neutralizer(word):
    if word.text.endswith('o') or word.text.endswith('a'):
        return word.text[:-1] + 'e'
    if word.text.endswith('os') or word.text.endswith('as'):
        return word.text[:-2] + 'es'
    return word.text


def neutralize(word):
    if word.upos == "DET":
        #TODO determinants need coreference resolution
        if word.head in roots_of_people or word.head in people:
            if re.search("Definite=Def", word.feats):
                #TODO omit determinant that preceds noun
                if omit_dets:
                    return "[omitted]"
                else:
                    return "ê"
            elif re.search("Definite=Ind", word.feats):
                return "ume"
            elif word.text == "seu" or word.text == "sua":
                return "sue"
            elif word.text == "seus" or word.text == "suas":
                return "sues"
            elif word.text == "meu" or word.text == "minha":
                return "minhe"
            elif word.text == "meus" or word.text == "meus":
                return "minhes"
        else:
            return word.text

    elif word.upos == "PRON":
        if word.head in roots_of_people:
            #TODO incomplete rules
            if word.text == "ele" or word.text == "ela":
                return "éle"
            elif word.text == "eles" or word.text == "elas":
                return "éles"
            elif word.text == "meu" or word.text == "minha":
                return "minhe"
            elif word.text == "meus" or word.text == "minhas":
                return "minhes"
            elif word.text == "seu" or word.text == "sua":
                return "sue"
            elif word.text == "seus" or word.text == "suas":
                return "sues"
            else:
                return word.text
        else:
            return word.text


    # specific case for proper nouns
    elif word.upos == "PROPN":
        #roots_of_people.append(word.head)
        return word.text


    # wordnet checks if the noun refers to a person
    elif word.upos == "NOUN":
        if check_refers_to_person(word):
            return e_termination_neutralizer(word)
        return word.text

    elif word.upos == "ADJ":
        if word.head in roots_of_people:
            return e_termination_neutralizer(word)
        return word.text

    return "[Unknown]"


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
print("Currently, Gender Neutralizer only supports a neutral form with an -e termination.")
print("Do you wish to omit determinants that precede proper nouns? This is recommended for legibility. (y/n)")
omit_dets = input()

# INPUT CHECK
while omit_dets not in ('y', 'n'):
    print("Please input y/n")
    omit_dets = input()

omit_dets = (omit_dets == 'y')



# CREATING NEW STRING
res = ""
for sentence in doc.sentences:
    roots_of_people, people = get_roots_of_people_and_people(sentence)
    for word in sentence.words:
        if word.upos == "DET" or word.upos == "PRON" or word.upos == "ADJ" or word.upos == "NOUN" or word.upos == "PROPN":
            neutral_word = neutralize(word)
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



