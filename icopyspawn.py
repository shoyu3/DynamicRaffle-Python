import base64

open_icon = open("icon.ico","rb") #icon.ico为你要放入的图标
b64str = base64.b64encode(open_icon.read())  #以base64的格式读出
open_icon.close()
write_data = "img=%s" % b64str
f = open("icon.py","w+")   #将上面读出的数据写入到icon.py的img数组中
f.write(write_data)
f.close()
