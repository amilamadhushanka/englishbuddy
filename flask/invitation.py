__author__ = 'Darani'

import numpy
import nltk
from nltk import pos_tag, word_tokenize
from nltk.tag import pos_tag
from nltk.tokenize import sent_tokenize
import re
import en
import keywords

def checkTypeWordCount(answer,question):
    count = 0
    status = ''
    sum = 0
    status1 = 'false'

    for word1 in word_tokenize(answer):
        if word1 == '.' or word1 == ',' or word1 == '\'' or word1 == '\"' or word1 == ':' or word1 == ';' or word1 == '?' or word1 == '/' or word1 == '\\' or word1 == '|' or word1 == ']' or word1 == '[' or word1 == '}' or word1 == '{' or word1 == '(' or word1 == ')' or word1 == '*' or word1 == '&' or word1 == '^' or word1 == '%' or word1 == '$' or word1 == '#' or word1 == '@' or word1 == '!' or word1 == '`' or word1 == '~' or word1 == '-' or word1 == '_' or word1 == '='or word1 == '+':
            print 'error'
        else:
            sum = sum +1
            print word1
    print sum

    words_ans = word_tokenize(answer)
    words_qus = word_tokenize(question)
    if words_ans[0]=="Invitation"or words_ans[0]=="INVITATION":
        print "Correct"
        count = count+0.25
    else:
        status = "Wrong"

    for word in words_qus:
        if en.is_number(word) and words_qus[words_qus.index(word)+1]== 'words':
            if sum >= word:
                print word
                count = count+0.25
            status1='true'

    if status1 == 'false':
        count = count+0.25

    return count,status



def includes(answer,question):

    count = 0
    sentences_qus= sent_tokenize(question)
    matching_count = 0

    for sentence_qus in sentences_qus:
      top = keywords.top(sentence_qus, nouns=True)
      words_ans = word_tokenize(answer)
      words_qus = word_tokenize(sentence_qus)
      for word_qus in words_qus:
       if word_qus == 'Include' or word_qus == 'include' or word_qus == 'Include:' :

          for count,word in top:
              for word_ans in words_ans:
                    if word == word_ans:
                        print word
                        matching_count = matching_count+1
                        #print matching_count

          #print len(top)
       defferent = len(top)- matching_count
       if (defferent+2)== 0 or (defferent+2)== 1 or (defferent+2)== 2:
             count = count + 0.5
    return count

def designation(answer, question):

    sentences_qus= sent_tokenize(question)
    count = 0
    name = ' '
    address = ' '
    for sentence_qus in sentences_qus:
      words_qus = word_tokenize(sentence_qus)
     # print sentence_qus
     # print words_qus

      words_ans = word_tokenize(answer)
      # print words_ans

      for word in words_qus:
          if word == 'You' or word == 'you' and words_qus[words_qus.index(word)+1] == 'are':
              #print 'heloo'
              index_you = words_qus.index(word)
              index_are = index_you+1
              index_last = words_qus.index('.')

              for s in range(index_are,index_last):
                  #check the post of writer

                  if words_qus[s]== 'of':

                      index_of = words_qus.index(words_qus[s])

                      for x in range(index_are, index_of):
                          i=7
                          for y in range(len(words_ans)-i, len(words_ans)):

                              if words_qus[x].lower() == words_ans[y].lower():
                                  if words_ans[y+1]==',':
                                    name = 'Correct'
                                    break
                              else:
                                  name = 'Wrong'
                              #print sentences_qus[x],',,',sentences_ans[y]
                              i= i-1

                    #address of the writer

                      for p in range(index_of, index_last):
                          j=7
                          for q in range(len(words_ans)-j, len(words_ans)):
                              if words_qus[p].lower() == words_ans[q].lower():
                                  address = 'Correct'
                                  break
                              else:
                                  address = 'Wrong'

                              j= j-1



          elif word == 'As' or word == 'as':
              index_as = words_ans.index(word)
              for s in range(index_as,len(words_qus)):
                  if words_qus[s]== 'of':
                      index_of = words_qus.index(words_qus[s])

                      for x in range(index_as, index_of):
                          i= 7
                          for y in range(len(words_ans)-i, len(words_ans)):
                              if sentence_qus[x].lower() == words_ans[y].lower():
                                  name = 'Correct'
                                  break
                              else:
                                  name = 'Wrong'
                              i= i-1

                      j= 7
                      for p in range(index_of, len(words_qus)):
                          for q in range(len(words_ans)-j, len(words_ans)):
                              if sentence_qus[p].lower() == words_ans[q].lower():
                                  address = 'Correct'
                                  break
                              else:
                                  address = 'Wrong'
                              j= j-1

      if name == 'Wrong' and address == 'Wrong' :

              i= 7
              for y in range(len(words_ans)-i, len(words_ans)):
                if 'secretary' == words_ans[y].lower() or 'monitor' == words_ans[y].lower() or 'principle' == words_ans[y].lower() or "teacher" == words_ans[y].lower() or 'head' == words_ans[y].lower() or 'leader' == words_ans[y].lower() or 'students' == words_ans[y].lower() or 'student' == words_ans[y].lower() :
                        name = 'Correct'
                        address = 'Correct'
                        break
                else:
                        name = 'Wrong'
                        i= i-1

      if name == 'Correct' and address == 'Correct':
                 count = 0.5

    return count , name, address

