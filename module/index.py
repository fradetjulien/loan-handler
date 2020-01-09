'''
Loan Handler
'''
import tkinter as tk
import tkinter.messagebox as message
from tkinter import filedialog as fd

FORM_FIELDS = ('First Name', 'Last Name', 'Social Security Number', 'Requested Loan Amount',
               'Interest Rate', 'Income', 'Credit Score', 'Home Value')

class Application(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.create_widgets()

    def create_widgets(self):
        self.quit_button = tk.Button(self, text='Quit', command=self.quit)

def clear_fields():
    '''
    Clear every fields present in the window
    '''
    return

def import_file():
    '''
    Import a CSV file
    '''
    filename = fd.askopenfilename(initialdir="/", title="Select a file",
                                  filetypes=(("CSV Files", "*.csv"),))
    return filename

def display_informations(criterias, entries):
    '''
    Display a summary of all informations
    '''
    message.showinfo("Success", "Congratulations, your loan has been accepted.")
    message.showinfo("Informations", "First Name : {}\nLast Name : {}\n"
                     "Income : ${}\nSocial Security Number : {}\nCredit Score : {}\n"
                     "Requested Loan Amount : ${}\nInterest Rate : {}%\nHome Value : ${}\n"
                     "Annual Interest Payment : $ {}\nInterest Payment to income : {}%\n"
                     "Loan to Home : {}%".format(entries['First Name'], entries['Last Name'],
                                                 entries['Income'],
                                                 entries['Social Security Number'],
                                                 entries['Credit Score'],
                                                 entries['Home Value'],
                                                 entries['Requested Loan Amount'],
                                                 entries['Interest Rate'],
                                                 criterias['annual_interest_payment'],
                                                 criterias['interest_payment_to_income'],
                                                 criterias['loan_to_home']))

def process_request(criterias, entries):
    '''
    Verify that all criterias are respected to give the loan
    '''
    if criterias['fail_number'] > 0:
        message.showinfo("Error", "Sorry, your request cannot be satisfied.")
        display_informations(criterias, entries)
        return False
    return True

def set_state(criterias):
    '''
    Depending on values, determine if tests are passed or failed
    '''
    if criterias['interest_payment_to_income']['value'] <= 0.25:
        criterias['interest_payment_to_income']['state'] = "Pass"
        criterias['fail_number'] = criterias['fail_number'] - 1
    if criterias['loan_to_home']['value'] <= 0.8:
        criterias['loan_to_home']['state'] = "Pass"
        criterias['fail_number'] = criterias['fail_number'] - 1
    if criterias['credit_score']['value'] > 650:
        criterias['credit_score']['state'] = "Pass"
        criterias['fail_number'] = criterias['fail_number'] - 1
    return criterias

def init_criterias(entries):
    '''
    Initialize a new dictionnary of criterias
    '''
    criterias = {
        "annual_interest_payment": None,
        "interest_payment_to_income": {
            "value": None,
            "state": "Fail"
        },
        "loan_to_home": {
            "value": None,
            "state": "Fail"
        },
        "credit_score": {
            "value": int(entries['Credit Score'].get()),
            "state": "Fail"
        },
        "fail_number": 3
    }
    return criterias

def compute_criterias(entries):
    '''
    With the recovered data, determine the values of the different criterias
    '''
    criterias = init_criterias(entries)
    try:
        criterias['annual_interest_payment'] = int(int(entries['Requested Loan Amount'].get())\
                                               * float(entries['Interest Rate'].get()) / 100)
        criterias['interest_payment_to_income']['value'] = int(criterias['annual_interest_payment']\
                                                            / int(entries['Income'].get()))
        criterias['loan_to_home']['value'] = int(int(entries['Requested Loan Amount'].get()))\
                                                / int(entries['Home Value'].get())
    except Exception as error:
        print('Error : {}'.format(error))
        return False
    return set_state(criterias)

def correct_credit_score(entries):
    '''
    Check if the Credit Score is a number between 0 and 850
    '''
    try:
        if int(entries['Credit Score'].get()) < 0 or int(entries["Credit Score"].get()) > 850:
            message.showinfo("Error", "Your Credit Score is invalid.")
            return False
    except Exception as error:
        message.showinfo("Error", "Please, insert a number for the Credit Score.")
        print("Error : {}".format(error))
        return False
    return True

def handle_fields(entries):
    '''
    Check that all fields have been filled in
    '''
    for field in FORM_FIELDS:
        if not entries[field].get():
            message.showinfo("Error", "Please, all fields are required.")
            return False
    return True

def submit_loan(entries):
    '''
    Manage each step to determine if the loan is accepted
    '''
    if not handle_fields(entries) or not correct_credit_score(entries):
        return False
    criterias = compute_criterias(entries)
    if not criterias:
        message.showinfo("Error", "Sorry, your request cannot be satisfied.")
        return False
    if process_request(criterias, entries):
        display_informations(criterias, entries)
        return True
    return False

def create_buttons(root, entries):
    '''
    Create buttons and setup listener
    '''
    submit = tk.Button(root, highlightbackground='black', text='Submit',
                       command=(lambda e=entries: submit_loan(e)))
    submit.pack(side=tk.LEFT, padx=5, pady=5)
    submit = tk.Button(root, highlightbackground='black', text='Import a CSV file',
                       command=(lambda e=entries: import_file()))
    submit.pack(side=tk.LEFT, padx=5, pady=5)
    submit = tk.Button(root, highlightbackground='black', text='Clear fields',
                       command=(lambda e=entries: clear_fields()))
    submit.pack(side=tk.LEFT, padx=5, pady=5)

def create_radio_buttons(root, entries):
    '''
    Radio buttons to decide the loan duration
    '''
    var = tk.IntVar()
    row = tk.Frame(root, bg='white')
    lab = tk.Label(row, width=22, text='Loan Duration : ', anchor='w')
    radiobutton_1 = tk.Radiobutton(root, variable=var, text="5 years",
                                   value=5, background='black')
    radiobutton_2 = tk.Radiobutton(root, variable=var, text="15 years",
                                   value=15, background='black')
    radiobutton_3 = tk.Radiobutton(root, variable=var, text="30 years",
                                   value=30, background='black')
    row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
    lab.pack(side=tk.LEFT)
    radiobutton_1.pack(anchor='w')
    radiobutton_2.pack(anchor='w')
    radiobutton_3.pack(anchor='w')
    entries['Loan Duration'] = var
    return entries

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
    entries = create_radio_buttons(root, entries)
    return entries

def init_window():
    '''
    Create the GUI application main window
    '''
    root = tk.Tk()
    root.title('Loan Handler')
    return root

if __name__ == '__main__':
    ROOT = init_window()
    ENTRIES = set_form(ROOT)
    create_buttons(ROOT, ENTRIES)
    ROOT.mainloop()
