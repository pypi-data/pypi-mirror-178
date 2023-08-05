from BroachRpc.common import GlobalVariable
from BroachRpc.exception import DefException
import logging
import time
from BroachRpc.network import RpcService

"""
rpc装饰器 获取程序启动时的函数路由表
"""
def rpcRoute(name=None):
    def getFun(fn):
        if name is None:
            routeName = fn.__name__
        else:
            routeName = name
        if GlobalVariable.FuncRoute.get(routeName) is None:
            GlobalVariable.FuncRoute[routeName] = fn
            logging.debug("function: "+routeName+" registry route success")
        else:
            logging.error(routeName+" registry route fail，name is replace")
        return fn
    return getFun

"""
rpc装饰器 调用rpc服务
"""
def rpcCall(name=None, timeoutNum=2):
    def getFun(fn):
        def getParams(*args, **kwargs):
            if name is None:
                routeName = fn.__name__
            else:
                routeName = name
            if routeName in GlobalVariable.FuncRoute.keys():
                logging.info("调用内部函数 -> "+routeName)
                rpcFn = GlobalVariable.FuncRoute.get(routeName)
                return rpcFn(*args, **kwargs)
            else:
                if routeName in GlobalVariable.FuncRouteRpc.keys():
                    rpcFnInfo = GlobalVariable.FuncRouteRpc.get(routeName)
                    if rpcFnInfo is not None:
                        #获取请求地址
                        with GlobalVariable.FuncRouteRpcLock:
                            reqAddress = getAddress(rpcFnInfo, timeoutNum)
                        if reqAddress == "":
                            raise DefException.RpcFuncNotFundError(routeName+" 没有可用的实例")
                        ip = reqAddress.split(":")[0]
                        port = reqAddress.split(":")[1]
                        result = RpcService.instance.sendRpc(ip,port,routeName, *args, **kwargs)
                        return result
                    else:
                        raise DefException.RpcFuncNotFundError(routeName+" 没有实例")
                else:
                    raise DefException.RpcFuncNotFundError(routeName+" 没有实例")
        return getParams
    return getFun

def getAddress(rpcFnInfo, num):
    ipList = rpcFnInfo.keys()
    minReqNum = 100
    address=""
    for addressItem in ipList:
        info = rpcFnInfo.get(addressItem)
        reqNum = info.get("reqNum")
        if reqNum >= 100:
            info["reqNum"] = 0
            reqNum = 0
        if reqNum < minReqNum and (time.time() - RpcService.instance.registerServer.get(addressItem)) <= GlobalVariable.HeartBeatTime*num :
            minReqNum = reqNum
            address = addressItem
    if address != "":
        rpcFnInfo.get(address)["reqNum"] = minReqNum + 1
    return address