def dateTimeVenue(answer):

    #date and time
    count = 0
    time = ''
    date = ''
    showtime = 'true'
    showdate = 'true'
    showvenue = 'true'
    sentences_ans= sent_tokenize(answer)
    for sentence_ans in sentences_ans:
        #print sentence_ans
        dateTime = re.findall(
    r"""(?ix)             # case-insensitive, verbose regex
    \b                    # match a word boundary
    (?:                   # match the following three times:
     (?:                  # either
      \d+                 # a number,
      (?:\.|st|nd|rd|th|a\.m|p\.m)* # followed by a dot, st, nd, rd, or th (optional)
      |                   # or a month name
      (?:(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*)
           )
       [\s./-]?           # followed by a date separator or whitespace (optional)
    ){3}                  # do this three times
    \b """,
    sentence_ans)

        if len(dateTime) == 2 or len(dateTime) == 1 :
         for d_time in dateTime:
            checkTime = re.findall(r'\d[\d]?\.\d\da\.m|\d[\d]?\.\d\dp\.m|\d[\d]?\.\d\d',d_time)
            if len(checkTime) != 0:
                time = d_time
                #print time
            else:
                date = d_time
              #print date

    #venue
        venue = re.findall(r'in .([A-Z]?[a-zA-Z]+?[\s-]*[A-Z]*[a-zA-Z]*)'
                           r'|at .([A-Z]?[a-zA-Z]+?[\s-]*[A-Z]*[a-zA-Z]*)'
                           r'|venue .([A-Z]?[a-zA-Z]+?[\s-]*[A-Z]*[a-zA-Z]*)'
                           r'|place .([A-Z]?[a-zA-Z]+?[\s-]*[A-Z]*[a-zA-Z]*)'
                           r'|in: - .([A-Z]?[a-zA-Z]+?[\s-]*[A-Z]*[a-zA-Z]*)'
                           r'|at: -.([A-Z]?[a-zA-Z]+?[\s-]*[A-Z]*[a-zA-Z]*)'
                           r'|venue: -.([A-Z]?[a-zA-Z]+?[\s-]*[A-Z]*[a-zA-Z]*)'
                           r'|place: -.([A-Z]?[a-zA-Z]+?[\s-]*[A-Z]*[a-zA-Z]*)'
                           r'|in - .([A-Z]?[a-zA-Z]+?[\s-]*[A-Z]*[a-zA-Z]*)'
                           r'|at -.([A-Z]?[a-zA-Z]+?[\s-]*[A-Z]*[a-zA-Z]*)'
                           r'|venue -.([A-Z]?[a-zA-Z]+?[\s-]*[A-Z]*[a-zA-Z]*)'
                           r'|place -.([A-Z]?[a-zA-Z]+?[\s-]*[A-Z]*[a-zA-Z]*)',sentence_ans.lower())

        print len(venue),len(time),len(date)
        print "v",venue
        if len(time) != 0 and len(date) != 0 and len(venue) != 0:
            count = 0.5
            showtime = 'true'
            showdate = 'true'
            showvenue = 'true'
            break
        else:
            if len(time) == 0:
             showtime = 'false'
            if len(date) == 0:
             showdate = 'false'
            if len(venue) == 0:
             showvenue = 'false'

    return  count,showtime,showdate,showvenue