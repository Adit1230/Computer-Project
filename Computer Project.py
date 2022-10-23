from tkinter import *
from tkinter import messagebox
import sqlite3

user_list=[]

def init():
    conn=sqlite3.connect("Database.db")
    cur=conn.cursor()

    if cur.execute("""SELECT * FROM sqlite_master WHERE type='table'""").fetchall()==[]:
        cur.execute("""CREATE TABLE Users(Name text, Username text, Password text, Balance int);""")

    conn.commit()
    conn.close()
    init_login('start')

def init_login(From):
    global tb_username
    global tb_password
    global login_win

    if From=='signup':
        signup_win.destroy()
    elif From=='main':
        main_win.destroy()
    
    login_win=Tk()
    login_win.title("Login page")
    
    lbl_login=Label(login_win,text="Login").grid(row=0,column=0,columnspan=2)

    lbl_username=Label(login_win,text="Username:").grid(row=1,column=0)
    tb_username=Entry(login_win)
    tb_username.grid(row=1,column=1)
    
    lbl_password=Label(login_win,text="Password:").grid(row=2,column=0)
    tb_password=Entry(login_win,show='*')
    tb_password.grid(row=2,column=1)
    
    btn_login=Button(text="Login",command=login)
    btn_login.grid(row=3,column=0,columnspan=2)

    lbl_signup=Label(login_win,text="Don't have an account?").grid(row=4,column=0,columnspan=2)
    btn_signup=Button(text="Signup",command=lambda: init_signup('login'))
    btn_signup.grid(row=5,column=0,columnspan=2)

    login_win.mainloop()

def init_signup(From):
    global signup_win
    global tb_name
    global tb_username
    global tb_password
    global tb_reenterpass
    global tb_initdep

    if From=='login':
        login_win.destroy()
    elif From=='main':
        main_win.destroy()
    
    signup_win = Tk()

    signup_win.title("Sign-up Page")
    signup_win.geometry('350x250')

    lbl_createacnt=Label(signup_win,text= 'Create an Account').grid(row=0,column=0,columnspan=2)

    lbl_name=Label(signup_win,text='Enter Name:').grid(row=1,column=0)
    tb_name=Entry(signup_win,width=10)
    tb_name.grid(row=1, column=1)

    lbl_username=Label(signup_win, text= 'Enter Username:').grid(row=2,column=0)
    tb_username=Entry(signup_win,width=10)
    tb_username.grid(row=2,column=1)

    lbl_password=Label(signup_win, text= 'Enter Password:').grid(row=3,column=0)
    tb_password=Entry(signup_win,width=10,show='*')
    tb_password.grid(row=3,column=1)

    lbl_reenterpass=Label(signup_win,text='Re-enter password:').grid(row=4,column=0)
    tb_reenterpass=Entry(signup_win,width=10,show='*')
    tb_reenterpass.grid(row=4,column=1)

    lbl_initdep=Label(signup_win,text='Enter Initial Deposit:').grid(row=5,column=0)
    tb_initdep=Entry(signup_win,width=10)
    tb_initdep.grid(row=5,column=1)

    btn_signup=Button(signup_win, text='Sign Up',command=signup)
    btn_signup.grid(row=6,column=0,columnspan=2)

    lbl_login=Label(signup_win,text="Already have an account?").grid(row=7,column=0,columnspan=2)
    btn_login=Button(signup_win,text="Go back to login page",command=lambda: init_login('signup'))
    btn_login.grid(row=8,column=0,columnspan=2)

    signup_win.mainloop()

def init_main(From):
    global main_win
    global user_list
    
    if From=='login':
        login_win.destroy()
    elif From=='signup':
        signup_win.destroy()

    main_win=Tk()

    lbl_name=Label(main_win,text=("Name:"+user_list[1]))
    lbl_name.grid(row=0,column=0)
    
    lbl_username=Label(main_win,text=("Username:"+user_list[2]))
    lbl_username.grid(row=1,column=0)
    
    lbl_balance=Label(main_win,text=("Balance:"+str(user_list[4])))
    lbl_balance.grid(row=2,column=0)

    btn_logout=Button(main_win,text="Logout",command=lambda: init_login('main'))
    btn_logout.grid(row=3,column=0)
    
    main_win.mainloop()

def login():
    global user_list
    global tb_username
    global tb_password

    conn=sqlite3.connect("Database.db")
    cur=conn.cursor()
    
    if tb_username.get()=='' or tb_password.get()=='':
        messagebox.showwarning("All fields are required","Please enter all required fields")
        return()
    else:
        cur.execute("SELECT rowid,* FROM Users WHERE USERNAME=?",(tb_username.get(),))
        temp_list=cur.fetchone()
    
    if temp_list==None:
        messagebox.showwarning("Invalid username","Username does not exist")
        return()
    elif tb_password.get()==temp_list[3]:
        user_list=list(temp_list)
        login_win.destroy
        init_main('login')
        return()
    else:
        messagebox.showwarning("Wrong username or password","Username and password don't match")
        return()
    
    conn.commit()
    conn.close()

def signup():
    global user_list
    
    conn=sqlite3.connect("Database.db")
    cur=conn.cursor()
    
    if tb_name.get()=='' or tb_username.get()=='' or tb_password.get()=='' or tb_reenterpass.get()=='' or tb_initdep.get()=='':
        messagebox.showwarning("All fields are required","Please enter all required fields")
        return()
    elif len(tb_password.get())<8:
        messagebox.showwarning("Password too short","Password must be at least 8 characters long")
        return()
    elif tb_password.get()!=tb_reenterpass.get():
        messagebox.showwarning("Password does not match","Password entered in password textbox does not match password entered in reenter password textbox")
        return()
    elif not (tb_initdep.get().isdigit()):
        messagebox.showwarning("Invalid initial deposit","The initial deposit must be a number")
        return()
    else:
        cur.execute("SELECT rowid,* FROM Users WHERE Username=?",(tb_username.get(),))
        temp_list=cur.fetchone()

    if temp_list!=None:
        messagebox.showwarning("Username already taken","Please choose another username")
        return()
    else:
        cur.execute("INSERT INTO Users VALUES (?,?,?,?)",(tb_name.get(),tb_username.get(),tb_password.get(),int(tb_initdep.get())))
        conn.commit()
        
        cur.execute("SELECT rowid,* FROM Users WHERE Username=?",(tb_username.get(),))
        conn.commit()
        
        user_list=list(cur.fetchone())
        init_main('signup')

    conn.commit()
    conn.close()
    
init()
