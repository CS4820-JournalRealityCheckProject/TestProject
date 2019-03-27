import sys
from tkinter import messagebox


# メッセージボックス（はい・いいえ）
def resume_yesno(title, msg):
    return messagebox.askyesno(title, msg)


if __name__ == '__main__':
    print('this is')
    print(resume_yesno())
