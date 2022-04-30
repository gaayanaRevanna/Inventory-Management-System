from tkinter import*
from PIL import Image,ImageTk
from tkinter import ttk,messagebox 
import sqlite3
import time
import os
import tempfile
class BillClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1350x700+0+0")
        self.root.title("                                                                                                                             Inventory Management System | Developed By Gaayana And Jayanth")
        self.root.config(bg="white")
        self.cart_list=[]
        self.chk_print=0
        #----title----
        self.icon_title=PhotoImage(file="images/logo1.png")
        title=Label(self.root,text="Inventory Management System",image=self.icon_title,compound=LEFT,font=("rockwell",40,"bold"),bg="cyan4",fg="white",anchor="w",padx=20).place(x=0,y=0,relwidth=1,height=70)

        #----btn_logout----
        btn_logout=Button(self.root,text="Logout",command=self.logout,font=("rockwell",15,"bold"),bg="orangered2",cursor="hand2").place(x=1100,y=10,height=50,width=150)

        #----clock----
        self.lbl_clock=Label(self.root,text="Welcome to Inventory Management System\t\t Date: DD-MM-YYYY\t\t Time: HH:MM:SS",font=("rockwell",15,"italic"),bg="navy",fg="white")
        self.lbl_clock.place(x=0,y=70,relwidth=1,height=30)

        #========product_Frame=============
        ProductFrame1=Frame(self.root,bd=4,relief=RIDGE,bg="white")
        ProductFrame1.place(x=6,y=110,width=410,height=550)
        pTitle=Label(ProductFrame1,text="All Products",font=("rockwell",20),bg="dodgerblue4",fg="white").pack(side=TOP,fill=X)

        #=========product search frame==========
        self.var_search=StringVar() 
        ProductFrame2=Frame(ProductFrame1,bd=2,relief=RIDGE,bg="white")
        ProductFrame2.place(x=2,y=42,width=398,height=90) 

        lbl_search=Label(ProductFrame2,text="Search Product | By Name",font=("rockwell",15),bg="white",fg="green4").place(x=2,y=5)

        lbl_search=Label(ProductFrame2,text="Product Name",font=("rockwell",14),bg="white").place(x=2,y=45)
        txt_search=Entry(ProductFrame2,textvariable=self.var_search,font=("times new roman",15),bg="ivory").place(x=130,y=47,width=150,height=22)
        btn_search=Button(ProductFrame2,text="Search",command=self.search,font=("rockwell",15),bg="deepskyblue3",fg="white",cursor="hand2").place(x=285,y=45,width=100,height=25)
        btn_show_all=Button(ProductFrame2,text="Show all",command=self.show,font=("rockwell",15),bg="#083531",fg="white",cursor="hand2").place(x=285,y=10,width=100,height=25)

        #----------product details frame-----------------
        ProductFrame3=Frame(ProductFrame1,bd=3,relief=RIDGE)
        ProductFrame3.place(x=2,y=140,width=398,height=375)


        scrolly=Scrollbar(ProductFrame3,orient=VERTICAL)
        scrollx=Scrollbar(ProductFrame3,orient=HORIZONTAL)

        self.product_Table=ttk.Treeview(ProductFrame3,columns=("pid","name","price","qty","status"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.product_Table.xview)
        scrolly.config(command=self.product_Table.yview)

        self.product_Table.heading("pid",text="PID")
        self.product_Table.heading("name",text="Name")
        self.product_Table.heading("price",text="Price")
        self.product_Table.heading("qty",text="QTY")
        self.product_Table.heading("status",text="Status")
        self.product_Table["show"]="headings"
        self.product_Table.column("pid",width=50)
        self.product_Table.column("name",width=100)
        self.product_Table.column("price",width=100)
        self.product_Table.column("qty",width=50)
        self.product_Table.column("status",width=90)
        self.product_Table.pack(fill=BOTH,expand=1)
        self.product_Table.bind("<ButtonRelease-1>",self.get_data)
        lbl_note=Label(ProductFrame1,text="Note:'Enter 0 quantity to remove the product from the cart'",font=("times new roman",13),anchor='w',bg="white",fg="red4").pack(side=BOTTOM,fill=X)

        #=========customer frame========================= 
        self.var_cname=StringVar() 
        self.var_contact=StringVar()
        CustomerFrame1=Frame(self.root,bd=4,relief=RIDGE,bg="white")
        CustomerFrame1.place(x=420,y=110,width=530,height=70)    

        cTitle=Label(CustomerFrame1,text="Customer Details",font=("rockwell",15),bg="gray80").pack(side=TOP,fill=X)

        lbl_name=Label(CustomerFrame1,text="Name",font=("rockwell",15),bg="white").place(x=5,y=30)
        txt_name=Entry(CustomerFrame1,textvariable=self.var_cname,font=("times new roman",13),bg="ivory").place(x=70,y=35,width=180)

        lbl_contact=Label(CustomerFrame1,text="Contact No.",font=("rockwell",15),bg="white").place(x=270,y=30)
        txt_contact=Entry(CustomerFrame1,textvariable=self.var_contact,font=("times new roman",13),bg="ivory").place(x=380,y=35,width=140)
        #=============cal_cart frame==================== 

        Cal_Cart_Frame=Frame(self.root,bd=4,relief=RIDGE,bg="white")
        Cal_Cart_Frame.place(x=420,y=190,width=530,height=360) 
        

        #============calculator frame============
        self.var_cal_input=StringVar()
        Cal_Frame=Frame(Cal_Cart_Frame,bd=9,relief=RIDGE,bg="aquamarine")
        Cal_Frame.place(x=5,y=10,width=268,height=340) 
        self.txt_cal_input=Entry(Cal_Frame,textvariable=self.var_cal_input,font=('Arial',15,'bold'),width=21,bd=10,relief=GROOVE,state='readonly',justify=RIGHT)
        self.txt_cal_input.grid(row=0,columnspan=4)

        btn_7=Button(Cal_Frame,text='7',font=('arial',15,'bold'),command=lambda:self.get_input(7),bd=5,width=4,pady=10,cursor='hand2').grid(row=1,column=0)
        btn_8=Button(Cal_Frame,text='8',font=('arial',15,'bold'),command=lambda:self.get_input(8),bd=5,width=4,pady=10,cursor='hand2').grid(row=1,column=1)
        btn_9=Button(Cal_Frame,text='9',font=('arial',15,'bold'),command=lambda:self.get_input(9),bd=5,width=4,pady=10,cursor='hand2').grid(row=1,column=2)
        btn_sum=Button(Cal_Frame,text='+',font=('arial',15,'bold'),command=lambda:self.get_input('+'),bd=5,width=4,pady=10,cursor='hand2').grid(row=1,column=3)
        
        btn_4=Button(Cal_Frame,text='4',font=('arial',15,'bold'),command=lambda:self.get_input(4),bd=5,width=4,pady=10,cursor='hand2').grid(row=2,column=0)
        btn_5=Button(Cal_Frame,text='5',font=('arial',15,'bold'),command=lambda:self.get_input(5),bd=5,width=4,pady=10,cursor='hand2').grid(row=2,column=1)
        btn_6=Button(Cal_Frame,text='6',font=('arial',15,'bold'),command=lambda:self.get_input(6),bd=5,width=4,pady=10,cursor='hand2').grid(row=2,column=2)
        btn_sub=Button(Cal_Frame,text='-',font=('arial',15,'bold'),command=lambda:self.get_input('-'),bd=5,width=4,pady=10,cursor='hand2').grid(row=2,column=3)

        btn_1=Button(Cal_Frame,text='1',font=('arial',15,'bold'),command=lambda:self.get_input(1),bd=5,width=4,pady=10,cursor='hand2').grid(row=3,column=0)
        btn_2=Button(Cal_Frame,text='2',font=('arial',15,'bold'),command=lambda:self.get_input(2),bd=5,width=4,pady=10,cursor='hand2').grid(row=3,column=1)
        btn_3=Button(Cal_Frame,text='3',font=('arial',15,'bold'),command=lambda:self.get_input(3),bd=5,width=4,pady=10,cursor='hand2').grid(row=3,column=2)
        btn_mul=Button(Cal_Frame,text='*',font=('arial',15,'bold'),command=lambda:self.get_input('*'),bd=5,width=4,pady=10,cursor='hand2').grid(row=3,column=3)

        btn_0=Button(Cal_Frame,text='0',font=('arial',15,'bold'),command=lambda:self.get_input(0),bd=5,width=4,pady=15,cursor='hand2').grid(row=4,column=0)
        btn_C=Button(Cal_Frame,text='C',font=('arial',15,'bold'),command=self.clear_cal,bd=5,width=4,pady=15,cursor='hand2').grid(row=4,column=1)
        btn_eq=Button(Cal_Frame,text='=',font=('arial',15,'bold'),command=self.perform_cal,bd=5,width=4,pady=15,cursor='hand2').grid(row=4,column=2)
        btn_div=Button(Cal_Frame,text='/',font=('arial',15,'bold'),command=lambda:self.get_input('/'),bd=5,width=4,pady=15,cursor='hand2').grid(row=4,column=3)



        #==============cart frame==================
        cart_frame=Frame(Cal_Cart_Frame,bd=3,relief=RIDGE)
        cart_frame.place(x=280,y=8,width=245,height=342)
        self.cartTitle=Label(cart_frame,text="Cart \t Total Products: [0]",font=("rockwell",13),bg="gray80")
        self.cartTitle.pack(side=TOP,fill=X)


        scrolly=Scrollbar(cart_frame,orient=VERTICAL)
        scrollx=Scrollbar(cart_frame,orient=HORIZONTAL)

        self.CartTable=ttk.Treeview(cart_frame,columns=("pid","name","price","qty"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.CartTable.xview)
        scrolly.config(command=self.CartTable.yview)

        self.CartTable.heading("pid",text="PID")
        self.CartTable.heading("name",text="Name")
        self.CartTable.heading("price",text="Price")
        self.CartTable.heading("qty",text="QTY")       
        self.CartTable["show"]="headings"
        self.CartTable.column("pid",width=40)
        self.CartTable.column("name",width=90)
        self.CartTable.column("price",width=90)
        self.CartTable.column("qty",width=40)
        self.CartTable.pack(fill=BOTH,expand=1)
        self.CartTable.bind("<ButtonRelease-1>",self.get_data_cart)

        #==============add cart widget frame===================
        self.var_pid=StringVar()
        self.var_pname=StringVar()
        self.var_price=StringVar()
        self.var_qty=StringVar()
        self.var_stock=StringVar()
        
        Add_CartWidgetFrame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        Add_CartWidgetFrame.place(x=420,y=550,width=530,height=110) 

        lbl_p_name=Label(Add_CartWidgetFrame,text="Product Name",font=("rockwell",15),bg="white").place(x=5,y=5)
        txt_p_name=Entry(Add_CartWidgetFrame,textvariable=self.var_pname,font=("times new roman",15),bg="ivory",state='readonly').place(x=5,y=35,width=190,height=22)

        lbl_p_price=Label(Add_CartWidgetFrame,text="Price per qty",font=("rockwell",15),bg="white").place(x=230,y=5)
        txt_p_price=Entry(Add_CartWidgetFrame,textvariable=self.var_price,font=("times new roman",15),bg="ivory",state='readonly').place(x=230,y=35,width=150,height=22)

        lbl_p_qty=Label(Add_CartWidgetFrame,text="Quantity",font=("rockwell",15),bg="white").place(x=390,y=5)
        txt_p_qty=Entry(Add_CartWidgetFrame,textvariable=self.var_qty,font=("times new roman",15),bg="ivory").place(x=390,y=35,width=120,height=22)

        self.lbl_instock=Label(Add_CartWidgetFrame,text="In Stock",font=("rockwell",15),bg="white")
        self.lbl_instock.place(x=5,y=70)

        btn_clear_cart=Button(Add_CartWidgetFrame,text="Clear",command=self.clear_cart,font=("rockwell",15),bg="gray30",cursor="hand2").place(x=180,y=70,width=150,height=30)
        btn_add_cart=Button(Add_CartWidgetFrame,text="Add | Update Cart",command=self.add_update_cart,font=("rockwell",15),bg="dark orange",cursor="hand2").place(x=340,y=70,width=180,height=30)

        #=============billing area=======================
        billFrame=Frame(self.root,bd=2,relief=RIDGE,bg='white')
        billFrame.place(x=953,y=110,width=320,height=410)
        bTitle=Label(billFrame,text="Customer Bill Area",font=("rockwell",20),bg="orangered",fg="white").pack(side=TOP,fill=X)
        scrolly=Scrollbar(billFrame,orient=VERTICAL)
        scrolly.pack(side=RIGHT,fill=Y)
        self.txt_bill_area=Text(billFrame,yscrollcommand=scrolly.set)
        self.txt_bill_area.pack(fill=BOTH,expand=1)
        scrolly.config(command=self.txt_bill_area.yview)
        #============billing button====================
        billMenuFrame=Frame(self.root,bd=2,relief=RIDGE,bg='white')
        billMenuFrame.place(x=953,y=520,width=320,height=140)

        self.lbl_amt=Label(billMenuFrame,text="Bill Amount\n[0]",font=("goudy old style",15,"bold"),bg='midnightblue',fg="white")
        self.lbl_amt.place(x=2,y=5,width=105,height=70)

        self.lbl_discount=Label(billMenuFrame,text="Discount\n[5%]",font=("goudy old style",15,"bold"),bg='olivedrab',fg="white")
        self.lbl_discount.place(x=110,y=5,width=105,height=70)

        self.lbl_net_pay=Label(billMenuFrame,text="Net Pay\n[0]",font=("goudy old style",15,"bold"),bg='lightsteelblue4',fg="white")
        self.lbl_net_pay.place(x=218,y=5,width=105,height=70)


        btn_print=Button(billMenuFrame,text="Print",command=self.print_bill,font=("goudy old style",15,"bold"),bg='springgreen3',fg="white",cursor="hand2")
        btn_print.place(x=2,y=80,width=105,height=50)

        btn_clear_all=Button(billMenuFrame,text="Clear All",command=self.clear_all,font=("goudy old style",15,"bold"),bg='gray40',fg="white",cursor="hand2")
        btn_clear_all.place(x=110,y=80,width=105,height=50)

        btn_generate=Button(billMenuFrame,text="Generate Bill",command=self.generate_bill,font=("goudy old style",13,"bold"),bg='turquoise4',fg="white",cursor="hand2")
        btn_generate.place(x=218,y=80,width=105,height=50)

        self.show()  
        self.update_date_time()

#==================All Functions=============================================
    def get_input(self,num):
        xnum=self.var_cal_input.get()+str(num)
        self.var_cal_input.set(xnum)

    def clear_cal(self):
        self.var_cal_input.set('') 

    def perform_cal(self):
        result=self.var_cal_input.get()
        self.var_cal_input.set(eval(result))    

    def show(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            cur.execute("select pid,name,price,qty,status from product where status='Active'")
            rows=cur.fetchall()
            self.product_Table.delete(*self.product_Table.get_children())
            for row in rows:
                self.product_Table.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f'Error due to: {str(ex)}',parent=self.root)  

    def search(self):  
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:            
            if self.var_search.get()=="":   
                messagebox.showerror("Error","Search Input is required",parent=self.root)
            else:            
                cur.execute("select pid,name,price,qty,status from product where name LIKE '%"+self.var_search.get()+"%' and status='Active'")
                rows=cur.fetchall()
                if len(rows)!=0:        
                    self.product_Table.delete(*self.product_Table.get_children())
                    for row in rows:
                        self.product_Table.insert('',END,values=row)
                else:
                    messagebox.showerror("Error","No record found",parent=self.root)      
        except Exception as ex:
            messagebox.showerror("Error",f'Error due to: {str(ex)}',parent=self.root)  


    def get_data(self,ev):
        f=self.product_Table.focus()
        content=(self.product_Table.item(f))
        row=content['values']  
        self.var_pid.set(row[0])
        self.var_pname.set(row[1])
        self.var_price.set(row[2])
        self.lbl_instock.config(text=f"in stock [{str(row[3])}]")
        self.var_stock.set(row[3])
        self.var_qty.set('1')


    def get_data_cart(self,ev):
        f=self.CartTable.focus()
        content=(self.CartTable.item(f))
        row=content['values']  
        self.var_pid.set(row[0])
        self.var_pname.set(row[1])
        self.var_price.set(row[2])
        self.var_qty.set(row[3])
        self.lbl_instock.config(text=f"In Stock [{str(row[4])}]")
        self.var_stock.set(row[4])        


    def add_update_cart(self):
        if self.var_pid.get()=='':
            messagebox.showerror('Error',"Please select product from the list",parent=self.root)
        elif self.var_qty.get()=='':
            messagebox.showerror('Error',"Quantity is required!",parent=self.root)
        elif int(self.var_qty.get())>int(self.var_stock.get()):  
            messagebox.showerror('Error',"Invalid Quantity",parent=self.root)  
        else:  
            #price_cal=float(int(self.var_qty.get())*float(self.var_price.get())) 
            price_cal=self.var_price.get()   
            cart_data=[self.var_pid.get(),self.var_pname.get(),price_cal,self.var_qty.get(),self.var_stock.get()]   
            #==============update cart====================
            present='no'
            index_=0
            for row in self.cart_list:
                if self.var_pid.get()==row[0]:
                    present='yes'
                    break
                index_+=1
            if present=='yes':
                op=messagebox.askyesno('Confirm',"Product already present\nDo you want to Update|Remove from the Cart List",parent=self.root)    
                if op==True:
                    if self.var_qty.get()=="0":
                        self.cart_list.pop(index_)
                    else:
                        #self.cart_list[index_][2]=price_cal
                        self.cart_list[index_][3]=self.var_qty.get()   
            else:  
                self.cart_list.append(cart_data)
            self.show_cart()  
            self.bill_updates()     


    def bill_updates(self):
        self.bill_amnt=0
        self.net_pay=0
        self.discount=0
        for row in self.cart_list:
            self.bill_amnt=self.bill_amnt+(float(row[2])*int(row[3]))
        self.discount=(self.bill_amnt*5)/100
        self.net_pay=self.bill_amnt-self.discount 
        self.lbl_amt.config(text=f'Bill Amnt\n{str(self.bill_amnt)}')
        self.lbl_net_pay.config(text=f'Net Pay\n{str(self.net_pay)}')   
        self.cartTitle.config(text=f"Cart \t Total Products: [{str(len(self.cart_list))}]")


    def show_cart(self):
        try:
            self.CartTable.delete(*self.CartTable.get_children())
            for row in self.cart_list:
                self.CartTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f'Error due to: {str(ex)}',parent=self.root)


    def generate_bill(self):
        if self.var_cname.get()=='' or self.var_contact.get()=='':
            messagebox.showerror("Error",f'Customer Details Should Be Entered',parent=self.root)
        elif len(self.cart_list)==0:
            messagebox.showerror("Error",f'Please Add product to this cart!!!',parent=self.root)
        else:
            #===========bill top=======
            self.bill_top()
            #===========bill middle=======
            self.bill_middle()
            #===========bill bottom=======
            self.bill_bottom()
            #--------------------------------------
            fp=open(f'bill/{str(self.invoice)}.txt','w')
            fp.write(self.txt_bill_area.get('1.0',END))
            fp.close()
            messagebox.showinfo('Saved',"Bill has been generated/Saved in Backend",parent=self.root)
            self.chk_print=1


    def bill_top(self):
        self.invoice=int(time.strftime("%H%M%S"))+int(time.strftime("%d%m%Y"))
        bill_top_temp=f'''
  \tXYZ-Inventory
 Phone No. 98725***** B'lore-560008
{str("="*36)}
 Customer Name: {self.var_cname.get()}
 Ph no. :{self.var_contact.get()}
 Bill No. {str(self.invoice)}\t\tDate: {str(time.strftime("%d/%m/%Y"))}
{str("="*36)}
 Product Name    \t\tQTY \tPrice
{str("="*36)}
        '''
        self.txt_bill_area.delete('1.0',END)
        self.txt_bill_area.insert('1.0',bill_top_temp)

    def bill_bottom(self):
        bill_bottom_temp=f'''
{str("="*36)}
 Bill Amount\t\tRs.{self.bill_amnt}
 Discount\t\tRs.{self.discount}
 Net Pay\t\tRs.{self.net_pay}
{str("="*36)}\n
        '''
        self.txt_bill_area.insert(END,bill_bottom_temp)


    def bill_middle(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            for row in self.cart_list:
            # pid,name,price,qty,stock
                pid=row[0]
                name=row[1]
                qty=int(row[4])-int(row[3])
                if int(row[3])==int(row[4]):
                    status='Inactive'
                if int(row[3])!=int(row[4]):
                    status='Active'
                price=float(row[2])*int(row[3])
                price=str(price)
                self.txt_bill_area.insert(END,"\n "+name+"       \t\t"+row[3]+" \tRs."+price)
                #--------------Update qty in product table-------------------
                cur.execute('Update product set qty=?,status=? where pid=?',(
                    qty,
                    status,
                    pid
                ))
                con.commit()
            con.close()
            self.show()
        except Exception as ex:
            messagebox.showerror("Error",f'Error due to: {str(ex)}',parent=self.root)


    def clear_cart(self):
        self.var_pid.set('')
        self.var_pname.set('')
        self.var_price.set('')
        self.var_qty.set('')
        self.lbl_instock.config(text=f"In Stock")
        self.var_stock.set('')

    def clear_all(self):
        del self.cart_list[:]
        self.var_cname.set('')
        self.var_contact.set('')
        self.txt_bill_area.delete('1.0',END)
        self.cartTitle.config(text=f"Cart \t Total Product: [0]")
        self.var_search.set('')
        self.clear_cart()
        self.show()
        self.show_cart()

    def update_date_time(self):
        time_=time.strftime("%I:%M:%S")
        date_=time.strftime("%d-%m-%Y")
        self.lbl_clock.config(text=f"Welcome to Inventory Management System\t\t Date: {str(date_)}\t\t Time: {str(time_)}")
        self.lbl_clock.after(200,self.update_date_time)

    def print_bill(self):
        if self.chk_print==1:
            messagebox.showinfo('Print',"Please wait while printing",parent=self.root)
        else:
            messagebox.showinfo('Print',"Please generate bill, to print the receipt",parent=self.root)
            new_file=tempfile.mktemp('.txt')
            open(new_file,'w').write(self.txt_bill_area.get('1.0',END))
            os.startfile(new_file,'print')

    def logout(self):
        self.root.destroy()
        os.system("python login.py")

if __name__=="__main__":
    root=Tk()
    obj=BillClass(root)
    root.mainloop()
