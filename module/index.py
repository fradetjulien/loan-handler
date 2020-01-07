'''
Loan Handler
'''
import tkinter as tk
import tkinter.messagebox as message
from tkinter import filedialog as fd

form_fields = ('First Name', 'Last Name', 'Social Security Number', 'Requested Loan Amount',
               'Loan Duration', 'Interest Rate', 'Income', 'Credit Score')

def import_file():
    '''
    Import a CSV file
    '''
    filename = fd.askopenfilename(initialdir="/", title="Select a file",
                                  filetypes=(("CSV Files", "*.csv"),))

def submit_loan(entries):
    '''
    '''
    for field in form_fields:
        if not entries[field].get():
            return message.showinfo("Error", "Please, all fields are required.")

def create_buttons(root, entries):
    '''
    Create buttons and setup listener
    '''
    submit = tk.Button(root, text='Submit', command=(lambda e=entries: submit_loan(e)))
    submit.pack(side=tk.LEFT, padx=5, pady=5)
    submit = tk.Button(root, text='Import a CSV file', command=(lambda e=entries: import_file()))
    submit.pack(side=tk.LEFT, padx=5, pady=5)

def set_form(root):
    '''
    Construct the form
    '''
    entries = {}
    for field in form_fields:
        row = tk.Frame(root, bg='white')
        lab = tk.Label(row, width=22, text=field+" : ", anchor='w')
        ent = tk.Entry(row)
        row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        lab.pack(side=tk.LEFT)
        ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
        entries[field] = ent
    return entries

def init_window():
    '''
    Create the GUI application main window
    '''
    root = tk.Tk()
    root.title('Loan Handler')
    return root

if __name__ == '__main__':
    root = init_window()
    entries = set_form(root)
    create_buttons(root, entries)
    root.mainloop()
