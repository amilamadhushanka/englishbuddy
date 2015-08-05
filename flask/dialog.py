__author__ = 'AMILA MADHUSHANKA'

import nltk
import en
import re

def check(question, answer):
    # tagged_sent = nltk.pos_tag(question.split(" "))
    # print tagged_sent
    #
    # tagged_sent = nltk.pos_tag(answer.split(" "))
    # print tagged_sent

    answer_content_marks = 0

    question_key_words = en.content.keywords(question)
    answer_array = answer.strip('.').split(" ")

    # print question_key_words
    # print answer_array

    for word in question_key_words:
        for answer in answer_array:
            if (answer.upper().find(word[1]) != -1) or (answer.lower().find(word[1]) != -1):
                answer_content_marks = answer_content_marks + 2


    if answer_content_marks == 0:
        answer_content_marks = find_place(question, answer)

    if answer_content_marks == 0:
        answer_content_marks = find_date_time(question, answer)

    if answer_content_marks == 0:
        answer_content_marks = find_adjectives(question, answer_array)

    if answer_content_marks == 0:
        answer_content_marks = find_color(question, answer_array)

    # print answer_content_marks


    # print "Answer Content Marks : " + str(answer_content_marks)
    # print "##########"
    # print word_suggestions


    # answer_grammar_marks = GrammarCheckClass.check(answer)
    # print answer_grammar_marks

    return answer_content_marks



def find_place(question, answer):

    place_list=['where', 'Where']
    place = ''

    for word in place_list:
        if word in question:
            place = re.findall(r'in the.([A-Z]?[a-zA-Z]+?[\s-]*[A-Z]*[a-zA-Z]*)'
                               r'|at the.([A-Z]?[a-zA-Z]+?[\s-]*[A-Z]*[a-zA-Z]*)', answer)

    if len(place) != 0:
        return len(place)

    return 0

def find_date_time(question, answer):

    date_time_list=['When', 'when', 'date', 'time']

    for word in date_time_list:
        if word in question:
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
                \b """, answer)

            if len(dateTime) == 2 or len(dateTime) == 1:
                for d_time in dateTime:
                    checkTime = re.findall((r'\d[\d]?\.\d\da\.m|\d[\d]?\.\d\dp\.m'), d_time)
                    if len(checkTime) != 0:
                        time = d_time
                        return 2
                        print time
                    else:
                        date = d_time
                        return 2
                        print date

    # print place
    # print len(place)

    return 0

def find_adjectives(question, answer_array):
    adjectives_array = []
    answer_array_without_punctuation = []
    adjectives = []

    tagged_sent = nltk.pos_tag(question.split(" "))
    # print tagged_sent

    if [word for word, pos in tagged_sent if pos == 'JJ']:
        adjectives = [word for word, pos in tagged_sent if pos == 'JJ']

    for adj in adjectives:
        adj = adj.strip(',')
        adjectives_array.append(adj)

    for ans in answer_array:
        ans = ans.strip(",")
        answer_array_without_punctuation.append(ans)

    for word in answer_array_without_punctuation:
        if word in adjectives_array:
            return 2

    return 0

def find_color(question, answer_array):
    status = False
    color_synonyms = ['color', 'colour', 'paint', 'dye']
    color_names = ['Yellow', 'Red', 'Silver', 'Gray', 'Purple', 'Maroon', 'Green', 'Blue', 'Black', 'Pink', 'Magenta']
    color_names_1 = []

    for color in color_names:
        color_names_1.append(color.lower())

    for color in color_synonyms:
        if question.find(color) > 0:
            status = True
            break

    if status == False:
        return 0
    else:
        for color in color_names:
            if color in answer_array:
                return 2
        for color in color_names_1:
            if color in answer_array:
                return 2

    return 0

# # test
# check("Fay: Hi Jerry. The school year is almost over. Do you have any plans for the summer holiday?",
#       "Actually, I'm plannin on to go down to Guizhou Province.",
#       "Fay: Really? Why would you go to Guizhou? It's not a very popular tourist site.")

# find_place("Where are you?", "I'm in the class.")
# find_date_time("When is the party?","2015/09/12")