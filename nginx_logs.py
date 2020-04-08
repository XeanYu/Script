
# author: XeanYu
import os
from os import popen
import readline

class WebAccessLogFunction():
    
    # init
    def __init__(self):
        # Get Login User
        self.username = str(popen('whoami').read()).strip()

        # Input Your Web Access Log File Path
        print("\n\nHello %s,This Is Log Handler Software." % (self.username))
        self.LogFilePath = input("Web Access Log File Path: ")
    
    
        # Find File.
        result = os.path.exists(self.LogFilePath)
        while not result:
            print("\n[!] Not Found Web Access Log File.")
            try:
                self.LogFilePath = input("[exit] Web Access Log File Path: ")
            except KeyboardInterrupt as e:
                exit("[!] Ctrl + C")
            if self.LogFilePath == "exit":
                exit("[!] Exit.")
            result = os.path.exists(self.LogFilePath)
        
        print("[+] Found Web Access Log File!")
           

    # Print Most Requests IP Of Top n.
    def RequestTopIP(self,n=10):
        result = os.popen("awk '{a[$1]++}END{for(i in a)print a[i],i|\"sort -k1 -nr|head -n%s\"}' %s " % (str(n),self.LogFilePath)).read()
        result_list = []
        for i in result.split("\n"):
            if i:
                result_list.append(i)
        self.RequestTopTendict = {}
        if result_list:
            for i in result_list:
                dateline = str(i).split(" ")
                self.RequestTopTendict[dateline[1]] = dateline[0]
        else:
            return False

        for i in self.RequestTopTendict:
            print(str("IP: {ip}"+"[{num}]".rjust(20," ")).format(ip=str(i),num=str(self.RequestTopTendict.get(i))))
        
        return True
    
    
    # Print Most Request Page Of Top n 
    def RequestTopPage(self,n=10,IsFilterStatus=True):
        if IsFilterStatus:
            result = os.popen("cat %s |awk '{a[$7]++}END{for(i in a){if(!(match(i,\".js\")||match(i,\".css\")||match(i,\".png\")||match(i,\".jpg\")||match(i,\".ico\")||match(i,\".zip\") ))print a[i],i}}'|sort -k1 -nr|head -n%s" % (self.LogFilePath,str(n))).read()
        else:
            result = os.popen("awk '{a[$7]++}END{for(i in a)print a[i],i|\"sort -k1 -nr|head -n%s\"}' %s" % (str(n),self.LogFilePath)).read()

        result_list = []
        for i in result.split("\n"):
            if i:
                result_list.append(i)
        self.RequestTopPagedict  = {}
        if result_list:
            for i in result_list:
                dateline = str(i).split(" ")
                self.RequestTopPagedict[dateline[1]] = dateline[0]
        else:
            return False
        
        for i in self.RequestTopPagedict:
            print(str("Url: {url}"+"[{num}]".rjust(30," ")).format(url=str(i),num=str(self.RequestTopPagedict.get(i))))        
    
        return True


class OsLog():
    
    def __init__(self):
        pass
    
    def OSLoginingUser(self):
        AllUserLogining = os.popen("w").read()
        print(AllUserLogining)
        return True



def main(WebLog,OsLog):
    LogMenu = [
                'w1.查看访问次数排行前10的IP',
                "w2.查看访问次数排放前10的链接",
                'o1.查看当前系统中登录的用户',
                "exit.退出"
                ]
    tools = {
        "w1": WebLog.RequestTopIP,
        "w2": WebLog.RequestTopPage,
        "o1": OsLog.OSLoginingUser 
    }
    
    while True:
        os.system("clear")
        print("="*20)
        for i in LogMenu:
            print(i)

        command = input(">> ")

        # run
        if command in tools:
            print("\n\n\n")
            tools.get(command)()
            input()
        # exit
        if command == "exit":
            break

if __name__ == "__main__":
    #Os_Log = OSLoginingUser()
    oslogs = OsLog()
    weblogs = WebAccessLogFunction()
    main(weblogs,oslogs)   

    #logs.RequestTopIP()
    #logs.RequestTopPage(IsFilterStatus=False)
