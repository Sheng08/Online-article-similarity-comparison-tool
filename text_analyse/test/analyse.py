from jieba import lcut
import jieba.analyse
import collections

class Analyse:
    def get_Tfidf(self,text1,text2):#測試對比本地資料對比搜尋引擎方法
        # self.correlate.word.set_this_url(url)
        T1 = self.Count(text1)
        T2 = self.Count(text2)
        mergeword = self.MergeWord(T1,T2)
        return self.cosine_similarity(self.CalVector(T1,mergeword),self.CalVector(T2,mergeword))
        
    #分詞
    def Count(self,text):
        tag = jieba.analyse.textrank(text,topK=20)
        word_counts = collections.Counter(tag) #計數統計
        return word_counts
    #詞合併
    def MergeWord(self,T1,T2):
        MergeWord = []
        for i in T1:
            MergeWord.append(i)
        for i in T2:
            if i not in MergeWord:
                MergeWord.append(i)
        return MergeWord
    # 得出文件向量
    def CalVector(self,T1,MergeWord):
        TF1 = [0] * len(MergeWord)
        for ch in T1:
            TermFrequence = T1[ch]
            word = ch
            if word in MergeWord:
                TF1[MergeWord.index(word)] = TermFrequence
        return TF1
    #計算 TF-IDF
    def cosine_similarity(self,vector1, vector2):
        dot_product = 0.0
        normA = 0.0
        normB = 0.0

        for a, b in zip(vector1, vector2):#兩個向量組合成 [(1, 4), (2, 5), (3, 6)] 最短形式表現
            dot_product += a * b    
            normA += a ** 2
            normB += b ** 2
        if normA == 0.0 or normB == 0.0:
            return 0
        else:
            return round(dot_product / ((normA**0.5)*(normB**0.5))*100, 2)