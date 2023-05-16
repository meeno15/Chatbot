# Importing the libraries
from tkinter import *
from tkinter import messagebox
import os
import webbrowser

import numpy as np
import pandas as pd


class HyperlinkManager:

    def __init__(self, text):
        self.text = text
        self.text.tag_config("hyper", foreground="blue", underline=1)
        self.text.tag_bind("hyper", "<Enter>", self._enter)
        self.text.tag_bind("hyper", "<Leave>", self._leave)
        self.text.tag_bind("hyper", "<Button-1>", self._click)

        self.reset()

    def reset(self):
        self.links = {}

    def add(self, action):
        # add an action to the manager.  returns tags to use in
        # associated text widget
        tag = "hyper-%d" % len(self.links)
        self.links[tag] = action
        return "hyper", tag

    def _enter(self, event):
        self.text.config(cursor="hand2")

    def _leave(self, event):
        self.text.config(cursor="")

    def _click(self, event):
        for tag in self.text.tag_names(CURRENT):
            if tag[:6] == "hyper-":
                self.links[tag]()
                return


# Importing the dataset
training_dataset = pd.read_csv('Training.csv')
test_dataset = pd.read_csv('Testing.csv')

# Slicing and Dicing the dataset to separate features from predictions
X = training_dataset.iloc[:, 0:132].values
Y = training_dataset.iloc[:, -1].values

# Dimensionality Reduction for removing redundancies
dimensionality_reduction = training_dataset.groupby(training_dataset['prognosis']).max()

# Encoding String values to integer constants
from sklearn.preprocessing import LabelEncoder

labelencoder = LabelEncoder()
y = labelencoder.fit_transform(Y)

# Splitting the dataset into training set and test set
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0)

# Implementing the Decision Tree Classifier
from sklearn.tree import DecisionTreeClassifier

classifier = DecisionTreeClassifier()
classifier.fit(X_train, y_train)

# Saving the information of columns
cols = training_dataset.columns
cols = cols[:-1]

# Checking the Important features
importances = classifier.feature_importances_
indices = np.argsort(importances)[::-1]
features = cols

# Implementing the Visual Tree
from sklearn.tree import _tree


# Method to simulate the working of a Chatbot by extracting and formulating questions
def print_disease(node):
    # print(node)
    node = node[0]
    # print(len(node))
    val = node.nonzero()
    # print(val)
    disease = labelencoder.inverse_transform(val[0])
    return disease


def recurse(node, depth):
    global val, ans
    global tree_, feature_name, symptoms_present
    indent = "  " * depth
    if tree_.feature[node] != _tree.TREE_UNDEFINED:
        name = feature_name[node]
        threshold = tree_.threshold[node]
        yield name + " ?"

        #                ans = input()
        ans = ans.lower()
        if ans == 'yes':
            val = 1
        else:
            val = 0
        if val <= threshold:
            yield from recurse(tree_.children_left[node], depth + 1)
        else:
            symptoms_present.append(name)
            yield from recurse(tree_.children_right[node], depth + 1)
    else:
        strData = ""
        present_disease = print_disease(tree_.value[node])
        #                print( "You may have " +  present_disease )
        #                print()
        strData = "You may have :" + str(present_disease)

        QuestionDigonosis.objRef.txtDigonosis.insert(END, str(strData) + '\n')

        red_cols = dimensionality_reduction.columns
        symptoms_given = red_cols[dimensionality_reduction.loc[present_disease].values[0].nonzero()]
        #                print("Symptoms present  " + str(list(symptoms_present)))
        #                print()
        strData = "symptoms present:  " + str(list(symptoms_present))
        QuestionDigonosis.objRef.txtDigonosis.insert(END, str(strData) + '\n')
        #                print("Symptoms given "  +  str(list(symptoms_given)) )
        #                print()
        strData = "symptoms given: " + str(list(symptoms_given))
        QuestionDigonosis.objRef.txtDigonosis.insert(END, str(strData) + '\n')
        confidence_level = (1.0 * len(symptoms_present)) / len(symptoms_given)
        #                print("onfidence level is " + str(confidence_level))
        #                print()
        strData = "confidence level is: " + str(confidence_level)
        QuestionDigonosis.objRef.txtDigonosis.insert(END, str(strData) + '\n')
        #                print('The model suggests:')
        #                print()
        strData = 'The model suggests:'
        QuestionDigonosis.objRef.txtDigonosis.insert(END, str(strData) + '\n')
        row = doctors[doctors['disease'] == present_disease[0]]
        #                print('Consult ', str(row['name'].values))
        #                print()
        strData = 'Consult ' + str(row['name'].values)
        QuestionDigonosis.objRef.txtDigonosis.insert(END, str(strData) + '\n')
        #                print('Visit ', str(row['link'].values))
        # print(present_disease[0])
        hyperlink = HyperlinkManager(QuestionDigonosis.objRef.txtDigonosis)
        strData = 'Visit ' + str(row['link'].values[0])

        def click1():
            webbrowser.open_new(str(row['link'].values[0]))

        QuestionDigonosis.objRef.txtDigonosis.insert(INSERT, strData, hyperlink.add(click1))
        # QuestionDigonosis.objRef.txtDigonosis.insert(END,str(strData)+'\n')
        yield strData


