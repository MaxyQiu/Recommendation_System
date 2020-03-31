from bs4 import BeautifulSoup
from fileinput import filename
import re
import os
import string
import nltk
from nltk.tokenize import RegexpTokenizer
import json

tokenizer = RegexpTokenizer(r'\w+[\-]?\w+')





def block_construction(NUM):
  allblocks=[]
  block={}#key:documentID value:article
  flag=0
  emptycount=0

  # extract all the text to form blocks
  for filenum in range(1,NUM+1):
    flag+=1
    if flag <500:

      F= str(filenum)
      if os.path.getsize('/Users/maxyqiu/Desktop/IR&WebSearch/Research_Analysis_System/CrawledFiles/'+F+'.json'):
       with open('/Users/maxyqiu/Desktop/IR&WebSearch/Research_Analysis_System/CrawledFiles/'+F+'.json','r', errors='ignore') as f:
         print("now is F"+F)
         data=json.load(f)

        # read all data in F
         keys=data.keys()
         for key in keys:
           word_list=data[key]
         token_list=[]
         for num in range(0,len(word_list)):
            tokens=tokenizer.tokenize(word_list[num])
            for token in tokens:
                token= token.lower()
            token_list = token_list + (tokens.copy())

            tokens.clear()

         block[key]=token_list
      else:
       emptycount+=1

    else:
        flag=0
        allblocks.append(block.copy())
        print("now append a new block")
        block.clear()


  print("there is "+str(emptycount)+"files")
  return allblocks

def block_construction_nonduplicated(NUM):
    allblocks = []
    block = {}  # key:documentID value:article
    flag = 0
    emptycount = 0

    # extract all the text to form blocks
    for filenum in range(1, NUM + 1):
        flag += 1
        if flag < 500:

            F = str(filenum)
            if os.path.getsize(
                    '/Users/maxyqiu/Desktop/IR&WebSearch/Research_Analysis_System/CrawledFiles/' + F + '.json'):
                with open('/Users/maxyqiu/Desktop/IR&WebSearch/Research_Analysis_System/CrawledFiles/' + F + '.json',
                          'r', errors='ignore') as f:
                    print("now is F" + F)
                    data = json.load(f)

                    # read all data in F
                    keys = data.keys()
                    for key in keys:
                        word_list = data[key]
                    token_list=[]
                    for num in range(0, len(word_list)):
                        tokens = tokenizer.tokenize(word_list[num])
                        if(len(tokens)>0):
                         token_list=token_list+(tokens.copy())
                         tokens.clear()
                    print(token_list)
                    token_list = list(dict.fromkeys(token_list))
                    block[key] = token_list
            else:
                emptycount += 1

        else:
            flag = 0
            allblocks.append(block.copy())
            print("now append a new block")
            block.clear()

    print("there is " + str(emptycount) + "files")
    return allblocks


def block_construction_AInonduplicated(NUM):
    allblocks = []
    block = {}  # key:documentID value:article
    flag = 0
    emptycount = 0

    # extract all the text to form blocks
    for filenum in range(1, NUM + 1):
        flag += 1
        if flag < 500:

            F = str(filenum)
            if os.path.getsize(
                    '/Users/maxyqiu/Desktop/IR&WebSearch/Research_Analysis_System/AICrawledFiles/' + F + '.json'):
                with open('/Users/maxyqiu/Desktop/IR&WebSearch/Research_Analysis_System/AICrawledFiles/' + F + '.json',
                          'r', errors='ignore') as f:
                    print("now is F" + F)
                    data = json.load(f)

                    # read all data in F
                    keys = data.keys()
                    for key in keys:
                        word_list = data[key]
                    token_list=[]
                    for num in range(0, len(word_list)):
                        tokens = tokenizer.tokenize(word_list[num])
                        if(len(tokens)>0):
                         token_list=token_list+(tokens.copy())
                         tokens.clear()
                    print(token_list)
                    token_list = list(dict.fromkeys(token_list))
                    block[key] = token_list
            else:
                emptycount += 1

        else:
            flag = 0
            allblocks.append(block.copy())
            print("now append a new block")
            block.clear()

    print("there is " + str(emptycount) + "empty files")
    return allblocks









