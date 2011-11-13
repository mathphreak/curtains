import server
import tkinter

class CreateDialog(tkinter.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.grid(row=0, column=0)

        self.nameVar = tkinter.StringVar()
        self.pathVar = tkinter.StringVar()
        nameLabel = tkinter.Label(self, text="Name of movie:")
        pathLabel = tkinter.Label(self, text="Path to file:")
        nameEntry = tkinter.Entry(self, textvariable=self.nameVar)
        pathEntry = tkinter.Entry(self, textvariable=self.pathVar)
        browseButton = tkinter.Button(self, text="Browse...", command=self.browseClicked)
        okButton = tkinter.Button(self, text="OK", command=self.submit)
        cancelButton = tkinter.Button(self, text="Cancel", command=lambda *ignore: self.parent.destroy())

        nameLabel.grid(row=0, column=0, sticky=tkinter.W, pady=3, padx=3)
        nameEntry.grid(row=0, column=1, columnspan=2, sticky=tkinter.EW, pady=3, padx=3)
        pathLabel.grid(row=1, column=0, sticky=tkinter.W, pady=3, padx=3)
        pathEntry.grid(row=1, column=1, sticky=tkinter.EW, pady=3, padx=3)
        browseButton.grid(row=1, column=2, sticky=tkinter.EW, pady=3, padx=3)
        okButton.grid(row=2, column=1, sticky=tkinter.E, pady=3, padx=3)
        cancelButton.grid(row=2, column=2, sticky=tkinter.EW, pady=3, padx=3)

        nameEntry.focus_set()
        parent.bind("<Escape>", lambda *ignore: self.parent.destroy())

    def browseClicked(self, *ignore):
        filename = tkinter.filedialog.askopenfilename(
            title="curtain - select " + self.nameVar.get() + " file",
            initialdir=".",
            filetypes=[("Video files", "*." + server.video_file_extension)],
            defaultextension="." + server.video_file_extension,
            parent=self.parent)
        self.pathVar.set(filename)

    def submit(self, *ignore):
        name, path = (self.nameVar.get(), self.pathVar.get())
        server.DB.add(name, path)

if __name__ == "__main__":
    application = tkinter.Tk()
    application.title("Create Movie - curtains")
    window = CreateDialog(application)
    application.protocol("WM_DELETE_WINDOW", lambda *ignore: application.destroy())
    application.mainloop()
