import tkinter as tk
import random
import string
from tkinter import messagebox


class BankApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bank Application")
        self.root.configure(bg="#007BFF")  # Background color

        self.font_style = ("Helvetica", 12)
        self.label_font_style = ("Helvetica", 14, "bold")
        self.button_font_style = ("Helvetica", 12, "bold")

        self.username_label = tk.Label(root, text="Please Enter Username:", font=self.label_font_style, bg="#007BFF")
        self.username_label.pack()

        self.username_entry = tk.Entry(root, font=self.font_style)
        self.username_entry.pack()

        self.generate_password_button = tk.Button(root, text="Generate Password", font=self.button_font_style, command=self.generate_password)
        self.generate_password_button.pack()

        self.generated_password_label = tk.Label(root, text="Generated Password:", font=self.label_font_style, bg="#007BFF")
        self.generated_password_label.pack()

        self.generated_password_value = tk.StringVar()
        self.generated_password_display = tk.Label(root, textvariable=self.generated_password_value, font=self.font_style)
        self.generated_password_display.pack()

        self.balance_label = tk.Label(root, text="                  Please Enter Opening Balance:                  ", font=self.label_font_style, bg="#007BFF")
        self.balance_label.pack()

        self.balance_entry = tk.Entry(root, font=self.font_style)
        self.balance_entry.pack()

        self.register_button = tk.Button(root, text="Register", font=self.button_font_style, command=self.register)
        self.register_button.pack()

    def generate_password(self):

        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(characters) for _ in range(12))
        self.generated_password_value.set(password)
        username = self.username_entry.get()

        if not username:  # Check if username is empty
            messagebox.showerror("Error", "Username is required.")
            return




    def register(self):
        username = self.username_entry.get()
        balance = self.balance_entry.get()
        password = self.generated_password_value.get()

        if not username:  # Check if username is empty
            messagebox.showerror("Error", "Username is required.")
            return

        if not balance:  # Check if balance is empty
            messagebox.showerror("Error", "Opening balance is required.")
            return



        with open("users.txt", "a") as f:
            f.write(f"Username: {username}, Password: {password}, Balance: {balance}\n")

        self.username_entry.delete(0, tk.END)
        self.balance_entry.delete(0, tk.END)
        self.generated_password_value.set("")

        self.show_login_page(username, float(balance))


    def show_login_page(self, expected_username, opening_balance):
        self.root.destroy()
        login_root = tk.Tk()
        login_root.title("Login Page")
        login_root.configure(bg="#007BFF")

        self.login_font_style = ("Helvetica", 14, "bold")

        self.login_username_label = tk.Label(login_root, text="Username:", font=self.login_font_style, bg="#007BFF")
        self.login_username_label.pack()

        self.login_username_entry = tk.Entry(login_root, font=self.login_font_style)
        self.login_username_entry.pack()

        self.login_password_label = tk.Label(login_root, text="Password:", font=self.login_font_style, bg="#007BFF")
        self.login_password_label.pack()

        self.login_password_entry = tk.Entry(login_root, show="*", font=self.login_font_style)
        self.login_password_entry.pack()

        self.login_button = tk.Button(login_root, text="   Login   ", font=self.button_font_style, command=lambda: self.login(expected_username, opening_balance))
        self.login_button.pack()

        login_root.mainloop()

    def login(self, expected_username, opening_balance):
        username = self.login_username_entry.get()
        password = self.login_password_entry.get()

        if username == expected_username:
            self.show_balance_page(opening_balance)
        else:
            print("Login failed.")

    def show_balance_page(self, opening_balance):
        self.login_username_entry.delete(0, tk.END)
        self.login_password_entry.delete(0, tk.END)

        balance_root = tk.Tk()
        balance_root.title("Balance and Transactions")
        balance_root.configure(bg="#007BFF")

        self.balance_font_style = ("Helvetica", 18, "bold")

        self.balance_label = tk.Label(balance_root, text=f"Opening Balance: {opening_balance}", font=self.balance_font_style, bg="#007BFF")
        self.balance_label.pack()

        self.credit_label = tk.Label(balance_root, text="Credit:", font=self.label_font_style, bg="#007BFF")
        self.credit_label.pack()

        self.credit_entry = tk.Entry(balance_root, font=self.font_style)
        self.credit_entry.pack()

        self.credit_button = tk.Button(balance_root, text="Credit", font=self.button_font_style, command=self.credit)
        self.credit_button.pack()

        self.debit_label = tk.Label(balance_root, text="Debit:", font=self.label_font_style, bg="#007BFF")
        self.debit_label.pack()

        self.debit_entry = tk.Entry(balance_root, font=self.font_style)
        self.debit_entry.pack()

        self.debit_button = tk.Button(balance_root, text="Debit", font=self.button_font_style, command=self.debit)
        self.debit_button.pack()

        self.transactions_text = tk.Text(balance_root, font=self.font_style)
        self.transactions_text.pack()

        self.exit_button = tk.Button(balance_root, text="Exit", font=self.button_font_style, command=balance_root.destroy, bg="red", fg="white", width=20)
        self.exit_button.pack()

        balance_root.mainloop()

    def credit(self):
        credit_amount = float(self.credit_entry.get())
        current_balance = float(self.balance_label.cget("text").split(":")[1])
        new_balance = current_balance + credit_amount
        self.balance_label.config(text=f"Opening Balance: {new_balance}")
        transaction_info = f"Credit: {credit_amount}, Balance: {new_balance}\n"
        with open("transactions.txt", "a") as f:
            f.write(transaction_info)
        self.credit_entry.delete(0, tk.END)
        self.transactions_text.insert(tk.END, transaction_info)

    def debit(self):
        debit_amount = float(self.debit_entry.get())
        current_balance = float(self.balance_label.cget("text").split(":")[1])
        if debit_amount > current_balance:
            print("Debit amount exceeds balance.")
        else:
            new_balance = current_balance - debit_amount
            self.balance_label.config(text=f"Opening Balance: {new_balance}")
            transaction_info = f"Debit: {debit_amount}, Balance: {new_balance}\n"
            with open("transactions.txt", "a") as f:
                f.write(transaction_info)
            self.debit_entry.delete(0, tk.END)
            self.transactions_text.insert(tk.END, transaction_info)


if __name__ == "__main__":
    root = tk.Tk()
    app = BankApp(root)
    root.mainloop()