__author__ = 'AMILA MADHUSHANKA'

import nltk

def find_tense(sentence):

    tense = 'null'
    array = []

    tagged_sent = nltk.pos_tag(sentence.split())
    print tagged_sent

    if [word for word, pos in tagged_sent if pos == 'NNS']:

        array = ([word for word, pos in tagged_sent if pos == 'NNS'])

        for word in array:
            if word.find("'s") and word.find("'s") > 0:
                tense = "3rd person singular present"
                return tense


    if [word for word, pos in tagged_sent if pos == 'NNP']:

        array = ([word for word, pos in tagged_sent if pos == 'NNP'])

        for word in array:
            if (word.find("'s") and word.find("'s") > 0) or word.find("'ll") and word.find("'ll") > 0:
                tense = "3rd person singular present"
                return tense

    if [word for word, pos in tagged_sent if pos == 'VBZ']:
        tense = "3rd person singular present"

    elif [word for word, pos in tagged_sent if pos == 'VBP'] or [word for word, pos in tagged_sent if pos == 'MD']:
        tense = "singular present"

    elif [word for word, pos in tagged_sent if pos == 'VBN']:
        tense = "past participlet"

    elif [word for word, pos in tagged_sent if pos == 'VBG']:
        tense = "present participle"

    elif [word for word, pos in tagged_sent if pos == 'VBD']:
        tense = "past tense"

    elif [word for word, pos in tagged_sent if pos == 'VB']:
        tense = "base form"

    return tense


def check_tense(question, answer):
    question = find_tense(question)
    answer = find_tense(answer)

    if question == answer:
        return True

    return False


# print check_tense("Have you money to buy this?", "She have two thousand rupees. I hope that, it'll be enough.")
