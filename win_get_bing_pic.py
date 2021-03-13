# -*- coding: utf-8 -*-
from urllib import request
import sys, os
import time, types, json
import os.path as op
import win32api, win32con, win32gui

# default_encoding = 'utf-8'
# if sys.getdefaultencoding() != default_encoding:
# 	reload(sys)
# 	sys.setdefaultencoding(default_encoding)

TRY_TIMES = 1
DEFAULT_PIC_PATH = ""

if DEFAULT_PIC_PATH == "":
	DEFAULT_PIC_PATH = os.path.expanduser("~") + "\\Pictures\\Bing"

def schedule(a,b,c):
	per = 100.0 * a * b / c
	if per > 100 :
		print("\r100.00%")
		return
	print("\r%.2f%%" % per, end="")

def get_pic_URL():
	bing_json = ''
	req = request.Request(
		url = 'http://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1'
	)
	i = TRY_TIMES
	while True:
		try:
			bing_json = request.urlopen(req).read()
		except request.HTTPError as e:
			print(e)
			i = i - 1
			if i == 0:
				break
			time.sleep(5)
		else :
			break

	if bing_json:
		bing_dic = json.loads(bing_json)
		if bing_dic != None:
			return "http://cn.bing.com%s" % bing_dic['images'][0]['url']

	print("无法获取URL！")
	return ""

def set_wallpaper(pic_path):	
	if sys.platform == 'win32':
		k = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER, 'Control Panel\Desktop', 0, win32con.KEY_ALL_ACCESS)
		curpath = win32api.RegQueryValueEx(k, 'Wallpaper')[0]
		if curpath == pic_path:
			pass
		else:
			# win32api.RegSetValueEx(k, "WallpaperStyle", 0, win32con.REG_SZ, "2")#2 for tile,0 for center
			# win32api.RegSetValueEx(k, "TileWallpaper", 0, win32con.REG_SZ, "0")
			win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, pic_path, 1+2)
		win32api.RegCloseKey(k)
	else:
		curpath = commands.getstatusoutput('gsettings get org.gnome.desktop.background picture-uri')[1][1:-1]
		if curpath == pic_path:
			pass
		else:
			commands.getstatusoutput('DISPLAY=:0 gsettings set org.gnome.desktop.background picture-uri "%s"' % (picpath))


try:
	print("开始运行。")
	localtime = time.localtime(time.time())
	url = get_pic_URL()
	if url != '':
		print("URL:" + url)
		pic_name = url.split('/')[-1].split('&')[0].split('OHR.')[-1]
		pic_name = "%04d.%02d.%02d.%s" % (localtime.tm_year, localtime.tm_mon, localtime.tm_mday, pic_name)
		pic_path = "%s\\%s" % (DEFAULT_PIC_PATH, pic_name)
		if os.path.exists(pic_path):
			print("图片已存在！")
			exit()
		print("图片名：" + pic_name)
		print("开始下载...")
		try:
			request.urlretrieve(url, pic_path, schedule)
			set_wallpaper(pic_path)
			print("成功")
		except Exception as e:
			print(e)
			exit()
except KeyboardInterrupt:
	pass

