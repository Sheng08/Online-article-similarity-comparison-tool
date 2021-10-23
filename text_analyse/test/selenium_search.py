from selenium import webdriver
from bs4 import BeautifulSoup
import selenium.webdriver.support.ui as ui
import time

from analyse import Analyse
Analyse=Analyse()


def read_txt(path=''):
    f = open(path,'r' , encoding = 'utf8')
    return f.read()
txtsrc=read_txt('./txtsrc/test.txt')
# print(txtsrc)

url='https://www.google.com'
driver=webdriver.Chrome(executable_path='./driver/chromedriver.exe')
driver.get(url)
# wait = ui.WebDriverWait(driver,10)
driver.implicitly_wait(10) # seconds
#time.sleep(1)

# search_input = wait.until(lambda driver:driver.find_element_by_name("q"))
# search_input.send_keys('宜蘭大學')
# #time.sleep(1)
# search_btn = wait.until(lambda driver:driver.find_element_by_name('btnK'))
# search_btn.click()

search_input =driver.find_element_by_name("q")
search_input.send_keys('宜蘭')
#time.sleep(1)
search_btn = driver.find_element_by_name('btnK')
search_btn.click()


#time.sleep(2)#在此等待 使瀏覽器解析並渲染到瀏覽器

html=driver.page_source #獲取網頁內容
soup = BeautifulSoup(html, "html.parser")
search_res_list=soup.select('.yuRUbf')
print(search_res_list)

real_url_list=[]
count = 0
# print(search_res_list)
for el in search_res_list:
    if count <3:
        js = 'window.open("'+el.a['href']+'")'
        driver.execute_script(js)
        handle_this=driver.current_window_handle#獲取當前控制程式碼
        handle_all=driver.window_handles#獲取所有控制程式碼
        handle_exchange=None#要切換的控制程式碼
        for handle in handle_all:#不匹配為新控制程式碼
            if handle != handle_this:#不等於當前控制程式碼就交換
                handle_exchange = handle
        driver.switch_to.window(handle_exchange)#切換
        real_url=driver.current_url
        print("目前網站:", real_url)

        time.sleep(5)
        html_2=driver.page_source
        # print(html_2)
        print('文章相似度：',Analyse.get_Tfidf(txtsrc,html_2))

        real_url_list.append(real_url)#儲存結果
        driver.close()
        driver.switch_to.window(handle_this)
    else:
        break
    count += 1
# print(real_url_list)


