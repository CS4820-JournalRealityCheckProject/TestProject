import sys
from tkinter import messagebox


# メッセージボックス（はい・いいえ）
def resume_yesno(title, msg):
    return messagebox.askyesno(title, msg)


def pop_warn_no_doi():
    return messagebox.showwarning('NO-DOI has entries',
                                  'Check No-DOI file.')


if __name__ == '__main__':
    print('this is')
    print(resume_yesno('hi', 'continue?'))
    pop_warn_no_doi()
