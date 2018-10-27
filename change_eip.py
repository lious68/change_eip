#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sdk import UcloudApiClient
from config import *
import sys
import json

arg_length = len(sys.argv)
ApiClient = UcloudApiClient(base_url, public_key, private_key)
region = 'cn-south-02'


def CreateEip(): #创建EIP，并返回EIPId
    Parameters = {"Action": "AllocateEIP", "OperatorName": "Bgp", "Bandwidth": "2", "ChargeType": "Dynamic","Region": region}
    response = ApiClient.get("/", Parameters)
    return response['EIPSet'][0]['EIPId']

def  BindEIP(eip,uhostid): #绑定EIP，传入EIP和uhost ID参数。
     Parameters={
            "Action":"BindEIP",
            "EIPId":eip,
            "ResourceId":uhostid,
            "ResourceType":"uhost",
            "Region":region
            }
     response = ApiClient.get("/", Parameters);

def  UnBindEIP(eip,uhostid):  #解绑EIP，传入EIP和uhost的Id参数。
     Parameters={
            "Action":"UnBindEIP",
            "EIPId":eip,
            "ResourceId":uhostid,
            "ResourceType":"uhost",
            "Region":region
            }
     response = ApiClient.get("/", Parameters);


def ReleaseEIP(oldeip):
	Parameters={"Action":"ReleaseEIP","EIPId":oldeip,"Region":region}
	response = ApiClient.get("/", Parameters)


def GetEIPId(seq): #获取EIP和uhost的ID，并返回数组[eipid,uhostid]

    Parameters = {
        "Action": "DescribeUHostInstance",
        "Region": region,
    }
    response = ApiClient.get("/", Parameters)
    if (response['UHostSet'][seq]['IPSet'][1]['IPId']): #判断是否有公网IP
    	host_array = [response['UHostSet'][seq]['IPSet'][1]['IPId'],response['UHostSet'][seq]['UHostId']]
    	return host_array
    else:
    	print 'NO eip'

def main(): #主函数，组装逻辑，获取原EIP和UHOST--->创建新EIP-->绑定EIP--->卸载原来EIP--->释放原来EIP
    for seq in range(1,3):  #需要更换主机的顺序和数量，比如更换1-100台，则填(0,99)
        print "start the %d uhost"%seq
        host = GetEIPId(seq)
        eipnew = CreateEip()
        BindEIP(eipnew,host[1])
        UnBindEIP(host[0],host[1])
        ReleaseEIP(host[0])
        print "finished the %d uhost" %seq


if __name__=='__main__':
    main()