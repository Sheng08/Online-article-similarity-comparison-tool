from text_analyse.Manage import Manage

white_list=[]#白名单
#配置信息
conf={
       'engine':'google',
       'target_page':1,
       'white_list': white_list,
    }

print(Manage(conf).get_local_analyse())