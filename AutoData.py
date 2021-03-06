# -*- coding: utf-8 -*-
# @Time    : 2019.11.11
# @Author  : yaosichao
# @Email ：yaosichao0915@163.com
# @Github：https://github.com/yaosichao0915/AmazonWorkSheet/
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import calendar,datetime
import time,os,shutil,sys,re
import glob
import pandas as pd
Destination=str(os.getcwd())
TempFolder=Destination+"\\temp"
path_dir=str(os.path.dirname(os.path.abspath(__file__)))
class AmazonWorksheet():
    def __init__(self,ID,Date,driver,new_name):
        self.ID=ID
        self.Date=Date
        self.driver = driver
        self.new_name=new_name
    def rename_file(self,file):
        '''
        Move and rename the file into the specific directory
        file:str
            file name of the file 
        '''
        dst="%s\\%s"%(Destination,self.ID)
        if not os.path.exists(dst):
            os.makedirs(dst)
        shutil.move("%s\\%s"%(TempFolder,file), "%s\\%s.csv"%(dst,self.new_name))
        return 0
        
    def download_wait(self, directory, timeout, nfiles=None):
        """
        Wait for downloads to finish with a specified timeout.

        Args
        ----
        directory : str
            The path to the folder where the files will be downloaded.
        timeout : int
            How many seconds to wait until timing out.
        nfiles : int, defaults to None
            If provided, also wait for the expected number of files.

        """
        seconds = 0
        dl_wait = True
        while dl_wait and seconds < timeout:
            time.sleep(1)
            dl_wait = False
            files = os.listdir(directory)
            #print(files)
            if nfiles and len(files) != nfiles:
                dl_wait = True

            for fname in files:
                if fname.endswith('.crdownload'):
                    dl_wait = True
            seconds += 1
        if os.listdir(directory)!=[]:
            if (self.rename_file(os.listdir(directory)[0])==0):
                return seconds
            else: 
                print("Rename Error")
                return -1
        else:
            print("download failed")
            return -1

    def GrabThePage(self,url):    
        '''
        Page directing ,simulated click and invoke download function 
        url: str
            whole absolute url to the page to download the report
        '''
        starttime=time.time()
        self.driver.get("https://www.baidu.com") #to make sure it did jump
        self.driver.get(url)
        try: 
            element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="downloadCSV"]'))  #check the existence of button
            )
        except:
            print ("fail to locate downloadCSV, plz check both the webpage and script")
            input("Enter to exit")
            quit() 
            
        print("page loading sucess")
        time.sleep(1)                                                     #wait to be clickable
        for i in range(10):                                               #give time for retries due to bad connections
            try:
                self.driver.find_element_by_id("export").click()          #had to click export first then downloadcsv
                self.driver.find_element_by_id("downloadCSV").click()     #click may be wrong if the scale of chrome is not set at 100% 
            except:
                print("waiting to be clickable %s seconds"%(i+1))
                time.sleep(1)
                continue
            break
                
        print("Now downloading %s for the date of %s"%(self.ID,self.Date[0][:7]))
        time.sleep(5)
        duration = self.download_wait('%s'%TempFolder,20)
        print("downloaded and renamed,taking time of %s"%duration)
            

    
if __name__ == '__main__':
    def pickmonthgap(monthgap):
        '''
        Process the date inputed to be suitbable format and time gap
        monthgap: str
            such as '201901-201902'
        '''
        DateList=[]
        month_begin=monthgap.split('-')[0]
        month_end=monthgap.split('-')[1]
        year_begin=monthgap.split('-')[0][:4]
        year_end=monthgap.split('-')[1][:4]
        current_date = str(datetime.date.today())
        for y in range(int(year_begin),int(year_end)+1):
            for m in range(1,13):
                wday,monthRange = calendar.monthrange(y,m)
                day_begin = '%d-%02d-01' % (y,m)
                day_end = '%d-%02d-%02d' % (y,m,monthRange)
                if month_begin<=day_begin[:7].replace('-','')<=month_end and day_end<current_date:
                    DateList.append([day_begin,day_end])       #upto today time gap
        return (DateList)
        
    def date_format(Date,lang):     
        '''
        Formating the Date due to language used
        '''
        slash_lang=set(['en_US'])
        slash_2_lang=set(['es_ES','fr_FR','it_IT'])
        slash_3_lang=set(['ja_JP'])
        dash_lang=set(['zh_CN'])
        dot_lang=set(['ko_KR'])
        dot_2_lang=set(['de_DE'])
        if lang in slash_lang:
            for i in range(2):
                temp_list=[]
                temp_list.append(Date[i].split('-')[1])
                temp_list.append(Date[i].split('-')[2])
                temp_list.append(Date[i].split('-')[0])
                Date[i]=temp_list[0]+'/'+temp_list[1]+'/'+temp_list[2]
        if lang in dot_2_lang:
            for i in range(2):
                temp_list=[]
                temp_list.append(Date[i].split('-')[2])
                temp_list.append(Date[i].split('-')[1])
                temp_list.append(Date[i].split('-')[0])
                Date[i]=temp_list[0]+'.'+temp_list[1]+'.'+temp_list[2]
        if lang in slash_2_lang:
            for i in range(2):
                temp_list=[]
                temp_list.append(Date[i].split('-')[2])
                temp_list.append(Date[i].split('-')[1])
                temp_list.append(Date[i].split('-')[0])
                Date[i]=temp_list[0]+'/'+temp_list[1]+'/'+temp_list[2]
        if lang in dot_lang:
            Date[0]=Date[0].replace("-",".%20")
            Date[1]=Date[1].replace("-",".%20")
        if lang in slash_3_lang:
            Date[0]=Date[0].replace("-","/")
            Date[1]=Date[1].replace("-","/")
        if lang in dash_lang:
           return Date
        return Date    
    
    def cookie_modify(cookie):
        cookie_dict={}
        for content in cookie:
            cookie_dict.update({'%s'%content['name']: content['value']})
        return(cookie_dict)
        
    def concat(ID,Dir):
        '''
        concat all the csv in the folder into one file
        ID : str
            folder name to be used as the file name
        Dir : str
            absolute path to the folder
        '''
        os.chdir(Dir)
        df_list=[]
        csv_list = glob.glob('*.csv')
        for f in csv_list:
            df=pd.read_csv(f,encoding='utf-8')
            df.insert(0,'Source.Name',f.rstrip('.csv'))
            df_list.append(df)
        combined_csv=pd.concat(df_list,sort=False)
        combined_csv.to_csv("%s.csv"%ID,index=False,encoding='utf-8-sig')
        
    print("""
Plz follow the instruction below:
1. Input the Customer ID or name to give a name for the folder 
2. A Chrome page would pop up, change the Customer and region to the one you wish to run data from.
3. Do not close the Chrome page,switch to Command and press 'Enter’
4. The crawler would automatically download the file into a temp folder,
   File would be renamed and gathered into the folder named as the CustomerID/name you typed in, 
   and sorted by date
5. Two more optional choices are offered, 1)combine these files 2) download the montly summary report
5. After all this round of work done.Press 'Enter' and Chrome would close automatically
6. If you wish to crawl another Customer
   you should run another round(run this program again)

""")
    ID = input("input Customer ID/name:  ")
