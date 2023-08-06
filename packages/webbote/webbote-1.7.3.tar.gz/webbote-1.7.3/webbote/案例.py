from webbote import WebBotMain
import base64, time, winreg
def get_desktop():
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
    return winreg.QueryValueEx(key, "Desktop")[0]
d=WebBotMain.build() #默认是打开谷歌浏览器，默认port=26678
d.goto('https://www.baidu.com')
PageId=d.getCurPageId()
d.sendKeys('//*[@id="kw"]','美女')
a1=d.clickElement('//*[@id="su"]')
a2=d.clickElement('//*[@id="1"]/div/div[1]/div/div[1]/a[2]/img')
PageIds=d.getAllPageId()
for i in PageIds:
    if i !=PageId:
        d.switchPage(i)
time.sleep(2)
r=d.takeScreenshot('//*[@id="currentImg"]')
r_bytes = base64.b64decode(r)
with open(get_desktop()+'\\'+'截图.png','wb') as f:
    f.write(r_bytes)
