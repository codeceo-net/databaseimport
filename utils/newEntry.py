from tkinter import END
from tkinter.ttk import Entry
'''
自定义输入框
'''
class newEntry(Entry):
    def __init__(self, master=None, placeholder="PLACEHOLDER", color="grey"):
        super().__init__(master)

        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self["foreground"]

        self.bind("<FocusIn>", self.foc_in)
        self.bind("<FocusOut>", self.foc_out)

        self.put_placeholder()

    def put_placeholder(self):
        self.insert(0, self.placeholder)
        self["foreground"] = self.placeholder_color

    def foc_in(self, *args):
        aStr = self.placeholder_color.strip()
        bStr = str(self['foreground']) # _tkinter.Tcl_Obj对象转字符串 #print(type(a),type(b)) 打印变量类型
        cStr = self.get().strip()
        if aStr  ==  bStr and cStr == self.placeholder:
            self.delete("0", END)
            self["foreground"] = self.default_fg_color
    def foc_out(self, *args):
        if not self.get():
            self.put_placeholder()