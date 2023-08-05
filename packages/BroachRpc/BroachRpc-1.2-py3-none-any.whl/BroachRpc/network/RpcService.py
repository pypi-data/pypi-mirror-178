from BroachRpc.common import CommonDef,GlobalVariable
from BroachRpc.exception import DefException
from BroachRpc.network import RpcServer,RpcClient
import threading
import logging
import json
import time

"""
rpc 应用通信协议 json
{
  "funcId": "" , 远程调用函数id
  "args": "", 参数
  "kwargs": "", 参数
  "reqId": "0 18", 请求报文id 响应报文的话就是0
  "orgId": "0 18", 响应原报文id 请求报文的话就是0
  "status": "", 处理状态 200 成功 400 报错 404 找不到函数
  "result": "" 远程调用返回值
}
"""

@CommonDef.singleton
class RpcService:
    def __init__(self):
        self.rpcClient = RpcClient.RpcClient()
        self.rpcServer = RpcServer.RpcServer(self.rpcClient)
        self.rpcServer.addNESCallBack(self.__NESRevHandler)
        self.rpcServer.addCIMCallBack(self.__CIMRevHandler)
        self.__orgNES = {}
        self.__orgNESLock = threading.RLock()
        self.registerServer={} #集群实例总表
        self.setRouteSuccessServer=[] #记录成功来本机注册路由表的实例
    def serverStart(self):
        self.rpcServer.start()
        self.rpcServer.threadPool.submit(self.__addCluster)

    """
    rpc通信调用方法
    """
    def sendRpc(self, ip: str, port: int, funcId, *args, **kwargs):
        #走底层通信NES消息 发送NES消息 对方应答NES消息
        reqId = CommonDef.getId(18)
        rpcTimeOut = int(GlobalVariable.params["rpcTimeOut"])
        with self.__orgNESLock:
            while self.__orgNES.__contains__(reqId):
                reqId = CommonDef.getId(18)
            lock = threading.Condition()
            self.__orgNES[reqId] = {"lock": lock, "result": DefException.CallRpcTimeOutError("响应超时")}
        reqJson = {"funcId": funcId, "args":args, "kwargs": kwargs, "reqId": reqId, "orgId":"0"}
        lock.acquire()
        self.__sendNES(json.dumps(reqJson, ensure_ascii=False), ip, port)
        lock.wait(rpcTimeOut)
        lock.release()

        result = self.__orgNES.get(reqId).get("result")
        with self.__orgNESLock:
            self.__orgNES.pop(reqId)
        if isinstance(result, DefException.CallRpcTimeOutError) is True:
            raise result
        else:
            status = result.get("status")
        if status == "400":
            raise DefException.RpcError(result.get("result"))
        elif status == "404":
            raise DefException.RpcFuncNotFundError(result.get("result"))
        else:
            return result.get("result")
    """
    发送NES消息
    """
    def __sendNES(self, reqJsonStr, ip, port):
        msgId = CommonDef.getId(18)
        sendResult = self.rpcClient.sendNES(msgId, reqJsonStr, ip, port)
        while sendResult == "idRepeat":
            logging.error("NES通信消息id，重复异常。重新随机id")
            msgId = CommonDef.getId(18)
            sendResult = self.rpcClient.sendNES(msgId, reqJsonStr, ip, port)
        logging.debug("发送NES消息: "+reqJsonStr)
    """
    微服务上线规则 非udp广播模式
    先去配置的ip列表里请求集群中的主机获取集群信息 然后注册本机和本机的路由给所有集群里的主机
    """
    def __addCluster(self):
        addressList = GlobalVariable.params.get("clusterAddress")
        localIp = str(GlobalVariable.params.get("rpcIp"))
        localPort = str(GlobalVariable.params.get("rpcPort"))
        time.sleep(3) #等待一会儿 udp服务器起来再执行
        #获取集群实例总列表
        for address in addressList:
            ip = address.split(":")[0]
            port = address.split(":")[1]
            self.registerServer[address] = 0
            try:
                #获取其他主机里的集群主机信息
                serverInstanceList = self.sendRpc(ip, port, "__getServerInstance")
                if serverInstanceList is not None:
                    for item in serverInstanceList:
                        self.registerServer[item] = 0
                break
            except Exception as e:
                logging.error(str(e))
        logging.debug("获取集群实例列表成功: "+ str(self.registerServer))
        while True:
            try:
                for address in self.registerServer.keys():
                    ip = address.split(":")[0]
                    port = address.split(":")[1]
                    if self.registerServer.get(address) == 0:
                        #上线
                        try:
                            self.sendRpc(ip, port, "__setRpcRoute",
                                         {"address": GlobalVariable.params.get("rpcIp") + ":"
                                                     + str(GlobalVariable.params.get("rpcPort")),
                                          "route": getLocalRoute()})
                            msg = localIp + ":" + localPort + ":" + "online"
                            self.rpcClient.sendCIM(msg, ip, port)
                        except Exception as e:
                            logging.exception(exc_info=True, msg="向远程主机注册本机路由表失败 "+ str(e))
                    else:
                        #心跳
                        msg = localIp + ":" + localPort + ":" + "heartbeat"
                        self.rpcClient.sendCIM(msg, ip, port)
                    if address not in self.setRouteSuccessServer:
                        #让对方注册路由
                        msg = localIp + ":" + localPort + ":" + "getRoute"
                        self.rpcClient.sendCIM(msg, ip, port)
            except Exception as e:
                logging.exception(str(e),exc_info=True)
            time.sleep(GlobalVariable.HeartBeatTime)

    """
    处理收到的CIM消息
    """
    def __CIMRevHandler(self, msg):
        logging.debug("收到CIM消息: "+ msg)
        ip = msg.split(":")[0]
        port = msg.split(":")[1]
        thing = msg.split(":")[2] #cim事件
        if thing == "online":
            #主机上线事件
            self.registerServer[ip+":"+port] = time.time()
            #发送本机心跳
            localIp = str(GlobalVariable.params.get("rpcIp"))
            localPort = str(GlobalVariable.params.get("rpcPort"))
            msg = localIp + ":" + localPort + ":" + "heartbeat"
            self.rpcClient.sendCIM(msg, ip, port)
        elif thing == "heartbeat":
            #心跳事件
            self.registerServer[ip+":"+port] = time.time()
        elif thing == "getRoute":
            # 发送本机路由表给远程的主机
            try:
                self.sendRpc(ip, port, "__setRpcRoute",
                             {"address": GlobalVariable.params.get("rpcIp") + ":" + str(GlobalVariable.params.get("rpcPort")),
                              "route": getLocalRoute()})
            except Exception as e:
                logging.exception(exc_info=True, msg="远程主机注册本机路由表失败 " + ip+":"+port + str(e))

    """
    处理收到的NES消息
    """
    def __NESRevHandler(self, msg, revIp, revPort):
        try:
            revJson = json.loads(msg)
        except Exception as e:
            logging.exception(exc_info=True, msg="json 解析异常 "+str(e))
            return
        logging.debug("接收到NES消息: "+ msg)
        orgId = revJson.get("orgId")
        if str(orgId) != "0":
            #响应回调 结束阻塞
            if self.__orgNES.get(orgId) is not None:
                with self.__orgNESLock:
                    self.__orgNES.get(orgId)["result"] = revJson
                lock = self.__orgNES.get(orgId).get("lock")
                lock.acquire()
                lock.notify()
                lock.release()
        else:
            reqId = revJson.get("reqId")
            funcId = revJson.get("funcId")
            fn = GlobalVariable.FuncRoute.get(funcId)
            if fn is None:
                re = {"status": "404", "result": "funcNotFund", "orgId": reqId}
                self.__sendNES(json.dumps(re), revIp, revPort)
            else:
                args = revJson.get("args")
                kwargs = revJson.get("kwargs")
                try:
                    result = fn(*args, **kwargs)
                    status = "200"
                except Exception as e:
                    result = str(e)
                    status = "400"
                re = {"status": status, "result": result, "orgId": reqId}
                try:
                    reJson = json.dumps(re)
                except Exception as e:
                    reJson = json.dumps({"status": "400", "result": str(e), "orgId": reqId})
                self.__sendNES(reJson, revIp, revPort)

