# Online-article-similarity-comparison-tool

### 作品介紹
此作品為五人共同完成，此系統以四大功能整合而成，分別為資料收集與擷取、文本資料前處理、核心演算法以及介面開發。可提供使用者比對自己所撰寫的部落格文章是否被抄襲或盜用，透過文本分析的方法結合Google搜尋引與爬蟲技術。使用關鍵字自動化地找出與原文章類似的文章且做出相似度比較與進行排名，使用者亦可點選比對結果連結查看網站，並結合前端網頁設計以視覺化的方式呈現對比結果。

###  本作品中，我撰寫了以下主要功能：
>1.	針對文章進行Jieba斷詞
>2.	利用TextRank與tf-idf進行關鍵字提取
>3.	使用餘弦相似度比對文章相似程度
>4.	使用WebDrive與Selenium進行自動化網頁爬蟲並配合BeautifulSoup解析HTML碼，
擷取線上文章
>5.	使用Django、RWD、Ajax、Bootstrap、Chart.js等完成前端網頁
>6.	將成果部屬至Ngrok供使用者使用

### Run Code：
```
git clone https://github.com/Sheng08/Online-article-similarity-comparison-tool.git
cd Online-article-similarity-comparison-tool
python manage.py runserver
``` 

###  成果截圖：
線上文章相似度比較系統-主頁面<br>
![1](https://user-images.githubusercontent.com/58781800/140347158-0e4a34f7-c52a-49c0-9a42-3ed60a498586.png)
