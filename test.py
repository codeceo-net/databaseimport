
from tkinter import *
#创建tkinter窗口
base = Tk()
#屏幕的长度和宽度，以像素和毫米为单位
length_1= base.winfo_screenheight()
width_1= base.winfo_screenwidth()
length_2 = base.winfo_screenmmheight()
width_2 = base.winfo_screenmmwidth()
#screen Depth
screendepth = base.winfo_screendepth()
print("\n width x length (in pixels) = ",(width_1,length_1))
print("\n width x length (in mm) = ", (width_2, length_2))
print("\n Screen depth = ",screendepth)

displayW = 300
displayH = 300

cen_x = (width_1 - displayW) / 2
cen_y = (length_1 - displayH) / 2
# 设置窗口初始大小和位置
size_xy = '%dx%d+%d+%d' % (displayW, displayH, cen_x, cen_y)
base.geometry(f'{size_xy}')

mainloop()