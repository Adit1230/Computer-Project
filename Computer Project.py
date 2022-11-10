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
    login_win.geometry('1500x750')
    login_win.title("Login page")

    #Logo = PhotoImage(file ="Bank logo.jpg")
    #login_win.iconphoto(False, Logo)
    
    lbl_login=Label(login_win,text="Login",justify='center',font = ('Arial ' , 25)).place(relx=0.5,rely=0.35,anchor='c')

    lbl_username=Label(login_win,text="Username:", font = ('Arial' , 15)).place(relx=0.42,rely=0.4 , anchor='c')
    tb_username=Entry(login_win ,font = ('Arial' , 15))
    tb_username.place(relx=0.54,rely=0.4,anchor ='c')
    
    lbl_password=Label(login_win,text="Password:",font = ('Arial' , 15)).place(relx=0.42,rely=0.45 , anchor='c')
    tb_password=Entry(login_win,show='*',font = ('Arial' , 15))
    tb_password.place(relx=0.54,rely=0.45,anchor ='c')
    
    btn_login=Button(text="Login",command=login,font = ('Arial' , 15))
    btn_login.place(relx=0.5 , rely=0.51,anchor = 'c')

    lbl_signup=Label(login_win,text="Don't have an account?",font = ('Arial' , 15)).place(relx=0.5 , rely = 0.56 , anchor = 'c')
    btn_signup=Button(text="Signup",font = ('Arial' , 15),command=lambda: init_signup('login'))
    btn_signup.place(relx=0.5 , rely = 0.61, anchor = 'c')

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
    global frame_content
    global lbl_balance
    
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

    frame_btn=Frame(main_win,width=100,height=500,pady=10)
    frame_btn.grid(row=4,column=0)
    
    btn_deposit=Button(frame_btn,text='Deposit',command=lambda: display_tab('deposit')  )
    btn_deposit.grid(row=0,column=0)
    
    btn_withdrawal=Button(frame_btn,text='Withdraw',command=lambda: display_tab('withdraw') )
    btn_withdrawal.grid(row=1,column=0)

    btn_transfer=Button(frame_btn,text='Transfer',command=lambda: display_tab('transfer') )
    btn_transfer.grid(row=2,column=0)
    
    frame_content=Frame(main_win,width=500,height=500,pady=10)
    frame_content.grid(row=4,column=1)
    
    main_win.mainloop()
    
def display_tab(tab):
    for widgets in frame_content.winfo_children():
        widgets.destroy()

    if tab=='transfer':
        global tb_user
        global tb_transfer
        
        lbl_user=Label(frame_content,text='Enter username of recepient :').grid(row=0,column=0)
        tb_user=Entry(frame_content)
        tb_user.grid(row=0,column=1)

        lbl_amt=Label(frame_content,text='Enter amount to be transferred :').grid(row=1,column=0)
        tb_transfer=Entry(frame_content)
        tb_transfer.grid(row=1,column=1)

        btn_transfer = Button(frame_content , text = 'Transfer ' , command = transfer)
        btn_transfer.grid(row=2, column = 0 , columnspan = 2)

    if tab=='withdraw':
        global tb_withdraw
        
        lbl_withdraw = Label(frame_content , text = 'Enter amount to be withdrawn : ' ).grid(row=0 , column=0)
        tb_withdraw = Entry(frame_content)
        tb_withdraw.grid(row=0,column=1)
        btn_withdraw = Button(frame_content , text = 'Withdraw' , command = withdraw)
        btn_withdraw.grid(row=1, column=0, columnspan = 2)

    if tab=='deposit':
        global tb_deposit

        lbl_deposit = Label(frame_content , text = 'Enter amount to be deposited : ' ).grid(row=0 , column=0)
        tb_deposit = Entry(frame_content)
        tb_deposit.grid(row=0,column=1)
        btn_deposit = Button(frame_content , text = 'Deposit' , command = deposit)
        btn_deposit.grid(row=1, column=0, columnspan = 2)

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

def deposit():
    conn=sqlite3.connect("Database.db")
    cur=conn.cursor()
    
    if tb_deposit.get()=='':
        messagebox.showwarning("Invalid deposit amount","Please enter amount to deposit")
    elif not tb_deposit.get().isdigit():
        messagebox.showwarning("Invalid deposit amount","Amount to deposit should be a number")
    else:
        update_info()
        balance=user_list[4]
        
        cur.execute("UPDATE Users SET Balance = ? WHERE rowid = ?",(balance+int(tb_deposit.get()),user_list[0]))
        conn.commit()
        messagebox.showinfo("Transaction succesfull","Transaction completed successfully")
        update_info()

    conn.commit()
    conn.close()

