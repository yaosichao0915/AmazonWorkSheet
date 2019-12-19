import pandas as pd
import glob,os
class combine():
    def __init__(self,Dir,Folder):
        self.concat(Dir,Folder)    
    def concat(self,ID,Dir):
        os.chdir(Dir)
        df_list=[]
        csv_list = glob.glob('*.csv')
        for f in csv_list:
            df=pd.read_csv(f,encoding='utf-8')
            df.insert(0,'Source.Name',f.rstrip('.csv'))
            df_list.append(df)
        combined_csv=pd.concat(df_list)
        combined_csv.to_csv("%s.csv"%ID,index=False,encoding='utf-8-sig')

if __name__ == '__main__':
    Destination=".\\"
    print("The work folder is %s"%os.getcwd())
    input("Plz make sure you are in the right folder for combination")
    Dir=os.getcwd().split('\\')[-1]
    combine(Dir,os.getcwd())
