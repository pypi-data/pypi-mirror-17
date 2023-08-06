#!/usr/bin/env python
# _*_ coding=gbk _*_

u'''
����UDP��ʽ��ͨ��Э��
'''

import struct
import threading
import time
import socket
import binascii

CMD_SEARCH     = 0x01   # ��ȡ�豸��Ϣ
CMD_UPLOAD     = 0x02   # �ϴ�����
CMD_STARTUP    = 0x03   # ������д����
CMD_STATUS     = 0x04   # ��ȡ����״̬

# ��ӡstr�����Բ鿴
def debug_str(data):
    print  ' '.join(map(hex,map(ord,list(data))))
    
# ��Э�����
def PackData(cmd, data=''):
    u'''����Э���ʽ�������'''
    # ������: ͷ�����������ݳ�
    packlen = len(data)+11
    # ͷ����ʽ: ��־���������
    head = struct.pack('<IBH',0x55AA55AA,cmd,packlen)
    # ����CRCУ��: ͷ��+�հ�CRCռλ+���� һ�����У��
    crc = struct.pack('<I',binascii.crc32(head + struct.pack('<I',0) + data) & 0xffffffff)
    # ��ϳ����հ�
    return head + crc + data

# ��Э����
def UnPackData(data):
    u'''�������'''
    # ���ݳ��Ȳ��ܵ�����Сͷ������
    if not data or len(data)<11:
        return None
    rcrc = binascii.crc32(data[:7] + struct.pack('<I',0) + data[11:]) & 0xffffffff
    #debug_str(data)
    # ����ͷ���ֶ�
    flag,cmd,datalen,crc = struct.unpack('<IBHI',data[:11])
    #print hex(rcrc),hex(crc)
    if flag!=0x55AA55AA or datalen!=len(data) or rcrc!=crc:
        return None
    # ��֤ͨ���󷵻�ָ������ݲ���
    return cmd,data[11:]
    
# �㲥��ʽ�����豸�б�
def Search(listctrl):
    devlist = []
    try:
        # ��õ�ǰ��������Ӧ��IP
        addr = socket.getaddrinfo(socket.gethostname(),None)[-1][4][0]
        # Ŀ�ĵ�ַ�ǹ㲥
        dest = ('<broadcast>', 8081)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(5)
        # �󶨵�ǰIP�����Զ�ʹ�õ�ǰ���η��㲥
        s.bind((addr, 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, True)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        # ��������
        sendpack = PackData(0x01)
        #debug_str(sendpack)        
        s.sendto(sendpack, dest)
        n=0;
        while True:
            data, addr = s.recvfrom(1024)
            if data:
                rspcmd,data = UnPackData(data)
                if data and rspcmd==0x81:
                    # �����豸��Ӧ���豸��Ϣ
                    id,type,ver,sn,uuid = struct.unpack('<BBH16sI',data)
                    # print id,type,ver,sn,hex(uuid),hex(crc)
                    listctrl.InsertStringItem(n, str(id))
                    listctrl.SetStringItem(n, 1, str(hex(uuid)).upper())
                    listctrl.SetStringItem(n, 2, str(hex(ver))[2:])
                    listctrl.SetStringItem(n, 3, str(type))
                    listctrl.SetStringItem(n, 4, addr[0])
                    #listctrl.SetStringItem(n, 5, sn)
                    devlist.append((n,id,uuid,type,ver,sn,addr[0]))
                    n=n+1
        s.close()
    except:
        print 'err or timeout\n'
        s.close()
        pass
    print 'Search Finish.\n'
    return devlist

#�ϴ��ļ�ʱ�������ݰ�
def sendpack(s,dest,i,data):
    try:
        data = struct.pack('<H',i) + data
        s.sendto(PackData(0x02,data), dest)
        data, addr = s.recvfrom(1024)
        if data:
            rspcmd,data = UnPackData(data)
            if data and rspcmd==0x82:
                num,result = struct.unpack('<HB',data)
                #print 'num=',num,'ret=',result
                if num==i and result==0:
                    return True
                else:
                    return False
    except:
        print "senddata fail\n"
        return False

# �ϴ��ļ�����
def Upload(addr,data):        
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(5)
        i = 0 #�����
        # ѭ����ȡ���ݷ���,ÿ��512�ֽ�
        while len(data) > 0:
            if len(data) >= 512:
                block = data[0:512]
            else:
                block = data
            #print 'pack=',i,'len=',len(block)
            if sendpack(s,(addr, 8081),i,block):                    
                i=i+1
                data = data[512:]
            else:
                #����һ��ʧ��
                s.close()
                return False
        if len(data) == 0:#��ʾ��������
            s.close()
            return True
    except:
        print 'send udp timeout or err\n'
        s.close()
        pass

# �����̼�����
def StartUp(dest,key):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(5)
        # ��������
        sendpack = PackData(0x03,struct.pack('<B',1)+struct.pack('<I',key))
        #debug_str(sendpack)        
        s.sendto(sendpack, (dest,8081))
        while True:
            data, addr = s.recvfrom(1024)
            if data:
                rspcmd,data = UnPackData(data)
                if data and rspcmd==0x83:
                    result = struct.unpack('<B',data)
                    if result:
                        return True
                    else:
                        return False
        s.close()
    except:
        print 'err or timeout\n'
        s.close()
        return False

if __name__=="__main__":
    # ����
    t=PackData(5,'abcdefg')
    print UnPackData(t)
    
    SearchThread()
    pass