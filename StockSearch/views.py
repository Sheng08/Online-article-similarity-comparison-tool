# -*- coding: utf-8 -*-
from django.shortcuts import redirect, render
from django.http import HttpResponse,HttpResponseRedirect
from django.views.generic import TemplateView
from numpy import split
from StockSearch.forms import HomeForm
from StockSearch.models import Stock_Information
import matplotlib.pyplot as plt
import twstock
import time
import random, json
from django.views.decorators.csrf import csrf_exempt
from django import forms
import os
from djangoproject import settings

from text_analyse.Manage import Manage
from text_analyse.Analyse import Analyse
from text_analyse.FileHandle import FileHandle
file_upload_url = ''

def project(request):
    global file_upload_url
    txtsrc_name = ''
    if request.method == 'GET':
        return render(request,'index.html',locals())
    else:
        if request.POST.get('open_stock_code'):
            response_data ={}
            #爬蟲 文章比對
            white_list=[]#白名单 改針對多筆
            white_list.append(str(request.POST.get('whiteList')))

            #配置信息
            conf={
                'engine':str(request.POST.get('open_stock_code')),
                'target_page':int(request.POST.get('select')),
                'white_list': white_list,
                }

            # response_data = {}
            # response_data['FileName'] = txtsrc_name

            response_data = Manage(conf).get_local_analyse()
            # response_data = {"什麼是演算法": { "http://www.google.com/":100.0, "https://developer.mozilla.org/":30.0,  "https://www.w3schools.com/": 50.0}}
            file = list(FileHandle().get_text().values())

            # print(file[0])
            word_counts, tag = Analyse().Count(file[0])
            # print(tag)
            cutwords = Analyse().Topcount(file[0])
            # print(cutwords[tag[0]])
            response_data['Top'] = tag[0]
            response_data['TopCount'] = cutwords[tag[0]]
            response_data['Top20'] = tag
           
            # response_data = json.loads(response_data)
            print(response_data)

            os.remove(file_upload_url)

            compareResult_json_data = json.dumps(response_data)#转化为Json格式
            return HttpResponse(compareResult_json_data ,content_type='application/json')
        else:
            # if request.FILES.get('file').name:
            #     # uname = request.POST.get('username')
            #     file = request.FILES.get('file') #獲取文件要通過.FILES.get()來獲取文件數據
            #     file_name = file.name
            #     if file_name.split('.')[1]!='txt':
            #         return HttpResponse(json.dumps({"fail":"fileTypeError"}),content_type='application/json')
            #     else:
            #         path = os.path.join(settings.BASE_DIR,'text',file_name)#來拼接文件內路徑
            #         with open(path,'wb')as f:#將文件寫入本地
            #             for i in file:
            #                 f.write(i)
            #         return HttpResponse(json.dumps({"success":"SuccessUpload"}),content_type='application/json')
            file = request.FILES.get('file')  # 获取文件对象，包括文件名文件大小和文件内容
            # if file.name.split('.')[1]!='txt':
            #     return HttpResponse(json.dumps({"fail":"fileTypeError"}),content_type='application/json')
            curttime = time.strftime("%Y-%m-%d")
            # print(curttime)
            #规定上传目录
            upload_url = os.path.join(settings.BASE_DIR,'file_DB',curttime)
            #判断文件夹是否存在
            folder = os.path.exists(upload_url)
            # print(settings.BASE_DIR)

            txtsrc_name = file.name

            if not folder:
                os.makedirs(upload_url)
                print("創建資料夾")
            if file:
                file_name = file.name
                #判断文件是是否重名，懒得写随机函数，重名了，文件名加时间
                if os.path.exists(os.path.join(upload_url,file_name)):
                    name, etx = os.path.splitext(file_name)
                    addtime = time.strftime("%Y-%m-%d-%H-%M-%S")
                    finally_name = name + "_" + addtime + etx
                    #print(name, etx, finally_name)
                else:
                    finally_name = file.name
                #文件分块上传
                upload_file_to = open(os.path.join(upload_url, finally_name), 'wb+')

                for chunk in file.chunks():
                    upload_file_to.write(chunk)
                    # print(chunk)
                upload_file_to.close()

                #返回文件的URl
                file_upload_url = str(settings.BASE_DIR) + '/text_analyse/txtsrc/' + curttime + '/' + str(finally_name)
                print("DB: ", file_upload_url)
                #构建返回值

                
                upload_url = os.path.join(settings.BASE_DIR,'text_analyse','txtsrc')
                if len(os.listdir(upload_url)) != 0:  #判斷資料夾是否為空
                    print("資料夾有檔案")
                    for f in os.listdir(upload_url):
                        os.remove(os.path.join(upload_url, f))
                
                upload_file_to = open(os.path.join(upload_url, txtsrc_name), 'wb+')
                for chunk in file.chunks():
                    upload_file_to.write(chunk)
                upload_file_to.close()
                file_upload_url = str(settings.BASE_DIR) + '/text_analyse/txtsrc/'+ str(txtsrc_name)
                print("txtsrc: ", file_upload_url)
                
                response_data = {}
                response_data['FileName'] = txtsrc_name
                response_data['FileUrl'] = file_upload_url
                response_json_data = json.dumps(response_data)#转化为Json格式
                
               



                # #爬蟲 文章比對
                # white_list=[]#白名单
                # #配置信息
                # conf={
                #     'engine':'google',
                #     'target_page':1,
                #     'white_list': white_list,
                #     }

                # print(Manage(conf).get_local_analyse())

                return HttpResponse(response_json_data ,content_type='application/json')

    return HttpResponse(json.dumps({"null":"noWorking"}),content_type='application/json')
