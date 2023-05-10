from gn_grammar import semi_gn_alternatives, truly_gn_alternatives

# for nouns and adjectives
def e_termination_neutralizer(word, check_alt):
    # check if word already has a gender neutral alternative
    if check_alt:
        if word.text in semi_gn_alternatives.keys():
            return semi_gn_alternatives[word.text]
        elif word.text in truly_gn_alternatives.keys():
            return truly_gn_alternatives[word.text][0]
    # -co/-ca/-que
    if word.text.endswith(('co', 'ca')):
        return word.text[:-2] + 'que'
    elif word.text.endswith(('cos', 'cas')):
        return word.text[:-3] + 'ques'
    # -ço/-ça/-ce
    elif word.text.endswith(('ço', 'ça')):
        return word.text[:-2] + 'ce'
    elif word.text.endswith(('ços', 'ças')):
        return word.text[:-3] + 'ces'
    # -go/-ga/-gue
    elif word.text.endswith(('go', 'ga')):
        return word.text[:-1] + 'ue'
    elif word.text.endswith(('gos', 'gas')):
        return word.text[:-2] + 'ues'
    # -nho/-nha/-nhe
    elif word.text.endswith(('nho', 'nha')):
        return word.text[:-1] + 'e'
    elif word.text.endswith(('nhos', 'nhas')):
        return word.text[:-2] + 'es'
    # -ão/-ã/-ae
    elif word.text.endswith('ão'):
        return word.text[:-1] + 'e'
    elif word.text.endswith('ã'):
        return word.text + 'e'
    elif word.text.endswith('ãos'):
        return word.text[:-2] + 'es'
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
    elif word.text.endswith(('o', 'a')):
        return word.text[:-1] + 'e'
    elif word.text.endswith(('os', 'as')):
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