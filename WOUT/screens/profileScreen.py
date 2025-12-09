import customtkinter as ctk
import calendar
from datetime import datetime
import tkinter as tk

def create_profile(parent, db, user=None):
    try:
        # Clear parent
        for w in parent.winfo_children():
            w.destroy()
        
        main_container = ctk.CTkFrame(parent, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Safely extract user data from dict or tuple
        username = "User"
        display_name = "User"
        created_date = "N/A"
        user_id = None
        
        if user:
            try:
                if isinstance(user, dict):
                    user_id = user.get('id')
                    username = user.get('username', 'User')
                    display_name = user.get('display_name') or username
                    created_date = user.get('created_at', 'N/A')
                else:
                    user_id = user[0] if len(user) > 0 else None
                    username = user[1] if len(user) > 1 else "User"
                    display_name = user[3] if len(user) > 3 and user[3] else username
                    created_date = user[4] if len(user) > 4 else "N/A"
            except Exception as e:
                print(f"Error extracting user data: {e}")
        
        # Top header
        header_frame = ctk.CTkFrame(main_container, fg_color=("gray85", "#1a2940"), corner_radius=12)
        header_frame.pack(fill="x", pady=(0, 20))
        
        header_inner = ctk.CTkFrame(header_frame, fg_color=("gray85", "#1a2940"), corner_radius=10)
        header_inner.pack(fill="x", expand=True, padx=2, pady=2)
        
        ctk.CTkLabel(header_inner, text="💪 Profile", 
                     font=ctk.CTkFont(size=28, weight="bold"),
                     text_color=("gray10", "#ffd700")).pack(anchor="w", padx=20, pady=(16, 4))
        
        ctk.CTkLabel(header_inner, text=f"{display_name}", 
                     font=ctk.CTkFont(size=16, weight="bold"),
                     text_color=("gray50", "#90caf9")).pack(anchor="w", padx=20, pady=(0, 16))
        
        # Main content
        content_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        content_frame.pack(fill="both", expand=True)
        
        # Left side - Stats and info
        left_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Account info section with inline display name editor
        info_card = ctk.CTkFrame(left_frame, fg_color=("gray75", "#1a2940"), corner_radius=10)
        info_card.pack(fill="x", pady=(0, 20))
        
        info_border = ctk.CTkFrame(info_card, fg_color=("gray60", "#ffd700"), corner_radius=10)
        info_border.pack(fill="x", expand=True, padx=1, pady=1)
        
        info_inner = ctk.CTkFrame(info_border, fg_color=("gray75", "#1a2940"), corner_radius=9)
        info_inner.pack(fill="x", expand=True, padx=0, pady=0, ipadx=16, ipady=12)
        
        ctk.CTkLabel(info_inner, text="Account Information", 
                     font=ctk.CTkFont(size=12, weight="bold"),
                     text_color=("gray10", "#ffd700")).pack(anchor="w", pady=(0, 12))
        
        ctk.CTkLabel(info_inner, text=f"Username: {username}", 
                     font=ctk.CTkFont(size=10),
                     text_color=("gray40", "#90caf9")).pack(anchor="w", pady=4)
        
        # Inline display name editor
        display_name_frame = ctk.CTkFrame(info_inner, fg_color="transparent")
        display_name_frame.pack(fill="x", pady=4)
        
        ctk.CTkLabel(display_name_frame, text="Display Name: ", 
                     font=ctk.CTkFont(size=10),
                     text_color=("gray40", "#90caf9")).pack(side="left")
        
        display_name_var = ctk.StringVar(value=display_name)
        error_label = ctk.CTkLabel(info_inner, text="", 
                                  font=ctk.CTkFont(size=7),
                                  text_color=("red", "#ff6b6b"))
        
        def validate_display_name(value):
            """Validate: max 13 alphanumeric characters"""
            if len(value) > 13:
                error_label.configure(text="Max 13 characters")
                display_name_var.set(value[:13])
                return False
            
            if not all(c.isalnum() or c == ' ' for c in value):
                error_label.configure(text="Only letters, numbers, spaces")
                display_name_var.set(''.join(c for c in value if c.isalnum() or c == ' '))
                return False
            
            error_label.configure(text="")
            return True
        
        name_entry = ctk.CTkEntry(display_name_frame, textvariable=display_name_var,
                                 placeholder_text="Max 13 chars",
                                 width=120, height=28)
        name_entry.pack(side="left", padx=(0, 6))
        
        def save_display_name():
            new_name = display_name_var.get().strip()
            
            if not new_name:
                error_label.configure(text="Cannot be empty")
                return
            
            if not validate_display_name(new_name):
                return
            
            try:
                cursor = db.cursor()
                cursor.execute("UPDATE users SET display_name = ? WHERE id = ?",
                             (new_name, user_id))
                db.commit()
                error_label.configure(text="✓ Updated!", 
                                    text_color=("green", "#4caf50"))
                header_inner.winfo_children()[1].configure(text=new_name)
            except Exception as e:
                error_label.configure(text=f"Error: {str(e)[:20]}")
        
        save_btn = ctk.CTkButton(display_name_frame, text="Save",
                                command=save_display_name,
                                fg_color=("gray70", "#ffd700"),
                                text_color=("gray10", "black"),
                                hover_color=("gray60", "#ffed4e"),
                                font=ctk.CTkFont(size=8, weight="bold"),
                                width=50, height=28)
        save_btn.pack(side="left")
        
        error_label.pack(anchor="w", pady=(4, 0))
        
        # Calculate member duration
        try:
            if created_date != "N/A":
                member_since = datetime.fromisoformat(created_date.replace('Z', '+00:00'))
                now = datetime.now(member_since.tzinfo) if member_since.tzinfo else datetime.now()
                duration = now - member_since
                days = duration.days
                
                if days == 0:
                    duration_text = "Today"
                elif days == 1:
                    duration_text = "1 day"
                else:
                    duration_text = f"{days} days"
                
                member_info = f"Member for: {duration_text}"
            else:
                member_info = "Member Since: N/A"
        except:
            member_info = f"Member Since: {created_date}"
        
        ctk.CTkLabel(info_inner, text=member_info, 
                     font=ctk.CTkFont(size=10),
                     text_color=("gray40", "#90caf9")).pack(anchor="w", pady=4)
        
        # Stats cards
        stats_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
        stats_frame.pack(fill="x", pady=(0, 20))
        
        stats = [
            ("🏋️", "Workouts", "0"),
            ("⚡", "Streak", "0 days"),
            ("🎯", "Goals", "0"),
        ]
        
        for emoji, label, value in stats:
            stat_card = ctk.CTkFrame(stats_frame, fg_color=("gray80", "#1a2940"), 
                                    corner_radius=8)
            stat_card.pack(fill="x", pady=6)
            
            stat_border = ctk.CTkFrame(stat_card, fg_color=("gray70", "#ffd700"), corner_radius=8)
            stat_border.pack(fill="x", expand=True, padx=1, pady=1)
            
            stat_inner = ctk.CTkFrame(stat_border, fg_color=("gray80", "#1a2940"), 
                                     corner_radius=7)
            stat_inner.pack(fill="x", expand=True, padx=0, pady=0)
            
            stat_header = ctk.CTkFrame(stat_inner, fg_color="transparent")
            stat_header.pack(fill="x", padx=16, pady=(10, 0))
            
            ctk.CTkLabel(stat_header, text=emoji, 
                        font=ctk.CTkFont(size=18)).pack(side="left", padx=(0, 8))
            
            label_frame = ctk.CTkFrame(stat_header, fg_color="transparent")
            label_frame.pack(side="left", fill="x", expand=True)
            
            ctk.CTkLabel(label_frame, text=label, 
                        font=ctk.CTkFont(size=10, weight="bold"),
                        text_color=("gray20", "#ffd700")).pack(anchor="w")
            
            ctk.CTkLabel(stat_header, text=value, 
                        font=ctk.CTkFont(size=14, weight="bold"),
                        text_color=("gray10", "white")).pack(side="right")
            
            ctk.CTkLabel(stat_inner, text="", 
                        font=ctk.CTkFont(size=8),
                        text_color=("gray50", "#b3e5fc")).pack(anchor="w", padx=16, pady=(0, 10))
        
        # Right side - Calendar widget
        right_frame = ctk.CTkFrame(content_frame, fg_color=("gray80", "#1a2940"), 
                                  corner_radius=10, width=280)
        right_frame.pack_propagate(False)
        right_frame.pack(side="right", fill="y", padx=(10, 0))
        
        calendar_frame = ctk.CTkFrame(right_frame, fg_color=("gray80", "#1a2940"), corner_radius=8)
        calendar_frame.pack(fill="both", expand=True, padx=12, pady=12)
        
        ctk.CTkLabel(calendar_frame, text="📅 Calendar", 
                     font=ctk.CTkFont(size=12, weight="bold"),
                     text_color=("gray10", "#ffd700")).pack(pady=(0, 12))
        
        # Embed calendar
        cal_frame = ctk.CTkFrame(calendar_frame, fg_color=("white", "#0d1b2a"))
        cal_frame.pack(fill="both", expand=True)
        
        cal = calendar.monthcalendar(datetime.now().year, datetime.now().month)
        
        # Month/Year header
        month_label = ctk.CTkLabel(cal_frame, 
                                  text=datetime.now().strftime("%B %Y"),
                                  font=ctk.CTkFont(size=10, weight="bold"),
                                  text_color=("gray10", "#ffd700"))
        month_label.pack(pady=(8, 4))
        
        # Day labels
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        day_frame = ctk.CTkFrame(cal_frame, fg_color="transparent")
        day_frame.pack(fill="x", padx=4, pady=4)
        for day in days:
            ctk.CTkLabel(day_frame, text=day, 
                        font=ctk.CTkFont(size=8, weight="bold"),
                        text_color=("gray40", "#90caf9")).pack(side="left", expand=True)
        
        # Calendar grid
        for week in cal:
            week_frame = ctk.CTkFrame(cal_frame, fg_color="transparent")
            week_frame.pack(fill="x", padx=4, pady=2)
            for day in week:
                day_text = str(day) if day != 0 else ""
                day_label = ctk.CTkLabel(week_frame, text=day_text, 
                                        font=ctk.CTkFont(size=8),
                                        text_color=("gray50", "#90caf9") if day != 0 else ("white", "#1a2940"))
                day_label.pack(side="left", expand=True, fill="both")
    
    except Exception as e:
        print(f"Profile screen error: {e}")
        import traceback
        traceback.print_exc()