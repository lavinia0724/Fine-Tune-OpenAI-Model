import os
import jieba
import openai
import pytesseract
import pandas as pd

from PIL import Image
from pathlib import Path

openai.api_key = os.getenv("OPENAI_API_KEY")
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

pathlist = Path("C:\\Users\\momia\\Downloads\\pytesseract").glob('**/*.jpg')
# config = r'-c tessedit_char_blacklist= --psm 6'

prevPrompt = ''
prevAns = ''

# openai api fine_tunes.create -t "C:\Users\momia\Downloads\pytesseract\main.py" -m davinci

df = pd.DataFrame()  

for fontPath in pathlist:
  # print(fontPath)
  
  basename = os.path.splitext(os.path.basename(fontPath))[0]
  print('basename: ' + basename)

  # if not os.path.isdir(basename):
  #   os.mkdir(basename)  

  img = Image.open(f'{basename}.jpg')
  text = pytesseract.image_to_string(img, lang='chi_tra')
  # print(text)
  text = text.replace(' ', '')
  text = text.split('\n')

  for item in text[5:15]:
    if item == '' :
      continue
    # print(item)

    sentence = jieba.cut(item)
    sentence = (' '.join(sentence))
    print(sentence)
    sentence = sentence.replace(':', '熱量為')
    sentence = sentence.replace(';', '熱量為')
    # print()

    oriprompt = f"{sentence} 請在 20 字內說明要花多少時間運動才能消耗此熱量"
    # print(oriprompt)
    prompt = f"{prevPrompt}\n{prevAns}\n###\n{oriprompt}"
    print(prompt)
    response = openai.Completion.create(
      model="text-davinci-003",
      prompt=prompt,
      temperature=1,
      max_tokens=500,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0,
      stop=["###"]
    )
    # print(response)

    finish_reason = response['choices'][0]['finish_reason']
    responseText = response['choices'][0]['text']

    print(responseText)

    prevPrompt = oriprompt
    prevAns = responseText

    newRow = {
      'item':item, 
      'sentence':sentence, 
      'prompt':oriprompt, 
      'responseText':responseText, 
      'finish_reason':finish_reason}
    newRow = pd.DataFrame([newRow])
    df = pd.concat([df, newRow], axis=0, ignore_index=True)

df.to_csv("TrainingModel.csv", encoding="utf_8_sig")
df = pd.read_csv("TrainingModel.csv")

prepared_data = df.loc[:,['sentence','responseText']]
prepared_data.rename(columns={'sentence':'prompt', 'responseText':'completion'}, inplace=True)
prepared_data.to_csv('preparedData.csv', encoding="utf_8_sig", index=False)