#begin crawl
    try:
   
        chrome_options = webdriver.ChromeOptions() 
        chrome_options.add_argument("user-data-dir=%s\\ChromeProfile"%path_dir) #Path to your chrome profile
        prefs = {'download.default_directory' : '%s'%TempFolder,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": False}
        chrome_options.add_experimental_option('prefs', prefs)
       # print(os.getcwd())
        driver = webdriver.Chrome(options=chrome_options)
        driver.get("https://sellercentral.amazon.com/home")         #The page to change merchant and region
        print("plz make sure you've selected your customer, region and language correctly")
        input("Enter to confirm")
        
        currentPageUrl = driver.current_url
        url_head=re.search(r'https://(.*?)/.*',currentPageUrl)[1]    #Due to the difference of url among regions, use the shown one
        lang = cookie_modify(driver.get_cookies())['mons-lang']    #Due to the difference format of date among language, use the shown one
        monthgap = input ("input the month gap as '201909-201911': ")
        DateList=pickmonthgap(monthgap)
       
        for Date in DateList:
            Date1=Date.copy()
            Date_url = date_format(Date1,lang)
            detail_url="https://%s/gp/site-metrics/report.html#&cols=/c0/c1/c2/c3/c4/c5/c6/c7/c8/c9/c10/c11/c12/c13/c14/c15&sortColumn=16&filterFromDate=%s&filterToDate=%s&fromDate=%s&toDate=%s&reportID=102:DetailSalesTrafficByChildItem&sortIsAscending=0&currentPage=0&dateUnit=1&viewDateUnits=ALL&runDate="%(url_head,Date_url[0],Date_url[1],Date_url[0],Date_url[1])
            print(Date[0][:7])
            AmazonWorksheet(ID,Date,driver,Date[0][:7]).GrabThePage(detail_url)
        # combine 
        '''
        print ("\nDo you wish to combine? \nWarning! every csv in the folder would be combined")   
        choice = input ("Y/N?: ")
        if choice.lower()=='y':
            print("combining CSV...")
            try:
                concat(ID,'%s\\%s'%(Destination,ID))
                print ("combie job done!")
            except:
                print ("combine error!!! plz run combine code yourself")
        else:
            print ("You can run the combine code yourself")
        '''
        print("combining CSV...")
        try:
            concat(ID,'%s\\%s'%(Destination,ID))
            print ("combie job done!")
        except:
            print ("combine error!!! plz run combine code yourself")
        # for the sum report
        month = input("\nTo download the monthly summary report, input the starting month as '201801': ")
        current_month = str(datetime.date.today())[:7].replace('-','')
        monthgap = month + '-' + current_month
        DateList=pickmonthgap(monthgap)
        Date=[DateList[0][0],DateList[-1][1]]
        Date2=Date.copy()
        Date_url = date_format(Date2,lang)
        sum_url = "https://%s/gp/site-metrics/report.html#&cols=/c0/c1/c2/c3/c4/c5-orange/c6/c7/c8/c9/c10/c11/c12/c14-blue/c16/c17/c20&sortColumn=1&filterFromDate=%s&filterToDate=%s&fromDate=%s&toDate=%s&reportID=102:SalesTrafficTimeSeries&sortIsAscending=1&currentPage=0&dateUnit=3&viewDateUnits=ALL&runDate="%(url_head,Date_url[0],Date_url[1],Date_url[0],Date_url[1])
        AmazonWorksheet(ID,Date,driver,'monthly summary report').GrabThePage(sum_url)
        driver.quit()
        print("All work done")
        input("Enter to quit")
    except Exception as ex:
        print("Ops! Someting goes wrong")
        print (ex)
        input("error!!!Plz check the error message above!") 
