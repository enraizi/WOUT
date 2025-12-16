import os
import customtkinter as ctk
from PIL import Image

from screens import home_screen, login_screen, profile_screen, reg_screen, routines_screen
from database import connect_db
from screens import sidebar

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
        
        # Store app instance reference in root for sidebar refresh
        self.root.app_instance = self
        
        # Fixed window size - permanent resolution
        WINDOW_WIDTH = 1400
        WINDOW_HEIGHT = 800
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.resizable(False, False)
        
        # Center window on screen
        self.root.update_idletasks()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (WINDOW_WIDTH // 2)
        y = (screen_height // 2) - (WINDOW_HEIGHT // 2)
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x}+{y}")

        self._setup_layout()
        self._load_branding()
        self.show_login()
        self.root.mainloop()

    def _setup_layout(self):
        self.container = ctk.CTkFrame(self.root, corner_radius=0, fg_color=("white", "#0a0e27"))
        self.container.pack(fill="both", expand=True, padx=0, pady=0)

        # sidebar column
        self.side_frame = ctk.CTkFrame(self.container, width=200, corner_radius=0, 
                                       fg_color=("gray96", "#0d1b2a"))
        self.side_frame.pack_propagate(False)
        self.side_frame.pack(side="left", fill="y", padx=0, pady=0)

        # main content
        self.main_frame = ctk.CTkFrame(self.container, corner_radius=0, fg_color=("white", "#0a0e27"))
        self.main_frame.pack(side="left", fill="both", expand=True, padx=0, pady=0)

        # right branding
        self.brand_frame = ctk.CTkFrame(self.container, width=300, corner_radius=0,
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

        # Top section - Premium header
        top_section = ctk.CTkFrame(self.brand_frame, fg_color=("gray88", "#1a2940"), corner_radius=0)
        top_section.pack(fill="x", padx=0, pady=0)

        # Logo container - larger with glow effect
        logo_container = ctk.CTkFrame(top_section, fg_color="transparent")
        logo_container.pack(fill="x", padx=20, pady=4)

        img_path = os.path.join(self.base_dir, "assets", "logo.png")
        try:
            image = Image.open(img_path).convert("RGBA")
            image = image.resize((220, 220), Image.LANCZOS)
            ctk_image = ctk.CTkImage(light_image=image, dark_image=image, size=(220, 220))
            logo = ctk.CTkLabel(logo_container, image=ctk_image, text="")
            logo.image = ctk_image
            logo.pack()
        except Exception as e:
            print(f"Logo load error: {e}")
            ctk.CTkLabel(logo_container, text="💪",
                         font=ctk.CTkFont(size=64, weight="bold"),
                         text_color=("white", "white")).pack()
        
        ctk.CTkLabel(top_section, text="WOUT", 
                     font=ctk.CTkFont(size=48, weight="bold"),
                     text_color=("white", "#ffd700")).pack(pady=(12, 2))
        
        ctk.CTkLabel(top_section, text="Elite Fitness Tracker", 
                     font=ctk.CTkFont(size=14, weight="bold"),
                     text_color=("gray60", "#90caf9")).pack(pady=(0, 24))

        # Separator with gradient effect
        separator = ctk.CTkFrame(top_section, height=3, fg_color=("gray70", "#ffd700"))
        separator.pack(fill="x", padx=20, pady=(0, 0))

        # Bottom section - Features showcase
        self.bottom_section = ctk.CTkFrame(self.brand_frame, fg_color="transparent", corner_radius=0)
        self.bottom_section.pack(fill="both", expand=True, padx=0, pady=0)

        # Features container with title
        features_title = ctk.CTkFrame(self.bottom_section, fg_color="transparent")
        features_title.pack(fill="x", padx=12, pady=(16, 12))
        
        ctk.CTkLabel(features_title, text="Why WOUT?", 
                     font=ctk.CTkFont(size=16, weight="bold"),
                     text_color=("gray20", "#ffd700")).pack(anchor="w", padx=4)

        self.features_frame = ctk.CTkFrame(self.bottom_section, fg_color="transparent")
        self.features_frame.pack(fill="x", padx=12, pady=(0, 12))

        # Feature items - improved design
        features = [
            (" ⚡", "Lightning Fast", "Start workouts instantly"),
            (" 📊", "Deep Analytics", "Track every detail"),
            (" 🔥", "Motivation", "Stay consistent"),
            (" 🎯", "Smart Goals", "Achieve your targets"),
        ]

        self.feature_items = []
        for emoji, title, desc in features:
            feature_item = ctk.CTkFrame(self.features_frame, fg_color=("gray82", "#1a2940"), 
                                       corner_radius=10)
            feature_item.pack(fill="x", pady=6)

            feature_border = ctk.CTkFrame(feature_item, fg_color=("gray70", "#ffd700"), 
                                         corner_radius=10)
            feature_border.pack(fill="x", expand=True, padx=2, pady=2)

            feature_inner = ctk.CTkFrame(feature_border, fg_color=("gray82", "#1a2940"), 
                                        corner_radius=8)
            feature_inner.pack(fill="x", expand=True, padx=0, pady=0, ipadx=12, ipady=8)

            header_frame = ctk.CTkFrame(feature_inner, fg_color="transparent")
            header_frame.pack(fill="x")

            ctk.CTkLabel(header_frame, text=emoji, 
                        font=ctk.CTkFont(size=24, weight="bold")).pack(side="left", padx=(0.5, 1))
            
            title_label = ctk.CTkLabel(header_frame, text=title, 
                        font=ctk.CTkFont(size=14, weight="bold"),
                        text_color=("gray15", "#ffd700"))
            title_label.pack(side="left", fill="x", expand=True)

            desc_label = ctk.CTkLabel(feature_inner, text=desc, 
                        font=ctk.CTkFont(size=11),
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

        # Stats section - occupies dead space
        stats_section = ctk.CTkFrame(self.bottom_section, fg_color="transparent")
        stats_section.pack(fill="x", padx=12, pady=12)
        
        ctk.CTkFrame(stats_section, height=2, fg_color=("gray70", "#ffd700")).pack(fill="x", pady=(0, 12))
        
        # Three stat boxes
        stats_box = ctk.CTkFrame(stats_section, fg_color="transparent")
        stats_box.pack(fill="x")
        
        stats_data = [
            ("💪", "Workouts"),
            ("🔥", "Streak"),
            ("⏱️", "Time"),
        ]
        
        for emoji, label in stats_data:
            stat_card = ctk.CTkFrame(stats_box, fg_color=("gray80", "#1a2940"), corner_radius=8)
            stat_card.pack(side="left", fill="both", expand=True, padx=2)
            
            stat_border = ctk.CTkFrame(stat_card, fg_color=("gray65", "#ffd700"), corner_radius=8)
            stat_border.pack(fill="both", expand=True, padx=1, pady=1)
            
            stat_inner = ctk.CTkFrame(stat_border, fg_color=("gray80", "#1a2940"), corner_radius=7)
            stat_inner.pack(fill="both", expand=True, padx=0, pady=0, ipadx=8, ipady=8)
            
            ctk.CTkLabel(stat_inner, text=emoji, 
                        font=ctk.CTkFont(size=28, weight="bold")).pack(pady=(4, 2))
            ctk.CTkLabel(stat_inner, text=label, 
                        font=ctk.CTkFont(size=13),
                        text_color=("gray40", "#90caf9")).pack()

        # Bottom spacer - minimal
        self.spacer = ctk.CTkFrame(self.bottom_section, fg_color="transparent", height=1)
        self.spacer.pack(fill="both", expand=True)

        # Version footer (separated) - at bottom of brand_frame
        version_frame = ctk.CTkFrame(self.brand_frame, fg_color=("gray78", "#1a2940"), 
                                   corner_radius=10, height=35)
        version_frame.pack_propagate(False)
        version_frame.pack(fill="x", pady=8, padx=16, side="bottom")

        version_border = ctk.CTkFrame(version_frame, fg_color=("gray65", "#ffd700"), 
                                    corner_radius=10)
        version_border.pack(fill="both", expand=True, padx=2, pady=2)

        version_inner = ctk.CTkFrame(version_border, fg_color=("gray78", "#1a2940"), 
                                   corner_radius=8)
        version_inner.pack(fill="both", expand=True, padx=0, pady=0, ipadx=6, ipady=2)

        ctk.CTkLabel(version_inner, text="v1.0", 
                     font=ctk.CTkFont(size=14, weight="bold"),
                     text_color=("gray20", "#ffd700")).pack(expand=True)

    def _update_brand_responsiveness(self):
        """Update brand sidebar based on current page"""
        if not hasattr(self, 'feature_items') or not self.feature_items:
            return
        
        # Always show descriptions on all screens
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
            user_id = self.current_user.get('id') if self.current_user else None
            self.sb = sidebar.create_sidebar(self.side_frame, on_nav=self._on_nav, is_logged_in=is_logged, 
                                           current_page=self.current_page, db=self.db, user_id=user_id)
        except Exception as e:
            print(f"Sidebar refresh error: {e}")

    def _refresh_current_user(self):
        """Refresh current user data from database"""
        if self.current_user and isinstance(self.current_user, dict):
            try:
                cursor = self.db.cursor()
                cursor.execute("SELECT id, username, password, display_name, created_at, weight, weight_unit, birthdate FROM users WHERE id = ?", (self.current_user.get('id'),))
                user_row = cursor.fetchone()
                
                if user_row:
                    self.current_user = {
                        'id': user_row[0],
                        'username': user_row[1],
                        'password': user_row[2],
                        'display_name': user_row[3],
                        'created_at': user_row[4] if user_row[4] else "N/A",
                        'weight': user_row[5],
                        'weight_unit': user_row[6],
                        'birthdate': user_row[7]
                    }
            except Exception as e:
                print(f"Error refreshing user: {e}")

    def _on_nav(self, key):
        try:
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
            login_screen.login_window(self.main_frame, self.db, on_success=self._on_login_success, on_create_account=self.show_register)
        except Exception as e:
            print(f"Login screen error: {e}")

    def _on_login_success(self, user):
        self.current_user = user
        self._update_streak_on_login()
        self._refresh_current_user()
        self._refresh_sidebar()
        self.show_home()

    def _update_streak_on_login(self):
        """Update streak when user logs in"""
        if not self.current_user:
            return
        
        try:
            from datetime import datetime, timedelta
            
            user_id = self.current_user.get('id')
            cursor = self.db.cursor()
            
            # Get current streak and last login
            cursor.execute("SELECT streak, last_login FROM users WHERE id = ?", (user_id,))
            row = cursor.fetchone()
            
            today = datetime.now().date()
            current_streak = row[0] if row and row[0] else 0
            last_login = row[1] if row else None
            
            if last_login:
                try:
                    last_login_date = datetime.strptime(last_login, "%Y-%m-%d").date()
                    yesterday = today - timedelta(days=1)
                    
                    # If logged in yesterday, increment streak
                    if last_login_date == yesterday:
                        current_streak += 1
                    # If logged in today, keep streak same
                    elif last_login_date == today:
                        current_streak = current_streak
                    # If missed a day, reset streak to 1
                    else:
                        current_streak = 1
                except:
                    current_streak = 1
            else:
                # First login
                current_streak = 1
            
            # Update last login and streak
            cursor.execute("""
                UPDATE users 
                SET last_login = ?, streak = ?
                WHERE id = ?
            """, (today.strftime("%Y-%m-%d"), current_streak, user_id))
            
            self.db.commit()
            
            # Update current user object
            self.current_user['streak'] = current_streak
            self.current_user['last_login'] = today.strftime("%Y-%m-%d")
            
        except Exception as e:
            print(f"Error updating streak on login: {e}")
            import traceback
            traceback.print_exc()

    def show_register(self):
        try:
            self.current_page = "register"
            self._clear_main()
            self._update_brand_responsiveness()
            reg_screen.register_window(self.main_frame, self.db, 
                                     on_registered=self._on_registered,
                                     on_back_to_login=self.show_login)
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
            self._refresh_current_user()
            self._refresh_sidebar()
            self._clear_main()
            self._update_brand_responsiveness()
            home_screen.create_home(self.main_frame, self.db, user=self.current_user)
        except Exception as e:
            print(f"Home screen error: {e}")

    def show_routines(self):
        try:
            if not self.current_user:
                self.show_login()
                return
            self.current_page = "routines"
            self._refresh_current_user()
            self._refresh_sidebar()
            self._clear_main()
            self._update_brand_responsiveness()
            routines_screen.create_routines(self.main_frame, self.db, user=self.current_user)
        except Exception as e:
            print(f"Routines screen error: {e}")

    def show_profile(self):
        try:
            if not self.current_user:
                self.show_login()
                return
            self.current_page = "profile"
            self._refresh_current_user()
            self._refresh_sidebar()
            self._clear_main()
            self._update_brand_responsiveness()
            profile_screen.create_profile(self.main_frame, self.db, user=self.current_user)
        except Exception as e:
            print(f"Profile screen error: {e}")


if __name__ == "__main__":
    try:
        App()
    except Exception as e:
        print(f"App initialization error: {e}")
        import traceback
        traceback.print_exc()