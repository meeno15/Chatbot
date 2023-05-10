from tkinter import *
import os

def destroyPackWidget(parent):
    for e in parent.pack_slaves():
        e.destroy()

def register():
    global root, register_screen
    destroyPackWidget(root)
    register_screen = root
    register_screen.title("Register")
    register_screen.geometry("1000x500")

    global username
    global password
    global username_entry
    global password_entry
    username = StringVar()
    password = StringVar()

    Label(register_screen, text="Please enter the details below", font=("Monaco", 14)).pack(pady=10)
    username_label = Label(register_screen, text="Username: ", font=("Monaco", 12))
    username_label.pack()
    username_entry = Entry(register_screen, textvariable=username, font=("Monaco", 12))
    username_entry.pack()
    password_label = Label(register_screen, text="Password: ", font=("Monaco", 12))
    password_label.pack()
    password_entry = Entry(register_screen, textvariable=password, show='*', font=("Monaco", 12))
    password_entry.pack()
    Button(register_screen, text="Register", font=("Monaco", 12), bg="light blue", command=register_user).pack(pady=20)

def login(main_screen=None):
    global login_screen
    login_screen = Toplevel(main_screen)
    login_screen.title("Login")
    login_screen.geometry("1000x500")

    global username_verify
    global password_verify

    username_verify = StringVar()
    password_verify = StringVar()

    Label(login_screen, text="Please enter details below to login", font=("Monaco", 14)).pack(pady=10)
    Label(login_screen, text="Username: ", font=("Monaco", 12)).pack()
    Entry(login_screen, textvariable=username_verify, font=("Monaco", 12)).pack()
    Label(login_screen, text="Password: ", font=("Monaco", 12)).pack()
    Entry(login_screen, textvariable=password_verify, show='*', font=("Monaco", 12)).pack()
    Button(login_screen, text="Login", font=("Monaco", 12), bg="light blue", command=login_verify).pack(pady=20)
    Button(login_screen, text="Forgot Password", font=("Monaco", 12), bg="light blue", command=forgot_password).pack(pady=10)

def btnSucess_Click():
    global root
    destroyPackWidget(root)

def register_user():
    global root, username, password
    username_info = username.get()
    password_info = password.get()
    if not (3 <= len(username_info) <= 15 and 8 <= len(password_info) <= 20 and any(char.isdigit() for char in password_info)):
        Label(root, text="Invalid username or password. Username must be between 3 and 15 characters, password must be between 8 and 20 characters, and contain at least one digit.", font=("Calibri", 12), fg="red").pack(pady=10)
        return
    file = open(username_info, "w")
    file.write(username_info + "\n")
    file.write(password_info)
    file.close()

    username_entry.delete(0, END)
    password_entry.delete(0, END)

    Label(root, text="Registration is successful", fg="green", font=("Monaco", 14)).pack()
    Button(root,text="Click Here to proceed", font=("Monaco", 12), bg="light blue", command=btnSucess_Click).pack(pady=20)

def login_verify():
    global login_screen
    username1 = username_verify.get()
    password1 = password_verify.get()
    list_of_files = os.listdir()
    if username1 in list_of_files:
        file1 = open(username1, "r")
        verify = file1.read().splitlines()
        if password1 in verify:
            destroyPackWidget(login_screen)
            login_success()
        else:
            Label(login_screen, text="Invalid Password", font=("Monaco", 12), fg="red").pack(pady=10)

    else:
        Label(login_screen, text="User Not Found", font=("Monaco", 12), fg="red").pack(pady=10)

def login_success():
    global login_success_screen
    login_success_screen = Toplevel(login_screen)
    login_success_screen.title("Success")
    login_success_screen.geometry("1000x500")
    Label(login_success_screen, text="Login Success", font=("Monaco", 14)).pack(pady=10)
    Button(login_success_screen, text="OK", font=("Monaco", 12), bg="light blue", command=delete_login_success).pack(pady=20)
    Checkbutton(login_success_screen, text="Remember me", font=("Monaco", 12)).pack()

def delete_login_success():
    login_success_screen.destroy()

