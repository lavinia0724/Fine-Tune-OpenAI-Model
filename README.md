## LAVI's Fine-Tune OpenAI Model Code

## Info
- 利用 Python 套件 pytesseract  進行影像文字分析後，進行字串處理調整為可提供給 OpenAI GPT-3 model prompt 的詢問語句，並進行 OpenAI model 訓練，使訓練出的模型可根據訓練資料回答資訊

### OpenAI model Training instruction
- `openai tools fine_tunes.prepare_data -f <LOCAL_FILE>`
- `openai api fine_tunes.create -t <TRAIN_FILE_ID_OR_PATH> -m <BASE_MODEL>`
- `openai api fine_tunes.follow -i <YOUR_FINE_TUNE_JOB_ID>`

## Reference
- [Day 12 圖片轉文字 OCR 圖片字元辨識](https://ithelp.ithome.com.tw/articles/10289536)
- [Python自然語言處理(二)：使用jieba進行中文斷詞](https://yanwei-liu.medium.com/python%E8%87%AA%E7%84%B6%E8%AA%9E%E8%A8%80%E8%99%95%E7%90%86-%E4%BA%8C-%E4%BD%BF%E7%94%A8jieba%E9%80%B2%E8%A1%8C%E4%B8%AD%E6%96%87%E6%96%B7%E8%A9%9E-faf7828141a4)
- [OpenAI Prepare training data](https://platform.openai.com/docs/guides/fine-tuning/prepare-training-data)
