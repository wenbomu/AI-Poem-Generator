import random
import re
import os
import time
import json
import random
import g4f

# Get the rhyme of a Chinese character
def getRhyme(character: str) -> str:

  fname = "韵表.txt"

  f = open(fname, "r")

  yundict = {"X": "未知"}
  pzdict = {"X": "未知"}
  pzstate = "Ping"
  yunstate = "未知"
  line = f.readline().strip()
  while (line):
    if line == "Ping" or line == "Shang" or line == "Qu":
      pzstate = line
    elif len(line) >= 4:
      yunstate = line
    else:
      # Here line is a character
      yundict.update({line: yunstate})
      pzdict.update({line: pzstate})
    line = f.readline().strip()

  return yundict[character]



# Decide a rhyme
def decideARhyme() -> str:
  fname = "韵脚.txt"

  f = open(fname, "r")
  rhymes = []
  line = f.readline().strip()
  while (line):
    rhymes.append(line)
    line = f.readline().strip()

  return rhymes[random.randint(0, len(rhymes) - 1)]



# Get a template of a Song Ci
def getTemplate(cipai: str):

  fname = cipai + ".txt"

  f = open(fname, "r")

  cipaitemplate = []
  line = f.readline().strip()
  line = f.readline().strip()
  while (line):
    paragraph = re.split('，|、|。|！|？', line)
    template = [len(i) for i in paragraph]
    cipaitemplate.append(template)
    line = f.readline().strip()

  return cipaitemplate

# Get string materials of a topic
def getMaterials(sentences: str):

  sentenceDict = {3:["XXX"],4:["XXXX"],5:["XXXXX"],6:["XXXXXX"],7:["XXXXXXX"],8:["XXXXXXXX"],9:["XXXXXXXXX"]}
  lines = sentences.split('\n')
  for line in lines:
    shortSentences = re.split('，|、|。|！|？｜. | |：', line)
    print(shortSentences)
    for sentence in shortSentences:
      sentence = sentence.strip() 
      if (len(sentence) > 2 and len(sentence) < 10):
        sentenceDict.get(len(sentence)).append(sentence)
  return sentenceDict

cipai = input(f"输入你想要生成的宋词词牌: ")
keyword = input(f"输入你想要生成的宋词关键词: ")
template = getTemplate(cipai)

# Get response from chatGPT about poems with a certain topic
response = g4f.ChatCompletion.create(model=g4f.models.gpt_4, provider=g4f.Provider.GetGpt, messages=[
                                     {"role": "user", "content": "生成关于" + keyword + "的宋词，词牌为" + cipai + "，生成3首"}]) 
response += g4f.ChatCompletion.create(model=g4f.models.gpt_4, provider=g4f.Provider.GetGpt, messages=[
                                     {"role": "user", "content": "生成关于" + keyword + "的宋词，生成3首"}]) 
response += g4f.ChatCompletion.create(model=g4f.models.gpt_4, provider=g4f.Provider.GetGpt, messages=[
                                     {"role": "user", "content": "生成关于" + keyword + "的唐诗，生成3首"}]) 
sentenceDict = getMaterials(response)
print(sentenceDict)

# Decide a rhyme

rhyme = decideARhyme()

# Start to write Songci

print(getRhyme("李"))

output = ""
fname = cipai + ".txt"
f = open(fname, "r")
line = f.readline().strip()
output += line + "\n"
line = f.readline().strip()
while (line):
  paragraph = re.split('。|！|？', line)
  for subTemplate in paragraph:
    shortTemplate = re.split('，|、', subTemplate)
    for j in range(len(shortTemplate)):
      shortSentence = shortTemplate[j]
      if (len(shortSentence) < 2):
        continue
      sentencePool = sentenceDict.get(len(shortSentence))
      if (j < len(shortTemplate) - 1):    
        thisSentence = sentencePool[random.randint(0, len(sentencePool) - 1)]
        output += thisSentence + "，"
      else:
        tryNumber = 0
        while(tryNumber < 100):
          thisSentence = sentencePool[random.randint(0, len(sentencePool) - 1)]
          tryNumber = tryNumber + 1
          if(getRhyme(thisSentence[len(thisSentence)-1:]) == rhyme):
            output += thisSentence + "。"
            break
  line = f.readline().strip()

print(output)