# @csrf_exempt
# def stock(request):
#     if request.method=="GET":    
        
#         return render(request,'stock.html',locals())

#     else:
#         # print(request.body)  # 原始的请求体数据
#         # print ("AA", request.POST.get('open_stock_code'))
#         # print ("AA", request.POST.get('date'))
#         # print ("AA", request.POST.get('stock_name'))
#         if request.POST.get('stock_name'):
            
#             try:
#                 text = request.POST.get('stock_name')
#                 text = int(text)
#                 text = str(text)
#             except:
#                 for i in twstock.codes:
#                     if twstock.codes[i].name==text:
#                         text = str(i)
#                         break
#             try:
#                 stock1 = twstock.realtime.get(text)
#                 # print(stock1)
#                 # print(request.POST.get('open_stock_code'))
#                 # print(request.POST.get('month'))
#                 real_search_time = stock1['info']['time']
#                 code = stock1['info']['code']
#                 name = stock1['info']['name']
#                 fullname = stock1['info']['fullname']
#                 best_bid_price = [i.split('.')[0] for i in stock1['realtime']['best_bid_price']]
#                 best_bid_volume = [i.split('.')[0] for i in stock1['realtime']['best_bid_volume']]
#                 best_ask_price = [i.split('.')[0] for i in stock1['realtime']['best_ask_price']]
#                 best_ask_volume = [i.split('.')[0] for i in stock1['realtime']['best_ask_volume']]
#                 open = stock1['realtime']['open'].split('.')[0]
#                 high = stock1['realtime']['high'].split('.')[0]
#                 low = stock1['realtime']['low'].split('.')[0]
#                 # print(best_bid_price)
#                 # print(stock1)
#                 # f = 123
#                 # payload='{"fuck":{0}}'.format(123)
#                 # print(payload)
#                 # print(json.dumps(best_ask_volume))
#                 payload = '"real_search_time":"{}", "code":"{}", "name":"{}", "fullname":"{}", "best_bid_price":{}, "best_bid_volume":{}, "best_ask_price":{}, "best_ask_volume":{}, "open":"{}", "high":"{}", "low":"{}"'.format(real_search_time, code, name, fullname,json.dumps(best_bid_price) ,json.dumps(best_bid_volume) ,json.dumps(best_ask_price) ,json.dumps(best_ask_volume) , open, high, low)
#                 payload='{'+payload+'}'
#                 # print(payload)
#                 payload = json.loads(payload)
#                 print(payload)
#                 return HttpResponse(json.dumps(payload),content_type='application/json' )
#             except KeyError as e:
#                 print(e)
#                 return HttpResponse(json.dumps({"error":"stockInfoError"}),content_type='application/json' )
#             except Exception as e:
#                 print(e)
#                 return HttpResponse(json.dumps({"error":"UnkownError"}),content_type='application/json' )

#         # 如何一次判斷是否成功拿到form 不用多個判斷 有按鈕動作??
#         if  request.POST.get('open_stock_code') and request.POST.get('year'):
#                 # print(request.POST.get('open_stock_code'))
#                 # print(request.POST.get('year'))

#                 open_stock_code = str(request.POST.get('open_stock_code'))
#                 year = request.POST.get('year')

#                 year_day=[]
#                 year_open=[]
#                 year_high=[]
#                 year_low=[]
#                 year_close=[]
#                 year_set = Stock_Information.objects.filter(stock_code = open_stock_code, stock_year = year)
#                 for i in year_set:
#                     print('year_set:', i.stock_code, i.stock_year, i.stock_month, i.stock_day, i.stock_open, i.stock_high, i.stock_low, i.stock_close)
#                     year_day.append(str(i.stock_year)+'-'+str(i.stock_month)+'-'+str(i.stock_day))
#                     year_open.append(str(i.stock_open))
#                     year_high.append(str(i.stock_high))
#                     year_low.append(str(i.stock_low))
#                     year_close.append(str(i.stock_close))
#                 # print(year_day)
#                 # best_ask_volume = year_day
#                 # low = 'sdasdsa'
#                 # print(low)
#                 # return render(request,'stock.html',locals())
#                 payload = '"day":{}, "open":{}, "high":{}, "low":{}, "close":{}'.format(json.dumps(year_day) ,json.dumps(year_open),json.dumps(year_high),json.dumps(year_low),json.dumps(year_close))
#                 payload='{'+payload+'}'
#                 # print(payload)
#                 payload = json.loads(payload)
#                 # print(payload)
#                 return HttpResponse(json.dumps(payload),content_type='application/json' )

