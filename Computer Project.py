from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import sqlite3
import time
from PIL import ImageTk, Image

user_list=[]
trans_hist_limit=10
notif_limit=10

def init():
    conn=sqlite3.connect("Database.db")
    cur=conn.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS Users(Name text, Username text, Password text, Balance int, Trans_Hist text, Notifications text);""")

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
        user_list.clear()
        main_win.destroy()
    
    login_win=Tk()
    login_win.geometry('1500x750')
    login_win.title("Login page")

    Logo = ImageTk.PhotoImage(Image.open('Bank Logo.jpg'))
    login_win.iconphoto(False, Logo)

    Bg = ImageTk.PhotoImage(Image.open('Bank Background.jpg').resize((1500,750)))
    lbl_bg=Label(login_win, image=Bg)
    lbl_bg.pack()

    lbl_login=Label(login_win,text="Login",justify='center',font = ('Arial ' , 25), fg='#0f0',bg='#054175').place(relx=0.5,rely=0.35,anchor='c')

    lbl_username=Label(login_win,text="Username:", font = ('Arial' , 15), fg='#ffffff', bg='#054175').place(relx=0.42,rely=0.4 , anchor='c')
    tb_username=Entry(login_win ,font = ('Arial' , 15))
    tb_username.place(relx=0.54,rely=0.4,anchor ='c')
    
    lbl_password=Label(login_win,text="Password:",font = ('Arial' , 15), fg='#ffffff', bg='#054175').place(relx=0.42,rely=0.45 , anchor='c')
    tb_password=Entry(login_win,show='*',font = ('Arial' , 15))
    tb_password.place(relx=0.54,rely=0.45,anchor ='c')
    
    btn_login=Button(text="Login",command=login,font = ('Arial' , 15))
    btn_login.place(relx=0.5 , rely=0.51,anchor = 'c')
    login_win.bind('<Return>' , lambda event:login())

    lbl_signup=Label(login_win,text="Don't have an account?",font = ('Arial' , 15), fg='#c00', bg='#085B9D').place(relx=0.5 , rely = 0.56 , anchor = 'c')
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
    signup_win.geometry('1500x750')

    Logo = ImageTk.PhotoImage(Image.open('Bank Logo.jpg'))
    signup_win.iconphoto(False, Logo)

    Bg = ImageTk.PhotoImage(Image.open('Bank Background.jpg').resize((1500,750)))
    lbl_bg=Label(signup_win, image=Bg)
    lbl_bg.pack()
    
    frame_ui = Frame(signup_win, bg='#055a86')
    frame_ui.place(relx=0.375,rely=0.25)

    lbl_createacnt=Label(frame_ui,text= 'Create an Account', font = ('Arial' , 25), fg='#0f0', bg='#055a86').grid(row=0,column=0,columnspan=2)

    lbl_name=Label(frame_ui,text='Enter Name:', font = ('Arial ' , 15), bg='#055a86').grid(row=1,column=0,pady=5)
    tb_name=Entry(frame_ui, width=10, font = ('Arial' , 15))
    tb_name.grid(row=1, column=1, pady=5, padx=5)

    lbl_username=Label(frame_ui, text= 'Enter Username:', font = ('Arial' , 15), bg='#055a86').grid(row=2,column=0,pady=5)
    tb_username=Entry(frame_ui, width=10, font = ('Arial' , 15))
    tb_username.grid(row=2, column=1, pady=5, padx=5)

    lbl_password=Label(frame_ui, text= 'Enter Password:', font = ('Arial' , 15), bg='#055a86').grid(row=3,column=0,pady=5)
    tb_password=Entry(frame_ui,width=10,show='*', font = ('Arial' , 15))
    tb_password.grid(row=3, column=1, pady=5, padx=5)

    lbl_reenterpass=Label(frame_ui,text='Re-enter password:', font = ('Arial' , 15), bg='#055a86').grid(row=4,column=0,pady=5)
    tb_reenterpass=Entry(frame_ui,width=10,show='*', font = ('Arial' , 15))
    tb_reenterpass.grid(row=4, column=1, pady=5, padx=5)

    lbl_initdep=Label(frame_ui,text='Enter Initial Deposit:', font = ('Arial' , 15), bg='#055a86').grid(row=5,column=0,pady=5)
    tb_initdep=Entry(frame_ui,width=10, font = ('Arial' , 15))
    tb_initdep.grid(row=5, column=1, pady=5, padx=5)

    btn_signup=Button(frame_ui, text='Sign Up',command=signup, font = ('Arial' , 15))
    btn_signup.grid(row=6, column=0, columnspan=2, pady=10)
    signup_win.bind('<Return>' , lambda event:signup())

    lbl_login=Label(frame_ui, text="Already have an account?", font = ('Arial' , 15), fg='#a00', bg='#055a86').grid(row=7,column=0,columnspan=2,pady=15)
    btn_login=Button(frame_ui,text="Go back to login page", font = ('Arial' , 15), command=lambda: init_login('signup'))
    btn_login.grid(row=8,column=0,columnspan=2,pady=0)

    signup_win.mainloop()

def init_main(From):
    global main_win
    global user_list
    global frame_content
    global frame_centering
    global lbl_balance
    
    if From=='login':
        login_win.destroy()
    elif From=='signup':
        signup_win.destroy()
    
    conn=sqlite3.connect("Database.db")
    cur=conn.cursor()

    main_win=Tk()
    main_win.title("Main page")
    main_win.geometry('1250x750')

    Logo = ImageTk.PhotoImage(Image.open('Bank Logo.jpg'))
    main_win.iconphoto(False, Logo)

    Bg = ImageTk.PhotoImage(Image.open('Bank Background.jpg').resize((1500,750)))
    lbl_bg=Label(main_win, image=Bg)
    lbl_bg.place(relx=0,rely=0, anchor='nw')

    lbl_name=Label(main_win,text=("Name : "+user_list[1]), font = ('Arial' , 15))
    lbl_name.grid(row=0,column=0)
    
    lbl_username=Label(main_win,text=("Username : "+user_list[2]), font = ('Arial' , 15))
    lbl_username.grid(row=1,column=0)
    
    lbl_balance=Label(main_win,text=("Balance : "+str(user_list[4])), font = ('Arial' , 15))
    lbl_balance.grid(row=2,column=0)

    btn_logout=Button(main_win,text="Logout", font = ('Arial' , 15),command=lambda: init_login('main'))
    btn_logout.grid(row=3, column=0, pady=10)

    frame_btn=Frame(main_win,width=50,height=100)
    frame_btn.grid(row=4, column=0, sticky=N, pady=20)
    
    btn_deposit=Button(frame_btn,text='Deposit', width=15, font = ('Arial' , 15), command=lambda: display_tab('deposit')  )
    btn_deposit.grid(row=0,column=0)
    
    btn_withdrawal=Button(frame_btn,text='Withdraw', width=15, font = ('Arial' , 15), command=lambda: display_tab('withdraw') )
    btn_withdrawal.grid(row=1,column=0)

    btn_transfer=Button(frame_btn,text='Transfer', width=15, font = ('Arial' , 15), command=lambda: display_tab('transfer') )
    btn_transfer.grid(row=2,column=0)

    btn_history=Button(frame_btn,text='Transaction History', width=15, font = ('Arial' , 15), command=lambda: display_tab('transaction history') )
    btn_history.grid(row=3,column=0)
    
    frame_content=Frame(main_win,width=750,height=500,pady=10,padx=0,bg='#7fd2df')
    frame_content.grid(row=4,column=1)
    frame_content.grid_propagate(False)

    frame_centering=Frame(frame_content, bg='#7fd2df')
    frame_centering.place(relx=0.5,rely=0,anchor='n')

    for i in eval(user_list[6]):
        messagebox.showinfo("Money Transferred", i)
    user_list[6]='[]'

    cur.execute("UPDATE Users SET Notifications = '[]' WHERE rowid = ?", (user_list[0],))
    conn.commit()

    main_win.mainloop()

    conn.commit()
    conn.close()
    
def display_tab(tab):
    for widgets in frame_centering.winfo_children():
        widgets.destroy()

    if tab=='transfer':
        global tb_user
        global tb_transfer

        lbl_transfer=Label(frame_centering, text="Transfer", font = ('Arial' , 20, 'bold'), bg='#7fd2df', fg='#000000', pady=20).grid(row=0,column=0,columnspan=2)
        
        lbl_user=Label(frame_centering,text='Enter username of recepient :', font = ('Arial' , 15), bg='#7fd2df', fg='#000000').grid(row=1,column=0)
        tb_user=Entry(frame_centering, font = ('Arial' , 15))
        tb_user.grid(row=1,column=1)

        lbl_amt=Label(frame_centering,text='Enter amount to be transferred :', font = ('Arial' , 15), bg='#7fd2df', fg='#000000').grid(row=2,column=0)
        tb_transfer=Entry(frame_centering, font = ('Arial' , 15))
        tb_transfer.grid(row=2,column=1)

        btn_transfer = Button(frame_centering , text = 'Transfer ', font = ('Arial',15), command = lambda: transfer(tb_transfer.get(), tb_user.get()))
        btn_transfer.grid(row=3, column = 0 , columnspan = 2, pady=10)
        main_win.bind('<Return>' , lambda event:transfer(tb_transfer.get(), tb_user.get()))

    elif tab=='withdraw':
        global tb_withdraw

        lbl_withdraw=Label(frame_centering, text="Withdraw", font = ('Arial' , 20, 'bold'), bg='#7fd2df', fg='#000000', pady=20).grid(row=0,column=0,columnspan=2)
        
        lbl_amount= Label(frame_centering , text = 'Enter amount to be withdrawn : ', font = ('Arial',15), bg='#7fd2df', fg='#000000').grid(row=1,column=0)
        tb_amount = Entry(frame_centering, font = ('Arial' , 15))
        tb_amount.grid(row=1,column=1)
        btn_withdraw = Button(frame_centering , text = 'Withdraw', font = ('Arial' , 15) , command = lambda: withdraw(tb_amount.get()))
        btn_withdraw.grid(row=2, column=0, columnspan = 2, pady=10)
        main_win.bind('<Return>' , lambda event:withdraw(tb_amount.get()))

    elif tab=='deposit':
        global tb_deposit

        lbl_deposit=Label(frame_centering, text="Deposit", font = ('Arial' , 20, 'bold'), bg='#7fd2df', fg='#000000', pady=20).grid(row=0,column=0,columnspan=2)
        
        lbl_amount= Label(frame_centering , text = 'Enter amount to be deposited : ', font = ('Arial' , 15), bg='#7fd2df', fg='#000000').grid(row=1 , column=0)
        tb_amount = Entry(frame_centering, font = ('Arial' , 15))
        tb_amount.grid(row=1,column=1)
        btn_deposit = Button(frame_centering , text = 'Deposit', font = ('Arial' , 15), command = lambda: deposit(tb_amount.get()))
        btn_deposit.grid(row=2, column=0, columnspan = 2, pady=10)
        main_win.bind('<Return>' , lambda event:deposit(tb_amount.get()))

    elif tab=='transaction history':
        lbl_TransHist=Label(frame_centering, text="Transaction History", font = ('Arial' , 20, 'bold'), bg='#7fd2df', fg='#000000', pady=20).grid(row=0,column=0)
                
        style = ttk.Style()
        style.configure("Style1.Treeview", font=('Arial', 15))
        style.configure("Style1.Treeview.Heading", font=('Arial',15,'bold'))
        
        table = ttk.Treeview(frame_centering, style="Style1.Treeview")

        table['columns'] = ("Date", "Transaction", "Change in balance", "Total balance")

        table.column("#0", width=0, stretch=NO)
        table.column("Date", anchor=CENTER, width=125)
        table.column("Transaction", anchor=W, width=300)
        table.column("Change in balance", anchor=CENTER, width=150)
        table.column("Total balance", anchor=CENTER, width=125)

        table.heading("#0", text='', anchor=CENTER)
        table.heading("Date", text="Date", anchor=CENTER)
        table.heading("Transaction", text="Transaction", anchor=W)
        table.heading("Change in balance", text="Change in Bal.", anchor=CENTER)
        table.heading("Total balance", text="Total Bal.", anchor=CENTER)

        update_info()

        for i in range(len(user_list[5])):
            table.insert(parent='', index=0, iid = len(user_list[5])-i, text='', values = user_list[5][i])

        table.grid(row=1,column=0)

        main_win.bind('<Return>', lambda event:display_tab('transaction history'))
    
    return()

def login():
    global user_list
    global tb_username
    global tb_password

    conn=sqlite3.connect("Database.db")
    cur=conn.cursor()
    
    if tb_username.get()=='' or tb_password.get()=='':
        messagebox.showwarning("All fields are required","Please enter all required fields")
    else:
        cur.execute("SELECT rowid,* FROM Users WHERE USERNAME=?",(tb_username.get(),))
        temp_list=cur.fetchone()
    
        if temp_list==None:
            messagebox.showwarning("Invalid username","Username does not exist")
        elif tb_password.get()==temp_list[3]:
            user_list=list(temp_list)
            user_list[5]=eval(user_list[5])

            init_main('login')
        else:
            messagebox.showwarning("Wrong username or password","Username and password don't match")

   
    conn.commit()
    conn.close()
    return()

def signup():
    global user_list
    
    conn=sqlite3.connect("Database.db")
    cur=conn.cursor()
    
    if tb_name.get()=='' or tb_username.get()=='' or tb_password.get()=='' or tb_reenterpass.get()=='' or tb_initdep.get()=='':
        messagebox.showwarning("All fields are required","Please enter all required fields")
    elif len(tb_password.get())<8:
        messagebox.showwarning("Password too short","Password must be at least 8 characters long")
    elif tb_password.get()!=tb_reenterpass.get():
        messagebox.showwarning("Password does not match","Password entered in password textbox does not match password entered in reenter password textbox")
    elif not (tb_initdep.get().isdigit()):
        messagebox.showwarning("Invalid initial deposit","The initial deposit must be a number")
    else:
        cur.execute("SELECT rowid,* FROM Users WHERE Username=?",(tb_username.get(),))
        temp_list=cur.fetchone()

        if temp_list!=None:
            messagebox.showwarning("Username already taken","Please choose another username")
        else:
            cur.execute("INSERT INTO Users VALUES (?,?,?,?,?,?)",(tb_name.get(),tb_username.get(),tb_password.get(),int(tb_initdep.get()),'[]','[]'))
            conn.commit()
            
            cur.execute("SELECT rowid,* FROM Users WHERE Username=?",(tb_username.get(),))
            conn.commit()
            
            user_list=list(cur.fetchone())
            user_list[5]=eval(user_list[5])
            init_main('signup')

    conn.commit()
    conn.close()
    return()

def deposit(amount):
    conn=sqlite3.connect("Database.db")
    cur=conn.cursor()
    
    if amount=='':
        messagebox.showwarning("Invalid deposit amount","Please enter amount to deposit")
    elif not amount.isdigit():
        messagebox.showwarning("Invalid deposit amount","Amount to deposit should be a number")
    else:
        update_info()
        balance=user_list[4]
        
        cur.execute("UPDATE Users SET Balance = ? WHERE rowid = ?",(balance+int(amount),user_list[0]))
        conn.commit()

        trans_hist=list(user_list[5])
        if len(trans_hist)>=trans_hist_limit:
            trans_hist.pop(0)
        trans_hist.append([time.strftime("%d/%m/%Y"), "Deposited Rs."+amount, '+'+amount, balance+int(amount)])
        cur.execute("UPDATE Users SET Trans_Hist = ? WHERE rowid = ?",(str(trans_hist),user_list[0]))
        
        messagebox.showinfo("Transaction succesfull","Transaction completed successfully")
        update_info()

    conn.commit()
    conn.close()
    return()
    
def withdraw(amount):
    conn=sqlite3.connect("Database.db")
    cur=conn.cursor()

    if amount=='':
        messagebox.showwarning("Invalid withdraw amount","Please enter amount to withdraw")
    elif not amount.isdigit():
        messagebox.showwarning("Invalid withdraw amount","Amount to withdraw should be a number")
    else:
        update_info()
        balance=int(user_list[4])
        
        if int(amount)>balance:
            messagebox.showwarning("Error","You cannot withdraw more than you have in your account")
        else:
            auth_win=Toplevel(main_win)
            auth_win.title("Authentication")

            Logo = ImageTk.PhotoImage(Image.open('Bank Logo.jpg'))
            auth_win.iconphoto(False, Logo)

            def confirm_pass():
                    if tb_pass.get()==user_list[3]:
                        auth_win.destroy()
                        
                        cur.execute("UPDATE Users SET Balance = ? WHERE rowid = ?",(balance-int(amount),user_list[0]))
                        conn.commit()

                        trans_hist=list(user_list[5])
                        if len(trans_hist)>=trans_hist_limit:
                            trans_hist.pop(0)
                        trans_hist.append([time.strftime("%d/%m/%Y"), "Withdrawed Rs."+amount , '-'+amount, balance-int(amount)])
                        cur.execute("UPDATE Users SET Trans_Hist = ? WHERE rowid = ?",(str(trans_hist),user_list[0]))
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
            auth_win.bind('<Return>', lambda event:confirm_pass())

            auth_win.mainloop()
                
    conn.commit()
    conn.close()
    return()

def transfer(amount,user):
    conn=sqlite3.connect("Database.db")
    cur=conn.cursor()
    
    if amount=='':
        messagebox.showwarning("Invalid transfer amount","Please enter amount to transfer")
    elif not amount.isdigit():
        messagebox.showwarning("Invalid transfer amount","Amount to transfer should be a number")
    elif user==user_list[2]:
        messagebox.showwarning("Invalid Username","You cannot transfer money to yourself")
    else:
        update_info()
        balance=int(user_list[4])
        
        cur.execute("SELECT rowid, Balance, Trans_Hist, Notifications FROM Users WHERE Username=?",(user,))
        conn.commit()
        transferee_list=cur.fetchone()
        
        if float(amount) > balance:
            messagebox.showwarning("Error","You cannot transfer more than you have in your account")
        elif transferee_list==None:
            messagebox.showwarning("Invalid Username","No account with username "+user+" exists")
        else:
            auth_win=Toplevel(main_win)
            auth_win.title("Authentication")

            Logo = ImageTk.PhotoImage(Image.open('Bank Logo.jpg'))
            auth_win.iconphoto(False, Logo)

            def confirm_pass():
                if tb_pass.get()==user_list[3]:
                    auth_win.destroy()
                    
                    cur.execute("UPDATE Users SET Balance=? WHERE rowid=?",(balance-int(amount),user_list[0]))
                    conn.commit()

                    cur.execute("UPDATE Users SET Balance=? WHERE rowid=?",(transferee_list[1]+int(amount),transferee_list[0]))
                    conn.commit()

                    trans_hist=list(user_list[5])
                    if len(trans_hist)>=trans_hist_limit:
                        trans_hist.pop(0)
                    trans_hist.append([time.strftime("%d/%m/%Y"), "Transferred Rs."+amount+" to "+user, '-'+amount, balance-int(amount)])
                    cur.execute("UPDATE Users SET Trans_Hist = ? WHERE rowid = ?",(str(trans_hist),user_list[0]))
                    conn.commit()

                    trans_hist=eval(transferee_list[2])
                    if len(trans_hist)>=trans_hist_limit:
                        trans_hist.pop(0)
                    trans_hist.append([time.strftime("%d/%m/%Y"), "Received Rs."+amount+" from "+user_list[2], '+'+amount, transferee_list[1]+int(amount)])
                    cur.execute("UPDATE Users SET Trans_Hist = ? WHERE rowid = ?",(str(trans_hist),transferee_list[0]))
                    conn.commit()

                    notifications=eval(transferee_list[3])
                    if len(notifications)>=notif_limit:
                        notifications.pop(0)
                    notifications.append("Received Rs."+amount+" from "+user_list[2])
                    cur.execute("UPDATE Users SET Notifications = ? WHERE rowid = ?", (str(notifications), transferee_list[0]))
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
            auth_win.bind('<Return>', lambda event:confirm_pass())

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
    user_list[5]=eval(user_list[5])

    lbl_balance.config(text=("Balance : "+str(user_list[4])))
    
    conn.commit()
    conn.close()

init()
