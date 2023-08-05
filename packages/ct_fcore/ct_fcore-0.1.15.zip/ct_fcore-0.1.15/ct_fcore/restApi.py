# coding:utf-8
from config import appConfig
import json, copy, logging
from tornado.gen import Task
from tornado import gen
from cache import cacheClient
from tornado.httpclient import AsyncHTTPClient,HTTPRequest
import urllib

client = AsyncHTTPClient()
log = logging.getLogger("ct-fcore.rest_api")

@gen.coroutine
def post(url,body=None,headers=None,cache=None, contentType=None, mode="ucore", access=None):
    if body is None: body={}
    if headers is None: headers={}
    if access is None: access={}
    kwstr = None
    if cacheClient and cache:
        kwcp = {}
        kwcp["url"] = url
        kwcp["headers"] = headers
        kwcp["body"] = body
        kwcp["method"] = "post"
        kwcp["access"] = access
        kwstr = json.dumps(kwcp)
        result = yield Task(cacheClient.get, kwstr)
        if result:
            try:
                resp = eval(result)
            except Exception,e:
                print (e)
                resp = {"error":str(e),"body":result}
            raise gen.Return(resp)
    if "http" not in url:
        url = appConfig.restApiServer+url
    try:
        if contentType:
            headers["Content-Type"] = contentType
        if mode == "ucore":
            # 收拾headers
            if not contentType:
                headers["Content-Type"] = "application/x-www-form-urlencoded"
            for k,v in headers.items(): #headers 只能接收str
                if v:
                    headers[k] = str(headers[k])
                else:
                    del headers[k]
            # 收拾body
            if not isinstance(body, dict):
                body = json.loads(body)
            # 获取数据权限
            if access.get("userId") and access.get("role"):
                filter = yield post(appConfig.accessUri,{
                    "url":url,
                    "userId":access.get("userId"),
                    "role":access.get("role")
                }, mode="json")
                body = dict(filter, **body)
            for k,v in body.items():
                if v is None:
                    del body[k]
            body = urllib.urlencode(body)
            resp = yield client.fetch(HTTPRequest(url=url,method="POST",headers=headers,body=body))
            try:
                resp = json.loads(str(resp.body))
                if resp.get("statusCode") and resp.get("statusCode")!=800:
                    resp = {"error_type":"statusCode is not 800", "response":resp,"body":body,"headers":headers,"url":url}
                    log.error(json.dumps({"error_type":"statusCode is not 800", "response":resp,"body":body,"headers":headers,"url":url}))
            except Exception,e:
                resp = ({"error_type":"json.loads failed!","error":str(e),"response.body":resp.get("body"),"body":body,"headers":headers,"url":url})
                log.error(json.dumps({"error_type":"json.loads failed!","error":str(e),"response.body":resp.get("body"),"body":body,"headers":headers,"url":url}))
        elif mode == "json":
            headers["Content-Type"] = "application/json"
            # 获取数据权限
            if access.get("userId") and access.get("role"):
                filter = yield post(appConfig.accessUri,{
                    "url":url,
                    "userId":access.get("userId"),
                    "role":access.get("role")
                }, mode="json")
                body = dict(filter, **body)
            resp = yield client.fetch(HTTPRequest(url=url,method="POST",headers=headers,body=json.dumps(body)))
            log.info(json.dumps({"response":resp.body,"body":json.dumps(body),"headers":headers,"url":url,"method":"POST"}))
            try:
                resp = json.loads(resp.body)
            except UnicodeDecodeError:
                resp = json.loads(resp.body, encoding="gb2312")
        elif mode == "normal":
            resp = yield client.fetch(HTTPRequest(url=url,method="POST",headers=headers,body=body))
            log.info(json.dumps({"response":resp,"body":body,"headers":headers,"url":url,"method":"POST"}))
        else:
            raise Exception(u"你传入了一个稀奇古怪的mode:{}".format(mode))
    except Exception,e:
        resp={"error":str(e),"error_type":"fetch_error","url":url,"headers":headers,"body":body}
        log.error(json.dumps(resp))
    if cacheClient and cache:
        yield Task(cacheClient.set, kwstr, resp)
    raise gen.Return(resp)


@gen.coroutine
def get(url,headers=None,body=None,cache=None, mode="ucore", access=None):
    if body is None: body={}
    if headers is None: headers={}
    if access is None: access={}
    kwstr = None
    if cacheClient and cache:
        kwcp = {}
        kwcp["url"] = url
        kwcp["headers"] = headers
        kwcp["body"] = body
        kwcp["method"] = "get"
        kwcp["access"] = access
        kwstr = json.dumps(kwcp)
        result = yield Task(cacheClient.get, kwstr)
        if result:
            try:
                resp = eval(result)
            except Exception,e:
                print (e)
                resp = {"error":str(e),"body":result}
            raise gen.Return(resp)
    if "http" not in url:
        url = appConfig.restApiServer+url
    try:
        if mode == "ucore":
            # 获取数据权限
            if access.get("userId") and access.get("role"):
                filter = yield post(appConfig.accessUri,{
                    "url":url,
                    "userId":access.get("userId"),
                    "role":access.get("role")
                }, mode="json")
                body = dict(filter, **body)
            resp = yield client.fetch(HTTPRequest(url=url,method="GET",headers=headers,body=body))
        elif mode == "json":
            # 获取数据权限
            if access.get("userId") and access.get("role"):
                filter = yield post(appConfig.accessUri,{
                    "url":url,
                    "userId":access.get("userId"),
                    "role":access.get("role")
                }, mode="json")
                body = dict(filter, **body)
            resp = yield client.fetch(HTTPRequest(url=url,method="GET",headers=headers,body=json.dumps(body)))
            resp = json.loads(resp.body)
            log.info(json.dumps({"response":resp,"body":body,"headers":headers,"url":url,"method":"GET"}))
        elif mode == "normal":
            resp = yield client.fetch(HTTPRequest(url=url,method="GET",headers=headers,body=body))
            log.info(json.dumps({"response":resp,"body":body,"headers":headers,"url":url,"method":"GET"}))
        else:
            raise Exception(u"你传入了一个稀奇古怪的mode:{}".format(mode))
    except Exception,e:
        resp={"error":str(e),"error_type":"fetch_error","url":url,"headers":headers,"body":body}
        log.error(json.dumps(resp))
    if cacheClient and cache:
        yield Task(cacheClient.set, kwstr, resp)
    raise gen.Return(resp)



