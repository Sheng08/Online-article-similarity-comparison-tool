from text_analyse.Browser import BrowserManage
from text_analyse.Analyse import Analyse
from text_analyse.FileHandle import FileHandle

class Manage:
    def __init__(self,conf):
        self.drvier=BrowserManage(conf)
        self.textdic=FileHandle().get_text()
        self.analyse=Analyse()
    def get_local_analyse(self):    
        resdic={}
        # print(self.textdic)
        for g in self.textdic:
            res={}
            # print("g", g)
            # for迴圈遍立dict會只有key值留存 為甚麼
            self.drvier.set_(g)
            url_content=self.drvier.search()#获取搜索结果及内容
            # print(url_content)
            for g1 in url_content:
                res[g1]=self.analyse.get_Tfidf(self.textdic[g],url_content[g1])
            resdic[g]=res
        return resdic