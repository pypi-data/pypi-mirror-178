from aibotweb import webBot
import base64, time, winreg
def get_desktop():
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
    return winreg.QueryValueEx(key, "Desktop")[0]
d=webBot()
d.goto('https://www.baidu.com')
PageId=d.getCurPageId()
time.sleep(1)
d.sendKeys('//*[@id="kw"]','美女')
time.sleep(1)
d.clickElement('//*[@id="su"]')
time.sleep(1)
d.clickElement('//*[@id="1"]/div/div[1]/div/div[1]/a[2]/img')
PageIds=d.getAllPageId().split('|')
for i in PageIds:
    if i !=PageId:
        d.switchPage(i)
time.sleep(2)
r=d.takeScreenshot()
r_bytes = base64.b64decode(r)
with open(get_desktop()+'\\'+'截图.png','wb') as f:
    f.write(r_bytes)


