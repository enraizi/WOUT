# ...existing code...
import os
import customtkinter as ctk
from PIL import Image

from database import connect_db
from screens import loginScreen, homeScreen, regScreen, sidebar, routinesScreen, profileScreen

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class App:
    def __init__(self):
        self.base_dir = os.path.dirname(__file__)
        db_path = os.path.join(self.base_dir, "wout.db")
        self.db = connect_db(db_path)
        self.current_user = None
        self.current_page = None

        self.root = ctk.CTk()
        self.root.title("WOUT - Workout Optimization and Unified Tracking")
        self.root.geometry("1200x700")
        self.root.minsize(1000, 600)
        self.root.bind("<Configure>", self._on_window_resize)

        self._setup_layout()
        self._load_branding()
        self.show_login()
        self._center_window()
        self.root.mainloop()

    def _setup_layout(self):
        self.container = ctk.CTkFrame(self.root, corner_radius=0, fg_color=("white", "#0a0e27"))
        self.container.pack(fill="both", expand=True, padx=0, pady=0)

        # sidebar column - darker premium look
        self.side_frame = ctk.CTkFrame(self.container, width=200, corner_radius=0, 
                                       fg_color=("gray96", "#0d1b2a"))
        self.side_frame.pack_propagate(False)
        self.side_frame.pack(side="left", fill="y", padx=0, pady=0)

        # main content
        self.main_frame = ctk.CTkFrame(self.container, corner_radius=0, fg_color=("white", "#0a0e27"))
        self.main_frame.pack(side="left", fill="both", expand=True, padx=0, pady=0)

        # right branding - premium gradient design
        self.brand_frame = ctk.CTkFrame(self.container, width=280, corner_radius=0,
                                        fg_color=("gray93", "#0d1b2a"))
        self.brand_frame.pack_propagate(False)
        self.brand_frame.pack(side="right", fill="y", padx=0, pady=0)

        try:
            self.sb = sidebar.create_sidebar(self.side_frame, on_nav=self._on_nav, is_logged_in=False, current_page=self.current_page)
        except Exception as e:
            print(f"Sidebar error: {e}")

    def _load_branding(self):
        """Load and display branding with premium design"""
        for widget in self.brand_frame.winfo_children():
            widget.destroy()

        # Top section with premium gradient
        top_section = ctk.CTkFrame(self.brand_frame, fg_color=("gray88", "#1a2940"), corner_radius=0)
        top_section.pack(fill="x", padx=0, pady=0)

        # Logo container
        logo_container = ctk.CTkFrame(top_section, fg_color="transparent")
        logo_container.pack(fill="both", expand=True, padx=20, pady=24)

        img_path = os.path.join(self.base_dir, "assets", "logo.png")
        try:
            image = Image.open(img_path).convert("RGBA")
            image = image.resize((100, 100), Image.LANCZOS)
            ctk_image = ctk.CTkImage(light_image=image, dark_image=image, size=(100, 100))
            logo = ctk.CTkLabel(logo_container, image=ctk_image, text="")
            logo.image = ctk_image
            logo.pack()
        except Exception as e:
            print(f"Logo load error: {e}")
            ctk.CTkLabel(logo_container, text="💪",
                         font=ctk.CTkFont(size=48, weight="bold"),
                         text_color=("white", "white")).pack()
        
        # Brand name with premium styling
        ctk.CTkLabel(top_section, text="WOUT", 
                     font=ctk.CTkFont(size=32, weight="bold"),
                     text_color=("white", "#ffd700")).pack(pady=(8, 2))
        
        ctk.CTkLabel(top_section, text="Elite Fitness Tracker", 
                     font=ctk.CTkFont(size=10, weight="bold"),
                     text_color=("gray60", "#90caf9")).pack(pady=(0, 24))

        # Premium separator
        separator = ctk.CTkFrame(top_section, height=3, fg_color=("gray70", "#ffd700"))
        separator.pack(fill="x", padx=20, pady=(0, 0))

        # Bottom section - Features (scrollable)
        self.bottom_section = ctk.CTkScrollableFrame(self.brand_frame, fg_color="transparent", corner_radius=0)
        self.bottom_section.pack(fill="both", expand=True, padx=0, pady=0)

        # Features container
        self.features_frame = ctk.CTkFrame(self.bottom_section, fg_color="transparent")
        self.features_frame.pack(fill="x", padx=12, pady=20)

        # Premium feature items
        features = [
            ("⚡", "Lightning Fast", "Start workouts instantly"),
            ("📊", "Deep Analytics", "Track every detail"),
            ("🎯", "AI Plans", "Smart routines"),
            ("🔥", "Motivation", "Stay consistent"),
        ]

        self.feature_items = []
        for emoji, title, desc in features:
            feature_item = ctk.CTkFrame(self.features_frame, fg_color=("gray82", "#1a2940"), 
                                       corner_radius=10)
            feature_item.pack(fill="x", pady=8)

            feature_border = ctk.CTkFrame(feature_item, fg_color=("gray70", "#ffd700"), 
                                         corner_radius=10)
            feature_border.pack(fill="x", expand=True, padx=2, pady=2)

            feature_inner = ctk.CTkFrame(feature_border, fg_color=("gray82", "#1a2940"), 
                                        corner_radius=8)
            feature_inner.pack(fill="x", expand=True, padx=0, pady=0, ipadx=12, ipady=10)

            # Feature header
            header_frame = ctk.CTkFrame(feature_inner, fg_color="transparent")
            header_frame.pack(fill="x")

            ctk.CTkLabel(header_frame, text=emoji, 
                        font=ctk.CTkFont(size=16, weight="bold")).pack(side="left", padx=(0, 8))
            
            title_label = ctk.CTkLabel(header_frame, text=title, 
                        font=ctk.CTkFont(size=10, weight="bold"),
                        text_color=("gray15", "#ffd700"))
            title_label.pack(side="left", fill="x", expand=True)

            # Feature description
            desc_label = ctk.CTkLabel(feature_inner, text=desc, 
                        font=ctk.CTkFont(size=8),
                        text_color=("gray50", "#90caf9"),
                        wraplength=240, justify="left")
            desc_label.pack(anchor="w", padx=28, pady=(4, 0))

            self.feature_items.append({
                "container": feature_item,
                "desc": desc_label,
                "title": title_label,
                "border": feature_border,
                "inner": feature_inner
            })

        # Bottom spacer
        self.spacer = ctk.CTkFrame(self.bottom_section, fg_color="transparent", height=20)
        self.spacer.pack(fill="both", expand=True)

        # Premium footer info
        footer_frame = ctk.CTkFrame(self.bottom_section, fg_color=("gray78", "#1a2940"), 
                                   corner_radius=10)
        footer_frame.pack(fill="x", pady=16, padx=12)

        footer_border = ctk.CTkFrame(footer_frame, fg_color=("gray65", "#ffd700"), 
                                    corner_radius=10)
        footer_border.pack(fill="x", expand=True, padx=2, pady=2)

        footer_inner = ctk.CTkFrame(footer_border, fg_color=("gray78", "#1a2940"), 
                                   corner_radius=8)
        footer_inner.pack(fill="x", expand=True, padx=0, pady=0, ipadx=12, ipady=12)

        ctk.CTkLabel(footer_inner, text="🏆 Version 1.0", 
                     font=ctk.CTkFont(size=9, weight="bold"),
                     text_color=("gray20", "#ffd700")).pack()
        ctk.CTkLabel(footer_inner, text="Your Personal Fitness Champion", 
                     font=ctk.CTkFont(size=8),
                     text_color=("gray50", "#90caf9")).pack(pady=(3, 0))

    def _update_brand_responsiveness(self):
        """Update brand sidebar based on current page"""
        if not hasattr(self, 'feature_items') or not self.feature_items:
            return
            
        if self.current_page in ["routines", "profile"]:
            for item in self.feature_items:
                item["desc"].pack_forget()
        else:
            for item in self.feature_items:
                item["desc"].pack(anchor="w", padx=28, pady=(4, 0))

    def _on_window_resize(self, event=None):
        """Handle window resize for responsive design"""
        pass

    def _clear_main(self):
        for w in self.main_frame.winfo_children():
            w.destroy()

    def _refresh_sidebar(self):
        """Refresh sidebar based on login status"""
        for w in self.side_frame.winfo_children():
            w.destroy()
        try:
            is_logged = self.current_user is not None
            self.sb = sidebar.create_sidebar(self.side_frame, on_nav=self._on_nav, is_logged_in=is_logged, current_page=self.current_page)
        except Exception as e:
            print(f"Sidebar refresh error: {e}")

    def _on_nav(self, key):
        try:
            # Prevent navigation to the same page
            if key == self.current_page:
                return
            
            if key == "home":
                self.show_home()
            elif key == "routines":
                self.show_routines()
            elif key == "profile":
                self.show_profile()
            elif key == "logout":
                self.current_user = None
                self.current_page = None
                self._refresh_sidebar()
                self.show_login()
        except Exception as e:
            print(f"Navigation error: {e}")

    def show_login(self):
        try:
            self.current_page = "login"
            self._clear_main()
            self._update_brand_responsiveness()
            loginScreen.login_window(self.main_frame, self.db, on_success=self._on_login_success, on_create_account=self.show_register)
        except Exception as e:
            print(f"Login screen error: {e}")

    def _on_login_success(self, user):
        self.current_user = user
        self._refresh_sidebar()
        self.show_home()

    def show_register(self):
        try:
            self.current_page = "register"
            self._clear_main()
            self._update_brand_responsiveness()
            regScreen.register_window(self.main_frame, self.db, on_registered=self._on_registered)
        except Exception as e:
            print(f"Register screen error: {e}")

    def _on_registered(self, user):
        self.current_user = user
        self._refresh_sidebar()
        self.show_home()

    def show_home(self):
        try:
            if not self.current_user:
                self.show_login()
                return
            self.current_page = "home"
            self._refresh_sidebar()
            self._clear_main()
            self._update_brand_responsiveness()
            homeScreen.create_home(self.main_frame, self.db, user=self.current_user)
        except Exception as e:
            print(f"Home screen error: {e}")

    def show_routines(self):
        try:
            if not self.current_user:
                self.show_login()
                return
            self.current_page = "routines"
            self._refresh_sidebar()
            self._clear_main()
            self._update_brand_responsiveness()
            routinesScreen.create_routines(self.main_frame, self.db, user=self.current_user)
        except Exception as e:
            print(f"Routines screen error: {e}")

    def show_profile(self):
        try:
            if not self.current_user:
                self.show_login()
                return
            self.current_page = "profile"
            self._refresh_sidebar()
            self._clear_main()
            self._update_brand_responsiveness()
            profileScreen.create_profile(self.main_frame, self.db, user=self.current_user)
        except Exception as e:
            print(f"Profile screen error: {e}")

    def _center_window(self):
        self.root.update_idletasks()
        w = self.root.winfo_width()
        h = self.root.winfo_height()
        ws = self.root.winfo_screenwidth()
        hs = self.root.winfo_screenheight()
        x = (ws // 2) - (w // 2)
        y = (hs // 2) - (h // 2)
        self.root.geometry(f'{w}x{h}+{x}+{y}')


if __name__ == "__main__":
    try:
        App()
    except Exception as e:
        print(f"App initialization error: {e}")
        import traceback
        traceback.print_exc()
# ...existing code...