def tree_to_code(tree, feature_names):
    global tree_, feature_name, symptoms_present
    tree_ = tree.tree_
    # print(tree_)
    feature_name = [
        feature_names[i] if i != _tree.TREE_UNDEFINED else "undefined!"
        for i in tree_.feature
    ]
    # print("def tree({}):".format(", ".join(feature_names)))
    symptoms_present = []


#        recurse(0, 1)


def execute_bot():
    #    print("Please reply with yes/Yes or no/No for the following symptoms")
    tree_to_code(classifier, cols)


# This section of code to be run after scraping the data

doc_dataset = pd.read_csv('doctors_dataset.csv', names=['Name', 'Description'])

diseases = dimensionality_reduction.index
diseases = pd.DataFrame(diseases)

doctors = pd.DataFrame()
doctors['name'] = np.nan
doctors['link'] = np.nan
doctors['disease'] = np.nan

doctors['disease'] = diseases['prognosis']

doctors['name'] = doc_dataset['Name']
doctors['link'] = doc_dataset['Description']

record = doctors[doctors['disease'] == 'AIDS']
record['name']
record['link']


# Execute the bot and see it in Action
# execute_bot()

class QuestionDigonosis(Frame):
    objIter = None
    objRef = None

    def __init__(self, master=None):
        master.title("Question Diagnosis")
        master.geometry("1200x800") # Increased the size of the frame
        master.state("z")
        QuestionDigonosis.objRef = self
        super().__init__(master=master)
        self["bg"] = "lightsteelblue"
        self.pack(expand=True, fill=BOTH)  # Added to make the frame responsive
        self.createWidget()
        self.iterObj = None

    def createWidget(self):
        self.lblQuestion = Label(self, text="Question", width=12, bg="lightgreen", font=("Monaco", 18))
        self.lblQuestion.grid(row=0, column=0, rowspan=4, padx=10, pady=10)

        self.lblDigonosis = Label(self, text="Diagnosis", width=12, bg="lightgreen", font=("Monaco", 18))
        self.lblDigonosis.grid(row=5, column=0, sticky="n", pady=10)

        self.txtQuestion = Text(self, width=100, height=10, font=("Monaco", 16)) # Increased width
        self.txtQuestion.grid(row=0, column=1, rowspan=4, columnspan=20, padx=10, pady=10) # Increased height

        self.varDiagonosis = StringVar()
        self.txtDigonosis = Text(self, width=100, height=20, font=("Monaco", 16)) # Increased width
        self.txtDigonosis.grid(row=5, column=1, columnspan=20, rowspan=20, pady=10) # Increased height

        self.btnNo = Button(self, text="No", width=20, bg="coral", font=("Monaco", 16), command=self.btnNo_Click) # Increased width and font size
        self.btnNo.grid(row=27, column=0, pady=10)

        self.btnYes = Button(self, text="Yes", width=20, bg="lightgreen", font=("Monaco", 16), command=self.btnYes_Click) # Increased width and font size
        self.btnYes.grid(row=27, column=1, sticky="w", pady=10)

        self.btnClear = Button(self, text="Clear", width=20, bg="coral", font=("Monaco", 16), command=self.btnClear_Click) # Increased width and font size
        self.btnClear.grid(row=28, column=0, pady=10)

        self.btnStart = Button(self, text="Start", width=20, bg="lightgreen", font=("Monaco", 16), command=self.btnStart_Click) # Increased width and font size
        self.btnStart.grid(row=28, column=1, sticky="w", pady=10)


    def btnNo_Click(self):
        global val, ans
        global val, ans
        ans = 'No'
        str1 = QuestionDigonosis.objIter.__next__()
        self.txtQuestion.delete(0.0, END)
        self.txtQuestion.insert(END, str1 + "\n")

    def btnYes_Click(self):
        global val, ans
        ans = 'Yes'
        self.txtDigonosis.delete(0.0, END)
        str1 = QuestionDigonosis.objIter.__next__()

    #        self.txtDigonosis.insert(END,str1+"\n")

    def btnClear_Click(self):
        self.txtDigonosis.delete(0.0, END)
        self.txtQuestion.delete(0.0, END)

    def btnStart_Click(self):
        execute_bot()
        self.txtDigonosis.delete(0.0, END)
        self.txtQuestion.delete(0.0, END)
        self.txtDigonosis.insert(END, "Could you please indicate 'Yes' or 'No' for each of the symptoms mentioned in the above question")
        QuestionDigonosis.objIter = recurse(0, 1)
        str1 = QuestionDigonosis.objIter.__next__()
        self.txtQuestion.insert(END, str1 + "\n")