def main_account_screen(frmmain):
    global root
    root = frmmain
    root.geometry("1000x500")
    root.title("Account Login")
    Label(root,text="HealthBot", bg="light blue", width="300", height="2", font=("Monaco", 14)).pack(pady=10)
    Button(root,text="Login", font=("Monaco", 12), bg="light green", height="2", width="30", command=login).pack(pady=10)
    Button(root,text="Register", font=("Monaco", 12), bg="light green", height="2", width="30", command=register).pack(pady=10)

def forgot_password():
    global forgot_password_screen
    forgot_password_screen = Toplevel(login_screen)
    forgot_password_screen.title("Forgot Password")
    forgot_password_screen.geometry("1000x500")
    global username_forgot
    global security_question
    global security_answer

    username_forgot = StringVar()
    security_question = StringVar()
    security_answer = StringVar()

    Label(forgot_password_screen, text="Please enter your username", font=("Monaco", 14)).pack(pady=10)
    Entry(forgot_password_screen, textvariable=username_forgot, font=("Monaco", 12)).pack()
    Button(forgot_password_screen, text="Next", font=("Monaco", 12), bg="light blue",
           command=security_question_verification).pack(pady=20)

def security_question_verification():
    global forgot_password_screen
    global security_question_screen
    username_forgot1 = username_forgot.get()
    list_of_files = os.listdir()
    if username_forgot1 in list_of_files:
        file1 = open(username_forgot1, "r")
        verify = file1.read().splitlines()
        security_question1 = verify[2]
        file1.close()
        security_question_screen = Toplevel(forgot_password_screen)
        security_question_screen.title("Security Question Verification")
        security_question_screen.geometry("300x250")
        Label(security_question_screen, text=security_question1, font=("Monaco", 14)).pack(pady=10)
        Entry(security_question_screen, textvariable=security_answer, font=("Monaco", 12)).pack()
        Button(security_question_screen, text="Submit", font=("Monaco", 12), bg="light blue", command=password_reset_verification).pack(pady=20)

def password_reset_verification():
    global forgot_password_screen
    global password_reset_screen
    username_forgot2 = username_forgot.get()
    security_answer1 = security_answer.get()
    list_of_files = os.listdir()
    if username_forgot2 in list_of_files:
        file1 = open(username_forgot2, "r")
        verify = file1.read().splitlines()
        security_answer2 = verify[3]
        file1.close()
        if security_answer1 == security_answer2:
            password_reset_screen = Toplevel(security_question_screen)
            password_reset_screen.title("Password Reset")
            password_reset_screen.geometry("1000x500")

            global new_password
            global new_password_verify

            new_password = StringVar()
            new_password_verify = StringVar()

            Label(password_reset_screen, text="Please enter a new password", font=("Monaco", 14)).pack(pady=10)
            Label(password_reset_screen, text="Password: ", font=("Monaco", 12)).pack()
            Entry(password_reset_screen, textvariable=new_password, show='*', font=("Monaco", 12)).pack()
            Label(password_reset_screen, text="Confirm Password: ", font=("Monaco", 12)).pack()
            Entry(password_reset_screen, textvariable=new_password_verify, show='*', font=("Monaco", 12)).pack()
            Button(password_reset_screen, text="Reset Password", font=("Monaco", 12), bg="light blue",
                   command=password_reset).pack(pady=20)
        else:
            Label(security_question_screen, text="Incorrect Answer", font=("Monaco", 12), fg="red").pack(pady=10)
    else:
        Label(forgot_password_screen, text="User Not Found", font=("Monaco", 12), fg="red").pack(pady=10)


def password_reset():
    global password_reset_screen
    new_password1 = new_password.get()
    new_password2 = new_password_verify.get()
    if new_password1 == new_password2:
        username_forgot3 = username_forgot.get()
        list_of_files = os.listdir()
        file1 = open(username_forgot3, "w")
        file1.write(username_forgot3 + "\n")
        file1.write(new_password1 + "\n")
        file1.write("\n")
        file1.close()
        Label(password_reset_screen, text="Password Reset Successful", font=("Monaco", 14)).pack(pady=10)
        Button(password_reset_screen, text="OK", font=("Monaco", 12), bg="light blue", command=delete_password_reset).pack(pady=20)
    else:
        Label(password_reset_screen, text="Passwords do not match", font=("Monaco", 12), fg="red").pack(pady=10)

def delete_password_reset():
    password_reset_screen.destroy()

root = Tk()
main_account_screen(root)
root.mainloop()








