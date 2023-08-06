import subprocess,json,socket,time

class WebBotMain:
    wait_timeout = 3  # seconds
    interval_timeout = 0.5  # seconds

    def __init__(self,port):
        self.port = port
        address_info = socket.getaddrinfo("127.0.0.1", port, socket.AF_INET, socket.SOCK_STREAM)[0]
        family, socket_type, proto, _, socket_address = address_info
        self.__sock = socket.socket(family, socket_type, proto)
        time.sleep(2)
        while True:
            try:
                self.__sock.connect(socket_address)
                print('连接浏览器成功')
                break
            except Exception as connect_error:
                print(connect_error)
                print('重试')

    @classmethod
    def build(cls, address="127.0.0.1",port=26678,browserName='chrome',debugPort = 0,userDataDir="./UserData",browserPath='null',argument = "null") -> "WebBotMain":
        """
        :param address: 字符串型，默认"127.0.0.1", webDriver服务地址。假如值为 "127.0.0.1"脚本会自动启动WebDriver.exe，如果是远程服务地址，用户需要手动启动WebDriver.exe 并且提供启动参数。
        :param port: 整型，默认52020，服务端口
        :param browserName: 字符串型，默认"chrome"，浏览器名称 "edge"和"chrome"，其他chromium内核浏览器需要指定browserPath参数
        :param debugPort: 整型，可选参数，调试端口。默认 0 随机端口。指定端口则接管已打开的浏览器。启动浏览应指定的参数 --remote-debugging-port=19222 --user-data-dir=C:\\Users\\电脑用户名\\AppData\\Local\\Google\\Chrome\\User Data【Edge浏览器的接管必须要有用户配置文件夹设置，且是要打开浏览器状态下进行接管】
        :param userDataDir: 字符串型，可选参数，用户数据目录,默认./UserData。多进程同时操作多个浏览器数据目录不能相同
        :param browserPath: 字符串型，可选参数，浏览器路径
        :param argument: 字符串型，可选参数，浏览器启动参数。例如：无头模式: --headless   设置代理：--proxy-server=127.0.0.1:8080
        :return: object
        命令行启动示例：WebDriver.exe "{\"driverPort\":26678, \"browserName\":\"chrome\", \"debugPort\":0, \"userDataDir\":\"./UserData\", \"browserPath\":\"null\", \"argument\":\"null\"}"
        """
        subprocess.Popen(['WebDriver.exe', json.dumps(
            {"driverPort": port, "browserName": browserName, "debugPort": debugPort,
             "userDataDir": userDataDir, "browserPath": browserPath, "argument": argument})])
        return WebBotMain(port)

    def __send_data(self, *args) -> str:
        """
        发送TCP命令
        :param args: 参照开源协议 http://www.ai-bot.net/aiboteProtocol.html#4
        """
        args_len = ""
        args_text = ""

        for argv in args:
            if argv is None:
                argv = ""
            elif isinstance(argv, bool) and argv:
                argv = "true"
            elif isinstance(argv, bool) and not argv:
                argv = "false"

            argv = str(argv)
            args_text += argv
            args_len += str(len(argv)) + "/"

        data = (args_len.strip("/") + "\n" + args_text).encode("utf8")

        # self.log.debug(rf"---> {data}")
        self.__sock.sendall(data)
        data_length, data = self.__sock.recv(self.port).split(b"/", 1)

        while int(data_length) > len(data):
            data += self.__sock.recv(self.port)
        # self.log.debug(rf"<--- {data}")

        return data.decode("utf8").strip()

    def sendData(self, *args) -> str:
        return self.__send_data(self, *args)

    # ###############
    #   页面和导航   #
    # ###############
    def goto(self,url) -> bool:
        """
        跳转url
        :param url: 字符串型, 网址
        """
        result = self.__send_data('goto', url)
        return result == "true"

    def newPage(self,url) -> bool:
        """
        新建tab页面并跳转到指定url
        :param url: 字符串型, 网址
        """
        result = self.__send_data("newPage", url)
        return result == "true"

    def back(self) -> bool:
        """
        回退
        """
        result = self.__send_data("back")
        return result == "true"

    def forward(self) -> bool:
        """
        前进
        """
        result = self.__send_data("forward")
        return result == "true"

    def refresh(self) -> bool:
        """
        刷新
        """
        result = self.__send_data("refresh")
        return result == "true"
        
    def getCurPageId(self) -> str:
        """
        获取当前页面ID
        """
        result = self.__send_data("getCurPageId")
        return result

    def getAllPageId(self) -> list[str]:
        """
        返回页面ID数组
        """
        result = self.__send_data("getAllPageId").split('|')

        return result
    
    def switchPage(self,pageId) -> bool:
        """
        切换页面
        :param pageId: 字符串型, 要切换的页面ID
        """
        result = self.__send_data("switchPage", pageId)
        return result == "true"

    def closePage(self) -> bool:
        """
        关闭当前页面
        """
        result = self.__send_data("closePage")
        return result == "true"

    def getCurrentUrl(self):
        """
        获取当前URL
        """
        result = self.__send_data("getCurrentUrl")
        return result
        
    def getTitle(self):
        """
        获取页面标题
        """
        result = self.__send_data("getTitle")
        return result

    # #############
    #    IFrame   #
    # #############
    def switchFrame(self,frameUrl)-> bool:
        """
        通过url切换frame
        :param frameUrl: 字符串型，要切换frame的src链接。如果目标iframe没有scr连接，应当使用所在的iframe框架的链接
        """
        result = self.__send_data("switchFrame", frameUrl)
        return result == "true"
        
    def switchMainFrame(self) -> bool:
        """
        切换主frame
        """
        result = self.__send_data("switchMainFrame")
        return result == "true"

    # #############
    #    元素操作   #
    # #############
    def clickElement(self,xpath) -> bool:
        """
        点击元素
        :param xpath: 字符串型，元素路径
        """
        result = self.__send_data("clickElement", xpath)
        return result == "true"

    def setElementValue(self,xpath, value) -> bool:
        """
        设置编辑框内容
        :param xpath: 字符串型，元素路径
        :param value: 字符串型，输入的值
        """
        result = self.__send_data("setElementValue", xpath, value)
        return result == "true"

    def getElementText(self,xpath) -> str:
        """
        获取文本
        :param xpath: 字符串型，元素路径
        """
        result = self.__send_data("getElementText", xpath)
        return result
    
    def getElementOuterHTML(self,xpath):
        """
        获取outerHTML
        :param xpath: 字符串型，元素路径
        """
        result = self.__send_data("getElementOuterHTML", xpath)
        return result

    def getElementInnerHTML(self,xpath) -> str:
        """
        获取innerHTML
        :param xpath: 字符串型，元素路径
        """
        result = self.__send_data("getElementInnerHTML", xpath)
        return result
        
    def setElementAttribute(self, xpath, attributeName, value) -> bool:
        """
        设置属性值
        :param xpath:
        :param attributeName: 指定的属性名
        :param value: 属性值
        """
        result = self.__send_data("setElementAttribute", xpath, attributeName, value)
        return result == "true"
        
    def getElementAttribute(self,xpath, attributeName) -> str:
        """
        获取属性值
        :param xpath: 字符串型，元素路径
        :param attributeName: 指定的属性名
        """
        result = self.__send_data("getElementAttribute", xpath,attributeName)
        return result
        
    def getElementRect(self,xpath):
        """
        获取矩形位置
        :param xpath: 字符串型，元素路径
        """
        result = self.__send_data("getElementRect", xpath)
        return result
        
    def isSelected(self, xpath) -> bool:
        """
        判断该元素是否选中
        :param xpath: 字符串型，元素路径
        """
        result = self.__send_data("isSelected",  xpath)
        return result == "true"
    
    def isDisplayed(self,xpath) -> bool:
        """
        判断该元素是否可见
        :param xpath: 字符串型，元素路径
        """
        result = self.__send_data("isDisplayed", xpath)
        return result == "true"
    
    def isEnabled(self,xpath) -> bool:
        """
        判断元素是否可用
        :param xpath: 字符串型，元素路径
        """
        result = self.__send_data("isEnabled", xpath)
        return result == "true"
        
    def clearElement(self,xpath) -> bool:
        """
        清除元素值
        :param xpath: 字符串型，元素路径
        """
        result = self.__send_data("clearElement", xpath)
        return result == "true"

    # #############
    #   鼠标键盘   #
    # #############
    def sendKeys(self,xpath, text) -> bool:
        """
        发送文本
        :param xpath: 元素路径，如果元素不能设置焦点，应ClickMouse 点击锁定焦点输入
        :param text: 要输入的文本，例如sendKeys('//*[@id="kw"]', 'aibote\r'); aibote换行
        """
        result = self.__send_data("sendKeys", xpath,text)
        return result == "true"
        
    def sendVk(self,vkCode)-> bool:
        """
        发送Vk虚拟键
        :param vkCode: 整型，VK键值，仅支持 回退键:8  回车键:13  空格键:32  方向左键:37  方向上键:38  方向右键:39  方向下键:40  删除键:46
        """
        result = self.__send_data("sendVk", vkCode)
        return result == "true"
    
    def clickMouse(self, x, y, msg) -> bool:
        """
        点击鼠标
        :param x: 整型，横坐标，非Windows坐标，页面左上角为起始坐标
        :param y: 整型，纵坐标，非Windows坐标，页面左上角为起始坐标
        :param msg: 整型，单击左键:1  单击右键:2  按下左键:3  弹起左键:4  按下右键:5  弹起右键:6  双击左键:7
        """
        result = self.__send_data("clickMouse", x, y,msg)
        return result == "true"
    
    def moveMouse(self, x, y):
        """
        移动鼠标
        :param x: 整型，横坐标，非Windows坐标，页面左上角为起始坐标
        :param y: 整型，纵坐标，非Windows坐标，页面左上角为起始坐标
        """
        result = self.__send_data("moveMouse", x, y)
        return result
        
        
    def wheelMouse(self, deltaX, deltaY, x=0, y=0) -> bool:
        """
        滚动鼠标
        :param deltaX: 整型，水平滚动条移动的距离
        :param deltaY: 整型，垂直滚动条移动的距离
        :param x: 整型，可选参数，鼠标横坐标位置， 默认为0
        :param y: 整型，可选参数，鼠标纵坐标位置， 默认为0
        """
        result = self.__send_data("wheelMouse",deltaX, deltaY, x, y)
        return result == "true"
        
    def clickMouseByXpath(self, xpath, msg) -> bool:
        """
        通过xpath点击鼠标(元素中心点)
        :param xpath: 字符串型，元素路径
        :param msg: 整型，单击左键:1  单击右键:2  按下左键:3  弹起左键:4  按下右键:5  弹起右键:6  双击左键:7
        """
        result = self.__send_data("clickMouseByXpath", xpath, msg)
        return result == "true"
        
    def moveMouseByXpath(self,xpath) -> bool:
        """
        通过xpath 移动鼠标(元素中心点)
        :param xpath: 字符串型，元素路径
        """
        result = self.__send_data("moveMouseByXpath", xpath)
        return result == "true"
        
    def wheelMouseByXpath(self, xpath, deltaX, deltaY) -> bool:
        """
        通过xpath 滚动鼠标
        :param xpath: 字符串型，元素路径
        :param deltaX: 整型，水平滚动条移动的距离
        :param deltaY: 整型，垂直滚动条移动的距离
        """
        result = self.__send_data("wheelMouseByXpath", xpath, deltaX, deltaY)
        return result == "true"

    # #############
    #     截图     #
    # #############
    def takeScreenshot(self, xpath = None) ->str:
        """
        截图
        :param xpath: 可选参数，默认截取全屏, 如果指定元素路径，则截取元素图片。
        :return: 'base-64编码字符串，PNG格式'
        """
        if xpath:
            result = self.__send_data("takeScreenshot", xpath)
        else:
            result = self.__send_data("takeScreenshot")
        return result

    # ##################
    #  alert/prompt弹窗  #
    # ##################
    def clickAlert(self,acceptOrCancel, promptText = "") -> bool:
        """
        点击警告框
        :param acceptOrCancel: 布尔型，true接受, false取消
        :param promptText: 字符串型，可选参数，输入prompt警告框文本
        :return:
        """
        result = self.__send_data("clickAlert", acceptOrCancel, promptText)
        return result == "true"
    
    def getAlertText(self) ->str:
        """
        获取警告框内容
        """
        result = self.__send_data("getAlertText")
        return result

    # ###############
    #   cookie操作   #
    # ###############
    def getCookies(self, url) ->str:
        """
        获取指定url匹配的cookies
        :param url: 字符串型，指定的url http://或https:// 起头
        :return:
        """
        result = self.__send_data("getCookies", url)
        return result
        
    def getAllCookies(self) -> str:
        """
        获取cookies
        :return:
        """
        result = self.__send_data("getAllCookies")
        return result
        
    def setCookie(self, cookieParam) -> bool:
        """
        设置cookie
        :param cookieParam: 字典型，{"name":string, "value":string, "url":string, "domain":string, "path":string,
            "secure":boolean, "httpOnly":boolean, "sameSite":string, "expires":number, "priority":string,
            "sameParty":boolean, "sourceScheme":string, "sourcePort":number, "partitionKey":string}
            name、value和url必填参数，其他参数可选
        :return:
        """
        #必填
        name = cookieParam["name"]
        value = cookieParam["value"]
        url = cookieParam["url"]
        #
        #可选
        domain = path = sameSite = priority = sourceScheme = partitionKey = ""
        secure = httpOnly = sameParty = False
        expires = sourcePort = 0
        #
        if "domain" in cookieParam:
            domain = cookieParam["domain"]
        if "path" in cookieParam:
            path = cookieParam["path"]
        if "secure" in cookieParam:
            secure = cookieParam["secure"]
        if "httpOnly" in cookieParam:
            httpOnly = cookieParam["httpOnly"]
        if "sameSite" in cookieParam:
            sameSite = cookieParam["sameSite"]
        if "expires" in cookieParam:
            expires = cookieParam["expires"]
        if "priority" in cookieParam:
            priority = cookieParam["priority"]
        if "sameParty" in cookieParam:
            sameParty = cookieParam["sameParty"]
        if "sourceScheme" in cookieParam:
            sourceScheme = cookieParam["sourceScheme"]
        if "sourcePort" in cookieParam:
            sourcePort = cookieParam["sourcePort"]
        if "partitionKey" in cookieParam:
            partitionKey = cookieParam["partitionKey"]
        strData = ("setCookie", name, value, url, domain, path, secure, httpOnly, sameSite, expires, priority, sameParty, sourceScheme, sourcePort, partitionKey)
        result = self.__send_data(strData)
        return result == "true"

    # ################
    #  注入JavaScript  #
    # ################
    def executeScript(self,script) ->str:
        """
        执行JavaScript 代码
        :param script: 字符串型，注入的js代码
        :return: 假如注入代码为函数且有return语句，则返回retrun 的值，否则返回null;
        注入示例：(function () {return "aibote rpa"})();
        """
        result = self.__send_data("executeScript", script)
        return result

    # #############
    #   浏览器窗口   #
    # #############
    def getWindowPos(self) -> str:
        """
        获取窗口位置和状态
        :return: 成功返回矩形位置和窗口状态，失败返回null
        """
        result = self.__send_data("getWindowPos")
        return result

    def setWindowPos(self, windowState, rect=None) -> bool:
        """
        设置窗口位置和状态
        :param windowState: 字符串型，窗口状态，正常:"normal"  最小化:"minimized"  最大化:"maximized"  全屏:"fullscreen"
        :param rect: [left, top, width, height]，可选参数，浏览器窗口位置，此参数仅windowState 值为 "normal" 时有效
        """
        if rect is None:
            rect = [0, 0, 0, 0]
        result = self.__send_data("setWindowPos", windowState, rect[0], rect[1], rect[2], rect[3])
        return result == "true"