def withdraw():
    conn=sqlite3.connect("Database.db")
    cur=conn.cursor()

    if tb_withdraw.get()=='':
        messagebox.showwarning("Invalid withdraw amount","Please enter amount to withdraw")
        return()
    elif not tb_withdraw.get().isdigit():
        messagebox.showwarning("Invalid withdraw amount","Amount to withdraw should be a number")
        return()
    else:
        update_info()
        balance=int(user_list[4])
        
        if int(tb_withdraw.get())>balance:
            messagebox.showwarning("Error","You cannot withdraw more than you have in your account")
            return()
        else:
            auth_win=Toplevel(main_win)

            def confirm_pass():
                    if tb_pass.get()==user_list[3]:
                        auth_win.destroy()
                        
                        cur.execute("UPDATE Users SET Balance = ? WHERE rowid = ?",(balance-int(tb_withdraw.get()),user_list[0]))
                        conn.commit()
                        
                        messagebox.showinfo("Transaction succesful","Amount withdrawn successfully")
                        update_info()
                    else:
                        auth_win.destroy()
                        messagebox.showwarning("Authentication failed","Wrong password, Please try again.")

            lbl_auth=Label(auth_win,text="Please confirm your password to continue")
            lbl_auth.grid(row=0,column=0,columnspan=2)
            lbl_pass=Label(auth_win,text="Password:")
            lbl_pass.grid(row=1,column=0)
            tb_pass=Entry(auth_win,show='*')
            tb_pass.grid(row=1,column=1)
            btn_auth=Button(auth_win,text="Confirm",command=confirm_pass)
            btn_auth.grid(row=2,column=0,columnspan=2)

            auth_win.mainloop()
                
    conn.commit()
    conn.close()
    return()

def transfer():
    conn=sqlite3.connect("Database.db")
    cur=conn.cursor()

    transfer_amount=tb_transfer.get()
    
    if transfer_amount=='':
        messagebox.showwarning("Invalid transfer amount","Please enter amount to transfer")
    elif not transfer_amount.isdigit():
        messagebox.showwarning("Invalid transfer amount","Amount to transfer should be a number")
    elif tb_user.get()==user_list[2]:
        messagebox.showwarning("Invalid Username","You cannot transfer money to yourself"
    else:
        update_info()
        balance=int(user_list[4])
        
        cur.execute("SELECT rowid,Balance FROM Users WHERE Username=?",(tb_user.get(),))
        transferee_list=cur.fetchone()
        
        if float(transfer_amount) >balance:
            messagebox.showwarning("Error","You cannot transfer more than you have in your account")
            return()
        elif transferee_list==None:
            messagebox.showwarning("Invalid Username","No account with username "+tb_user.get()+" exists")
        else:
            auth_win=Toplevel(main_win)

            def confirm_pass():
                if tb_pass.get()==user_list[3]:
                    auth_win.destroy()
                    
                    cur.execute("UPDATE Users SET Balance=? WHERE rowid=?",(balance-int(transfer_amount),user_list[0]))
                    conn.commit()

                    cur.execute("UPDATE Users SET Balance=? WHERE rowid=?",(transferee_list[1]+int(transfer_amount),transferee_list[0]))
                    conn.commit()

                    messagebox.showinfo("Transaction successful","Transaction completed successfully")
                    update_info()
                    
                    return()
                    
                else:
                    auth_win.destroy()
                    messagebox.showwarning("Authentication failed","Wrong password, Please try again.")
                    return()

            lbl_auth=Label(auth_win,text="Please confirm your password to continue")
            lbl_auth.grid(row=0,column=0,columnspan=2)
            lbl_pass=Label(auth_win,text="Password:")
            lbl_pass.grid(row=1,column=0)
            tb_pass=Entry(auth_win,show='*')
            tb_pass.grid(row=1,column=1)
            btn_auth=Button(auth_win,text="Confirm",command=confirm_pass)
            btn_auth.grid(row=2,column=0,columnspan=2)

            auth_win.mainloop()
            
        conn.commit()
        conn.close()
        return()
            
def update_info():
    global user_list
    
    conn=sqlite3.connect("Database.db")
    cur=conn.cursor()

    cur.execute("SELECT rowid, * FROM Users WHERE rowid = ?",(user_list[0],))
    user_list=list(cur.fetchone())

    lbl_balance.config(text=("Balance:"+str(user_list[4])))
    
    conn.commit()
    conn.close()

init()
