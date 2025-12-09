# ...existing code...
import customtkinter as ctk

def create_sidebar(parent, on_nav=None, is_logged_in=False, current_page=None):
    frame = ctk.CTkFrame(parent, corner_radius=0, fg_color="transparent")
    frame.pack(fill="both", expand=True, padx=0, pady=0)

    def nav(k):
        if on_nav:
            on_nav(k)

    # Top section
    top_frame = ctk.CTkFrame(frame, fg_color="transparent")
    top_frame.pack(fill="x", padx=12, pady=(16, 12))

    ctk.CTkLabel(top_frame, text="WOUT", font=ctk.CTkFont(size=16, weight="bold")).pack()

    if is_logged_in:
        # Menu separator
        separator = ctk.CTkFrame(frame, height=1, fg_color=("gray80", "#333333"))
        separator.pack(fill="x", padx=8, pady=12)

        # Navigation buttons
        nav_frame = ctk.CTkFrame(frame, fg_color="transparent")
        nav_frame.pack(fill="x", padx=8, pady=(0, 8))

        # Home button
        home_btn = ctk.CTkButton(nav_frame, text="🏠 Home", command=lambda: nav("home"), 
                     fg_color=("#2563eb" if current_page == "home" else ("gray90", "#2a2a2a")), 
                     text_color=("white" if current_page == "home" else ("black", "white")),
                     hover_color=("gray75", "#3a3a3a") if current_page != "home" else ("#2563eb", "#1e40af"),
                     corner_radius=8, state=("disabled" if current_page == "home" else "normal"))
        home_btn.pack(fill="x", pady=4)

        # Routines button
        routines_btn = ctk.CTkButton(nav_frame, text="📋 Routines", command=lambda: nav("routines"),
                     fg_color=("#2563eb" if current_page == "routines" else ("gray90", "#2a2a2a")), 
                     text_color=("white" if current_page == "routines" else ("black", "white")),
                     hover_color=("gray75", "#3a3a3a") if current_page != "routines" else ("#2563eb", "#1e40af"),
                     corner_radius=8, state=("disabled" if current_page == "routines" else "normal"))
        routines_btn.pack(fill="x", pady=4)

        # Profile button
        profile_btn = ctk.CTkButton(nav_frame, text="👤 Profile", command=lambda: nav("profile"),
                     fg_color=("#2563eb" if current_page == "profile" else ("gray90", "#2a2a2a")), 
                     text_color=("white" if current_page == "profile" else ("black", "white")),
                     hover_color=("gray75", "#3a3a3a") if current_page != "profile" else ("#2563eb", "#1e40af"),
                     corner_radius=8, state=("disabled" if current_page == "profile" else "normal"))
        profile_btn.pack(fill="x", pady=4)

        # Spacer
        spacer = ctk.CTkFrame(frame, fg_color="transparent")
        spacer.pack(fill="both", expand=True)

        # Logout button at bottom
        logout_frame = ctk.CTkFrame(frame, fg_color="transparent")
        logout_frame.pack(fill="x", padx=8, pady=8)
        ctk.CTkButton(logout_frame, text="🚪 Logout", command=lambda: nav("logout"), 
                     fg_color="#ef4444", hover_color="#dc2626", corner_radius=8).pack(fill="x", pady=4)
    else:
        # Login message
        msg_frame = ctk.CTkFrame(frame, fg_color="transparent")
        msg_frame.pack(fill="both", expand=True, padx=12, pady=24)
        ctk.CTkLabel(msg_frame, text="Welcome to WOUT", font=ctk.CTkFont(size=13, weight="bold")).pack()
        ctk.CTkLabel(msg_frame, text="Sign in or create an account to continue.", wraplength=170, 
                    justify="center", text_color="gray").pack(pady=(8, 0))

    return frame
# ...existing code...