class MainForm(Frame):
    main_Root = None

    def destroyPackWidget(self, parent):
        for e in parent.pack_slaves():
            e.destroy()

    def __init__(self, master=None):
        MainForm.main_Root = master
        super().__init__(master=master)
        master.geometry("1000x500")
        master.title("Account")
        self.createWidget()

    def createWidget(self):
        self.lblMsg = Label(self, text="Fatma ~Your Health Assistant", bg="#4287f5", fg="white", width="280",
                                height="2", font=("Monaco", 18, "bold"))
        self.lblMsg.pack(pady=20)

        self.btnLogin = Button(self, text="LOGIN", bg="#ffa500", fg="black", height="2", width="20",
                                   font=("Monaco", 24), command=self.lblLogin_Click)
        self.btnLogin.pack(pady=20)

        self.btnRegister = Button(self, text="REGISTER", bg="#ffa500", fg="black", height="2", width="20",
                                      font=("Monaco", 24), command=self.btnRegister_Click)
        self.btnRegister.pack(pady=20)

        self.lblTeam = Label(self, text="Created by:", bg="#4287f5", fg="white", width="250", height="1", padx=10,
                                 pady=10, font=("Monaco", 18))
        self.lblTeam.pack()

        self.lblTeam1 = Label(self, text="--", bg="white", width="250", height="1", font=("Calibri", 13))
        self.lblTeam1.pack()

        self.lblTeam2 = Label(self, text="--", bg="white", width="250", height="1", font=("Calibri", 13))
        self.lblTeam2.pack()

    def lblLogin_Click(self):
        self.destroyPackWidget(MainForm.main_Root)
        frmLogin=Login(MainForm.main_Root)
        frmLogin.pack()

    def btnRegister_Click(self):
        self.destroyPackWidget(MainForm.main_Root)
        frmSignUp = SignUp(MainForm.main_Root)
        frmSignUp.pack()

