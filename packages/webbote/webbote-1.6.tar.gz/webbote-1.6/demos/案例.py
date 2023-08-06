from webbote import WebBotMain
import base64, time, winreg
def get_desktop():
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
    return winreg.QueryValueEx(key, "Desktop")[0]
web=WebBotMain.build(address='127.0.0.1', port=26678, browserName='chrome', debugPort=0, userDataDir='./UserData', browserPath='null', argument='null')
web.goto('https://www.baidu.com')
PageId=web.getCurPageId()
web.sendKeys('//*[@id="kw"]','美女')
web.clickElement('//*[@id="su"]')
web.clickElement('//*[@id="1"]/div/div[1]/div/div[1]/a[2]/img')
PageIds=web.getAllPageId()
for i in PageIds:
    if i !=PageId:
        web.switchPage(i)
time.sleep(2)
r=web.takeScreenshot('//*[@id="currentImg"]')
r_bytes = base64.b64decode(r)
with open(get_desktop()+'\\'+'美女.png','wb') as f:
    f.write(r_bytes)


