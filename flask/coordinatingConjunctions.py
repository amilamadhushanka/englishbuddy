__author__ = 'AMILA MADHUSHANKA'

import nltk
import ginger_python2_new as Grammar

# Valid conjunctions list
valid_conjunctions = ['and', 'or', 'but', 'for', 'yet', 'nor', 'So', 'so']


# Check the conjunction is correct
def check(sentence, answer):
    tagged_sent = nltk.pos_tag(sentence.split())
    print tagged_sent

    if [word for word, pos in tagged_sent if pos == 'CC' and word == answer]:
        conjunction = [word for word, pos in tagged_sent if pos == 'CC' and word == answer]
        conjunctions = conjunction[0], 'CC'

        print 'Conjunction : ' + conjunction[0]

        if conjunction[0] == 'or':
            if "neither" in sentence:
                if sentence.find("nor") < 0:
                    # print 'wrong'
                    return False
            elif (tagged_sent[tagged_sent.index(conjunctions) - 1][1] == 'VBD' or
                    tagged_sent[tagged_sent.index(conjunctions) - 1][1] == 'NNP' or
                    tagged_sent[tagged_sent.index(conjunctions) - 1][1] == 'NN' or
                    tagged_sent[tagged_sent.index(conjunctions) - 1][1] == 'NNS') and (
                    tagged_sent[tagged_sent.index(conjunctions) + 1][1] == 'VB' or
                    tagged_sent[tagged_sent.index(conjunctions) + 1][1] == 'JJ' or
                    tagged_sent[tagged_sent.index(conjunctions) + 1][1] == 'NNP'):

                if Grammar.main(sentence)[1] =="Good English":
                    # print sentence
                    return True
                else:
                    # print 'wrong'
                    return False

        elif conjunction[0] == 'but':
            if (tagged_sent[tagged_sent.index(conjunctions) - 1][1] == 'JJ' or
                        tagged_sent[tagged_sent.index(conjunctions) - 1][1] == 'RB' or
                        tagged_sent[tagged_sent.index(conjunctions) - 1][1] == 'NNS' or
                        tagged_sent[tagged_sent.index(conjunctions) - 1][1] == 'NN') and (
                            tagged_sent[tagged_sent.index(conjunctions) + 1][1] == 'PRP' or
                            tagged_sent[tagged_sent.index(conjunctions) + 1][1] == 'RB'):

                if Grammar.main(sentence)[1] =="Good English":
                    # print sentence
                    return True
                else:
                    # print 'wrong'
                    return False
            else:
                # print 'wrong'
                return False

        elif conjunction[0] == 'and':
            if (tagged_sent[tagged_sent.index(conjunctions) - 1][1] == 'NNS' or
                        tagged_sent[tagged_sent.index(conjunctions) - 1][1] == 'JJ') and \
                            tagged_sent[tagged_sent.index(conjunctions) + 1][1] == 'NNP':

                if Grammar.main(sentence)[1] =="Good English":
                    # print sentence
                    return True
                else:
                    # print 'wrong'
                    return False
            else:
                # print 'wrong'
                return False

        elif conjunction[0] == 'nor':
            if "neither" in sentence:
                if sentence.find("neither") < sentence.find("nor"):
                    if Grammar.main(sentence)[1] =="Good English":
                        # print sentence
                        return True
                    else:
                        # print 'wrong'
                        return False
                else:
                    # print 'wrong'
                    return False
            elif (tagged_sent[tagged_sent.index(conjunctions) - 1][1] == 'NN' or
                        tagged_sent[tagged_sent.index(conjunctions) - 1][1] == 'VBD' or
                        tagged_sent[tagged_sent.index(conjunctions) - 1][1] == 'NNP' or
                        tagged_sent[tagged_sent.index(conjunctions) - 1][1] == '-NONE-') and (
                        tagged_sent[tagged_sent.index(conjunctions) + 1][1] == 'NNP' or
                        tagged_sent[tagged_sent.index(conjunctions) + 1][1] == 'WP' or
                        tagged_sent[tagged_sent.index(conjunctions) + 1][1] == 'MD' or
                    tagged_sent[tagged_sent.index(conjunctions) + 1][1] == 'VBZ'):

                if Grammar.main(sentence)[1] =="Good English":
                    # print sentence
                    return True
                else:
                    # print 'wrong'
                    return False
            else:
                # print 'wrong'
                return False
        else:
            print 'else'
            return False


    elif [word for word, pos in tagged_sent if pos == 'RB' and word == answer]:
        conjunction = [word for word, pos in tagged_sent if pos == 'RB' and word == answer]
        conjunctions = conjunction[0], 'RB'

        # print 'Conjunction : ' + conjunction[0]

        if conjunction[0] == 'so':
            if (tagged_sent[tagged_sent.index(conjunctions) - 1][1] == 'NN' or
                        tagged_sent[tagged_sent.index(conjunctions) - 1][1] == 'JJ') and (
                    tagged_sent[tagged_sent.index(conjunctions) + 1][1] == 'RB' or
                    tagged_sent[tagged_sent.index(conjunctions) + 1][1] == 'PRP'):

                if Grammar.main(sentence)[1] =="Good English":
                    # print sentence
                    return True
                else:
                    # print 'wrong'
                    return False
            else:
                # print 'wrong'
                return False

        elif conjunction[0] == 'yet':
            if (tagged_sent[tagged_sent.index(conjunctions) - 1][1] == 'NN' or
                    tagged_sent[tagged_sent.index(conjunctions) - 1][1] == 'NNP') and (
                    tagged_sent[tagged_sent.index(conjunctions) + 1][1] == 'PRP$' or
                    tagged_sent[tagged_sent.index(conjunctions) + 1][1] == 'PRP'):

                if Grammar.main(sentence)[1] =="Good English":
                    # print sentence
                    return True
                else:
                    # print 'wrong'
                    return False
            else:
                # print 'wrong'
                return False
        else:
            print 'else'
            return False


    elif [word for word, pos in tagged_sent if pos == 'IN' and word == answer]:
        conjunction = [word for word, pos in tagged_sent if pos == 'IN' and word == answer]
        conjunctions = conjunction[0], 'IN'

        # print 'Conjunction : ' + conjunction[0]

        if conjunction[0] == 'so':
            if (tagged_sent[tagged_sent.index(conjunctions) - 1][1] == 'NN') and (
                    tagged_sent[tagged_sent.index(conjunctions) + 1][1] == 'VBP' or
                    tagged_sent[tagged_sent.index(conjunctions) + 1][1] == 'PRP'):

                if Grammar.main(sentence)[1] =="Good English":
                    # print sentence
                    return True
                else:
                    # print 'wrong'
                    return False
            else:
                # print 'wrong'
                return False

        elif conjunction[0] == 'for':
            if (tagged_sent[tagged_sent.index(conjunctions) - 1][1] == 'NNP' or
                    tagged_sent[tagged_sent.index(conjunctions) - 1][1] == 'NN' or
                    tagged_sent[tagged_sent.index(conjunctions) - 1][1] == 'RB') and (
                    tagged_sent[tagged_sent.index(conjunctions) + 1][1] == 'PRP$' or
                    tagged_sent[tagged_sent.index(conjunctions) + 1][1] == 'PRP'):

                if Grammar.main(sentence)[1] =="Good English":
                    # print sentence
                    return True
                else:
                    # print 'wrong'
                    return False
            else:
                # print 'wrong'
                return False

        else:
            print 'else'
            return False


    elif [word for word, pos in tagged_sent if (pos == 'NN') and (word == answer or word == answer + ',')]:
        conjunction = [word for word, pos in tagged_sent if pos == 'NN' and (word == answer or word == answer + ',')]
        conjunctions = conjunction[0], 'NN'

        # print 'Conjunction : ' + conjunction[0]

        if conjunction[0] == 'So,':
            if (tagged_sent.index(conjunctions) == 0) and (
                    tagged_sent[tagged_sent.index(conjunctions) + 1][1] == 'DT' or
                    tagged_sent[tagged_sent.index(conjunctions) + 1][1] == 'PRP'):
                if Grammar.main(sentence)[1] =="Good English":
                    # print sentence
                    return True
                else:
                    # print 'wrong'
                    return False
            else:
                # print 'wrong'
                return False
        else:
            print 'else'
            return False


    else:
        return False


# Find correct conjunction
def find_correct_conjunction(sentence):
    for item in valid_conjunctions:
        newSentence=sentence.split("#")[0]+item+sentence.split("#")[1]
        status=check(newSentence, item)
        if status == True:
            return item



# sentence = "He is neither sane nor brilliant."
# answer = "nor"
#
# # Execute Function
# check(sentence, answer)
# find_correct_conjunction("You'd better do your homework, # you'll get a terrible grade.")
