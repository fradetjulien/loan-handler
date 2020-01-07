'''
Loan Handler
'''
import tkinter as tk
import tkinter.messagebox as message
from tkinter import filedialog as fd

FORM_FIELDS = ('First Name', 'Last Name', 'Social Security Number', 'Requested Loan Amount',
               'Loan Duration', 'Interest Rate', 'Income', 'Credit Score')

def import_file():
    '''
    Import a CSV file
    '''
    filename = fd.askopenfilename(initialdir="/", title="Select a file",
                                  filetypes=(("CSV Files", "*.csv"),))
    return filename

def process_request(criterias, entries):
    '''
    Verify that all criterias are respected to give the loan
    '''
    try:
        if 100 * (criterias['annual_interest_payment'] / entries['Income'].get()) > 20 or\
        criterias['loan_to_income'] > 4 or entries['Credit Score'].get() < 600:
            message.showinfo("Error", "Sorry, your request cannot be satisfied.")
            return False
    except Exception as error:
        print('Sorry, failure while processing request.\n{}'.format(error))
        return False
    return True

def init_criterias():
    '''
    Initialize a new dictionnary of criterias
    '''
    criterias = {
        "annual_interest_payment": None,
        "loan_to_income": None,
    }
    return criterias

def compute_criterias(entries):
    '''
    With the recovered datas, determine if the loan is accepted
    '''
    criterias = init_criterias()
    try:
        criterias['annual_interest_payment'] = entries['Requested Loan Amount'].get() * entries['Interest Rate'].get()
        criterias['loan_to_income'] = entries['Requested Loan Amount'].get() / entries['Income'].get()
    except Exception as error:
        print('Error : {}'.format(error))
    return criterias

def handle_fields(entries):
    '''
    Check that all fields have been filled in
    '''
    for field in FORM_FIELDS:
        if not entries[field].get():
            return message.showinfo("Error", "Please, all fields are required.")

def submit_loan(entries):
    '''
    Manage each step to determine if the loan is accepted
    '''
    handle_fields(entries)
    criterias = compute_criterias(entries)
    process_request(criterias, entries)

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
    for field in FORM_FIELDS:
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
