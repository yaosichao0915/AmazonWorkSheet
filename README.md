# AmazonWorkSheet
Free your hands when you are dealing with the sellercenter reports  
## What can this script do?  
**Within the date range given, it would download the reports automatically and then combine them.**

The function is based on chromedirver,it is more like "help you click".  
Safety guranted, for your own convinence, the steps such as logining, choosing customer or regions are all completed on your own Chrome, fully in your charge.   

## How to use?
### 1.download latest python（windows）
https://www.python.org/downloads/release/latest

double click to run the installer. 

![安装图](https://github.com/yaosichao0915/AmazonWorkSheet/blob/master/readme_pic/win-install-dialog.png)

**Remember to select "add python to path"**

### 2.download the chromedriver compatible with your Chrome
https://chromedriver.chromium.org/downloads
Extract the chromedriver.exe out, and put it in the same folder of this script.  
(usually an older version of chromedriver.exe would not hurt, but someday you need to replace it)

### 3.another preprations
open the "Command Prompt" short for "CMD".
press "win" button and directly type "CMD" and Enter. 

![安装图](https://github.com/yaosichao0915/AmazonWorkSheet/blob/master/readme_pic/pic1.png)

The following needs some typing work

```
python --version 
```
	
if shows this

![安装图](https://github.com/yaosichao0915/AmazonWorkSheet/blob/master/readme_pic/pic2.png)

python is installed correctly and you are good to go next

install some python requirements

```
pip install selenium
```
then
```
pip install pandas
```

if all good, you have successfully set up an environment for the script

### Run the script!

You got 2 choices to run the script:

the more formal way:

	cd "to the path you put your codes"     // for example 'cd D:\newfolder\'
	python AmazonAuto.py
	
or the easier way is:
```
double click this script and CMD would pop and automatically running
```
## Final words

This is a personal work to help to save time.  
It is clearly not perfect, not that robust, but it works.  
However due to unpredictable reasons,such as connection error,server error, or even typo, plz be patient and try one more time.  
**And it is your own duty to check the data downloaded.**

Use it wisely and I am happy to hear any suggestions.
