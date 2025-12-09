# ...existing code...
import customtkinter as ctk
from database import create_user

def register_window(parent, db_conn, on_registered=None):
    frame = ctk.CTkFrame(parent, corner_radius=0, fg_color="transparent")
    frame.pack(fill="both", expand=True, padx=0, pady=0)

    center_frame = ctk.CTkFrame(frame, fg_color="transparent")
    center_frame.pack(fill="both", expand=True)

    content_frame = ctk.CTkFrame(center_frame, fg_color=("gray92", "#1f1f1f"), corner_radius=12)
    content_frame.pack(padx=40, pady=40, ipadx=32, ipady=32)

    ctk.CTkLabel(content_frame, text="Create Account", font=ctk.CTkFont(size=22, weight="bold")).pack(pady=(0, 24))

    username_var = ctk.StringVar()
    password_var = ctk.StringVar()
    display_var = ctk.StringVar()

    # Display Name field
    ctk.CTkLabel(content_frame, text="Display Name:", 
                 font=ctk.CTkFont(size=12, weight="bold"),
                 text_color=("gray10", "#ffd700")).pack(anchor="w", pady=(16, 4))
    display_name_entry = ctk.CTkEntry(content_frame, placeholder_text="Enter your display name (e.g., Gym Rat)", textvariable=display_var, width=320, height=40)
    display_name_entry.pack(fill="x", pady=(0, 12))

    # Username field
    ctk.CTkLabel(content_frame, text="Username:", 
                 font=ctk.CTkFont(size=12, weight="bold"),
                 text_color=("gray10", "#ffd700")).pack(anchor="w", pady=(0, 4))
    username_entry = ctk.CTkEntry(content_frame, placeholder_text="Enter username", textvariable=username_var, width=320, height=40)
    username_entry.pack(fill="x", pady=(0, 12))
    
    ctk.CTkEntry(content_frame, placeholder_text="Password", show="*", textvariable=password_var, width=320, height=40).pack(pady=(0, 12))

    status = ctk.CTkLabel(content_frame, text="", text_color="red", font=ctk.CTkFont(size=11))
    status.pack(pady=(0, 12))

    def handle_register():
        u = username_var.get().strip()
        p = password_var.get().strip()
        d = display_var.get().strip() or None
        if not u or not p or not d:
            status.configure(text="Username, password, and display name required")
            return
        created = create_user(db_conn, u, p, d)
        if created:
            status.configure(text="")
            if on_registered:
                on_registered(created)
        else:
            status.configure(text="Username already taken")

    btn_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
    btn_frame.pack(pady=(12, 0))

    ctk.CTkButton(btn_frame, text="Create Account", command=handle_register, width=310, height=40,
                 font=ctk.CTkFont(size=13, weight="bold"), corner_radius=8).pack(pady=(0, 12))
    ctk.CTkButton(btn_frame, text="Back to Login", command=lambda: None, width=310, height=40,
                 fg_color=("gray80", "#2a2a2a"), text_color=("black", "white"),
                 hover_color=("gray65", "#3a3a3a"), font=ctk.CTkFont(size=13),
                 corner_radius=8).pack()

    return frame
# ...existing code...