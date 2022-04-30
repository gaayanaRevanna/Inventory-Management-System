import email
from tkinter import*
from PIL import ImageTk
from tkinter import messagebox
import sqlite3
import os
class Login_System:
    def __init__(self,root):
        self.root=root
        self.root.title("                                                                                                                                                            Login System | Developed By Gaayana & Jayanth | TechnoCrats")
        self.root.geometry("1350x700+0+0")
        self.root.config(bg="#fafafa")
        #-------------images--------------
        self.phone_image=ImageTk.PhotoImage(file="images/phone.png")
        self.lbl_Phone_image=Label(self.root,image=self.phone_image,bd=0).place(x=200,y=50)

        #-------------Login_Frame---------
        self.user_id=StringVar()
        self.password=StringVar()

        login_frame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        login_frame.place(x=650,y=90,width=370,height=460)

        title=Label(login_frame,text="User Login",font=("Elephant",30,"bold"),bg="white").place(x=0,y=30,relwidth=1)

        lbl_user=Label(login_frame,text="User ID",font=("Rockwell",15),bg="white",fg="#767171").place(x=40,y=100)
        txt_user_id=Entry(login_frame,textvariable=self.user_id,font=("Andalus",15),bg="alice blue",fg="gray10").place(x=50,y=140,width=250)

        lbl_pass=Label(login_frame,text="Password",font=("Rockwell",15),bg="white",fg="#767171").place(x=40,y=200)
        txt_pass=Entry(login_frame,textvariable=self.password,show="*",font=("Andalus",15),bg="alice blue",fg="gray10").place(x=50,y=240,width=250)

        btn_login=Button(login_frame,command=self.login,text="Login ~>",font=("Arial Rounded MT Bold",15),bg="green4",activebackground="#27AE60",fg="mint cream",activeforeground="white",cursor="hand2").place(x=50,y=300,width=250,height=35)
        hr=Label(login_frame,bg="lightgray").place(x=50,y=370,width=250,height=2)
        or_=Label(login_frame,text="OR",bg="white",fg="#767171",font=("times new roman",15)).place(x=150,y=355)
        btn_forget=Button(login_frame,text='Forgot Password?',command=self.forgot_window,font=("Andalus",13),bg="white",fg="dodgerblue4",bd=0,activebackground="white",activeforeground="navy").place(x=110,y=390)

        #---------Frame2------------
        register_frame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        register_frame.place(x=650,y=570,width=370,height=60)
        lbl_reg=Label(register_frame,text="Don't have an account ?",font=("Andalus",13),bg="white",fg="gray10").place(x=40,y=15)
        btn_signup=Button(register_frame,text='Sign Up',command=self.Register,font=("Andalus",13),bg="white",fg="dodgerblue4",bd=0,activebackground="white",activeforeground="navy").place(x=230,y=12)

        #---------Animation Images-------
        self.im1=ImageTk.PhotoImage(file="images/im1.png")
        self.im2=ImageTk.PhotoImage(file="images/im2.png")
        self.im3=ImageTk.PhotoImage(file="images/im3.png")
        self.lbl_change_image=Label(self.root,bg="white")
        self.lbl_change_image.place(x=367,y=153,width=240,height=428)

        self.animate()

#-------------------All Functions-----------------------------------------
    def animate(self):
        self.im=self.im1
        self.im1=self.im2
        self.im2=self.im3
        self.im3=self.im
        self.lbl_change_image.config(image=self.im)
        self.lbl_change_image.after(2000,self.animate)

    def login(self):
        con=sqlite3.connect(database=r'ims.db') 
        cur=con.cursor()
        try:
            if self.user_id.get()=="" or self.password.get()=="":
                messagebox.showerror('Error',"All fields are required",parent=self.root)
            else:
                cur.execute("select utype from register where userid=? AND upass=?",(self.user_id.get(),self.password.get()))
                user=cur.fetchone()
                if user==None:
                    messagebox.showerror('Error',"Invalid EMPLOYEE ID/PASSWORD",parent=self.root)
                else:
                    if user[0]=="Employee":
                        self.root.destroy()
                        os.system("python billing.py")
                    else:
                        self.root.destroy()
                        os.system("python dashboard.py")
        except Exception as ex:
            messagebox.showerror("Error",f'Error due to: {str(ex)}',parent=self.root)

    def forgot_window(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.employee_id.get()=="":
                messagebox.showerror('Error',"Employee ID is required!!",parent=self.root)
            else:
                cur.execute("select email from employee where eid=?",(self.employee_id.get(),))
                email=cur.fetchone()
                if email==None:
                    messagebox.showerror('Error',"Invalid EMPLOYEE ID,try agaim",parent=self.root)
                else:
                    #------------------Forgot Window--------------------
                    self.var_otp=StringVar()
                    self.var_new_pass=StringVar()
                    self.var_conf_pass=StringVar()
                    #call send_email_function()
                    self.forgot_win=Toplevel(self.root)
                    self.forgot_win.title('RESET PASSWORD')
                    self.forgot_win.geometry('400x350+500+100')
                    self.forgot_win.focus_force()
                    title=Label(self.forgot_win,text='Reset Password',font=("Elephant",15),bg="navy",fg="white").pack(side=TOP,fill=X)
                    lbl_reset=Label(self.forgot_win,text="Enter OTP sent on registered Email:",font=("rockwell",15)).place(x=20,y=60)
                    txt_reset=Entry(self.forgot_win,textvariable=self.var_otp,font=("Andalus",15),bg="alice blue",fg="gray10").place(x=20,y=100,width=250,height=30)
                    self.btn_reset=Button(self.forgot_win,text="Submit",font=("Arial Rounded MT Bold",15),bg='dodgerblue4',fg='azure')
                    self.btn_reset.place(x=280,y=99,width=100,height=30)

                    lbl_new_pass=Label(self.forgot_win,text="New Password:",font=("rockwell",15)).place(x=20,y=160)
                    txt_new_pass=Entry(self.forgot_win,textvariable=self.var_new_pass,font=("Andalus",15),bg="alice blue",fg="gray10").place(x=20,y=190,width=250,height=30)

                    lbl_c_pass=Label(self.forgot_win,text="Confirm Password:",font=("rockwell",15)).place(x=20,y=225)
                    txt_c_pass=Entry(self.forgot_win,textvariable=self.var_conf_pass,font=("Andalus",15),bg="alice blue",fg="gray10").place(x=20,y=255,width=250,height=30)
                    self.btn_update=Button(self.forgot_win,text="Update",state=DISABLED,font=("Arial Rounded MT Bold",15),bg='dodgerblue4',fg='azure')
                    self.btn_update.place(x=100,y=299,width=100,height=30)

        except Exception as ex:
            messagebox.showerror("Error",f'Error due to: {str(ex)}',parent=self.root)

    def Register(self):
        os.system("python register.py")        



root=Tk()
obj=Login_System(root)
root.mainloop()