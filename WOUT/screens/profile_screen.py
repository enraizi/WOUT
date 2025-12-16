import customtkinter as ctk
import calendar
from datetime import datetime
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from crud import routines_crud

def create_profile(parent, db, user=None):
    try:
        for w in parent.winfo_children():
            w.destroy()
        
        main_container = ctk.CTkFrame(parent, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=32, pady=32)
        
        # Extract user data
        username = "User"
        display_name = "User"
        created_at = "N/A"
        user_id = None
        weight = None
        weight_unit = "kg"
        birthdate = None
        
        if user:
            try:
                if isinstance(user, dict):
                    user_id = user.get('id')
                    username = user.get('username', 'User')
                    display_name = user.get('display_name') or username
                    created_at = user.get('created_at', 'N/A')
                    weight = user.get('weight')
                    weight_unit = user.get('weight_unit', 'kg')
                    birthdate = user.get('birthdate')
                else:
                    user_id = user[0] if len(user) > 0 else None
                    username = user[1] if len(user) > 1 else "User"
                    display_name = user[3] if len(user) > 3 and user[3] else username
                    created_at = user[4] if len(user) > 4 else "N/A"
            except Exception as e:
                print(f"Error extracting user data: {e}")
        
        # Fetch latest user data from database
        if user_id:
            try:
                cursor = db.cursor()
                cursor.execute("SELECT display_name, weight, weight_unit, birthdate, created_at FROM users WHERE id = ?", (user_id,))
                db_row = cursor.fetchone()
                if db_row:
                    display_name = db_row[0] if db_row[0] else username
                    weight = db_row[1]
                    weight_unit = db_row[2] if db_row[2] else "kg"
                    birthdate = db_row[3]
                    created_at = db_row[4] if db_row[4] else "N/A"
            except Exception as e:
                print(f"Error fetching user details: {e}")
        
        # Define modal functions FIRST (before they're used)
        def open_weight_modal():
            root = parent.winfo_toplevel()
            modal = ctk.CTkToplevel(root)
            modal.title("Edit Weight")
            modal.geometry("400x300")
            modal.resizable(False, False)
            modal.grab_set()
            
            modal.update_idletasks()
            root.update_idletasks()
            x = root.winfo_x() + (root.winfo_width() // 2) - 200
            y = root.winfo_y() + (root.winfo_height() // 2) - 150
            modal.geometry(f"+{x}+{y}")
            
            modal_frame = ctk.CTkFrame(modal, fg_color=("gray95", "#1a1f26"), corner_radius=0)
            modal_frame.pack(fill="both", expand=True, padx=0, pady=0)
            
            # Header with gradient effect
            header = ctk.CTkFrame(modal_frame, fg_color=("gray85", "#2a3a4a"), corner_radius=0)
            header.pack(fill="x", padx=0, pady=0)
            
            ctk.CTkLabel(header, text="⚖️ Edit Weight",
                        font=ctk.CTkFont(size=15, weight="bold"),
                        text_color=("gray10", "#ffd700")).pack(pady=16, padx=20)
            
            # Content area with scrollable frame
            scrollable_frame = ctk.CTkScrollableFrame(modal_frame, fg_color="transparent", corner_radius=0)
            scrollable_frame.pack(fill="both", expand=True, padx=0, pady=0)
            
            weight_var = ctk.StringVar(value=str(weight) if weight else "70")
            unit_var = ctk.StringVar(value=weight_unit)
            error_msg = ctk.CTkLabel(scrollable_frame, text="",
                                    font=ctk.CTkFont(size=9),
                                    text_color=("#dc2626", "#ff6b6b"))
            error_msg.pack(anchor="w", pady=(12, 8), padx=24)
            
            # Weight input with arrow buttons - modern spinner
            weight_frame = ctk.CTkFrame(scrollable_frame, fg_color="transparent")
            weight_frame.pack(fill="x", padx=24, pady=(0, 16))
            
            input_row = ctk.CTkFrame(weight_frame, fg_color="transparent")
            input_row.pack(fill="x")
            
            # Up arrow button
            def decrease_weight():
                try:
                    current = float(weight_var.get())
                    weight_var.set(str(max(20, current - 0.5)))
                except:
                    pass
            
            ctk.CTkButton(input_row, text="▲", command=decrease_weight,
                         width=50, height=45, corner_radius=8,
                         font=ctk.CTkFont(size=16, weight="bold"),
                         fg_color=("gray75", "#2a3a4a"),
                         text_color=("gray20", "#ffd700"),
                         hover_color=("gray65", "#3a4a5a")).pack(side="left", padx=(0, 10))
            
            # Weight display - large and prominent
            weight_display = ctk.CTkEntry(input_row, textvariable=weight_var,
                                         font=ctk.CTkFont(size=20, weight="bold"),
                                         justify="center",
                                         height=45, border_width=2,
                                         border_color=("gray70", "#ffd700"),
                                         fg_color=("white", "#2a2f36"),
                                         text_color=("gray10", "#ffd700"))
            weight_display.pack(side="left", fill="x", expand=True, padx=0)
            
            # Down arrow button
            def increase_weight():
                try:
                    current = float(weight_var.get())
                    weight_var.set(str(min(300, current + 0.5)))
                except:
                    pass
            
            ctk.CTkButton(input_row, text="▼", command=increase_weight,
                         width=50, height=45, corner_radius=8,
                         font=ctk.CTkFont(size=16, weight="bold"),
                         fg_color=("gray75", "#2a3a4a"),
                         text_color=("gray20", "#ffd700"),
                         hover_color=("gray65", "#3a4a5a")).pack(side="left", padx=(10, 0))
            
            # Unit selection - modern toggle
            unit_frame = ctk.CTkFrame(scrollable_frame, fg_color="transparent")
            unit_frame.pack(fill="x", padx=24, pady=(0, 20))
            
            unit_buttons = ctk.CTkFrame(unit_frame, fg_color=("gray85", "#2a3a4a"), corner_radius=8)
            unit_buttons.pack(fill="x")
            
            kg_btn = ctk.CTkButton(unit_buttons, text="Kilograms (kg)",
                         corner_radius=6,
                         fg_color=("#2563eb" if weight_unit == "kg" else "#3a3a3a", "#2563eb" if weight_unit == "kg" else "#3a3a3a"),
                         text_color=("white" if weight_unit == "kg" else "gray60", "white" if weight_unit == "kg" else "#e0e0e0"),
                         font=ctk.CTkFont(size=11, weight="bold"),
                         hover_color=("#1d4ed8" if weight_unit == "kg" else "#4a4a4a", "#1d4ed8" if weight_unit == "kg" else "#4a4a4a"),
                         border_width=0)
            kg_btn.pack(side="left", fill="both", expand=True, padx=4, pady=4)
            
            lbs_btn = ctk.CTkButton(unit_buttons, text="Pounds (lbs)",
                         corner_radius=6,
                         fg_color=("#2563eb" if weight_unit == "lbs" else "#3a3a3a", "#2563eb" if weight_unit == "lbs" else "#3a3a3a"),
                         text_color=("white" if weight_unit == "lbs" else "gray60", "white" if weight_unit == "lbs" else "#e0e0e0"),
                         font=ctk.CTkFont(size=11, weight="bold"),
                         hover_color=("#1d4ed8" if weight_unit == "lbs" else "#4a4a4a", "#1d4ed8" if weight_unit == "lbs" else "#4a4a4a"),
                         border_width=0)
            lbs_btn.pack(side="left", fill="both", expand=True, padx=4, pady=4)
            
            def set_kg():
                unit_var.set("kg")
                kg_btn.configure(fg_color=("#2563eb", "#2563eb"), text_color=("white", "white"))
                lbs_btn.configure(fg_color=("#3a3a3a", "#3a3a3a"), text_color=("gray60", "#e0e0e0"))
            
            def set_lbs():
                unit_var.set("lbs")
                lbs_btn.configure(fg_color=("#2563eb", "#2563eb"), text_color=("white", "white"))
                kg_btn.configure(fg_color=("#3a3a3a", "#3a3a3a"), text_color=("gray60", "#e0e0e0"))
            
            kg_btn.configure(command=set_kg)
            lbs_btn.configure(command=set_lbs)
            
            # Button frame - fixed at bottom
            button_frame = ctk.CTkFrame(modal_frame, fg_color=("gray85", "#2a3a4a"), corner_radius=0)
            button_frame.pack(fill="x", padx=0, pady=0, side="bottom")
            
            button_inner = ctk.CTkFrame(button_frame, fg_color="transparent")
            button_inner.pack(fill="x", padx=24, pady=12)
            
            def save_weight():
                try:
                    w_str = weight_var.get().strip()
                    if not w_str:
                        error_msg.configure(text="Please enter a weight")
                        return
                    w = float(w_str)
                    if w < 20 or w > 300:
                        error_msg.configure(text="Weight must be between 20 and 300")
                        return
                    u = unit_var.get()
                    cursor = db.cursor()
                    cursor.execute("UPDATE users SET weight = ?, weight_unit = ? WHERE id = ?",
                                 (w, u, user_id))
                    db.commit()
                    modal.destroy()
                    create_profile(parent, db, user)
                except ValueError:
                    error_msg.configure(text="Please enter a valid number")
                except Exception as e:
                    error_msg.configure(text=f"Error: {str(e)[:30]}")
            
            ctk.CTkButton(button_inner, text="Cancel", command=modal.destroy,
                         width=75, height=44, corner_radius=8,
                         font=ctk.CTkFont(size=11, weight="bold"),
                         fg_color=("gray80", "#2a3a4a"),
                         text_color=("gray20", "#e0e0e0"),
                         hover_color=("gray70", "#3a4a5a")).pack(side="left", padx=(0, 10))
            
            ctk.CTkButton(button_inner, text="Save", command=save_weight,
                         width=75, height=44, corner_radius=8,
                         font=ctk.CTkFont(size=11, weight="bold"),
                         fg_color=("#2563eb", "#2563eb"),
                         text_color=("white", "white"),
                         hover_color=("#1d4ed8", "#1d4ed8")).pack(side="left")

        def open_birthdate_modal():
            root = parent.winfo_toplevel()
            modal = ctk.CTkToplevel(root)
            modal.title("Select Birthdate")
            modal.geometry("460x540")
            modal.resizable(False, False)
            modal.grab_set()
            
            modal.update_idletasks()
            root.update_idletasks()
            x = root.winfo_x() + (root.winfo_width() // 2) - 230
            y = root.winfo_y() + (root.winfo_height() // 2) - 270
            modal.geometry(f"+{x}+{y}")
            
            modal_frame = ctk.CTkFrame(modal, fg_color=("gray95", "#1a1f26"), corner_radius=0)
            modal_frame.pack(fill="both", expand=True, padx=0, pady=0)
            
            # Header
            header = ctk.CTkFrame(modal_frame, fg_color=("gray85", "#2a3a4a"), corner_radius=0)
            header.pack(fill="x", padx=0, pady=0)
            
            ctk.CTkLabel(header, text="📅 Select Your Birthdate",
                        font=ctk.CTkFont(size=15, weight="bold"),
                        text_color=("gray10", "#ffd700")).pack(pady=16, padx=20)
            
            # Content area
            content = ctk.CTkFrame(modal_frame, fg_color="transparent")
            content.pack(fill="both", expand=True, padx=24, pady=20)
            
            # Parse existing birthdate
            current_year = datetime.now().year
            current_month = datetime.now().month
            current_day = datetime.now().day
            
            if birthdate:
                try:
                    bd = datetime.strptime(birthdate, "%Y-%m-%d")
                    current_year = bd.year
                    current_month = bd.month
                    current_day = bd.day
                except:
                    pass
            
            error_msg = ctk.CTkLabel(content, text="",
                                    font=ctk.CTkFont(size=9),
                                    text_color=("#dc2626", "#ff6b6b"))
            error_msg.pack(anchor="w", pady=(0, 12))
            
            # Year selector
            year_frame = ctk.CTkFrame(content, fg_color="transparent")
            year_frame.pack(fill="x", pady=10)
            
            ctk.CTkLabel(year_frame, text="Year:", font=ctk.CTkFont(size=11, weight="bold"),
                        text_color=("gray20", "#e0e0e0")).pack(anchor="w", pady=(0, 8))
            
            year_var = ctk.StringVar(value=str(current_year))
            
            def decrease_year():
                try:
                    current = int(year_var.get())
                    year_var.set(str(max(1920, current - 1)))
                except:
                    pass
            
            def increase_year():
                try:
                    current = int(year_var.get())
                    year_var.set(str(min(datetime.now().year, current + 1)))
                except:
                    pass
            
            year_input = ctk.CTkFrame(year_frame, fg_color="transparent")
            year_input.pack(fill="x")
            
            ctk.CTkButton(year_input, text="−", command=decrease_year, width=45, height=40,
                         corner_radius=6, font=ctk.CTkFont(size=18, weight="bold"),
                         fg_color=("gray80", "#2a3a4a"), text_color=("gray20", "#e0e0e0"),
                         hover_color=("gray70", "#3a4a5a")).pack(side="left", padx=(0, 8))
            
            year_display = ctk.CTkEntry(year_input, textvariable=year_var, width=100,
                                       font=ctk.CTkFont(size=14, weight="bold"), justify="center",
                                       height=40, border_width=1, border_color=("gray70", "#3a4a5a"),
                                       fg_color=("white", "#2a2f36"))
            year_display.pack(side="left", fill="x", expand=True, padx=0)
            
            ctk.CTkButton(year_input, text="+", command=increase_year, width=45, height=40,
                         corner_radius=6, font=ctk.CTkFont(size=18, weight="bold"),
                         fg_color=("gray80", "#2a3a4a"), text_color=("gray20", "#e0e0e0"),
                         hover_color=("gray70", "#3a4a5a")).pack(side="left", padx=(8, 0))
            
            # Month selector
            month_frame = ctk.CTkFrame(content, fg_color="transparent")
            month_frame.pack(fill="x", pady=10)
            
            ctk.CTkLabel(month_frame, text="Month:", font=ctk.CTkFont(size=11, weight="bold"),
                        text_color=("gray20", "#e0e0e0")).pack(anchor="w", pady=(0, 8))
            
            month_var = ctk.StringVar(value=str(current_month))
            
            def decrease_month():
                try:
                    current = int(month_var.get())
                    month_var.set(str(max(1, current - 1)))
                except:
                    pass
            
            def increase_month():
                try:
                    current = int(month_var.get())
                    month_var.set(str(min(12, current + 1)))
                except:
                    pass
            
            month_input = ctk.CTkFrame(month_frame, fg_color="transparent")
            month_input.pack(fill="x")
            
            ctk.CTkButton(month_input, text="−", command=decrease_month, width=45, height=40,
                         corner_radius=6, font=ctk.CTkFont(size=18, weight="bold"),
                         fg_color=("gray80", "#2a3a4a"), text_color=("gray20", "#e0e0e0"),
                         hover_color=("gray70", "#3a4a5a")).pack(side="left", padx=(0, 8))
            
            month_display = ctk.CTkEntry(month_input, textvariable=month_var, width=100,
                                        font=ctk.CTkFont(size=14, weight="bold"), justify="center",
                                        height=40, border_width=1, border_color=("gray70", "#3a4a5a"),
                                        fg_color=("white", "#2a2f36"))
            month_display.pack(side="left", fill="x", expand=True, padx=0)
            
            ctk.CTkButton(month_input, text="+", command=increase_month, width=45, height=40,
                         corner_radius=6, font=ctk.CTkFont(size=18, weight="bold"),
                         fg_color=("gray80", "#2a3a4a"), text_color=("gray20", "#e0e0e0"),
                         hover_color=("gray70", "#3a4a5a")).pack(side="left", padx=(8, 0))
            
            # Day selector
            day_frame = ctk.CTkFrame(content, fg_color="transparent")
            day_frame.pack(fill="x", pady=10)
            
            ctk.CTkLabel(day_frame, text="Day:", font=ctk.CTkFont(size=11, weight="bold"),
                        text_color=("gray20", "#e0e0e0")).pack(anchor="w", pady=(0, 8))
            
            day_var = ctk.StringVar(value=str(current_day))
            
            def decrease_day():
                try:
                    current = int(day_var.get())
                    day_var.set(str(max(1, current - 1)))
                except:
                    pass
            
            def increase_day():
                try:
                    current = int(day_var.get())
                    day_var.set(str(min(31, current + 1)))
                except:
                    pass
            
            day_input = ctk.CTkFrame(day_frame, fg_color="transparent")
            day_input.pack(fill="x")
            
            ctk.CTkButton(day_input, text="−", command=decrease_day, width=45, height=40,
                         corner_radius=6, font=ctk.CTkFont(size=18, weight="bold"),
                         fg_color=("gray80", "#2a3a4a"), text_color=("gray20", "#e0e0e0"),
                         hover_color=("gray70", "#3a4a5a")).pack(side="left", padx=(0, 8))
            
            day_display = ctk.CTkEntry(day_input, textvariable=day_var, width=100,
                                      font=ctk.CTkFont(size=14, weight="bold"), justify="center",
                                      height=40, border_width=1, border_color=("gray70", "#3a4a5a"),
                                      fg_color=("white", "#2a2f36"))
            day_display.pack(side="left", fill="x", expand=True, padx=0)
            
            ctk.CTkButton(day_input, text="+", command=increase_day, width=45, height=40,
                         corner_radius=6, font=ctk.CTkFont(size=18, weight="bold"),
                         fg_color=("gray80", "#2a3a4a"), text_color=("gray20", "#e0e0e0"),
                         hover_color=("gray70", "#3a4a5a")).pack(side="left", padx=(8, 0))
            
            # Month name display
            month_names = ["", "January", "February", "March", "April", "May", "June",
                          "July", "August", "September", "October", "November", "December"]
            
            date_preview = ctk.CTkLabel(content, text="",
                                       font=ctk.CTkFont(size=12, weight="bold"),
                                       text_color=("gray10", "#ffd700"))
            date_preview.pack(pady=16)
            
            def update_preview(*args):
                try:
                    y = int(year_var.get())
                    m = int(month_var.get())
                    d = int(day_var.get())
                    if 1 <= m <= 12 and 1 <= d <= 31:
                        date_preview.configure(text=f"{month_names[m]} {d}, {y}")
                except:
                    pass
            
            year_var.trace("w", update_preview)
            month_var.trace("w", update_preview)
            day_var.trace("w", update_preview)
            update_preview()
            
            # Button frame
            button_frame = ctk.CTkFrame(content, fg_color="transparent")
            button_frame.pack(fill="x", pady=(8, 0))
            
            def save_birthdate():
                try:
                    year = int(year_var.get().strip())
                    month = int(month_var.get().strip())
                    day = int(day_var.get().strip())
                    
                    date_obj = datetime(year, month, day)
                    date_str = date_obj.strftime("%Y-%m-%d")
                    
                    cursor = db.cursor()
                    cursor.execute("UPDATE users SET birthdate = ? WHERE id = ?",
                                 (date_str, user_id))
                    db.commit()
                    modal.destroy()
                    create_profile(parent, db, user)
                except ValueError:
                    error_msg.configure(text="Please enter a valid date")
                except Exception as e:
                    error_msg.configure(text=f"Error: {str(e)[:30]}")
            
            ctk.CTkButton(button_frame, text="Cancel", command=modal.destroy,
                         width=75, height=44, corner_radius=8,
                         font=ctk.CTkFont(size=11, weight="bold"),
                         fg_color=("gray80", "#2a3a4a"),
                         text_color=("gray20", "#e0e0e0"),
                         hover_color=("gray70", "#3a4a5a")).pack(side="left", padx=(0, 10))
            
            ctk.CTkButton(button_frame, text="Save", command=save_birthdate,
                         width=75, height=44, corner_radius=8,
                         font=ctk.CTkFont(size=11, weight="bold"),
                         fg_color=("#2563eb", "#2563eb"),
                         text_color=("white", "white"),
                         hover_color=("#1d4ed8", "#1d4ed8")).pack(side="left")

        def open_display_name_modal():
            root = parent.winfo_toplevel()
            modal = ctk.CTkToplevel(root)
            modal.title("Edit Display Name")
            modal.geometry("420x260")
            modal.resizable(False, False)
            modal.grab_set()
            
            modal.update_idletasks()
            root.update_idletasks()
            x = root.winfo_x() + (root.winfo_width() // 2) - 210
            y = root.winfo_y() + (root.winfo_height() // 2) - 130
            modal.geometry(f"+{x}+{y}")
            
            modal_frame = ctk.CTkFrame(modal, fg_color=("gray95", "#1a1f26"), corner_radius=0)
            modal_frame.pack(fill="both", expand=True, padx=0, pady=0)
            
            # Header
            header = ctk.CTkFrame(modal_frame, fg_color=("gray85", "#2a3a4a"), corner_radius=0)
            header.pack(fill="x", padx=0, pady=0)
            
            ctk.CTkLabel(header, text="✏️ Edit Display Name",
                        font=ctk.CTkFont(size=15, weight="bold"),
                        text_color=("gray10", "#ffd700")).pack(pady=16, padx=20)
            
            # Content area (fixed height, not scrollable)
            content = ctk.CTkFrame(modal_frame, fg_color="transparent", height=100)
            content.pack(fill="x", expand=False, padx=24, pady=16)
            content.pack_propagate(False)
            
            display_name_var = ctk.StringVar(value=display_name)
            error_msg = ctk.CTkLabel(content, text="",
                                    font=ctk.CTkFont(size=9),
                                    text_color=("#dc2626", "#ff6b6b"))
            error_msg.pack(anchor="w", pady=(0, 8))
            
            # Input field
            entry = ctk.CTkEntry(content, textvariable=display_name_var,
                                placeholder_text="Max 13 characters",
                                height=44, border_width=2,
                                border_color=("gray70", "#ffd700"),
                                fg_color=("white", "#2a2f36"),
                                text_color=("gray10", "#ffd700"),
                                font=ctk.CTkFont(size=12, weight="bold"))
            entry.pack(fill="x", pady=(0, 8))
            
            counter_label = ctk.CTkLabel(content, text=f"{len(display_name)}/13",
                                        font=ctk.CTkFont(size=9, weight="bold"),
                                        text_color=("gray60", "#90caf9"))
            counter_label.pack(anchor="e")
            
            def validate_input(value):
                if len(value) > 13:
                    display_name_var.set(value[:13])
                    return False
                if not all(c.isalnum() or c == ' ' for c in value):
                    display_name_var.set(''.join(c for c in value if c.isalnum() or c == ' '))
                    return False
                error_msg.configure(text="")
                return True
            
            def update_counter(*args):
                validate_input(display_name_var.get())
                counter_label.configure(text=f"{len(display_name_var.get())}/13")
            
            display_name_var.trace("w", update_counter)
            
            # Button frame - fixed at bottom
            button_frame = ctk.CTkFrame(modal_frame, fg_color=("gray85", "#2a3a4a"), corner_radius=0)
            button_frame.pack(fill="x", padx=0, pady=0, side="bottom")
            
            button_inner = ctk.CTkFrame(button_frame, fg_color="transparent")
            button_inner.pack(fill="x", padx=24, pady=12)
            
            def save_changes():
                new_name = display_name_var.get().strip()
                if not new_name:
                    error_msg.configure(text="Cannot be empty")
                    return
                if not validate_input(new_name):
                    error_msg.configure(text="Invalid characters")
                    return
                try:
                    cursor = db.cursor()
                    cursor.execute("UPDATE users SET display_name = ? WHERE id = ?",
                                 (new_name, user_id))
                    db.commit()
                    modal.destroy()
                    create_profile(parent, db, user)
                except Exception as e:
                    error_msg.configure(text=f"Error: {str(e)[:20]}")
            
            ctk.CTkButton(button_inner, text="Cancel", command=modal.destroy,
                         width=75, height=44, corner_radius=8,
                         font=ctk.CTkFont(size=11, weight="bold"),
                         fg_color=("gray80", "#2a3a4a"),
                         text_color=("gray20", "#e0e0e0"),
                         hover_color=("gray70", "#3a4a5a")).pack(side="left", padx=(0, 10))
            
            ctk.CTkButton(button_inner, text="Save", command=save_changes,
                         width=75, height=44, corner_radius=8,
                         font=ctk.CTkFont(size=11, weight="bold"),
                         fg_color=("#2563eb", "#2563eb"),
                         text_color=("white", "white"),
                         hover_color=("#1d4ed8", "#1d4ed8")).pack(side="left")

        # Header with username
        header_frame = ctk.CTkFrame(main_container, fg_color="transparent", height=60)
        header_frame.pack(fill="x", pady=(0, 20))
        header_frame.pack_propagate(False)
        
        ctk.CTkLabel(header_frame, text="Profile", 
                     font=ctk.CTkFont(size=28, weight="bold"),
                     text_color=("gray10", "#ffffff")).pack(anchor="w", pady=(0, 8))
        
        username_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        username_frame.pack(anchor="w", fill="x")
        
        ctk.CTkLabel(username_frame, text=f"@{username}", 
                     font=ctk.CTkFont(size=13, weight="bold"),
                     text_color=("gray10", "#ffd700")).pack(side="left", padx=(0, 8))
        
        ctk.CTkLabel(username_frame, text=f"({display_name})", 
                     font=ctk.CTkFont(size=11),
                     text_color=("gray60", "#a0a0a0")).pack(side="left", padx=(0, 12))

        # Edit button in header
        def open_edit_modal():
            root = parent.winfo_toplevel()
            modal = ctk.CTkToplevel(root)
            modal.title("Edit Display Name")
            modal.geometry("360x160")
            modal.resizable(False, False)
            modal.grab_set()
            
            modal.update_idletasks()
            root.update_idletasks()
            
            x = root.winfo_x() + (root.winfo_width() // 2) - 180
            y = root.winfo_y() + (root.winfo_height() // 2) - 80
            modal.geometry(f"+{x}+{y}")
            
            modal_frame = ctk.CTkFrame(modal, fg_color=("white", "#1a1f26"))
            modal_frame.pack(fill="both", expand=True, padx=20, pady=20)
            
            ctk.CTkLabel(modal_frame, text="Edit Display Name",
                        font=ctk.CTkFont(size=13, weight="bold"),
                        text_color=("gray10", "#ffffff")).pack(pady=(0, 16), padx=12)
            
            display_name_var = ctk.StringVar(value=display_name)
            error_msg = ctk.CTkLabel(modal_frame, text="",
                                    font=ctk.CTkFont(size=9),
                                    text_color=("#dc2626", "#ff6b6b"))
            
            def validate_input(value):
                if len(value) > 13:
                    display_name_var.set(value[:13])
                    return False
                if not all(c.isalnum() or c == ' ' for c in value):
                    display_name_var.set(''.join(c for c in value if c.isalnum() or c == ' '))
                    return False
                error_msg.configure(text="")
                return True
            
            entry_frame = ctk.CTkFrame(modal_frame, fg_color="transparent")
            entry_frame.pack(fill="x", pady=(0, 12), padx=12)
            
            entry = ctk.CTkEntry(entry_frame, textvariable=display_name_var,
                                placeholder_text="Max 13 characters",
                                height=40, border_width=1,
                                border_color=("gray80", "#333333"),
                                fg_color=("gray95", "#2a2f36"))
            entry.pack(side="left", fill="x", expand=True, padx=(0, 8))
            
            counter = ctk.CTkLabel(entry_frame, text=f"{len(display_name)}/13",
                                  font=ctk.CTkFont(size=8),
                                  text_color=("gray60", "#a0a0a0"))
            counter.pack(side="right")
            
            def update_counter(*args):
                validate_input(display_name_var.get())
                counter.configure(text=f"{len(display_name_var.get())}/13")
            
            display_name_var.trace("w", update_counter)
            
            def save_changes():
                new_name = display_name_var.get().strip()
                if not new_name:
                    error_msg.configure(text="Cannot be empty")
                    return
                if not validate_input(new_name):
                    error_msg.configure(text="Invalid characters")
                    return
                try:
                    cursor = db.cursor()
                    cursor.execute("UPDATE users SET display_name = ? WHERE id = ?",
                                 (new_name, user_id))
                    db.commit()
                    modal.destroy()
                except Exception as e:
                    error_msg.configure(text=f"Error: {str(e)[:20]}")
            
            button_frame = ctk.CTkFrame(modal_frame, fg_color="transparent")
            button_frame.pack(fill="x", padx=12)
            
            ctk.CTkButton(button_frame, text="Cancel", command=modal.destroy,
                         width=70, height=36, corner_radius=6,
                         font=ctk.CTkFont(size=10),
                         fg_color=("gray90", "#2a2f36"),
                         text_color=("gray20", "#e0e0e0"),
                         hover_color=("gray80", "#333333")).pack(side="left", padx=(0, 8))
            
            ctk.CTkButton(button_frame, text="Save", command=save_changes,
                         width=70, height=36, corner_radius=6,
                         font=ctk.CTkFont(size=10, weight="bold"),
                         fg_color=("#2563eb", "#2563eb"),
                         hover_color=("#1d4ed8", "#1d4ed8")).pack(side="left")
            
            error_msg.pack(anchor="w", pady=(8, 0), padx=12)

        ctk.CTkButton(username_frame, text="✏️",
                     command=open_display_name_modal,
                     width=28, height=28, corner_radius=6,
                     font=ctk.CTkFont(size=10),
                     fg_color=("gray90", "#2a2f36"),
                     text_color=("gray60", "#e0e0e0"),
                     hover_color=("gray80", "#333333")).pack(side="left")

        # Top section - Account Details and Calendar
        top_section = ctk.CTkFrame(main_container, fg_color="transparent", height=300)
        top_section.pack(fill="both", expand=False, padx=0, pady=(0, 20))
        top_section.pack_propagate(False)

        # Left side - Account Details
        left_frame = ctk.CTkFrame(top_section, fg_color="transparent")
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 12))

        account_card = ctk.CTkFrame(left_frame, fg_color=("gray95", "#1a1f26"), corner_radius=12)
        account_card.pack(fill="both", expand=True)

        account_border = ctk.CTkFrame(account_card, fg_color=("gray75", "#ffd700"), corner_radius=12)
        account_border.pack(fill="both", expand=True, padx=1, pady=1)

        account_inner = ctk.CTkFrame(account_border, fg_color=("gray95", "#1a1f26"), corner_radius=11)
        account_inner.pack(fill="both", expand=True, padx=0, pady=0, ipadx=16, ipady=12)

        ctk.CTkLabel(account_inner, text="  Account Details", 
                     font=ctk.CTkFont(size=14, weight="bold"),
                     text_color=("gray10", "#ffd700")).pack(anchor="w", pady=(0, 4))

        # Account info items
        info_items = [
            ("  👤 Username", f" {username}"),
            ("  ⚖️ Weight", f" {weight} {weight_unit}" if weight else " Not set"),
            ("  📅 Birthdate", f" {birthdate}" if birthdate else " Not set"),
            ("  📅 Date Joined", f" {created_at}"),
        ]

        for label, value in info_items:
            info_row = ctk.CTkFrame(account_inner, fg_color="transparent")
            info_row.pack(fill="x", anchor="w", pady=4)
            
            ctk.CTkLabel(info_row, text=label, 
                        font=ctk.CTkFont(size=13, weight="bold"),
                        text_color=("gray60", "#90caf9")).pack(anchor="w", pady=(0, 3))
            
            value_row = ctk.CTkFrame(info_row, fg_color="transparent")
            value_row.pack(fill="x", anchor="w")
            
            ctk.CTkLabel(value_row, text=value, 
                        font=ctk.CTkFont(size=14, weight="bold"),
                        text_color=("gray10", "#ffffff")).pack(side="left", padx=(0, 10))
            
            if "Weight" in label:
                ctk.CTkButton(value_row, text="✏️", command=open_weight_modal,
                             width=24, height=24, corner_radius=4,
                             font=ctk.CTkFont(size=9),
                             fg_color=("gray90", "#2a2f36"),
                             text_color=("gray60", "#e0e0e0"),
                             hover_color=("gray80", "#333333")).pack(side="left")
            elif "Birthdate" in label:
                ctk.CTkButton(value_row, text="✏️", command=open_birthdate_modal,
                             width=24, height=24, corner_radius=4,
                             font=ctk.CTkFont(size=9),
                             fg_color=("gray90", "#2a2f36"),
                             text_color=("gray60", "#e0e0e0"),
                             hover_color=("gray80", "#333333")).pack(side="left")

        # Right side - Calendar
        right_frame = ctk.CTkFrame(top_section, fg_color=("gray95", "#1a1f26"), corner_radius=12)
        right_frame.pack(side="right", fill="both", expand=True, padx=(12, 0))

        cal_border = ctk.CTkFrame(right_frame, fg_color=("gray75", "#ffd700"), corner_radius=12)
        cal_border.pack(fill="both", expand=True, padx=1, pady=1)

        cal_inner = ctk.CTkFrame(cal_border, fg_color=("gray95", "#1a1f26"), corner_radius=11)
        cal_inner.pack(fill="both", expand=True, padx=0, pady=0, ipadx=12, ipady=12)

        ctk.CTkLabel(cal_inner, text="  📅 Calendar",
                     font=ctk.CTkFont(size=14, weight="bold"),
                     text_color=("gray10", "#ffd700")).pack(anchor="w", pady=(0, 16))

        cal_frame = ctk.CTkFrame(cal_inner, fg_color="transparent")
        cal_frame.pack(fill="both", expand=True)

        cal = calendar.monthcalendar(datetime.now().year, datetime.now().month)
        today = datetime.now().day

        ctk.CTkLabel(cal_frame, text=datetime.now().strftime("%B %Y"),
                    font=ctk.CTkFont(size=13, weight="bold"),
                    text_color=("gray10", "#ffffff")).pack(pady=(0, 12))

        day_frame = ctk.CTkFrame(cal_frame, fg_color="transparent")
        day_frame.pack(fill="x", pady=(0, 10))

        for day in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]:
            ctk.CTkLabel(day_frame, text=day, font=ctk.CTkFont(size=11, weight="bold"),
                        text_color=("gray60", "#a0a0a0"), width=36).pack(side="left", expand=True)

        for week in cal:
            week_frame = ctk.CTkFrame(cal_frame, fg_color="transparent")
            week_frame.pack(fill="x", pady=3)

            for day in week:
                if day == 0:
                    ctk.CTkLabel(week_frame, text="", font=ctk.CTkFont(size=11),
                                width=36).pack(side="left", expand=True)
                elif day == today:
                    circle = ctk.CTkFrame(week_frame, fg_color=("#2563eb", "#2563eb"),
                                         corner_radius=16, width=36, height=36)
                    circle.pack(side="left", expand=True)
                    circle.pack_propagate(False)
                    ctk.CTkLabel(circle, text=str(day), font=ctk.CTkFont(size=11, weight="bold"),
                                text_color=("white", "white"), fg_color="transparent").pack(expand=True)
                else:
                    ctk.CTkLabel(week_frame, text=str(day), font=ctk.CTkFont(size=11),
                                text_color=("gray60", "#a0a0a0"), width=36).pack(side="left", expand=True)

        # Bottom section - Favorite Routines (SCROLLABLE)
        fav_section = ctk.CTkFrame(main_container, fg_color="transparent")
        fav_section.pack(fill="both", expand=True, padx=0, pady=(0, 0))

        ctk.CTkLabel(fav_section, text="⭐ Favorite Routines", 
                     font=ctk.CTkFont(size=13, weight="bold"),
                     text_color=("gray10", "#ffd700")).pack(anchor="w", pady=(0, 12))

        fav_card = ctk.CTkFrame(fav_section, fg_color=("gray95", "#1a1f26"), corner_radius=12)
        fav_card.pack(fill="both", expand=True)

        fav_border = ctk.CTkFrame(fav_card, fg_color=("gray75", "#ffd700"), corner_radius=12)
        fav_border.pack(fill="both", expand=True, padx=1, pady=1)

        fav_inner = ctk.CTkFrame(fav_border, fg_color=("gray95", "#1a1f26"), corner_radius=11)
        fav_inner.pack(fill="both", expand=True, padx=0, pady=0, ipadx=20, ipady=16)

        try:
            favorite_routines = routines_crud.get_favorite_routines(db, user_id)
        except Exception as e:
            print(f"Error fetching favorite routines: {e}")
            favorite_routines = []

        if not favorite_routines:
            empty_frame = ctk.CTkFrame(fav_inner, fg_color="transparent")
            empty_frame.pack(fill="both", expand=True)
            
            ctk.CTkLabel(empty_frame, text="No pinned routines yet", 
                        font=ctk.CTkFont(size=11),
                        text_color=("gray60", "#a0a0a0")).pack(expand=True)
        else:
            fav_scroll = ctk.CTkScrollableFrame(fav_inner, fg_color="transparent", corner_radius=0)
            fav_scroll.pack(fill="both", expand=True)

            for routine in favorite_routines:
                routine_name = routine.get('name', 'Unnamed') if isinstance(routine, dict) else routine[2]
                
                fav_item = ctk.CTkFrame(fav_scroll, fg_color=("gray90", "#2a2f36"), corner_radius=8)
                fav_item.pack(fill="x", pady=6)
                
                fav_item_inner = ctk.CTkFrame(fav_item, fg_color="transparent")
                fav_item_inner.pack(fill="both", expand=True, padx=12, pady=10)
                
                ctk.CTkLabel(fav_item_inner, text=f"⭐ {routine_name}", 
                            font=ctk.CTkFont(size=11, weight="bold"),
                            text_color=("gray10", "#ffd700")).pack(anchor="w")

    except Exception as e:
        print(f"Profile screen error: {e}")
        import traceback
        traceback.print_exc()