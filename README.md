## LAVI's Fine-Tune OpenAI Model Side Project
###### tags: `Side Project` `OpenAI API` `pytesseract` `LAVI` `2023` 
[Fine-Tune OpenAI](https://platform.openai.com/docs/guides/fine-tuning/fine-tuning) davinci model with pytesseract

## Information
### Summary
- 利用 Python 套件 pytesseract 進行影像文字分析後，將字串處理為可提供給 OpenAI GPT-3 model prompt 的語句形式
- 進行 OpenAI model 訓練，使訓練出的模型可根據訓練資料回答資訊

### Details
#### 1. 預處理
- 將 OpenAI API key 放進系統環境變數
- 將想 text detection 的圖片放好後，修改程式中讀取圖片的路徑
- pytesseract 套件預設提取英文字，故需下載繁體中文包 (放在 Program Files\Tesseract-OCR 中讀取)

#### 2. pytesseract 讀取圖片後進行字串處理
- 利用 PIL 的 `pytesseract.image_to_string` 讀取指定圖片上的文字內容，語言使用 chi_tra (繁體中文)
- 用 replace 將讀取的不必要空白取代，並對整體文字內容進行 split 切割成獨立字串

#### 3. OpenAI 模型訓練
- 將處理好的字串進行 jieba 切割
    - 因為 OpenAI 讀取關鍵字時難以正確判斷中文字串語意，可利用 jieba 斷詞器對字串進行權重切割，可另 OpenAI 模型更好的對關鍵詞進行訓練
- 利用 `prompt = f"{prevPrompt}\n{prevAns}\n###\n{oriprompt}"` 使上一筆的查詢與結果可影響當前的輸入訓練結果，使各筆輸出結果判斷越漸相似
- 利用 `openai.Completion.create()` 對 OpenAI davinci model 進行訓練

#### 4. 整理收到的回應與每筆輸出資訊
- 利用 pandas 中 `pd.concat` 將每筆資訊整合

#### 5. 儲存整理好的資訊
- 利用 `df.to_csv("TrainingModel.csv", encoding="utf_8_sig")` 將資訊輸出成 `.csv` 檔案

#### 6. OpenAI Fine-Tune model 資料預處理
- Fine-Tune mode 指定訓練資料欄位名稱為：`prompt`、`completion`
- 調整好欄位資訊後輸出成 `.csv` 檔案
    - OpenAI 官方文件說可以提供 `.csv` 檔，而他在 Fine-Tune 你的模型時會將其轉為 `.jsonl` 格式

#### 7. Fine-Tune Training Command
- `openai tools fine_tunes.prepare_data -f <LOCAL_FILE>`
    - 讀取 `preparedData.csv` 為我的 fine_tune prepare data
- `openai api fine_tunes.create -t <TRAIN_FILE_ID_OR_PATH> -m <BASE_MODEL>`
    - 利用 prepare data 生成一個 `.jsonl` 檔案後利用其和 davinci model 進行 fine-tune 訓練
- `openai api fine_tunes.follow -i <YOUR_FINE_TUNE_JOB_ID>`
    - 查看我目前模型訓練的進度
    - 看你的 model 排隊進 queue 裡被訓練了沒，可能會花 30 min 到 1 hr 不等
    
#### 8. 測試模型訓練完的結果
- 進到 [OpenAI playground](https://platform.openai.com/playground) 後選擇你的 Fine-Tune 模型
- 在僅輸入 keyword 的前提下，輸出會與你的 Training Dataset 相似邏輯

## Reference
- [iThome 圖片轉文字 OCR 圖片字元辨識](https://ithelp.ithome.com.tw/articles/10289536)
- [iThome 聽過 OCR 嗎? 實作看看吧 -- pytesseract](https://ithelp.ithome.com.tw/articles/10227263)
- [Tesseract 使用＆安裝＆訓練](https://hackmd.io/@DCT/Tesseract-OCR-%E6%96%87%E5%AD%97%E8%BE%A8%E8%AD%98)
- [Python自然語言處理(二)：使用jieba進行中文斷詞](https://yanwei-liu.medium.com/python%E8%87%AA%E7%84%B6%E8%AA%9E%E8%A8%80%E8%99%95%E7%90%86-%E4%BA%8C-%E4%BD%BF%E7%94%A8jieba%E9%80%B2%E8%A1%8C%E4%B8%AD%E6%96%87%E6%96%B7%E8%A9%9E-faf7828141a4)
- [Python - 知名 Jieba 中文斷詞工具教學](https://blog.kennycoder.io/2020/02/12/Python-%E7%9F%A5%E5%90%8DJieba%E4%B8%AD%E6%96%87%E6%96%B7%E8%A9%9E%E5%B7%A5%E5%85%B7%E6%95%99%E5%AD%B8/)
- [OpenAI Prepare training data](https://platform.openai.com/docs/guides/fine-tuning/prepare-training-data)