"""
返回本机信息
"""
def getServerInstance():
    if instance is not None:
        return list(instance.registerServer.keys())
    else:
        return []

"""
外部主机注册路由表到本机
"""
def setRpcRoute(rpcRoute:dict):
    if rpcRoute is not None:
        address = rpcRoute.get("address")
        route = rpcRoute.get("route")
        with GlobalVariable.FuncRouteRpcLock:
            for funcId in route:
                funcIdInfo = GlobalVariable.FuncRouteRpc.get(funcId)
                if funcIdInfo is None:
                    GlobalVariable.FuncRouteRpc[funcId] = {address:{"errorRadio": 0, "reqNum": 0}}
                else:
                    if funcIdInfo.get(address) is None:
                        funcIdInfo[address] = {"errorRadio": 0, "reqNum": 0}
        logging.debug("收到路由表 "+str(rpcRoute))
        instance.setRouteSuccessServer.append(address)
    return "ok"

"""
获取本机可暴露的路由list
"""
def getLocalRoute():
    re = []
    for item in GlobalVariable.FuncRoute.keys():
        if item[0:2] != "__":
            re.append(item)
    return re
GlobalVariable.FuncRoute["__getServerInstance"] = getServerInstance
GlobalVariable.FuncRoute["__setRpcRoute"] = setRpcRoute
instance = None
