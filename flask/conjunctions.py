__author__ = 'AMILA MADHUSHANKA'

import nltk

# Valid conjunctions list
valid_conjunctions = ['and', 'or', 'but', 'for', 'yet', 'nor', 'So', 'so', 'Although', 'although', 'Since', 'since',
                      'Because', 'because', 'after', 'Before', 'before', 'If', 'if', 'Once', 'once', 'until', 'Unless',
                      'unless', 'When', 'when', 'while', 'where', 'whether', 'As', 'as', 'though']


# Check the conjunction is correct
def check(sentence, answer):
    tagged_sent = nltk.pos_tag(sentence.split())
    print tagged_sent

    if [word for word, pos in tagged_sent if pos == 'CC' and word == answer]:
        conjunction = [word for word, pos in tagged_sent if pos == 'CC' and word == answer]
        conjunctions = conjunction[0], 'CC'

        print 'Conjunction : ' + conjunction[0]

        if conjunction[0] == 'or':
            if (tagged_sent[tagged_sent.index(conjunctions) - 1][1] == 'VBD' or
                        tagged_sent[tagged_sent.index(conjunctions) - 1][1] == 'NNS') and (
                    tagged_sent[tagged_sent.index(conjunctions) + 1][1] == 'VB' or
                    tagged_sent[tagged_sent.index(conjunctions) + 1][1] == 'NNP'):
                print sentence
                return True
            else:
                print 'wrong'
                return False
        elif conjunction[0] == 'but':
            if (tagged_sent[tagged_sent.index(conjunctions) - 1][1] == 'JJ' or
                        tagged_sent[tagged_sent.index(conjunctions) - 1][1] == 'NNS' or
                        tagged_sent[tagged_sent.index(conjunctions) - 1][1] == 'NN') and (
                    tagged_sent[tagged_sent.index(conjunctions) + 1][1] == 'PRP' or
                    tagged_sent[tagged_sent.index(conjunctions) + 1][1] == 'RB'):
                print sentence
                return True
            else:
                print 'wrong'
                return False
        elif conjunction[0] == 'and':
            if (tagged_sent[tagged_sent.index(conjunctions) - 1][1] == 'NNS' or
                        tagged_sent[tagged_sent.index(conjunctions) - 1][1] == 'JJ') and \
                            tagged_sent[tagged_sent.index(conjunctions) + 1][1] == 'NNP':
                print sentence
                return True
            else:
                print 'wrong'
                return False
        elif conjunction[0] == 'nor':
            if (tagged_sent[tagged_sent.index(conjunctions) - 1][1] == 'NN' or
                        tagged_sent[tagged_sent.index(conjunctions) - 1][1] == 'VBD' or
                        tagged_sent[tagged_sent.index(conjunctions) - 1][1] == 'NNP' or
                        tagged_sent[tagged_sent.index(conjunctions) - 1][1] == '-NONE-') and (
                        tagged_sent[tagged_sent.index(conjunctions) + 1][1] == 'NNP' or
                        tagged_sent[tagged_sent.index(conjunctions) + 1][1] == 'WP' or
                        tagged_sent[tagged_sent.index(conjunctions) + 1][1] == 'MD' or
                    tagged_sent[tagged_sent.index(conjunctions) + 1][1] == 'VBZ'):
                print sentence
                return True
            else:
                print 'wrong'
                return False
        else:
            print 'else'
            return False


    elif [word for word, pos in tagged_sent if pos == 'RB' and word == answer]:
        conjunction = [word for word, pos in tagged_sent if pos == 'RB' and word == answer]
        conjunctions = conjunction[0], 'RB'

        print 'Conjunction : ' + conjunction[0]

        if conjunction[0] == 'so':
            if (tagged_sent[tagged_sent.index(conjunctions) - 1][1] == 'NN' or
                        tagged_sent[tagged_sent.index(conjunctions) - 1][1] == 'JJ') and (
                    tagged_sent[tagged_sent.index(conjunctions) + 1][1] == 'RB' or
                    tagged_sent[tagged_sent.index(conjunctions) + 1][1] == 'PRP'):
                print sentence
                return True
            else:
                print 'wrong'
                return False
        elif conjunction[0] == 'yet':
            if (tagged_sent[tagged_sent.index(conjunctions) - 1][1] == 'NN') and (
                    tagged_sent[tagged_sent.index(conjunctions) + 1][1] == 'PRP$' or
                    tagged_sent[tagged_sent.index(conjunctions) + 1][1] == 'PRP'):
                print sentence
                return True
            else:
                print 'wrong'
                return False
        elif conjunction[0] == 'once':
            if (tagged_sent[tagged_sent.index(conjunctions) - 1][1] == 'PRP' or
                    tagged_sent[tagged_sent.index(conjunctions) - 1][1] == 'RP') and (
                    tagged_sent[tagged_sent.index(conjunctions) + 1][1] == 'PRP$' or
                    tagged_sent[tagged_sent.index(conjunctions) + 1][1] == 'DT' or
                    tagged_sent[tagged_sent.index(conjunctions) + 1][1] == 'PRP'):
                print sentence
                return True
            else:
                print 'wrong'
                return False
        elif conjunction[0] == 'Once':
            if (tagged_sent.index(conjunctions) == 0) and (
                        tagged_sent[tagged_sent.index(conjunctions) + 1][1] == 'PRP$' or \
                        tagged_sent[tagged_sent.index(conjunctions) + 1][1] == 'PRP' or \
                        tagged_sent[tagged_sent.index(conjunctions) + 1][1] == 'DT'):
                print sentence
                return True
            else:
                print 'wrong'
                return False
        else:
            print 'else'
            return False


    elif [word for word, pos in tagged_sent if pos == 'IN' and word == answer]:
        conjunction = [word for word, pos in tagged_sent if pos == 'IN' and word == answer]
        conjunctions = conjunction[0], 'IN'

        print 'Conjunction : ' + conjunction[0]

        if conjunction[0] == 'so':
            if (tagged_sent[tagged_sent.index(conjunctions) - 1][1] == 'NN') and (
                    tagged_sent[tagged_sent.index(conjunctions) + 1][1] == 'VBP' or
                    tagged_sent[tagged_sent.index(conjunctions) + 1][1] == 'PRP'):
                print sentence
                return True
            else:
                print 'wrong'
                return False
        # elif conjunction[0] == 'for':
        #     if (tagged_sent[tagged_sent.index(conjunctions) - 1][1] == 'NNP' or
        #                 tagged_sent[tagged_sent.index(conjunctions) - 1][1] == 'NN') and (
        #             tagged_sent[tagged_sent.index(conjunctions) + 1][1] == 'PRP$' or
        #             tagged_sent[tagged_sent.index(conjunctions) + 1][1] == 'PRP'):
        #         print sentence
        #         return True
        #     else:
        #         print 'wrong'
        #         return False
        elif conjunction[0] == 'Although':
            if (tagged_sent.index(conjunctions) == 0) and (
                    tagged_sent[tagged_sent.index(conjunctions) + 1][1] == 'PRP' or
                    tagged_sent[tagged_sent.index(conjunctions) + 1][1] == 'PRP$'):
                print sentence
                return True
            else:
                print 'wrong'
                return False
        elif conjunction[0] == 'although':
            if (tagged_sent[tagged_sent.index(conjunctions) - 1][1] == 'JJ' or
                tagged_sent[tagged_sent.index(conjunctions) - 1][1] == 'IN') and (
                tagged_sent[tagged_sent.index(conjunctions) + 1][1] == 'PRP' or
                tagged_sent[tagged_sent.index(conjunctions) + 1][1] == 'JJ'):
                print sentence
                return True
            else:
                print 'wrong'
                return False
        elif conjunction[0] == 'Since':
            if (tagged_sent.index(conjunctions) == 0) and (
                    tagged_sent[tagged_sent.index(conjunctions) + 1][1] == 'PRP' or
                    tagged_sent[tagged_sent.index(conjunctions) + 1][1] == 'JJ'):
                print sentence
                return True
            else:
                print 'wrong'
                return False
        elif conjunction[0] == 'since':
            if (tagged_sent[tagged_sent.index(conjunctions) - 1][1] == 'VBN' or
                        tagged_sent[tagged_sent.index(conjunctions) - 1][1] == 'NN' or
                        tagged_sent[tagged_sent.index(conjunctions) - 1][1] == 'VBG' or
                        tagged_sent[tagged_sent.index(conjunctions) - 1][1] == 'NNS') and (
                        tagged_sent[tagged_sent.index(conjunctions) + 1][1] == 'PRP' or
                        tagged_sent[tagged_sent.index(conjunctions) + 1][1] == 'JJ' or
                        tagged_sent[tagged_sent.index(conjunctions) + 1][1] == 'PRP$'):
                print sentence
                return True
            else:
                print 'wrong'
                return False
        elif conjunction[0] == 'after':
            if (tagged_sent[tagged_sent.index(conjunctions) - 1][1] == 'NNS' or
                        tagged_sent[tagged_sent.index(conjunctions) - 1][1] == 'PRP' or
                        tagged_sent[tagged_sent.index(conjunctions) - 1][1] == 'RP' or
                        tagged_sent[tagged_sent.index(conjunctions) - 1][1] == 'NN') and (
                            tagged_sent[tagged_sent.index(conjunctions) + 1][1] == 'PRP' or
                            tagged_sent[tagged_sent.index(conjunctions) + 1][1] == 'DT'):
                print sentence
                return True
            else:
                print 'wrong'
                return False
        elif conjunction[0] == 'because':
            if (tagged_sent[tagged_sent.index(conjunctions) - 1][1] == 'NN' or
                        tagged_sent[tagged_sent.index(conjunctions) - 1][1] == 'IN' or
                        tagged_sent[tagged_sent.index(conjunctions) - 1][1] == 'NNS') and (
                        tagged_sent[tagged_sent.index(conjunctions) + 1][1] == 'PRP' or
                        tagged_sent[tagged_sent.index(conjunctions) + 1][1] == 'JJ'):
                print sentence
                return True
            else:
                print 'wrong'
                return False
        elif conjunction[0] == 'Because':
            if (tagged_sent.index(conjunctions) == 0) and (
                    tagged_sent[tagged_sent.index(conjunctions) + 1][1] == 'PRP' or
                    tagged_sent[tagged_sent.index(conjunctions) + 1][1] == 'PRP$'):
                print sentence
                return True
            else:
                print 'wrong'
                return False
        elif conjunction[0] == 'before':
            if (tagged_sent[tagged_sent.index(conjunctions) - 1][1] == 'NNS' or
                        tagged_sent[tagged_sent.index(conjunctions) - 1][1] == 'RP') and (
                        tagged_sent[tagged_sent.index(conjunctions) + 1][1] == 'PRP' or
                        tagged_sent[tagged_sent.index(conjunctions) + 1][1] == 'DT' or
                        tagged_sent[tagged_sent.index(conjunctions) + 1][1] == 'PRP$'):
                print sentence
                return True
            else:
                print 'wrong'
                return False
        elif conjunction[0] == 'Before':
            if (tagged_sent.index(conjunctions) == 0) and (
                    tagged_sent[tagged_sent.index(conjunctions) + 1][1] == 'PRP' or
                    tagged_sent[tagged_sent.index(conjunctions) + 1][1] == 'PRP$'):
                print sentence
                return True
            else:
                print 'wrong'
                return False
        elif conjunction[0] == 'If':
            if (tagged_sent.index(conjunctions)==0) and (tagged_sent[tagged_sent.index(conjunctions) + 1][1] == 'PRP' or
                    tagged_sent[tagged_sent.index(conjunctions) + 1][1] == 'PRP$'):
                print sentence
                return True
            else:
                print 'wrong'
                return False
        elif conjunction[0] == 'if':
            if (tagged_sent[tagged_sent.index(conjunctions) - 1][1] == 'NN') and (
                    tagged_sent[tagged_sent.index(conjunctions) + 1][1] == 'PRP' or
                    tagged_sent[tagged_sent.index(conjunctions) + 1][1] == 'PRP$'):
                print sentence
                return True
            else:
                print 'wrong'
                return False
        elif conjunction[0] == 'until':
            if (tagged_sent[tagged_sent.index(conjunctions) - 1][1] == 'RB' or
                        tagged_sent[tagged_sent.index(conjunctions) - 1][1] == 'RP' or
                        tagged_sent[tagged_sent.index(conjunctions) - 1][1] == 'VB' or
                        tagged_sent[tagged_sent.index(conjunctions) - 1][1] == 'NN') and (
                        tagged_sent[tagged_sent.index(conjunctions) + 1][1] == 'PRP' or
                        tagged_sent[tagged_sent.index(conjunctions) + 1][1] == 'PRP$' or
                        tagged_sent[tagged_sent.index(conjunctions) + 1][1] == 'DT' or
                        tagged_sent[tagged_sent.index(conjunctions) + 1][1] == 'NN'):
                print sentence
                return True
            else:
                print 'wrong'
                return False
        elif conjunction[0] == 'unless':
            if (tagged_sent[tagged_sent.index(conjunctions) - 1][1] == 'NN' or
                        tagged_sent[tagged_sent.index(conjunctions) - 1][1] == 'RP' or
                        tagged_sent[tagged_sent.index(conjunctions) - 1][1] == 'IN') and (
                        tagged_sent[tagged_sent.index(conjunctions) + 1][1] == 'PRP' or
                        tagged_sent[tagged_sent.index(conjunctions) + 1][1] == 'PRP$'):
                print sentence
                return True
            else:
                print 'wrong'
                return False
        elif conjunction[0] == 'Unless':
            if (tagged_sent.index(conjunctions) == 0) and (
                    tagged_sent[tagged_sent.index(conjunctions) + 1][1] == 'PRP' or
                    tagged_sent[tagged_sent.index(conjunctions) + 1][1] == 'PRP$'):
                print sentence
                return True
            else:
                print 'wrong'
                return False
        elif conjunction[0] == 'while':
            if (tagged_sent[tagged_sent.index(conjunctions) - 1][1] == 'PRP' or
                        tagged_sent[tagged_sent.index(conjunctions) - 1][1] == 'VBD' or
                        tagged_sent[tagged_sent.index(conjunctions) - 1][1] == 'VBG' or
                        tagged_sent[tagged_sent.index(conjunctions) - 1][1] == 'IN' or
                        tagged_sent[tagged_sent.index(conjunctions) - 1][1] == 'NN') and (
                        tagged_sent[tagged_sent.index(conjunctions) + 1][1] == 'PRP' or
                        tagged_sent[tagged_sent.index(conjunctions) + 1][1] == 'DT' or
                        tagged_sent[tagged_sent.index(conjunctions) + 1][1] == 'PRP$'):
                print sentence
                return True
            else:
                print 'wrong'
                return False
        elif conjunction[0] == 'whether':
            if (tagged_sent[tagged_sent.index(conjunctions) - 1][1] == 'JJ' or
                        tagged_sent[tagged_sent.index(conjunctions) - 1][1] == 'VB' or
                        tagged_sent[tagged_sent.index(conjunctions) - 1][1] == 'PRP') and (
                        tagged_sent[tagged_sent.index(conjunctions) + 1][1] == 'PRP' or
                        tagged_sent[tagged_sent.index(conjunctions) + 1][1] == 'PRP$' or
                        tagged_sent[tagged_sent.index(conjunctions) + 1][1] == 'CC'):
                print sentence
                return True
            else:
                print 'wrong'
                return False
        elif conjunction[0] == 'As':
            if (tagged_sent.index(conjunctions) == 0) and (
                        tagged_sent[tagged_sent.index(conjunctions) + 1][1] == 'PRP' or \
                        tagged_sent[tagged_sent.index(conjunctions) + 1][1] == 'NNP' or \
                        tagged_sent[tagged_sent.index(conjunctions) + 1][1] == 'JJ'):
                print sentence
                return True
            else:
                print 'wrong'
                return False
        elif conjunction[0] == 'as':
            if (tagged_sent[tagged_sent.index(conjunctions) - 1][1] == 'IN') and (
                    tagged_sent[tagged_sent.index(conjunctions) + 1][1] == 'PRP' or
                    tagged_sent[tagged_sent.index(conjunctions) + 1][1] == 'RB'):
                print sentence
                return True
            else:
                print 'wrong'
                return False
        elif conjunction[0] == 'though':
            if (tagged_sent[tagged_sent.index(conjunctions) - 1][1] == 'IN') and (
                    tagged_sent[tagged_sent.index(conjunctions) + 1][1] == 'PRP'):
                print sentence
                return True
            else:
                print 'wrong'
                return False
        else:
            print 'else'
            return False


    elif [word for word, pos in tagged_sent if (pos == 'NN') and (word == answer or word == answer + ',')]:
        conjunction = [word for word, pos in tagged_sent if pos == 'NN' and (word == answer or word == answer + ',')]
        conjunctions = conjunction[0], 'NN'

        print 'Conjunction : ' + conjunction[0]

        if conjunction[0] == 'So,':
            if (tagged_sent.index(conjunctions) == 0) and (
                    tagged_sent[tagged_sent.index(conjunctions) + 1][1] == 'DT' or
                    tagged_sent[tagged_sent.index(conjunctions) + 1][1] == 'PRP'):
                print sentence
                return True
            else:
                print 'wrong'
                return False
        else:
            print 'else'
            return False


    elif [word for word, pos in tagged_sent if pos == 'WRB' and word == answer]:
        conjunction = [word for word, pos in tagged_sent if pos == 'WRB' and word == answer]
        conjunctions = conjunction[0], 'WRB'

        print 'Conjunction : ' + conjunction[0]

        if conjunction[0] == 'When':
            if (tagged_sent.index(conjunctions) == 0) and (
                tagged_sent[tagged_sent.index(conjunctions) + 1][1] == 'PRP'):
                print sentence
                return True
            else:
                print 'wrong'
                return False

        elif conjunction[0] == 'when':
            if (tagged_sent[tagged_sent.index(conjunctions) - 1][1] == 'RP' or
                        tagged_sent[tagged_sent.index(conjunctions) - 1][1] == 'NN' or
                        tagged_sent[tagged_sent.index(conjunctions) - 1][1] == 'PRP') and (
                        tagged_sent[tagged_sent.index(conjunctions) + 1][1] == 'PRP' or
                        tagged_sent[tagged_sent.index(conjunctions) + 1][1] == 'PRP$'):
                print sentence
                return True
            else:
                print 'wrong'
                return False
        elif conjunction[0] == 'where':
            if (tagged_sent[tagged_sent.index(conjunctions) - 1][1] == 'PRP' or
                        tagged_sent[tagged_sent.index(conjunctions) - 1][1] == 'VBZ' or
                        tagged_sent[tagged_sent.index(conjunctions) - 1][1] == 'VB' or
                        tagged_sent[tagged_sent.index(conjunctions) - 1][1] == 'VBP') and (
                        tagged_sent[tagged_sent.index(conjunctions) + 1][1] == 'PRP' or
                        tagged_sent[tagged_sent.index(conjunctions) + 1][1] == 'PRP$' or
                        tagged_sent[tagged_sent.index(conjunctions) + 1][1] == 'NNP' or
                        tagged_sent[tagged_sent.index(conjunctions) + 1][1] == 'DT' or
                        tagged_sent[tagged_sent.index(conjunctions) + 1][1] == 'JJ'):
                print sentence
                return True
            else:
                print 'wrong'
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



# sentence = "I want to go there again, for it was a wonderful trip."
# answer = "for"
#
# # Execute Function
# check(sentence, answer)
# find_correct_conjunction("I want to go there again # it was a wonderful trip.")
