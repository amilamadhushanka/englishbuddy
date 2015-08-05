__author__ = 'AMILA MADHUSHANKA'

import nltk

def find_tence(sentence):

    tagged_sent = nltk.pos_tag(sentence.split())
    print tagged_sent

    if [word for word, pos in tagged_sent if pos == 'NNS']:
        noun_plural = [word for word, pos in tagged_sent if pos == 'NNS']

        print 'noun_plural : ' + noun_plural[0]

        if noun_plural[0].find("'s") and noun_plural[0].find("'s") > 0:
            tence = "3rd person singular present"
            return tence

    elif [word for word, pos in tagged_sent if pos == 'VBZ']:
        tence = "3rd person singular present"
        return tence

    elif [word for word, pos in tagged_sent if pos == 'VBP']:
        tence = "singular present"
        return tence

    elif [word for word, pos in tagged_sent if pos == 'VBN']:
        tence = "past participlet"
        return tence

    elif [word for word, pos in tagged_sent if pos == 'VBG']:
        tence = "present participle"
        return tence

    elif [word for word, pos in tagged_sent if pos == 'VBD']:
        tence = "past tense"
        return tence

    elif [word for word, pos in tagged_sent if pos == 'VB']:
        tence = "base form"
        return tence

    return "null"


def check_tence(question, answer):
    question = find_tence(question)
    answer = find_tence(answer)

    if question == answer:
        return True

    return False



