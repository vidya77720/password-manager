"""
Password Generator GUI Application
A simple, user-friendly graphical interface for password generation
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import logging
from password_generator import PasswordGenerator

# Setup GUI-specific logging
gui_logger = logging.getLogger(__name__)


class PasswordGeneratorGUI:
    """Graphical User Interface for Password Generator"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Password Generator")
        self.root.geometry("500x600")
        self.root.resizable(False, False)
        
        # Initialize password generator
        self.generator = PasswordGenerator()
        
        # Create GUI elements
        self.create_widgets()
        
        gui_logger.info("GUI Application started")
    
    def create_widgets(self):
        """Create all GUI widgets"""
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="Password Generator", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Password Length Section
        length_frame = ttk.LabelFrame(main_frame, text="Password Length", padding="10")
        length_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(length_frame, text="Length:").grid(row=0, column=0, sticky=tk.W)
        
        self.length_var = tk.IntVar(value=12)
        self.length_spinbox = ttk.Spinbox(length_frame, from_=4, to=50, 
                                         textvariable=self.length_var, width=10)
        self.length_spinbox.grid(row=0, column=1, sticky=tk.W, padx=5)
        
        # Character Options Section
        options_frame = ttk.LabelFrame(main_frame, text="Character Options", padding="10")
        options_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        self.uppercase_var = tk.BooleanVar(value=True)
        self.lowercase_var = tk.BooleanVar(value=True)
        self.digits_var = tk.BooleanVar(value=True)
        self.symbols_var = tk.BooleanVar(value=True)
        self.exclude_similar_var = tk.BooleanVar(value=False)
        
        ttk.Checkbutton(options_frame, text="Uppercase (A-Z)", 
                       variable=self.uppercase_var).grid(row=0, column=0, sticky=tk.W)
        ttk.Checkbutton(options_frame, text="Lowercase (a-z)", 
                       variable=self.lowercase_var).grid(row=1, column=0, sticky=tk.W)
        ttk.Checkbutton(options_frame, text="Digits (0-9)", 
                       variable=self.digits_var).grid(row=2, column=0, sticky=tk.W)
        ttk.Checkbutton(options_frame, text="Symbols (!@#$%)", 
                       variable=self.symbols_var).grid(row=3, column=0, sticky=tk.W)
        ttk.Checkbutton(options_frame, text="Exclude Similar (i, l, 1, L, o, 0, O)", 
                       variable=self.exclude_similar_var).grid(row=4, column=0, sticky=tk.W)
        
        # Generate Button
        self.generate_button = ttk.Button(main_frame, text="Generate Password", 
                                        command=self.generate_password)
        self.generate_button.grid(row=3, column=0, columnspan=2, pady=15, sticky=(tk.W, tk.E))
        
        # Result Section
        result_frame = ttk.LabelFrame(main_frame, text="Generated Password", padding="10")
        result_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        self.password_var = tk.StringVar(value="Click Generate to create password")
        self.password_entry = ttk.Entry(result_frame, textvariable=self.password_var, 
                                       font=("Courier", 12), width=40)
        self.password_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=5)
        
        # Copy Button
        self.copy_button = ttk.Button(result_frame, text="Copy to Clipboard", 
                                     command=self.copy_to_clipboard)
        self.copy_button.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)
        
        # Strength Indicator
        self.strength_var = tk.StringVar(value="Strength: Not generated")
        self.strength_label = ttk.Label(result_frame, textvariable=self.strength_var, 
                                       font=("Arial", 10))
        self.strength_label.grid(row=2, column=0, sticky=tk.W, pady=5)
        
        # History Section
        history_frame = ttk.LabelFrame(main_frame, text="Recent Passwords", padding="10")
        history_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        self.history_text = scrolledtext.ScrolledText(history_frame, height=6, width=50, 
                                                     font=("Courier", 9))
        self.history_text.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # History Buttons
        history_button_frame = ttk.Frame(history_frame)
        history_button_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Button(history_button_frame, text="Refresh History", 
                  command=self.refresh_history).grid(row=0, column=0, padx=2)
        ttk.Button(history_button_frame, text="Clear History", 
                  command=self.clear_history).grid(row=0, column=1, padx=2)
        
        # Configure grid weights
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Load initial history
        self.refresh_history()
    
    def generate_password(self):
        """Generate password based on user preferences"""
        try:
            length = self.length_var.get()
            use_uppercase = self.uppercase_var.get()
            use_lowercase = self.lowercase_var.get()
            use_digits = self.digits_var.get()
            use_symbols = self.symbols_var.get()
            exclude_similar = self.exclude_similar_var.get()
            
            # Validate at least one character type is selected
            if not any([use_uppercase, use_lowercase, use_digits, use_symbols]):
                messagebox.showerror("Error", "Please select at least one character type")
                return
            
            # Generate password
            password = self.generator.generate(
                length=length,
                use_uppercase=use_uppercase,
                use_lowercase=use_lowercase,
                use_digits=use_digits,
                use_symbols=use_symbols,
                exclude_similar=exclude_similar
            )
            
            # Update display
            self.password_var.set(password)
            
            # Check and display strength
            strength_result = self.generator.check_strength(password)
            self.strength_var.set(f"Strength: {strength_result['strength']} "
                                f"({strength_result['score']}/{strength_result['max_score']})")
            
            # Color code strength
            if strength_result['strength'] == "Strong":
                self.strength_label.config(foreground="green")
            elif strength_result['strength'] == "Medium":
                self.strength_label.config(foreground="orange")
            else:
                self.strength_label.config(foreground="red")
            
            # Refresh history
            self.refresh_history()
            
            gui_logger.info(f"Password generated via GUI: length={length}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate password: {str(e)}")
            gui_logger.error(f"GUI password generation failed: {e}")
    
    def copy_to_clipboard(self):
        """Copy generated password to clipboard"""
        password = self.password_var.get()
        if password and password != "Click Generate to create password":
            self.root.clipboard_clear()
            self.root.clipboard_append(password)
            messagebox.showinfo("Success", "Password copied to clipboard!")
            gui_logger.info("Password copied to clipboard via GUI")
        else:
            messagebox.showwarning("Warning", "No password to copy")
    
    def refresh_history(self):
        """Refresh the history display"""
        self.history_text.delete(1.0, tk.END)
        
        recent_passwords = self.generator.get_recent_passwords(count=5)
        if recent_passwords:
            for i, pwd in enumerate(recent_passwords, 1):
                self.history_text.insert(tk.END, f"{i}. {pwd}\n")
        else:
            self.history_text.insert(tk.END, "No recent passwords")
        
        gui_logger.info("History refreshed in GUI")
    
    def clear_history(self):
        """Clear password history"""
        if messagebox.askyesno("Confirm", "Are you sure you want to clear all password history?"):
            self.generator.clear_history()
            self.refresh_history()
            messagebox.showinfo("Success", "Password history cleared!")
            gui_logger.info("History cleared via GUI")


def main():
    """Main function to run the GUI application"""
    root = tk.Tk()
    app = PasswordGeneratorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
