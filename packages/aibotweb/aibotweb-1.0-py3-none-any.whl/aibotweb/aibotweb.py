import subprocess,json,socket,time

#用法 d = webBot(address="127.0.0.1",port=52020,browserName='chrome',debugPort = 0,userDataDir="./UserData",browserPath='null',argument = "null")
class webBot:
    def __init__(self,address="127.0.0.1",port=52020,browserName='chrome',debugPort = 0,userDataDir="./UserData",browserPath='null',argument = "null"):
        '''
        browserName: chrome/edge(360安全浏览器使用chrome)
        debugPort: 接管浏览器，实测360安全浏览器,edge,chrome正常
                    浏览器打开参数添加 --remote-debugging-port=19222
        browserPath: 除chrome和edge外，需要指定浏览器路径
        By 陈月归（网名） 951163006@qq.com
        '''
        self.__debugPort=debugPort
        self.__browserPath=browserPath
        self.__address=address
        self.__browserName=browserName
        self.__userDataDir=userDataDir
        self.__port=port
        self.__sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.__argument=argument
        #print(json.dumps({"driverPort":self.__port, "browserName":self.__browserName, "debugPort":self.__debugPort, "userDataDir":self.__userDataDir, "browserPath":self.__browserPath, "argument":"null"}))
        subprocess.Popen(['WebDriver.exe',json.dumps({"driverPort":self.__port, "browserName":self.__browserName, "debugPort":self.__debugPort, "userDataDir":self.__userDataDir, "browserPath":self.__browserPath, "argument":argument})])
        while 1:
            try:
                self.__sock.connect((self.__address,self.__port))
                print("连接成功")
                return None
            except Exception as error:
                print('错误，端口是否被占用，是否刚才用同样的端口打开过浏览器没关，若有，请关闭浏览器和本程序重新运行\n')
                print('等待1秒后重试')
                print(error, '\n')
                time.sleep(1)
                print('再次连接')
        
    def sendData(self, *args) -> str:
        """
        参考AiBot.py模块作者:河畔
        用sendData()可直接调用开源源码
        查看 http://www.ai-bot.net/aiboteProtocol.html#4
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
        self.__sock.sendall(data)
        data_length, data = self.__sock.recv(self.__port).split(b"/", 1)

        while int(data_length) > len(data):
            data += self.__sock.recv(self.__port)
        result = data.decode("utf8").strip()
        if result == 'true':
            return True
        elif result == 'false':
            return False
        else:
            return result
    

    #
    #页面和导航
    #
    def goto(self,url) -> bool:
        '''
        跳转url
        '''
        result = self.sendData('goto', url)
        return result

    def newPage(self,url) -> bool:
        '''
        新建tab页面并跳转到指定url
        '''
        result = self.sendData("newPage", url)
        return result
    def back(self) -> bool:
        '''
        后退
        '''
        result = self.sendData("back")
        return result
    def forward(self) -> bool:
        '''
        前进
        '''
        result = self.sendData("forward")
        return result
    def refresh(self) -> bool:
        '''
        刷新
        '''
        result = self.sendData("refresh")
        return result
        
    def getCurPageId(self) -> str:
        '''
        获取当前页面ID
        '''
        result = self.sendData("getCurPageId")
        return result
    def getAllPageId(self):
        '''返回页面ID数组'''
        
        result = self.sendData("getAllPageId")
        return result
    
    def switchPage(self,pageId) -> bool:
        '''
        pageId: 要切换的页面ID
        '''
        result = self.sendData("switchPage", pageId)
        return result
    
    def closePage(self) -> bool:
        '''
        bug：关闭后就废了，无法继续操作
        关闭当前页面
        '''
        return "bug严重，暂不使用"
        result = self.sendData("closePage")
        return result
    def getCurrentUrl(self):
        '''获取当前URL'''
        result = self.sendData("getCurrentUrl")
        return result
        
    def getTitle(self):
        '''获取页面标题'''
        result = self.sendData("getTitle")
        return result
    #
    #IFrame
    #
    def switchFrame(self,frameUrl)-> bool:
        '''
        通过url切换frame
        frameUrl： 字符串型，要切换frame的src链接。
                    如果目标iframe没有scr连接，应当使用所在的iframe框架的链接
        '''
        result = self.sendData("switchFrame", frameUrl)
        return result
        
    def switchMainFrame(self) -> bool:
        '''
        切换主frame
        '''
        result = self.sendData("switchMainFrame")
        return result
    #
    #元素操作
    #
    def clickElement(self,xpath) -> bool:
        '''
        点击元素
        '''
        result = self.sendData("clickElement", xpath)
        return result
    def setElementValue(self,xpath, value) -> bool:
        '''
        设置编辑框内容
        xpath: 元素路径
        value: 输入的值
        '''
        result = self.sendData("setElementValue", xpath, value)
        return result
    def getElementText(self,xpath) -> str:
        '''
        获取文本
        xpath:元素路径
        '''
        result = self.sendData("getElementText", xpath)
        return result
    
    def getElementOuterHTML(self,xpath):
        '''
        获取outerHTML
        xpath: 元素路径
        '''
        result = self.sendData("getElementOuterHTML", xpath)
        return result
    def getElementInnerHTML(self,xpath):
        '''
        获取innerHTML
        xpath: 元素路径
        '''
        result = self.sendData("getElementInnerHTML", xpath)
        return result
        
    def setElementAttribute(self, xpath, attributeName, value) -> bool:
        '''
        设置属性值
        xpath: 元素路径
        attributeName: 指定的属性名
        value: 属性值
        '''
        result = self.sendData("setElementAttribute", xpath, attributeName, value)
        return result
        
    def getElementAttribute(self,xpath, attributeName):
        '''
        获取属性值
        xpath: 元素路径
        attributeName: 指定的属性名
        '''
        result = self.sendData("getElementAttribute", xpath,attributeName)
        return result
        
    def getElementRect(self,xpath) -> dict:
        '''
        获取矩形位置
        xpath: 元素路径
        '''
        result = self.sendData("getElementRect", xpath)
        return result
        
    def isSelected(self, xpath) -> bool:
        '''
        判断该元素是否选中
        xpath: 元素路径
        '''
        result = self.sendData("isSelected",  xpath)
        return result
    
    def isDisplayed(self,xpath) -> bool:
        '''
        判断该元素是否可见
        xpath: 元素路径
        '''
        result = self.sendData("isDisplayed", xpath)
        return result
    
    def isEnabled(self,xpath) -> bool:
        '''
        判断元素是否可用
        xpath: 元素路径
        '''
        result = self.sendData("isEnabled", xpath)
        return result
        
    def clearElement(self,xpath) -> bool:
        '''
        清除元素值
        xpath: 元素路径
        '''
        result = self.sendData("clearElement", xpath)
        return result

    #
    #鼠标键盘
    #
    def sendKeys(self,xpath, text) -> bool:
        '''
        发送文本
        xpath: 元素路径，如果元素不能设置焦点，应ClickMouse 点击锁定焦点输入
        text: 要输入的文本，例如sendKeys('//*[@id="kw"]', 'aibote\r'); aibote换行
        '''
        result = self.sendData("sendKeys", xpath,text)
        return result
        
    def sendVk(self,vkCode)-> bool:
        '''
        发送Vk虚拟键
        vkCode: 整型，VK键值，仅支持 回退键:8  回车键:13  空格键:32  方向左键:37  方向上键:38  方向右键:39  方向下键:40  删除键:46       
        '''
        result = self.sendData("sendVk", vkCode)
        return result
    
    def clickMouse(self, x, y, msg) -> bool:
        '''
        点击鼠标
        x: 整型，横坐标，非Windows坐标，页面左上角为起始坐标
        y: 整型，纵坐标，非Windows坐标，页面左上角为起始坐标
        msg: 整型，单击左键:1  单击右键:2  按下左键:3  弹起左键:4  按下右键:5  弹起右键:6  双击左键:7 
        '''
        result = self.sendData("clickMouse", x, y,msg)
        return result
    
    def moveMouse(self, x, y):
        '''
        移动鼠标
        参数一 整型，横坐标，非Windows坐标，页面左上角为起始坐标
        参数二 整型，纵坐标，非Windows坐标，页面左上角为起始坐标
        '''
        result = self.sendData("moveMouse", x, y)
        return result
        
        
    def wheelMouse(self, deltaX, deltaY, x=0, y=0) -> bool:
        '''
        滚动鼠标
        deltaX: 整型，水平滚动条移动的距离
        deltaY: 整型，垂直滚动条移动的距离
        x: 整型，可选参数，鼠标横坐标位置， 默认为0
        y: 整型，可选参数，鼠标纵坐标位置， 默认为0
        '''
        result = self.sendData("wheelMouse",deltaX, deltaY, x, y)
        return result
        
    def clickMouseByXpath(self, xpath, msg) -> bool:
        '''
        通过xpath: 点击鼠标(元素中心点)
        xpath: 字符串型，元素路径
        msg: 整型，单击左键:1  单击右键:2  按下左键:3  弹起左键:4  按下右键:5  弹起右键:6  双击左键:7 
        '''
        result = self.sendData("clickMouseByXpath", xpath, msg)
        return result
        
    def moveMouseByXpath(self,xpath) -> bool:
        '''
        通过xpath 移动鼠标(元素中心点)
        xpath: 字符串型，元素路径
        '''
        result = self.sendData("moveMouseByXpath", xpath)
        return result
        
    def wheelMouseByXpath(self, xpath, deltaX, deltaY) -> bool:
        '''
        【待测试】
        通过xpath 滚动鼠标
        xpath: 字符串型，元素路径
        deltaX: 整型，水平滚动条移动的距离
        deltaY: 整型，垂直滚动条移动的距离
        
        '''
        result = self.sendData("wheelMouseByXpath", xpath, deltaX, deltaY)
        return result
    #
    #截图
    #
    def takeScreenshot(self, xpath = None) ->'base-64编码字符串，PNG格式':
        '''
        截图
        xpath: 可选参数，默认截取全屏, 如果指定元素路径，则截取元素图片。
        '''
        if xpath:
            result = self.sendData("takeScreenshot", xpath)
        else:
            result = self.sendData("takeScreenshot")
        return result
    #
    #alert/prompt弹窗    
    #
    def clickAlert(self,acceptOrCancel, promptText = "") -> bool:
        '''
        点击警告框
        acceptOrCancel： 布尔型，true接受, false取消
        promptText： 字符串型，可选参数，输入prompt警告框文本
        '''
        result = self.sendData("clickAlert", acceptOrCancel, promptText)
        return result
    
    def getAlertText(self) ->str:
        '''
        获取警告框内容
        '''
        result = self.sendData("getAlertText")
        return result
        
    #
    #cookie操作
    #
    def getCookies(self, url) ->"json格式字符串":
        '''
        获取指定url匹配的cookies
        url: 字符串型，指定的url http://或https:// 起头
        '''
        result = self.sendData("getCookies", url)
        return result
        
    def getAllCookies(self) -> 'json格式字符串':
        '''
        获取cookies
        '''
        result = self.sendData("getAllCookies")
        return result
        
    def setCookie(self, cookieParam) -> bool:
        '''
        设置cookie
        cookieParam: 字典型，{"name":string, "value":string, "url":string, "domain":string, "path":string, "secure":boolean, "httpOnly":boolean, "sameSite":string, "expires":number, "priority":string, "sameParty":boolean, "sourceScheme":string, "sourcePort":number, "partitionKey":string}  name、value和url必填参数，其他参数可选
        '''
        #必填
        name = cookieParam["name"]
        value = cookieParam["value"]
        url = cookieParam["url"]
        #
        
        #可选
        domain = ""
        path = ""
        secure = false
        httpOnly = false
        sameSite = ""
        expires = 0
        priority = ""
        sameParty = false
        sourceScheme = ""
        sourcePort = 0
        partitionKey = ""
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
        strRet = self.sendData(strData)
        if(strRet == "false"):
            return false
        else:
            return true
        
        
        
    #
    #注入JavaScript
    #
    def executeScript(self,script) ->str:
        '''
        执行JavaScript 代码
        script： 字符串型，注入的js代码
        假如注入代码为函数且有return语句，则返回retrun 的值，否则返回null;
        注入示例：(function () {return "aibote rpa"})();
        '''
        result = self.sendData("executeScript", script)
        return result
        

    #
    #浏览器窗口
    #
    def getWindowPos(self) ->'json格式字符串':
        '''
        获取窗口位置和状态
        成功返回矩形位置和窗口状态，失败返回null
        '''
        result = self.sendData("getWindowPos")
        return result
        
    
    def setWindowPos(self, windowState, rect = [0,0,0,0]) -> bool:
        '''
        设置窗口位置和状态
        windowState: 字符串型，窗口状态，正常:"normal"  最小化:"minimized"  最大化:"maximized"  全屏:"fullscreen"
        rect: [left, top, width, height]，可选参数，浏览器窗口位置，此参数仅windowState 值为 "normal" 时有效
        '''
        result = self.sendData("setWindowPos", windowState, rect[0], rect[1], rect[2], rect[3])
        return result
