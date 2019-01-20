import tkinter as tk


class Application(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.said = False
        self.master = master
        self.pack()
        self.create_widget()

    def create_widget(self):
        self.say_hello = tk.Button(self)
        self.say_hello["text"] = "my first app"
        self.say_hello["command"] = self.speak
        self.say_hello.pack(side="top")

        self.quit = tk.Button(self, text = "QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")

    def speak(self):
        print("Clicked")
        if self.said:
            self.say_hello["text"] = "hello"
        else:
            self.say_hello["text"] = "goodbye"
        self.said = not self.said

root = tk.Tk()
app = Application(master=root)
app.mainloop()