#         elif  request.POST.get('open_stock_code') and request.POST.get('month'):
#                 # print(request.POST.get('open_stock_code'))
#                 # print(request.POST.get('month'))

#                 open_stock_code = str(request.POST.get('open_stock_code'))
#                 date = request.POST.get('month')
#                 # print()
#                 year = date.split('-')[0]
#                 month = date.split('-')[1] #能用str to datetime

#                 month_day=[]
#                 month_open=[]
#                 month_high=[]
#                 month_low=[]
#                 month_close=[]

#                 month_set = Stock_Information.objects.filter(stock_code = open_stock_code, stock_year = year, stock_month = month)
#                 # print(month_set)
#                 for i in month_set:
#                     print('month_set:', i.stock_code, i.stock_year, i.stock_month, i.stock_day, i.stock_open)
#                     month_day.append(str(i.stock_year)+'-'+str(i.stock_month)+'-'+str(i.stock_day))
#                     month_open.append(str(i.stock_open))
#                     month_high.append(str(i.stock_high))
#                     month_low.append(str(i.stock_low))
#                     month_close.append(str(i.stock_close))
#                 payload = '"day":{}, "open":{}, "high":{}, "low":{}, "close":{}'.format(json.dumps(month_day) ,json.dumps(month_open),json.dumps(month_high),json.dumps(month_low),json.dumps(month_close))
#                 payload='{'+payload+'}'
#                 # print(payload)
#                 payload = json.loads(payload)
#                 return HttpResponse(json.dumps(payload),content_type='application/json' )

#         # if request.POST.get('open_type'):

#         #     # open_stock_type = ['6180(橘子)','2317(鴻海)','3008(大立光)','2330(台積電)','2886(兆豐金)','2002(中鋼)','3260(威剛)','2603(長榮)','2377(微星)','2609(陽明)']
#         #     open_stock_type = ['6180','2317','3008','2330','2886','2002','3260','2603','2377','2609']
#         #     if request.POST.get('open_type')=='year':
#         #         open_year = ['2020','2021']
#         #         open_type_select = "年開盤"
#         #     else:
#         #         open_year = ['2020','2021']
#         #         open_month = list([i for i in range(1,13)])
#         #         open_type_select = "月開盤"
    
#         # if  request.POST.get('open_stock_year2') and request.POST.get('open_stock_month') and request.POST.get('open_stock_code'):

#         #         year_day=[]
#         #         year_open=[]
#         #         set1 = Stock_Information.objects.filter(stock_code = str(request.POST.get('open_stock_code')), stock_year = str(request.POST.get('open_stock_year2')), stock_month = str(request.POST.get('open_stock_month')))
#         #         print(set1)
#         #         for i in set1:
#         #             print('set1:',i.stock_code,i.stock_year,i.stock_month,i.stock_day,i.stock_open)
#         #             year_day.append(str(i.stock_year)+'-'+str(i.stock_month)+'-'+str(i.stock_day))
#         #             year_open.append(str(i.stock_open))

#         #         # plt.style.use("ggplot")

#         #         # plt.figure(figsize=(250,200))
#         #         # plt.xticks(rotation=45,fontsize=10)

#         #         # plt.plot(year_day,year_open,'s-',color = 'r')

#         #         # plt.xlabel("time", fontsize='20')
#         #         # plt.ylabel("price", fontsize='20')
#         #         # plt.title(str(i.stock_year)+"年開盤走勢圖", fontproperties="SimSun", fontsize='30') 

#         #         # plt.legend(loc = "best", fontsize=20)
                
#         # elif request.POST.get('open_stock_year1') and request.POST.get('open_stock_code'):

#         #         month_day=[]
#         #         month_open=[]
#         #         set2 = Stock_Information.objects.filter(stock_code = str(request.POST.get('open_stock_code')), stock_year = str(request.POST.get('open_stock_year1')))
#         #         for i in set2:
#         #             print('set2:',i.stock_code,i.stock_year,i.stock_month,i.stock_day,i.stock_open)
#         #             month_day.append(str(i.stock_year)+'-'+str(i.stock_month)+'-'+str(i.stock_day))
#         #             month_open.append(str(i.stock_open))
                
#         #         plt.style.use("ggplot")

#         #         plt.figure(figsize=(250,200))
#         #         plt.xticks(rotation=45,fontsize=10)

#         #         plt.plot(month_day, month_open,'s-',color = 'r')

#         #         plt.xlabel("time", fontsize='20')
#         #         plt.ylabel("price", fontsize='20')
#         #         plt.title(str(i.stock_year)+"年"+str(i.stock_month)+"月開盤走勢圖", fontproperties="SimSun", fontsize='30') 

#         #         plt.legend(loc = "best", fontsize=20)
#         #         plt.show()
                
#         # return render(request,'stock.html',locals())