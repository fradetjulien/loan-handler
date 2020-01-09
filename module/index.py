'''
Loan Handler
'''
import tkinter as tk
import tkinter.messagebox as message
from tkinter import filedialog as fd
import pandas as pd

FORM_FIELDS = ('First Name', 'Last Name', 'Social Security Number', 'Requested Loan Amount',
               'Interest Rate', 'Income', 'Credit Score', 'Home Value')

class Application:
    '''
    Create the GUI application main window
    '''
    def __init__(self, root):
        self.root = root
        self.root.title('Loan Handler')
        self.entries = {}
        self.create_widgets()

    def create_widgets(self):
        '''
        Create all fields, buttons and radios buttons inside the window
        '''
        self.set_form()
        self.create_buttons()
        self.create_radio_buttons()

    def set_form(self):
        '''
        Construct the form
        '''
        for field in FORM_FIELDS:
            row = tk.Frame(self.root, bg='white')
            lab = tk.Label(row, width=22, text=field+" : ", anchor='w')
            ent = tk.Entry(row)
            row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
            lab.pack(side=tk.LEFT)
            ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
            self.entries[field] = ent

    def create_buttons(self):
        '''
        Create buttons and setup listener
        '''
        submit = tk.Button(self.root, highlightbackground='black', text='Submit',
                           command=(lambda e=self.entries: self.submit_loan(e)))
        submit.pack(side=tk.LEFT, padx=5, pady=5)
        submit = tk.Button(self.root, highlightbackground='black', text='Import a CSV file',
                           command=(lambda e=self.entries: self.import_file(e)))
        submit.pack(side=tk.LEFT, padx=5, pady=5)
        submit = tk.Button(self.root, highlightbackground='black', text='Clear fields',
                           command=(lambda e=self.entries: self.clear_fields(self.entries)))
        submit.pack(side=tk.LEFT, padx=5, pady=5)
        submit = tk.Button(self.root, highlightbackground='black', text='Quit',
                           command=(lambda e=self.entries: self.root.quit()))
        submit.pack(side=tk.LEFT, padx=5, pady=5)

    def create_radio_buttons(self):
        '''
        Radio buttons to decide the loan duration
        '''
        var = tk.IntVar()
        row = tk.Frame(self.root, bg='white')
        lab = tk.Label(row, width=22, text='Loan Duration : ', anchor='w')
        radiobutton_1 = tk.Radiobutton(self.root, variable=var, text="5 years",
                                       value=5, background='black')
        radiobutton_2 = tk.Radiobutton(self.root, variable=var, text="15 years",
                                       value=15, background='black')
        radiobutton_3 = tk.Radiobutton(self.root, variable=var, text="30 years",
                                       value=30, background='black')
        row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        lab.pack(side=tk.LEFT)
        radiobutton_1.pack(anchor='w')
        radiobutton_2.pack(anchor='w')
        radiobutton_3.pack(anchor='w')
        self.entries['Loan Duration'] = var

    @staticmethod
    def clear_fields(entries):
        '''
        Clear every fields present in the window
        '''
        for field in FORM_FIELDS:
            entries[field].delete(0, 'end')

    @staticmethod
    def import_file(entries):
        '''
        Import a CSV file and filled in entries from values
        '''
        file_path = fd.askopenfilename(initialdir="/", title="Select a file",
                                       filetypes=(("CSV Files", "*.csv"),))
        df = pd.read_csv(file_path)
        i = 0
        for field in FORM_FIELDS:
            entries[field].delete(0, 'end')
            entries[field].insert(0, df['Value'][i])
            i = i + 1

    @staticmethod
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
            message.showinfo("Success", "Congratulations, your loan has been accepted.")
            display_informations(criterias, entries)
            return True
        return False

def handle_fields(entries):
    '''
    Check that all fields have been filled in
    '''
    for field in FORM_FIELDS:
        if not entries[field].get():
            message.showinfo("Error", "Please, all fields are required.")
            return False
    return True

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

def process_request(criterias, entries):
    '''
    Verify that all criterias are respected to give the loan
    '''
    if criterias['fail_number'] > 0:
        message.showinfo("Error", "Sorry, your request cannot be satisfied.")
        display_informations(criterias, entries)
        return False
    return True

def display_informations(criterias, entries):
    '''
    Display a summary of all informations
    '''
    message.showinfo("Informations", "First Name : {}\nLast Name : {}\n"
                     "Income : ${}\nSocial Security Number : {}\n"
                     "Requested Loan Amount : ${}\nInterest Rate : {}%\nHome Value : ${}\n"
                     "Annual Interest Payment : $ {}\n"
                     "Interest Payment to income : {}% - State : {}\n"
                     "Loan to Home : {}% - State : {}\n"
                     "Credit Score : {}"
                     " - State : {}\n".format(entries['First Name'].get(),
                                              entries['Last Name'].get(),
                                              entries['Income'].get(),
                                              entries['Social Security Number'].get(),
                                              entries['Requested Loan Amount'].get(),
                                              entries['Interest Rate'].get(),
                                              entries['Home Value'].get(),
                                              criterias['annual_interest_payment'],
                                              criterias['interest_payment_to_income']['value'],
                                              criterias['interest_payment_to_income']['state'],
                                              criterias['loan_to_home']['value'],
                                              criterias['loan_to_home']['state'],
                                              criterias['credit_score']['value'],
                                              criterias['credit_score']['state']))

if __name__ == '__main__':
    ROOT = tk.Tk()
    APP = Application(ROOT)
    ROOT.mainloop()
