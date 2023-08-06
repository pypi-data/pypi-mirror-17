#!/usr/bin/env python
# _*_ coding=gbk _*_


import wx
import threading
import func
import images
import udp
import uart
import binascii


class MyFrame(wx.Frame):
    def __init__(self):
        self.devlist = []
        wx.Frame.__init__(self, parent=None, title=u"ά������", 
            size=(520,384), style=wx.SYSTEM_MENU|wx.CAPTION|wx.CLOSE_BOX|wx.MINIMIZE_BOX)  
        
        # ���Panel���  
        panel = wx.Panel(parent=self)  

        # ��ʾ�豸�б�
        self.list_ctrl = wx.ListCtrl(parent=panel, pos=(5,5), size=(504,200), style=wx.LC_REPORT|wx.BORDER_SUNKEN)
        self.list_ctrl.InsertColumn(0, u'ID', width=30)
        self.list_ctrl.InsertColumn(1, u'UUID', width=70)
        self.list_ctrl.InsertColumn(2, u'VER', width=60)
        self.list_ctrl.InsertColumn(3, u'TYPE', width=50)
        self.list_ctrl.InsertColumn(4, u'IP', width=100)
        self.list_ctrl.InsertColumn(5, u'SN', width=130)
        self.list_ctrl.InsertColumn(6, u'.', width=40)

        # self.list_ctrl.InsertStringItem(0, '1')
        # self.list_ctrl.SetStringItem(0, 1, "AAAABBCC")
        # self.list_ctrl.SetStringItem(0, 2, "V%2.2f"%10.01)
        self.viewmenu = wx.Menu() 
        mmi = wx.MenuItem(self.viewmenu, wx.NewId(),u'ˢ���豸')  
        self.viewmenu.AppendItem(mmi)
        # �󶨲˵����¼�  
        self.viewmenu.Bind(wx.EVT_MENU, self.OnRightDown_ref, mmi) 
        # ���б��Ҽ������¼�
        self.list_ctrl.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
        
        self.staticText3 = wx.StaticText(parent=panel, label=u'�ļ�·��:', 
            pos=wx.Point(5, 200+12), size=wx.Size(60, 24), style=0)
              
        # �ļ�·����ʾ
        self.textCtrl_BinPath1 = wx.TextCtrl(parent=panel, pos=wx.Point(80, 200+10),
            size=wx.Size(370, 24), style=0, value=u'')
        self.textCtrl_BinPath1.Bind(wx.EVT_KILL_FOCUS, self.OnTextCtrl_BinPath1KillFocus)

        # ��ѡ���ļ��Ի���
        self.button_BinPath1 = wx.Button(label=u'���',parent=panel,
            pos=wx.Point(460, 200+10), size=wx.Size(50, 24), style=0)
        self.button_BinPath1.Bind(wx.EVT_BUTTON, self.OnButton_BinPath1Button)

        self.staticBox1 = wx.StaticBox(parent=panel, label=u'ѡ��', 
            pos=wx.Point(5,243), size=wx.Size(400,105), style=0)
        
        # ִ����������
        self.btn=wx.Button(parent=panel, label= u'��ʼ����', pos=(410, 250), size=(100, 100))  
        # �󶨰�ť�����¼�
        self.btn.Bind(wx.EVT_BUTTON, self.OnMyButtonClick)

        #self.icon = wx.Icon('logo.ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(images.AppIcon.GetIcon())
        self.Centre() #������ʾ
        self.Show(True)#����һ��������ʾFrame���

        threading.Thread(target=self.SearchThread).start()
        
    def OnRightDown(self,event):
        self.PopupMenu(self.viewmenu,event.GetPosition())
        
    def OnRightDown_ref(self,event):
        self.list_ctrl.DeleteAllItems()
        self.devlist = []
        threading.Thread(target=self.SearchThread).start()
        
    def OnTextCtrl_BinPath1KillFocus(self, event):
        func.check_file_exist(self.textCtrl_BinPath1,1)
        event.Skip()
        
    def OnButton_BinPath1Button(self, event):
        func.set_file_path(self,self.textCtrl_BinPath1)
        event.Skip()
        
    def OnMyButtonClick(self,event):
        if self.textCtrl_BinPath1.GetValue() and self.list_ctrl.GetItemCount()>0:
            self.Upgrade()
        else:
            wx.MessageDialog(None, u"��ѡ��̼��ļ�!", u"����", wx.OK | wx.ICON_HAND).ShowModal()

    # �㲥��ʽ�����豸�б�
    def SearchThread(self):
        self.devlist = udp.Search(self.list_ctrl)

    def Upgrade(self):
        if self.list_ctrl.GetItemCount() == 0:
            wx.MessageDialog(None, u"���豸!", u"����", wx.OK | wx.ICON_HAND).ShowModal()
            return
        
        for i in range(self.list_ctrl.GetItemCount()):
            self.list_ctrl.SetItemBackgroundColour(i, "white")

        for i in range(self.list_ctrl.GetItemCount()):
            addr = self.list_ctrl.GetItemText(i,4)
            image = file(self.textCtrl_BinPath1.GetValue(), 'rb').read()
            if udp.Upload(addr,image):
                if udp.StartUp(addr,binascii.crc32(image) & 0xffffffff):
                    self.list_ctrl.SetStringItem(i, 6, 'OK')
                    self.list_ctrl.SetItemBackgroundColour(i, "green")
                else:
                    self.list_ctrl.SetStringItem(i, 6, 'ERR')
                    self.list_ctrl.SetItemBackgroundColour(i, "red")                   
            else:
                self.list_ctrl.SetStringItem(i, 6, 'ERR')
                self.list_ctrl.SetItemBackgroundColour(i, "red")

    # ��ӡstr�����Բ鿴
    def debug_str(self, data):
        print  ' '.join(map(hex,map(ord,list(data))))
        
if __name__=="__main__":
    app = wx.App()
    MyFrame()
    app.MainLoop()  
    
