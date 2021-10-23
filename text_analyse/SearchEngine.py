#搜尋引擎配置
class EngineConfManage:
    def get_Engine_conf(self,engine_name):
        if engine_name=='google':
            return GoogleEngineConf()

class EngineConf:
    def __init__(self):
        self.engineConf={}
    def get_conf(self):
        return self.engineConf

class GoogleEngineConf(EngineConf):
    engineConf={}
    def __init__(self):
        self.engineConf['searchTextID']='q'
        self.engineConf['searchBtnID']='btnK'
        # self.engineConf['nextPageBtnID_xpath_f']='//*[@id="page"]/div/a[10]'
        # self.engineConf['nextPageBtnID_xpath_s']='//*[@id="page"]/div/a[11]'
        self.engineConf['nextPageBtnID']='pnnext'
        self.engineConf['searchContentHref_class']='yuRUbf'
        self.engineConf['website']='https://www.google.com'