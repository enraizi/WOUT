import customtkinter as ctk

def register_window(parent, db, on_registered=None, on_back_to_login=None):
    for w in parent.winfo_children():
        w.destroy()
    
    frame = ctk.CTkFrame(parent, fg_color="transparent")
    frame.pack(fill="both", expand=True, padx=40, pady=40)
    
    center_frame = ctk.CTkFrame(frame, fg_color="transparent")
    center_frame.pack(expand=True, fill="both", padx=200)
    
    # Header
    ctk.CTkLabel(center_frame, text="Create Account", 
                 font=ctk.CTkFont(size=28, weight="bold"),
                 text_color=("gray10", "#ffffff")).pack(pady=(0, 8))
    
    ctk.CTkLabel(center_frame, text="Join WOUT today", 
                 font=ctk.CTkFont(size=12),
                 text_color=("gray60", "#a0a0a0")).pack(pady=(0, 32))
    
    # Form
    form = ctk.CTkFrame(center_frame, fg_color="transparent")
    form.pack(fill="x")
    
    # Display Name
    ctk.CTkLabel(form, text="Display Name", 
                 font=ctk.CTkFont(size=11, weight="bold"),
                 text_color=("gray20", "#e0e0e0")).pack(anchor="w", pady=(0, 8), padx=4)
    
    display_name_entry = ctk.CTkEntry(form, placeholder_text="Your display name",
                                     height=44, border_width=1,
                                     border_color=("gray80", "#333333"),
                                     fg_color=("gray95", "#1a1f26"))
    display_name_entry.pack(fill="x", pady=(0, 16))
    
    # Username
    ctk.CTkLabel(form, text="Username", 
                 font=ctk.CTkFont(size=11, weight="bold"),
                 text_color=("gray20", "#e0e0e0")).pack(anchor="w", pady=(0, 8), padx=4)
    
    username_entry = ctk.CTkEntry(form, placeholder_text="Choose a username",
                                 height=44, border_width=1,
                                 border_color=("gray80", "#333333"),
                                 fg_color=("gray95", "#1a1f26"))
    username_entry.pack(fill="x", pady=(0, 16))
    
    # Password
    ctk.CTkLabel(form, text="Password", 
                 font=ctk.CTkFont(size=11, weight="bold"),
                 text_color=("gray20", "#e0e0e0")).pack(anchor="w", pady=(0, 8), padx=4)
    
    password_entry = ctk.CTkEntry(form, placeholder_text="Enter password", show="*",
                                 height=44, border_width=1,
                                 border_color=("gray80", "#333333"),
                                 fg_color=("gray95", "#1a1f26"))
    password_entry.pack(fill="x", pady=(0, 16))
    
    # Confirm Password
    ctk.CTkLabel(form, text="Confirm Password", 
                 font=ctk.CTkFont(size=11, weight="bold"),
                 text_color=("gray20", "#e0e0e0")).pack(anchor="w", pady=(0, 8), padx=4)
    
    confirm_pwd_entry = ctk.CTkEntry(form, placeholder_text="Confirm password", show="*",
                                    height=44, border_width=1,
                                    border_color=("gray80", "#333333"),
                                    fg_color=("gray95", "#1a1f26"))
    confirm_pwd_entry.pack(fill="x", pady=(0, 24))
    
    error_label = ctk.CTkLabel(form, text="", 
                              font=ctk.CTkFont(size=10),
                              text_color=("#dc2626", "#ff6b6b"))
    error_label.pack(pady=(0, 16), padx=4)
    
    def register():
        username = username_entry.get().strip()
        password = password_entry.get()
        confirm_password = confirm_pwd_entry.get()
        display_name = display_name_entry.get().strip()
        
        if not username or not password or not display_name:
            error_label.configure(text="All fields are required")
            return
        
        if password != confirm_password:
            error_label.configure(text="Passwords don't match")
            return
        
        try:
            from datetime import datetime
            
            cursor = db.cursor()
            cursor.execute("SELECT id FROM users WHERE LOWER(username) = LOWER(?)", (username,))
            
            if cursor.fetchone():
                error_label.configure(text="Username already exists")
                return
            
            current_date = datetime.now().strftime("%Y-%m-%d")
            
            cursor.execute(
                "INSERT INTO users (username, password, display_name, created_at) VALUES (?, ?, ?, ?)",
                (username, password, display_name, current_date)
            )
            db.commit()
            
            user = {
                'id': cursor.lastrowid,
                'username': username,
                'password': password,
                'display_name': display_name,
                'created_at': current_date
            }
            
            if on_registered:
                on_registered(user)
        except Exception as e:
            error_label.configure(text=f"Registration failed: {str(e)}")
    
    # Buttons
    button_frame = ctk.CTkFrame(form, fg_color="transparent")
    button_frame.pack(fill="x")
    
    register_btn = ctk.CTkButton(button_frame, text="Create Account", command=register,
                                height=48, font=ctk.CTkFont(size=12, weight="bold"),
                                fg_color=("#2563eb", "#2563eb"),
                                hover_color=("#1d4ed8", "#1d4ed8"),
                                corner_radius=8)
    register_btn.pack(fill="x", pady=(0, 12))
    
    back_btn = ctk.CTkButton(button_frame, text="Back to Sign In", 
                            command=on_back_to_login,
                            height=44, font=ctk.CTkFont(size=12),
                            fg_color=("gray90", "#2a2f36"),
                            text_color=("gray20", "#e0e0e0"),
                            hover_color=("gray80", "#333333"),
                            corner_radius=8)
    back_btn.pack(fill="x")