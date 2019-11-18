# -*- coding: utf-8 -*-
# @Time    : 2019.11.11
# @Author  : yaosichao
# @Email ：yaosichao0915@163.com
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
class AamzonWorksheet():
    def __init__(self,ID,Date,driver,new_name):
        self.ID=ID
        self.Date=Date
        self.driver = driver
        self.new_name=new_name
    def rename_file(self,file):
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
            print("download timeout")
            return -1

    def GrabThePage(self,url):    
       # print(url)
        self.driver.get("https://www.baidu.com")
        self.driver.get(url)
        time.sleep(10)
        try:
            element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="downloadCSV"]'))
            )
            print("page loading sucess")
        finally:
            self.driver.find_element_by_id("export").click()
            self.driver.find_element_by_id("downloadCSV").click()
            print("Now downloading %s for the date of %s"%(self.ID,self.Date[0][:7]))
            time.sleep(5)
            duration = self.download_wait('%s'%TempFolder,20)
            print("downloaded and renamed,taking time of %s"%duration)
            
           # self.driver.quit()
    
if __name__ == '__main__':
    def pickmonthgap(monthgap):
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
                    DateList.append([day_begin,day_end])
        return (DateList)
    def concat(ID,Dir):
        os.chdir(Dir)
        df_list=[]
        csv_list = glob.glob('*.csv')
        for f in csv_list:
            df=pd.read_csv(f,encoding='utf-8')
            df.insert(0,'Source.Name',f.rstrip('.csv'))
            df_list.append(df)
        combined_csv=pd.concat(df_list)
        combined_csv.to_csv("%s.csv"%ID,index=False,encoding='utf-8-sig')
    print("""Plz follow the instruction below:
1. Input the Customer ID to give a name for the folder
2. A Chrome page would pop,change the Customer and region to the one you wish to crawl
3. Do not close the Chrome page,switch to CMD and check and press 'Enter’
4. The crawler would automatically download the file into the temp folder,
   File would be renamed and gathered into the folder named as the CustomerID you typed in
   sorted by date
5. Two more optional features, combine the files and download the sum worksheet report
5. After this round of work done.Chrome would close automatically,if you wish to crawl another Customer
   you should run another round(run this program again)


""")
    ID = input("input Customer ID:  ")
#begin crawl    
    chrome_options = webdriver.ChromeOptions() 
    chrome_options.add_argument("user-data-dir=%s\\ChromeProfile"%path_dir) #Path to your chrome profile
    prefs = {'download.default_directory' : '%s'%TempFolder,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True}
    chrome_options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://sellercentral.amazon.com/home")
    print("plz make sure you changed the customer correctly")
    input("Enter to confirm")
    currentPageUrl = driver.current_url
    region_code=re.search(r'amazon.(.*?)/.*',currentPageUrl)[1]
    monthgap = input ("input the month gap as '201909-201911': ")
    DateList=pickmonthgap(monthgap)
   
    for Date in DateList:
        detail_url="https://sellercentral.amazon.%s/gp/site-metrics/report.html#&cols=/c0/c1/c2/c3/c4/c5/c6/c7/c8/c9/c10/c11/c12/c13/c14/c15&sortColumn=16&filterFromDate=%s&filterToDate=%s&fromDate=%s&toDate=%s&reportID=102:DetailSalesTrafficByChildItem&sortIsAscending=0&currentPage=0&dateUnit=1&viewDateUnits=ALL&runDate="%(region_code,Date[0],Date[1],Date[0],Date[1])
        AamzonWorksheet(ID,Date,driver,Date[0][:7]).GrabThePage(detail_url)
    #driver.quit()
    # combine 
    print ("Do you wish to combine\nWarning!every csv in that folder would be combined")
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
    # for the sum report
    month = input("input the starting month of the sum report as '201801': ")
    current_month = str(datetime.date.today())[:7].replace('-','')
    monthgap = month + '-' + current_month
    DateList=pickmonthgap(monthgap)
    Date=[DateList[0][0],DateList[-1][1]]
    sum_url = "https://sellercentral.amazon.%s/gp/site-metrics/report.html#&cols=/c0/c1/c2/c3/c4/c5-orange/c6/c7/c8/c9/c10/c11/c12/c14-blue/c16/c17/c20&sortColumn=1&filterFromDate=%s&filterToDate=%s&fromDate=%s&toDate=%s&reportID=102:SalesTrafficTimeSeries&sortIsAscending=1&currentPage=0&dateUnit=3&viewDateUnits=ALL&runDate="%(region_code,Date[0],Date[1],Date[0],Date[1])
    AamzonWorksheet(ID,Date,driver,'sum').GrabThePage(sum_url)
    driver.quit()
    print("All work done")
    input("Enter to quit")

