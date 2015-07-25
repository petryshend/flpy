from Tkconstants import TOP, BOTTOM
from Tkinter import Tk, Entry, Label, mainloop, Button, StringVar, Frame
from credentials import Credentials
from women_done import WomenDone


class Gui:

    def __init__(self):
        self.root = Tk()
        self.credentials_frame = Frame(self.root)
        self.women_done_frame = Frame(self.root)
        self.credentials_frame.pack(side=TOP)
        self.women_done_frame.pack(side=BOTTOM)
        self.username_entry_variable = StringVar()
        self.username_entry_variable.set(Credentials.get()['username'])
        self.password_entry_variable = StringVar()
        self.password_entry_variable.set(Credentials.get()['password'])
        self.username_entry = Entry(self.credentials_frame, textvariable=self.username_entry_variable)
        self.password_entry = Entry(self.credentials_frame, textvariable=self.password_entry_variable)

    def start(self):
        self.construct_credentials_fields()
        self.construct_women_done_frame()
        mainloop()

    def construct_credentials_fields(self):
        username_label = Label(self.credentials_frame, text='Username')
        password_label = Label(self.credentials_frame, text='Password')
        username_label.grid(row=0, column=0)
        password_label.grid(row=1, column=0)

        save_button = Button(self.credentials_frame, text='Save', command=self.save_credentials)
        start_mailer_button = Button(self.credentials_frame, text='Start mailer', command=self.close_gui)

        self.username_entry.grid(row=0, column=1)
        self.password_entry.grid(row=1, column=1)
        save_button.grid(row=2, column=0)
        start_mailer_button.grid(row=2, column=1)

    def construct_women_done_frame(self):
        wd = WomenDone()
        women_done = wd.get()
        if len(women_done):
            clear_all_button = Button(
                self.women_done_frame,
                text="Clear ALL",
                command=self.clear_all,
                bg="lightblue"
            )
            clear_all_button.pack()
            buttons = []
            for i, woman in enumerate(women_done):
                button = Button(
                    self.women_done_frame,
                    text="Clear " + str(woman),
                    command=lambda url=woman: self.clear_woman(url)
                )
                buttons.append(button)
            for button in buttons:
                button.pack()

    def save_credentials(self):
        credentials = {
            'username': self.username_entry_variable.get(),
            'password': self.password_entry_variable.get()
        }
        Credentials.save(credentials)

    def clear_woman(self, url):
        wd = WomenDone()
        wd.remove(url)
        print "Cleared: " + str(url)

    def clear_all(self):
        wd= WomenDone()
        wd.clear()
        print "Cleared All"

    def close_gui(self):
        self.root.destroy()

