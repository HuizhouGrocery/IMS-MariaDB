import tkinter as tk
import ttkbootstrap as ttk
from tkinter import messagebox,PhotoImage,simpledialog
import json
import pymysql
from time import strftime
import pywinstyles
import uuid

PASSWORD = "12345"

def generate_short_uuid():
        #create random id for our ID PRIMARY KEY
        u = uuid.uuid4()
        first_five_chars = str(u)[:5]
        first_five_int = int(first_five_chars, 16)
        scaled_int = (first_five_int % 99999) + 1
        return scaled_int


def check_password():
        root = tk.Toplevel()
        root.withdraw() # Hide the main window
        root.iconbitmap(default=r"Your Working Directory\logo.png")

        attempt = simpledialog.askstring("Password Required ", "Please enter password if you want to continue:", show='*')
        if attempt == PASSWORD:
              messagebox.showinfo("Access Granted", "Password accepted! Performing sensitive command...")
              return True
        else:
              messagebox.showerror("Access Denied", "Incorrect password.")

        root.destroy()


class DatabaseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MariaDB Database Huizhou Grocery Inventory Management System")
        self.root.geometry("1100x800")
        self.root.tk.call("wm", "iconphoto", root._w, tk.PhotoImage(file=r"Your Working Directory\Order_image\logo.png"))
        pywinstyles.apply_style(root,"win7")

        # connect to an existing one Database
        # localhost means your current Desktop(laptop) or You could change it to server address
        # You will set up root and default password when you install MariaDB

        self.conn = pymysql.connect(host='localhost',user='root',password='default_password ',database='user or other name ')
        self.cursor = self.conn.cursor()

        # # Create a table if it doesn't exist
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS inventory (id INTEGER PRIMARY KEY, product_id TEXT, product_name TEXT, quantity TEXT)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS quantity_change (id BIGINT NOT NULL PRIMARY KEY, product_id TEXT, product_name TEXT, quantity_change_text TEXT,time TEXT)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS product_change (id INTEGER PRIMARY KEY,product_id TEXT, product_name TEXT, product_change_text TEXT,time TEXT )''')

        self.conn.commit()

        # Put logo image into GUI

        self.image = PhotoImage(file=r"Your Working Directory\logo.png")
        self.image_label = ttk.Label(root, image=self.image)
        self.image_label.place(x=500, y=20, width=110, height=127)


        # Create an entry box for the product ID
        self.product_id_label = ttk.Label(root, text="Product ID:",font=("Arial", 10))
        self.product_id_label.pack(pady=10)
        self.product_id_label.place(x=150, y=220)

        self.product_id_entry = ttk.Entry(root, state="normal")
        self.product_id_entry.pack(pady=10)
        self.product_id_entry.place(x=260, y=215)

        # Create a label for the product name
        self.product_name_label = ttk.Label(root, text="Product Name:",font=("Arial", 10))
        self.product_name_label.pack()
        self.product_name_label.place(x=150, y=275)

        # Create an entry box for the product name
        self.product_name_entry = ttk.Entry(root, state="normal")
        self.product_name_entry.pack(pady=10)
        self.product_name_entry.place(x=260, y=270)

        # Create a label for the product quantity
        self.product_quantity_label = ttk.Label(root, text="Quantity (Qty):",font=("Arial", 10))
        self.product_quantity_label.pack()
        self.product_quantity_label.place(x=150, y=325)

        self.product_quantity_entry = ttk.Entry(root, state="normal")
        self.product_quantity_entry.pack(pady=10)
        self.product_quantity_entry.place(x=260, y=320)

        # Create a label for the product quantity change
        self.quantity_change_label = ttk.Label(root, text="Quantity Change:",font=("Arial", 10))
        self.quantity_change_label.pack()
        self.quantity_change_label.place(x=150, y=380)

        # Create an entry box for the product quantity change
        self.quantity_change_entry = ttk.Entry(root, state="normal")
        self.quantity_change_entry.pack(pady=10)
        self.quantity_change_entry.place(x=260, y=375)

        # Create a button to get product details
        self.calculate_button = ttk.Button(root, text="Get Product",command=self.get_product)
        self.calculate_button.pack(pady=10)
        self.calculate_button.place(x=200, y=620,width = 120,height=45)

        # Create a button to add quantity
        self.add_quantity_button = ttk.Button(root, text="Add Quantity",command=self.add_quantity)
        self.add_quantity_button.pack(pady=10)
        self.add_quantity_button.place(x=400, y=620,width = 120,height=45)

        # Create a button to subtract quantity
        self.subtract_quantity_button = ttk.Button(root, text="Subtract Quantity",command=self.subtract_quantity)
        self.subtract_quantity_button.pack(pady=10)
        self.subtract_quantity_button.place(x=600, y=620,width = 130,height=45)

        self.clear_entry_button = ttk.Button(root, text="Clear Entry",command=self.clear_entry)
        self.clear_entry_button.pack(pady=10)
        self.clear_entry_button.place(x=800, y=620,width = 120,height=45)

       # Create a button to add or delete product
        self.add_product_button = ttk.Button(root, text="Add Product",command=self.add_product)
        self.add_product_button.pack(pady=10)
        self.add_product_button.place(x=200, y=700,width = 120,height=45)

        self.delete_product_button = ttk.Button(root, text="Delete Product",command=self.delete_product)
        self.delete_product_button.pack(pady=10)
        self.delete_product_button.place(x=400, y=700,width = 120,height=45)

    def get_product(self):

     try:
        #  input product name to find product
         product_name = self.product_name_entry.get().strip()

         # Retrieve the product details from the product database

         self.cursor.execute("SELECT * FROM inventory WHERE product_name = %s" , (product_name,))
         rows = self.cursor.fetchall()

         self.conn.commit()

         columns = [col[0] for col in self.cursor.description]
         data = [dict(zip(columns, row)) for row in rows]

         products = json.dumps(data, indent=2)

         product = json.loads(products)

         if product:

             quantity = int(product[0]['quantity'])

             self.product_id_entry.config(state="normal")
             self.product_id_entry.delete(0, tk.END)
             self.product_id_entry.insert(0, product[0]['id'])

             self.product_name_entry.config(state="normal")
             self.product_name_entry.delete(0, tk.END)
             self.product_name_entry.insert(0, product[0]['product_name'])

             self.product_quantity_entry.config(state="normal")
             self.product_quantity_entry.delete(0, tk.END)
             self.product_quantity_entry.insert(0, quantity)

         else:
             messagebox.showerror("Error", "Product not found")

     except Exception:
              messagebox.showerror("Error", "Product not found or Please input product ID")

    def add_quantity(self):

         try:
              product_id = self.product_id_entry.get()
              product_name = self.product_name_entry.get()
              quantity_change =  int(self.quantity_change_entry.get())
              time = strftime('%Y-%m-%d %H:%M:%S %p %a')

              res = messagebox.askquestion('Product Details', f'Do you want to add {quantity_change} Qty to the {product_name} ? ')
              if   res == 'yes':
                quantity_change_text = f'Added {quantity_change} Qty to the {product_name}'
                self.cursor.execute('UPDATE inventory SET quantity = quantity + %s WHERE id = %s', (quantity_change, product_id))
                sql = "INSERT INTO quantity_change (id, product_id, product_name, quantity_change_text, time) VALUES (%s,%s,%s,%s,%s)"
                data = (generate_short_uuid(),product_id, product_name, quantity_change_text, time)
                self.cursor.execute(sql, data)

                self.conn.commit()

                self.product_id_entry.config(state="normal")
                self.product_id_entry.delete(0, tk.END)

                self.product_name_entry.config(state="normal")
                self.product_name_entry.delete(0, tk.END)

                self.product_quantity_entry.config(state="normal")
                self.product_quantity_entry.delete(0, tk.END)

                self.quantity_change_entry.config(state="normal")
                self.quantity_change_entry.delete(0, tk.END)

                messagebox.showinfo('Response', f"You have added {quantity_change} Qty to {product_name} !")

              elif res == 'no':
                messagebox.showinfo('Response', 'You need to check this product name and quantity')
              else:
                messagebox.showwarning('error', 'Something went wrong!')

         except Exception:
              messagebox.showerror("Error", "Please input quantity")

    def subtract_quantity(self):
         try:
            product_id = self.product_id_entry.get()
            product_name = self.product_name_entry.get()
            quantity_change =  int(self.quantity_change_entry.get())
            time = strftime('%Y-%m-%d %H:%M:%S %p %a')

            res = messagebox.askquestion('Product Details', f'Do you want to subtract {quantity_change} Qty from the {product_name} ? ')
            if   res == 'yes':
                    quantity_change_text = f'Subtracted {quantity_change} Qty from the {product_name}'
                    self.cursor.execute('UPDATE inventory SET quantity = quantity - %s WHERE id = %s', (quantity_change, product_id))
                    sql = "INSERT INTO quantity_change (id, product_id, product_name,quantity_change_text,time) VALUES (%s,%s,%s,%s,%s)"
                    data = (generate_short_uuid(), product_id, product_name, quantity_change_text, time)
                    self.cursor.execute(sql, data)

                    self.conn.commit()

                    self.product_id_entry.config(state="normal")
                    self.product_id_entry.delete(0, tk.END)

                    self.product_name_entry.config(state="normal")
                    self.product_name_entry.delete(0, tk.END)

                    self.product_quantity_entry.config(state="normal")
                    self.product_quantity_entry.delete(0, tk.END)

                    self.quantity_change_entry.config(state="normal")
                    self.quantity_change_entry.delete(0, tk.END)

                    messagebox.showinfo('Response', f"You have subtracted {quantity_change} Qty from the {product_name} !")

            elif res == 'no':
                    messagebox.showinfo('Response', 'You need to check this product name and quantity')
            else:
                    messagebox.showwarning('error', 'Something went wrong!')

         except Exception:
              messagebox.showerror("Error", "Please input quantity")

    def add_product(self):
         try:

           product_id = self.product_id_entry.get()
           product_name = self.product_name_entry.get()
           quantity = int(self.quantity_change_entry.get())
           time = strftime('%Y-%m-%d %H:%M:%S %p %a')

           self.cursor.execute("SELECT * FROM inventory WHERE product_id = %s" , (product_id,))
           rows = self.cursor.fetchall()
           self.cursor.execute("SELECT * FROM inventory WHERE product_name = %s" , (product_name,))
           row = self.cursor.fetchall()

           if rows == () and row == ():

                res = messagebox.askquestion('Product Details', f'Do you want to add {product_name} and {quantity} Qty of this ? ')
                if   res == 'yes':

                        if check_password() == True:
                                product_change = f"Added {quantity} Qty {product_name} to the database"
                                sql = "INSERT INTO inventory (id, product_id, product_name,quantity) VALUES (%s,%s,%s,%s)"
                                data = (product_id,product_id,product_name,quantity)
                                self.cursor.execute(sql, data)
                                sql = "INSERT INTO product_change (id, product_id, product_name,product_change_text,time) VALUES (%s,%s,%s,%s,%s)"
                                data = (generate_short_uuid(), product_id,product_name,product_change,time)
                                self.cursor.execute(sql, data)

                                self.conn.commit()

                                self.product_id_entry.config(state="normal")
                                self.product_id_entry.delete(0, tk.END)

                                self.product_name_entry.config(state="normal")
                                self.product_name_entry.delete(0, tk.END)

                                self.product_quantity_entry.config(state="normal")
                                self.product_quantity_entry.delete(0, tk.END)

                                self.quantity_change_entry.config(state="normal")
                                self.quantity_change_entry.delete(0, tk.END)

                                messagebox.showinfo('Response',f"You have added {product_name} and {quantity} Qty of this!")

                        else: messagebox.showwarning('error', 'Something went wrong!')

                elif res == 'no':
                        messagebox.showinfo('Response', 'You need to check this product name and quantity')
                else:
                        messagebox.showwarning('error', 'Something went wrong!')
           else:
                messagebox.showwarning('error', 'Product already exists or Product ID already exists')

         except Exception:
              messagebox.showerror("Error", "Product already exists or quantity change can not be empty")

    def delete_product(self):
         try:
            product_id = self.product_id_entry.get()
            product_name = self.product_name_entry.get()
            time = strftime('%Y-%m-%d %H:%M:%S %p %a')

            if product_id != '' and product_name != '':

                res = messagebox.askquestion('Product Details', f'Do you want to delete Product ID {product_id} and {product_name} from database? ')
                if   res == 'yes':

                        if check_password() == True:

                                product_change = f"Deleted Product ID {product_id} and Product Name {product_name} from the database"
                                sql = "DELETE FROM inventory WHERE id = %s"
                                data = (product_id,)
                                self.cursor.execute(sql, data)
                                sql = "INSERT INTO product_change (id, product_id, product_name,product_change_text,time) VALUES (%s,%s,%s,%s,%s)"
                                data = (generate_short_uuid(), product_id,product_name,product_change,time)
                                self.cursor.execute(sql, data)

                                self.conn.commit()

                                self.product_id_entry.config(state="normal")
                                self.product_id_entry.delete(0, tk.END)

                                self.product_name_entry.config(state="normal")
                                self.product_name_entry.delete(0, tk.END)

                                self.product_quantity_entry.config(state="normal")
                                self.product_quantity_entry.delete(0, tk.END)

                                self.quantity_change_entry.config(state="normal")
                                self.quantity_change_entry.delete(0, tk.END)

                                messagebox.showinfo('Response', f"You have deleted Product ID {product_id} and {product_name} from database!")

                        else: messagebox.showwarning('error', 'Something went wrong!')

                elif res == 'no':
                        messagebox.showinfo('Response', 'You need to check this product name and quantity')
                else:
                        messagebox.showwarning('error', 'Something went wrong!')

            else:
                messagebox.showerror("Error", "Please input product id and product name")

         except Exception:
              messagebox.showerror("Error", "Please input product id")

    def clear_entry(self):
      try:

        self.product_id_entry.delete(0, tk.END)
        self.product_name_entry.delete(0, tk.END)
        self.product_quantity_entry.delete(0, tk.END)
        self.quantity_change_entry.delete(0, tk.END)

      except Exception:
              messagebox.showerror("Error", "You have cleared all entries")


if __name__ == "__main__":
    root = tk.Tk()
    app = DatabaseApp(root)
    root.mainloop()
