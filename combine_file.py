import pandas as pd
import glob,os,re
class combine():
    def __init__(self,Dir,Folder):
        self.concat(Dir,Folder)    
    def concat(self,ID,Dir):
        os.chdir(Dir)
        df_list=[]
        file_list = glob.glob('*.*')
        if (len(re.findall('.\.csv',str(file_list))) > len(re.findall('.\.xlsx',str(file_list))) ):
            file_type='csv'
        else: file_type='xlsx'
        csv_list = glob.glob('*.%s'%file_type)
        for f in csv_list:
            if file_type=='csv':
                df=pd.read_csv(f,encoding='utf-8')
            else: 
                df=pd.read_excel(f,encoding='utf-8')
            df.insert(0,'Source.Name',f.rstrip('*.%s'%file_type))
            df_list.append(df)        
        combined_csv=pd.concat(df_list,sort=True)
        if file_type=='csv':
            combined_csv.to_csv("%s.csv"%ID,index=False,encoding='utf-8-sig')
        else:
            combined_csv.to_excel("%s.xlsx"%ID,index=False,encoding='utf-8-sig')

if __name__ == '__main__':
    Destination=".\\"
    print("The work folder is %s"%os.getcwd())
    input("Plz make sure you are in the right folder for combination")
    Dir=os.getcwd().split('\\')[-1]
    combine(Dir,os.getcwd())
