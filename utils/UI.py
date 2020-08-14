import tkinter
from tkinter.filedialog import askopenfilename, askdirectory
from os import getcwd


class MyWindow(tkinter.Tk):
    def __init__(self, end_func):
        super().__init__()
        self.title("Wisdom Tests PDF Generator")
        self.wm_geometry('350x300')
        self.frame = tkinter.Frame(self)
        self.resizable(False, False)

        tkinter.Label(self.frame, text='Select Input File :').grid(column=1, row=1, pady=30, sticky='W')
        btn = tkinter.Button(self.frame, text="Choose File", command=self.get_file)
        btn.grid(column=2, row=1, pady=20, sticky='E')
        self.file = tkinter.Label(self.frame, text=f' ')
        self.file.grid(column=1, row=2, columnspan=2)

        tkinter.Label(self.frame, text='Select Destination Folder :').grid(column=1, row=3, pady=20, sticky='W')
        btn2 = tkinter.Button(self.frame, text="Choose Folder", command=self.get_dir)
        btn2.grid(column=2, row=3, pady=20, sticky='E')
        self.folder = tkinter.Label(self.frame, text=f' ')
        self.folder.grid(column=1, row=4, columnspan=2)

        btn3 = tkinter.Button(self.frame, text="Generate", command=lambda: end_func(self.source, self.dest, self.destroy))

        self.source = None
        self.dest = None

        btn3.grid(column=1, rowspan=2, row=5, pady=20, sticky='N')
        self.frame.pack()

    def get_file(self):
        self.source: str = askopenfilename(initialdir=getcwd(), filetypes=(
            ("Excel files", "*.xls;*.xlsx"),
            ("CSV files", "*.csv"),
        ))
        self.file.configure(text=f"Selected File : {self.source.split('/')[-1]}")


    def get_dir(self):
        self.dest = askdirectory(initialdir=getcwd())
        self.folder.configure(text=f"Selected File : {self.dest.split('/')[-1]}")