class Login(Frame):
    main_Root = None

    def destroyPackWidget(self, parent):
        for e in parent.pack_slaves():
            e.destroy()

    def __init__(self, master=None):
        Login.main_Root = master
        super().__init__(master=master)
        master.title("Login")
        master.geometry("1000x500")
        self.createWidget()

    def createWidget(self):
        self.lblMsg = Label(self, text="Fill in your details to login!!", width="300", font=("Monaco", 24), padx=10,
                            pady=10, bg="#4287f5", fg="white")
        self.lblMsg.pack()

        self.username = Label(self, text="Username", padx=10, pady=10, font=("Monaco", 20))
        self.username.pack()

        self.username_verify = StringVar()
        self.username_login_entry = Entry(self, textvariable=self.username_verify, font=("Monaco", 18))
        self.username_login_entry.pack()

        self.password = Label(self, text="Password", padx=10, pady=10, font=("Monaco", 20))
        self.password.pack()

        self.password_verify = StringVar()
        self.password_login_entry = Entry(self, textvariable=self.password_verify, show='*', font=("Monaco", 18))
        self.password_login_entry.pack()

        self.btnLogin = Button(self, text="Login", width=10, height=2, font=("Monaco", 20), bg="#ffa500",
                               fg="black", command=self.btnLogin_Click)
        self.btnLogin.pack(pady=10)

        self.btnRegister = Button(self, text="Register", width=10, height=2, font=("Monaco", 20), bg="#ffa500",
                                  fg="black", command=self.btnRegister_Click)
        self.btnRegister.pack(pady=10)

    def btnLogin_Click(self):
        username1 = self.username_login_entry.get()
        password1 = self.password_login_entry.get()

        list_of_files = os.listdir()
        if username1 in list_of_files:
            file1 = open(username1, "r")
            verify = file1.read().splitlines()
            if password1 in verify:
                messagebox.showinfo("Great", "Login Success!!")
                self.destroyPackWidget(Login.main_Root)
                frmQuestion = QuestionDigonosis(Login.main_Root)
                frmQuestion.pack()
            else:
                messagebox.showinfo("Wrong Login Details", "Please try again!!")
        else:
            messagebox.showinfo("User not recognized", "Please sign up for a new account.")

    def btnRegister_Click(self):
        self.destroyPackWidget(Login.main_Root)
        frmSignUp = SignUp(Login.main_Root)
        frmSignUp.pack()


class SignUp(Frame):
    main_Root = None

    def destroyPackWidget(self, parent):
        for e in parent.pack_slaves():
            e.destroy()

    def __init__(self, master=None):
        SignUp.main_Root = master
        super().__init__(master=master)
        master.title("Register")
        master.geometry("1000x500")
        self.createWidget()

    def createWidget(self):
        self.lblMsg = Label(self, text="Fill in the details below", width="300", font=("Monaco", 24), padx=10,
                            pady=10, bg="#4287f5", fg="white")
        self.lblMsg.pack()

        self.username_lable = Label(self, text="Username", padx=10, pady=10, font=("Monaco", 20))
        self.username_lable.pack()
        self.username = StringVar()
        self.username_entry = Entry(self, textvariable=self.username, font=("Monaco", 18))
        self.username_entry.pack()

        self.password_lable = Label(self, text="Password", padx=10, pady=10, font=("Monaco", 20))
        self.password_lable.pack()
        self.password = StringVar()
        self.password_entry = Entry(self, textvariable=self.password, show='*', font=("Monaco", 18))
        self.password_entry.pack()

        self.btnRegister = Button(self, text="Register", font=("Monaco", 20), bg="#ffa500", fg="black",
                                  command=self.register_user)
        self.btnRegister.pack(pady=20)

    def register_user(self):
        file = open(self.username_entry.get(), "w")
        file.write(self.username_entry.get() + "\n")
        file.write(self.password_entry.get())
        file.close()

        self.destroyPackWidget(SignUp.main_Root)

        self.lblSucess = Label(root, text="Registration was Successful", fg="black", font=("Monaco", 20))
        self.lblSucess.pack()

        self.btnSucess = Button(root, text="Click Here to proceed", command=self.btnSucess_Click)
        self.btnSucess.pack(pady=20)

    def btnSucess_Click(self):
        self.destroyPackWidget(SignUp.main_Root)
        frmQuestion = QuestionDigonosis(SignUp.main_Root)

        frmQuestion.pack()


root = Tk()

frmMainForm = MainForm(root)
frmMainForm.pack()
root.mainloop()


