# ...existing code...
import customtkinter as ctk
from database import verify_credentials

def login_window(parent, db_conn, on_success=None, on_create_account=None):
    """
    parent: CTkFrame to attach the login UI.
    db_conn: sqlite3.Connection
    on_success: callback(user_dict)
    on_create_account: callback to show registration UI (optional)
    """
    frame = ctk.CTkFrame(parent, corner_radius=0, fg_color="transparent")
    frame.pack(fill="both", expand=True, padx=0, pady=0)

    # Center content
    center_frame = ctk.CTkFrame(frame, fg_color="transparent")
    center_frame.pack(fill="both", expand=True)

    content_frame = ctk.CTkFrame(center_frame, fg_color=("gray92", "#1f1f1f"), corner_radius=12)
    content_frame.pack(padx=40, pady=40, ipadx=32, ipady=32)

    ctk.CTkLabel(content_frame, text="Sign In", font=ctk.CTkFont(size=22, weight="bold")).pack(pady=(0, 24))

    username_var = ctk.StringVar()
    password_var = ctk.StringVar()

    username_entry = ctk.CTkEntry(content_frame, placeholder_text="Username", textvariable=username_var, width=320, height=40)
    username_entry.pack(pady=(0, 12))
    password_entry = ctk.CTkEntry(content_frame, placeholder_text="Password", show="*", textvariable=password_var, width=320, height=40)
    password_entry.pack(pady=(0, 12))

    status = ctk.CTkLabel(content_frame, text="", text_color="red", font=ctk.CTkFont(size=11))
    status.pack(pady=(0, 12))

    def handle_login():
        user = username_var.get().strip()
        pwd = password_var.get().strip()
        if not user or not pwd:
            status.configure(text="Enter username and password")
            return
        u = verify_credentials(db_conn, user, pwd)
        if u:
            status.configure(text="")
            if on_success:
                on_success(u)
        else:
            status.configure(text="Invalid credentials")

    btn_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
    btn_frame.pack(pady=(12, 0))

    ctk.CTkButton(btn_frame, text="Sign In", command=handle_login, width=310, height=40,
                 font=ctk.CTkFont(size=13, weight="bold"), corner_radius=8).pack(pady=(0, 12))

    def open_create():
        if on_create_account:
            on_create_account()

    ctk.CTkButton(btn_frame, text="Create an Account", command=open_create, width=310, height=40,
                 fg_color=("gray80", "#2a2a2a"), text_color=("black", "white"),
                 hover_color=("gray65", "#3a3a3a"), font=ctk.CTkFont(size=13),
                 corner_radius=8).pack()

    return frame
# ...existing code...