import nltk
from nltk.tokenize import sent_tokenize

text="Keep quiet or go out."

sentences=sent_tokenize(text)
for sentence in sentences:

################simple present ##########################################################
  tagged_sent = nltk.pos_tag(sentence.split())
  print tagged_sent

  if[word for word,pos in tagged_sent if pos == 'PRP']:
    noun=  [word for word,pos in tagged_sent if pos == 'PRP']
    nouns = noun[0],'PRP'

    currant = tagged_sent.index(nouns)

    if noun[0]=='He' or noun[0]=='She' or noun[0]=='It' or noun[0]=='he' or noun[0]=='she' or noun[0]=='it':
        if tagged_sent[currant+1][1]=='VBZ':
            if tagged_sent[currant+1][0]=='is':
                if tagged_sent[currant+2][1]=='VBG' or tagged_sent[currant+2][1]=='RB' :
                   print sentence
            else:
                print sentence

        elif tagged_sent[currant+1][0]=='didn\'t' or tagged_sent[currant+1][0]=='did not':
              if tagged_sent[currant+2][1]=='VBP':
                print sentence

              else:
               print('wrong')


        elif tagged_sent[currant+1][1]=='RB':
              if tagged_sent[currant+2][1]=='VBZ':
                print sentence
              else:
               print('wrong')
        #past tense
        elif tagged_sent[currant+1][0]=='was':
                 print sentence
        elif tagged_sent[currant+1][1]=='VBD':
                 print sentence

        #future tense
        elif tagged_sent[currant+1][1]=='MD':
          if tagged_sent[currant+2][1]=='VB':
                 print sentence
          elif tagged_sent[currant+2][0]=='not':
                 print(sentence)

        else:
            print('wrong')

    elif noun[0]=='I':
        if tagged_sent[currant+1][1]=='VBP':
                print sentence

        elif tagged_sent[currant+1][0]=='don\'t' or tagged_sent[currant+1][0]=='do not':
              if tagged_sent[currant+2][1]=='VBP':
                print sentence

              else:
               print('wrong')


        elif tagged_sent[currant+1][1]=='RB':
              if tagged_sent[currant+2][1]=='VBZ':
                print sentence

              else:
               print('wrong')


        #past tense
        elif tagged_sent[currant+1][0]=='were':
                 print sentence

    #future tense
        elif tagged_sent[currant+1][1]=='MD':
            if tagged_sent[currant+2][1]=='VB':
                print sentence
            elif tagged_sent[currant+2][0]=='not':
                print(sentence)
            else:
                print('wrong')



    elif tagged_sent[currant+1][1]=='RB':
        if tagged_sent[currant+2][1]=='VBP':
                print sentence

        elif tagged_sent[currant+2][1]=='VB':
                print sentence
       #check
        elif tagged_sent[currant+2][1]=='VBD':
                 print sentence

        else:
          print('wrong')

    elif tagged_sent[currant+1][1]=='VBP':
                print sentence

    elif tagged_sent[currant+1][1]=='VB':
        print sentence
    #past tense
    elif tagged_sent[currant+1][0]=='were':
                 print sentence
    elif tagged_sent[currant+1][1]=='VBD':
                 print sentence

    #future tense
    elif tagged_sent[currant+1][1]=='MD':
          if tagged_sent[currant+2][1]=='VB':
                 print sentence
          elif tagged_sent[currant+2][0]=='not':
                 print(sentence)


    else:
        print('wrong')

  elif [word for word,pos in tagged_sent if pos == 'NN']:
    noun = [word for word,pos in tagged_sent if pos == 'NN']
    nouns = noun[0],'NN'
    #
    currant = tagged_sent.index(nouns)
    #

    if currant==1:
        if tagged_sent[currant-1][1]=='DT':
            if tagged_sent[currant-1][0]=='This' or tagged_sent[currant-1][0]=='That':


                          if tagged_sent[currant+1][1]=='VBZ':
                                         print sentence
                          elif tagged_sent[currant+1][1]=='RB':
                                if tagged_sent[currant+2][1]=='VBZ':
                                        print sentence

                                else:
                                  print('wrong')
                            #past tense
                          elif tagged_sent[currant+1][1]=='VBD':
                                         print sentence

                          elif tagged_sent[currant+1][0]=='was':
                                         print sentence
                            #future tense
                          elif tagged_sent[currant+1][1]=='MD':
                                  if tagged_sent[currant+2][1]=='VB':
                                         print sentence

                                  elif tagged_sent[currant+2][0]=='not':
                                         print(sentence)

                          else:
                                print 'wrong'
            else:
                print('wrong')


        else:
            if tagged_sent[currant+1][1]=='VBZ':
                         print sentence
            elif tagged_sent[currant+1][1]=='RB':
                if tagged_sent[currant+2][1]=='VBZ':
                    print sentence

                else:
                    print('wrong')
                            #past tense
            elif tagged_sent[currant+1][1]=='VBD':
                    print sentence

            elif tagged_sent[currant+1][0]=='was':
                     print sentence
                            #future tense
            elif tagged_sent[currant+1][1]=='MD':
                if tagged_sent[currant+2][1]=='VB':
                    print sentence

                elif tagged_sent[currant+2][0]=='not':
                    print(sentence)

            else:
               print 'wrong'

    else:
        if tagged_sent[currant+1][1]=='VBZ':
                         print sentence
        elif tagged_sent[currant+1][1]=='RB':
                if tagged_sent[currant+2][1]=='VBZ':
                    print sentence

                else:
                  print('wrong')
                            #past tense
        elif tagged_sent[currant+1][1]=='VBD':
                    print sentence

        elif tagged_sent[currant+1][0]=='was':
                     print sentence
                            #future tense
        elif tagged_sent[currant+1][1]=='MD':
                if tagged_sent[currant+2][1]=='VB':
                    print sentence

                elif tagged_sent[currant+2][0]=='not':
                    print(sentence)

        else:
            print 'wrong'


  elif( [word for word,pos in tagged_sent if pos == 'NNS']):

    noun=[word for word,pos in tagged_sent if pos == 'NNS']
    nouns = noun[0],'NNS'

    currant = tagged_sent.index(nouns)

    if currant==1:
        if tagged_sent[currant-1][1]=='DT':
            if tagged_sent[currant-1][0]=='These' or tagged_sent[currant-1][0]=='Those':


                            if tagged_sent[currant+1][1]=='VBP':
                                        print sentence

                            elif tagged_sent[currant+1][1]=='VB':
                                print sentence

                            #past tense
                            elif tagged_sent[currant+1][0]=='were':
                                         print sentence
                            elif tagged_sent[currant+1][1]=='RB':
                                if tagged_sent[currant+2][1]=='VBP':
                                        print sentence

                                elif tagged_sent[currant+2][1]=='VB':
                                        print sentence
                                else:
                                  print('wrong')
                            #future tense
                            elif tagged_sent[currant+1][1]=='MD':
                                  if tagged_sent[currant+2][1]=='VB':
                                         print sentence
                                  elif tagged_sent[currant+2][0]=='not':
                                         print(sentence)


                            else:
                                print('wrong')
            else:
                print('wrong')

        else:
             if tagged_sent[currant+1][1]=='VBP':
                            print sentence

             elif tagged_sent[currant+1][1]=='VB':
                                print sentence

                            #past tense
             elif tagged_sent[currant+1][0]=='were':
                        print sentence
             elif tagged_sent[currant+1][1]=='RB':

                if tagged_sent[currant+2][1]=='VBP':
                             print sentence

                elif tagged_sent[currant+2][1]=='VB':

                        print sentence
                else:
                   print('wrong')
                            #future tense
             elif tagged_sent[currant+1][1]=='MD':
                    if tagged_sent[currant+2][1]=='VB':
                            print sentence
                    elif tagged_sent[currant+2][0]=='not':
                            print(sentence)

                    else:
                        print('wrong')

    else:
         if tagged_sent[currant+1][1]=='VBP':
                        print sentence

         elif tagged_sent[currant+1][1]=='VB':
                        print sentence

                            #past tense
         elif tagged_sent[currant+1][0]=='were':
                        print sentence
         elif tagged_sent[currant+1][1]=='RB':
                if tagged_sent[currant+2][1]=='VBP':
                            print sentence

                elif tagged_sent[currant+2][1]=='VB':
                            print sentence
                else:
                    print('wrong')
                            #future tense
         elif tagged_sent[currant+1][1]=='MD':
                if tagged_sent[currant+2][1]=='VB':
                            print sentence
                elif tagged_sent[currant+2][0]=='not':
                            print(sentence)


         else:
            print('wrong')



  elif [word for word,pos in tagged_sent if pos == 'NNP']:

    noun = [word for word,pos in tagged_sent if pos == 'NNP']
    nouns = noun[0],'NNP'
    #
    currant = tagged_sent.index(nouns)

    if tagged_sent[currant+1][1]=='VBZ':
                print sentence

    elif tagged_sent[currant+1][1]=='RB':
        if tagged_sent[currant+2][1]=='VBZ':
                print sentence

        else:
          print('wrong')
    #past tense
    elif tagged_sent[currant+1][0]=='was':
                 print sentence
    elif tagged_sent[currant+1][1]=='VBD':
                 print sentence
     #future tense
    elif tagged_sent[currant+1][1]=='MD':
          if tagged_sent[currant+2][1]=='VB':
                 print sentence

          elif tagged_sent[currant+2][0]=='not':
                 print(sentence)

    else:
        print 'wrong'


    # #simple present 2




  elif [word for word,pos in tagged_sent if pos == 'NNS']:
    #
    noun = [word for word,pos in tagged_sent if pos == 'NNS']
    nouns = noun[0],'NNS'
    #
    currant = tagged_sent.index(nouns)
    #
    if tagged_sent[currant+1][0]=='do' or tagged_sent[currant+1][0]=='do not' or tagged_sent[currant+1][0]=='don\'t':
           if tagged_sent[currant+2][1]=='VBP' or tagged_sent[currant+2][1]=='VB':
               print(sentence)


           else:
               print 'wrong'

    elif tagged_sent[currant+1][1]=='RB':
        if tagged_sent[currant+2][0]=='do' or tagged_sent[currant+2][0]=='do not' or tagged_sent[currant+2][0]=='don\'t':
              if tagged_sent[currant+3][1]=='VBP' or tagged_sent[currant+3][1]=='VB':
                                                print sentence


        else:
          print('wrong')

    elif tagged_sent[currant+1][0]=='did' or tagged_sent[currant+1][0]=='did not' or tagged_sent[currant+1][0]=='didn\'t':
           if tagged_sent[currant+2][1]=='VB':
               print(sentence)


           else:
            print('wrong')




    else:
        print 'wrong'
  else:
      print('wrong')


###################simple present ##########################################################

########################simple past ###############################################################






###################simple past ##########################################################





