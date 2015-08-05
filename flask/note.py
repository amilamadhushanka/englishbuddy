__author__ = 'Darani'

import numpy
import nltk
from nltk import pos_tag, word_tokenize
from nltk.tag import pos_tag
from nltk.tokenize import sent_tokenize
import re
import en
import keywords

def sum_of_words(answer):

    sum = 0
    for word1 in word_tokenize(answer):
        if word1 == '.' or word1 == ',' or word1 == '\'' or word1 == '\"' or word1 == ':' or word1 == ';' or word1 == '?' or word1 == '/' or word1 == '\\' or word1 == '|' or word1 == ']' or word1 == '[' or word1 == '}' or word1 == '{' or word1 == '(' or word1 == ')' or word1 == '*' or word1 == '&' or word1 == '^' or word1 == '%' or word1 == '$' or word1 == '#' or word1 == '@' or word1 == '!' or word1 == '`' or word1 == '~' or word1 == '-' or word1 == '_' or word1 == '='or word1 == '+':
            print 'error'
        else:
            sum = sum +1
            #print word1

    return sum

def word_count(answer,question):

    words_qus = word_tokenize(question)
    count = 0
    status1 = 'false'
    for word in words_qus:
        if en.is_number(word) and words_qus[words_qus.index(word)+1]== 'words':
            if sum_of_words(answer) >= word:
                print word
                count = count+0.5
            status1 = 'true'
    if status1 == 'false':
        count = count+0.5
    return count

def note_receiver(answer):
    count = 0
    status = 'false'
    tag_words = pos_tag(answer.split())
    if (tag_words[0][1]=='NNP'or tag_words[1][1]=='NNP') and (tag_words[0][0].isupper() or tag_words[1][0].isupper):
        if (tag_words[0][1] == 'Dear' or tag_words[1][1] == 'Dear' ):
                print tag_words[0][0]
        else:
             count = count + 0.5
             status = 'true'
    return count,status

def note_writer(answer):

    count = 0
    status = 'false'
    status_your = 'correct'
    tag_words = pos_tag(answer.split())
    print 'val:', len(tag_words)
    word = tag_words[len(tag_words)-1][0]
    print 'll ',tag_words[len(tag_words)-1][0]
    if tag_words[len(tag_words)-3][0] == 'Yours' and (tag_words[len(tag_words)-2][0] == 'sincerely,' or tag_words[len(tag_words)-2][0] == 'Sincerely,' or tag_words[len(tag_words)-2][0] == 'faithfully,' or tag_words[len(tag_words)-2][0] == 'Faithfully,'):
        count = count + 0
        status_your = 'wrong'
    elif tag_words[len(tag_words)-2][0] == 'Yours' and (tag_words[len(tag_words)-1][0] == 'sincerely,' or tag_words[len(tag_words)-1][0] == 'Sincerely,' or tag_words[len(tag_words)-1][0] == 'faithfully,' or tag_words[len(tag_words)-1][0] == 'Faithfully,'):
        count = count + 0
        status_your = 'wrong'
    elif tag_words[len(tag_words)-2][0] == 'Your' :
        count = count + 0
        status_your = 'wrong'

    if tag_words[len(tag_words)-1][1] == 'NNP' and word[0].isupper() :
        if (word == 'Faithfully,') or (word == 'Sincerely,'):
            print 'yes'
        else:
            print tag_words[len(tag_words)-1][0]
            count = count + 0.5
            status = 'true'
    print 'stat',status
    print 'stat1',status_your
    return count,status,status_your

def note_body(answer,question):

    count = 0
    sentences_qus= sent_tokenize(question)

    for sentence_qus in sentences_qus:
          top = keywords.top(sentence_qus)
          words_ans = word_tokenize(answer)
          matching_count = 0
          for count,word in top:
              for word_ans in words_ans:
                    if word == word_ans:
                        print word
                        matching_count = matching_count+1

          different = len(top)- matching_count
          if (different+2)== 0 or (different+2)== 1 or (different+2)== 2:
             count = count + 0.5

    return count

