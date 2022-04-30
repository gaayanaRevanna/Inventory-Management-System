from tkinter import*
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import sqlite3
class registrationClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1100x500+220+130")
        self.root.title("                                                                                                                             Inventory Management System | Developed By Gaayana And Jayanth")
        self.root.config(bg="white")
        self.root.focus_force()
        self.var_eid=StringVar()
        self.var_ename=StringVar()
        self.var_usertype=StringVar()
        self.var_userid=StringVar()
        self.var_pass=StringVar()
        self.var_cpass=StringVar()  
              
        #-----------------------registration frame----------------------------
        register_frame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        register_frame.place(x=50,y=10,width=450,height=480)
        #-----------------------title--------------------------------------------
        title=Label(register_frame,text="User Registration",font=("rockwell",18),bg="red",fg="white").pack(side=TOP,fill=X)
        #-----------------------------column1--------------------------------------
        lbl_eid=Label(register_frame,text="Employee ID",font=("times new roman",18),bg="white").place(x=30,y=60)
        lbl_ename=Label(register_frame,text="Name",font=("times new roman",18),bg="white").place(x=30,y=160)
        lbl_utype=Label(register_frame,text="User Type",font=("times new roman",18),bg="white").place(x=30,y=210)
        lbl_userid=Label(register_frame,text="User Id",font=("times new roman",18),bg="white").place(x=30,y=260)
        lbl_pass=Label(register_frame,text="Password",font=("times new roman",18),bg="white").place(x=30,y=310)
        lbl_cpass=Label(register_frame,text="Confirm Password",font=("times new roman",18),bg="white").place(x=30,y=360)
        #-----------------------------------column2--------------------------------
        txt_eid=Entry(register_frame,textvariable=self.var_eid,font=("rockwell",15),bg='ivory').place(x=220,y=60,width=200)
        txt_ename=Entry(register_frame,textvariable=self.var_ename,font=("rockwell",15),bg='ivory',state='readonly').place(x=220,y=160,width=200)
        txt_utype=Entry(register_frame,textvariable=self.var_usertype,font=("rockwell",15),bg='ivory',state='readonly').place(x=220,y=210,width=200)
        txt_userid=Entry(register_frame,textvariable=self.var_userid,font=("rockwell",15),bg='ivory').place(x=220,y=260,width=200)
        txt_pass=Entry(register_frame,textvariable=self.var_pass,font=("rockwell",15),bg='ivory').place(x=220,y=310,width=200)
        txt_cpass=Entry(register_frame,textvariable=self.var_cpass,font=("rockwell",15),bg='ivory').place(x=220,y=360,width=200)
        #---------------------------------------register button--------------------------------
        btn_register=Button(register_frame,text="Register",command=self.register,font=("rockwell",15),bg="deepskyblue3",fg="white",cursor="hand2").place(x=150,y=410,width=100,height=40)
        #--------------------------get data button------------------------------------------------------
        btn_get_data=Button(register_frame,text="Get Data",command=self.set_name_utype,font=("rockwell",15),bg="green",fg="white",cursor="hand2").place(x=150,y=100,width=110,height=40)
        #------------------------------------------image------------------------------------------------
        self.bill_photo=Image.open("images/cat2.jpg")
        self.bill_photo=self.bill_photo.resize((500,500),Image.ANTIALIAS)
        self.bill_photo=ImageTk.PhotoImage(self.bill_photo)
        lbl_image=Label(self.root,image=self.bill_photo,bd=0)
        lbl_image.place(x=550,y=50)
#------------------------functionality----------------------------------------
   
    def set_name_utype(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:      
            cur.execute("Select name from register where eid=?",(self.var_eid.get(),))
            name=cur.fetchone()                               
            self.var_ename.set(name[0])
            cur.execute("Select utype from employee register where eid=?",(self.var_eid.get(),))
            utype=cur.fetchone()                      
            self.var_usertype.set(utype[0])
            if name==None or utype==None:
                messagebox.showerror('Error',"no record found",parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error",f'Error due to: {str(ex)}',parent=self.root) 
    

    def register(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_eid.get()=="" or self.var_ename.get()=="" or self.var_usertype.get()=="" or self.var_userid.get()=="" or self.var_pass.get()=="" or self.var_cpass.get()=="" :
                    messagebox.showerror("Error","All fields must be entered",parent=self.root)
            else:
                    cur.execute("select * from register where eid=?",(self.var_eid.get(),))
                    row=cur.fetchone()
                    if row[3]!=None and row[4]!=None:
                        messagebox.showerror("Error","Already Registered",parent=self.root)
                    elif self.var_pass.get()!=self.var_cpass.get():
                        messagebox.showerror("Error","incorrect input in confirm password field",parent=self.root)   
                    else:
                        cur.execute("Update register set userid=?,upass=? where eid=?",(                                            
                                            self.var_userid.get(),
                                            self.var_pass.get(),     
                                            self.var_eid.get(),                                                                         
                        ))
                        con.commit()
                        messagebox.showinfo("Success","Sucessfully Register",parent=self.root)                        
        except Exception as ex:
                messagebox.showerror("Error",f'Error due to: {str(ex)}',parent=self.root)

if __name__=="__main__":
    root=Tk()
    obj=registrationClass(root)
    root.mainloop()        