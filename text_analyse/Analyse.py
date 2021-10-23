from jieba import lcut
from jieba import cut_for_search
import jieba.analyse
import collections
from text_analyse.FileHandle import FileHandle

class Analyse:
    def get_Tfidf(self,text1,text2):
        # self.correlate.word.set_this_url(url)
        T1, tag1 = self.Count(text1)
        T2, tag2 = self.Count(text2)
        mergeword = self.MergeWord(T1,T2)
        return self.cosine_similarity(self.CalVector(T1,mergeword),self.CalVector(T2,mergeword))
        
    #分詞
    def Count(self,text):
        tag = jieba.analyse.textrank(text,topK=20)
        word_counts = collections.Counter(tag)
        return word_counts, tag
    #合并
    def MergeWord(self,T1,T2):
        MergeWord = []
        for i in T1:
            MergeWord.append(i)
        for i in T2:
            if i not in MergeWord:
                MergeWord.append(i)
        return MergeWord
    # 得出向量
    def CalVector(self,T1,MergeWord):
        TF1 = [0] * len(MergeWord)
        for ch in T1:
            TermFrequence = T1[ch]
            word = ch
            if word in MergeWord:
                TF1[MergeWord.index(word)] = TermFrequence
        return TF1
    #TF-IDF
    def cosine_similarity(self,vector1, vector2):
        dot_product = 0.0
        normA = 0.0
        normB = 0.0

        for a, b in zip(vector1, vector2):
            dot_product += a * b    
            normA += a ** 2
            normB += b ** 2
        if normA == 0.0 or normB == 0.0:
            return 0
        else:
            return round(dot_product / ((normA**0.5)*(normB**0.5))*100, 2)

    def Topcount(self, text):
        seg_list = cut_for_search(text)
        seg_list = [word for word in seg_list]

        cutwords = dict(collections.Counter(seg_list))
        # outputwords = {} 
        # for k, v in cutwords.items(): 
        #     if k in outputwords.keys(): 
        #         outputwords[k] += v 
        #     else: outputwords[k] = v 
        # outputwords_sorted = sorted(outputwords.items(), key= lambda x : x[1], reverse=True)[:21] 
        ## print outputwords_sorted ## 使輸出能正常顯示中文字元 
        # print(repr(outputwords_sorted).decode('unicode-escape')) 
        # print "" 
        # print np.shape(outputwords_sorted) 
        return cutwords