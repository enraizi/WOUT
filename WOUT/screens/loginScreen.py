import customtkinter as ctk

def login_window(parent, db, on_success=None, on_create_account=None):
    """
    parent: CTkFrame to attach the login UI.
    db_conn: sqlite3.Connection
    on_success: callback(user_dict)
    on_create_account: callback to show registration UI (optional)
    """
    for w in parent.winfo_children():
        w.destroy()
    
    frame = ctk.CTkFrame(parent, fg_color="transparent")
    frame.pack(fill="both", expand=True, padx=40, pady=40)
    
    # Center container
    center_frame = ctk.CTkFrame(frame, fg_color="transparent")
    center_frame.pack(expand=True, fill="both", padx=200)
    
    # Logo/Title
    ctk.CTkLabel(center_frame, text="💪", 
                 font=ctk.CTkFont(size=64, weight="bold")).pack(pady=(0, 20))
    
    ctk.CTkLabel(center_frame, text="WOUT", 
                 font=ctk.CTkFont(size=36, weight="bold"),
                 text_color=("gray10", "#ffffff")).pack(pady=(0, 8))
    
    ctk.CTkLabel(center_frame, text="Workout Tracker", 
                 font=ctk.CTkFont(size=14),
                 text_color=("gray60", "#a0a0a0")).pack(pady=(0, 40))
    
    # Form
    form = ctk.CTkFrame(center_frame, fg_color="transparent")
    form.pack(fill="x")
    
    ctk.CTkLabel(form, text="Username", 
                 font=ctk.CTkFont(size=12, weight="bold"),
                 text_color=("gray20", "#e0e0e0")).pack(anchor="w", pady=(0, 8), padx=4)
    
    username_entry = ctk.CTkEntry(form, placeholder_text="Enter username",
                                  height=44, border_width=1,
                                  border_color=("gray80", "#333333"),
                                  fg_color=("gray95", "#1a1f26"))
    username_entry.pack(fill="x", pady=(0, 16))
    
    ctk.CTkLabel(form, text="Password", 
                 font=ctk.CTkFont(size=12, weight="bold"),
                 text_color=("gray20", "#e0e0e0")).pack(anchor="w", pady=(0, 8), padx=4)
    
    password_entry = ctk.CTkEntry(form, placeholder_text="Enter password", show="*",
                                  height=44, border_width=1,
                                  border_color=("gray80", "#333333"),
                                  fg_color=("gray95", "#1a1f26"))
    password_entry.pack(fill="x", pady=(0, 24))
    
    error_label = ctk.CTkLabel(form, text="", 
                              font=ctk.CTkFont(size=10),
                              text_color=("#dc2626", "#ff6b6b"))
    error_label.pack(pady=(0, 12), padx=4)
    
    def login():
        username = username_entry.get().strip()
        password = password_entry.get()
        
        if not username or not password:
            error_label.configure(text="Please fill in all fields")
            return
        
        try:
            cursor = db.cursor()
            
            cursor.execute("""
                SELECT id, username, password, display_name, created_at 
                FROM users 
                WHERE LOWER(username) = LOWER(?)
            """, (username,))
            
            user_row = cursor.fetchone()
            
            if user_row:
                stored_id, stored_username, stored_password, stored_display_name, stored_created_at = user_row
                
                if stored_password == password:
                    user = {
                        'id': stored_id,
                        'username': stored_username,
                        'password': stored_password,
                        'display_name': stored_display_name,
                        'created_at': stored_created_at if stored_created_at else "N/A"
                    }
                    if on_success:
                        on_success(user)
                else:
                    error_label.configure(text="Invalid username or password")
            else:
                error_label.configure(text="Invalid username or password")
                
        except Exception as e:
            print(f"Login error: {e}")
            import traceback
            traceback.print_exc()
            error_label.configure(text=f"Login failed: {str(e)}")
    
    # Buttons
    login_btn = ctk.CTkButton(form, text="Sign In", command=login,
                             height=48, font=ctk.CTkFont(size=12, weight="bold"),
                             fg_color=("#2563eb", "#2563eb"),
                             hover_color=("#1d4ed8", "#1d4ed8"),
                             corner_radius=8)
    login_btn.pack(fill="x", pady=(16, 12))
    
    # Sign up prompt with clickable text
    signup_section = ctk.CTkFrame(form, fg_color="transparent")
    signup_section.pack(fill="x", pady=(0, 0))
    
    def go_to_signup():
        if on_create_account:
            on_create_account()
    
    ctk.CTkLabel(signup_section, text="Don't have an account? ", 
                 font=ctk.CTkFont(size=11),
                 text_color=("gray60", "#a0a0a0")).pack(side="left")
    
    signup_link = ctk.CTkLabel(signup_section, text="Sign up first",
                              font=ctk.CTkFont(size=11, weight="bold"),
                              text_color=("#2563eb", "#2563eb"),
                              cursor="hand2")
    signup_link.pack(side="left")
    
    # Bind click event to label
    signup_link.bind("<Button-1>", lambda e: go_to_signup())