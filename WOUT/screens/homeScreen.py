import customtkinter as ctk
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from crud import routinesCrud

def create_home(parent, db_conn, user=None, refresh_callback=None):
    frame = ctk.CTkFrame(parent, corner_radius=0, fg_color="transparent")
    frame.pack(fill="both", expand=True, padx=0, pady=0)

    if not user:
        ctk.CTkLabel(frame, text="Error: No user data.", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=20)
        return frame

    name = user.get("display_name") if isinstance(user, dict) else None
    username = user.get("username") if isinstance(user, dict) else str(user)
    user_id = user.get("id") if isinstance(user, dict) else None
    
    # Header
    header = ctk.CTkFrame(frame, fg_color="transparent", height=80)
    header.pack(fill="x", padx=32, pady=(24, 32))
    header.pack_propagate(False)
    
    ctk.CTkLabel(header, text=f"Welcome back, {name or username}", 
                 font=ctk.CTkFont(size=24, weight="bold"),
                 text_color=("gray10", "#ffffff")).pack(anchor="w")
    
    ctk.CTkLabel(header, text="Let's get a great workout in 💪", 
                 font=ctk.CTkFont(size=12),
                 text_color=("gray60", "#a0a0a0")).pack(anchor="w", pady=(4, 0))

    # Content area
    main_content = ctk.CTkFrame(frame, fg_color="transparent", corner_radius=0)
    main_content.pack(fill="both", expand=True, padx=32, pady=(0, 32))

    # Create a dynamic container that will hold either pinned or all routines
    content_container = ctk.CTkFrame(main_content, fg_color="transparent")
    content_container.pack(fill="both", expand=True, padx=0, pady=0)

    def refresh_content():
        """Refresh the entire content based on pinned routines availability"""
        for w in content_container.winfo_children():
            w.destroy()
        
        try:
            favorite_routines = routinesCrud.get_favorite_routines(db_conn, user_id=user_id)
        except Exception as e:
            print(f"Error fetching favorite routines: {e}")
            favorite_routines = []

        try:
            all_routines = routinesCrud.get_routines(db_conn, user_id=user_id)
        except Exception as e:
            print(f"Error fetching routines: {e}")
            all_routines = []

        # Filter out pinned routines for "Your Routines" section
        unpinned_routines = [r for r in all_routines if not (r.get('is_favorited', 0) if isinstance(r, dict) else (r[4] if len(r) > 4 else 0))]

        # If there are pinned routines, show them with all routines below
        if favorite_routines:
            # Calculate dynamic height based on unpinned routines count
            unpinned_count = len(unpinned_routines)
            if unpinned_count == 0:
                # No unpinned routines - give pinned section more space
                pinned_height = 350
            elif unpinned_count <= 2:
                # 1-2 unpinned routines - give pinned section more space
                pinned_height = 300
            elif unpinned_count <= 4:
                # 3-4 unpinned routines - balanced space
                pinned_height = 250
            else:
                # 5+ unpinned routines - give less space to pinned
                pinned_height = 200

            # Pinned section
            fav_label = ctk.CTkFrame(content_container, fg_color="transparent")
            fav_label.pack(fill="x", padx=0, pady=(0, 12))
            
            ctk.CTkLabel(fav_label, text="Pinned Routines", 
                         font=ctk.CTkFont(size=14, weight="bold"),
                         text_color=("gray10", "#ffffff")).pack(anchor="w")

            pinned_frame = ctk.CTkFrame(content_container, fg_color="transparent", height=pinned_height)
            pinned_frame.pack(fill="both", expand=False, padx=0, pady=(0, 16))
            pinned_frame.pack_propagate(False)

            pinned_scroll = ctk.CTkScrollableFrame(pinned_frame, fg_color="transparent")
            pinned_scroll.pack(fill="both", expand=True)

            for r in favorite_routines:
                routine_card = ctk.CTkFrame(pinned_scroll, fg_color=("gray95", "#1a1f26"),
                                           corner_radius=12, height=64)
                routine_card.pack(fill="x", pady=8)
                routine_card.pack_propagate(False)

                routine_name = r.get('name', 'Unnamed') if isinstance(r, dict) else r[2]
                routine_id = r.get('id') if isinstance(r, dict) else r[0]
                
                inner = ctk.CTkFrame(routine_card, fg_color="transparent")
                inner.pack(fill="both", expand=True, padx=16, pady=12)

                ctk.CTkLabel(inner, text="⭐ " + routine_name, 
                            font=ctk.CTkFont(size=12, weight="bold"),
                            text_color=("gray10", "#ffffff")).pack(side="left", fill="x", expand=True)

                def make_unpin_command(rid=routine_id):
                    def unpin_routine():
                        try:
                            routinesCrud.favorite_routine(db_conn, rid, user_id)
                            refresh_content()
                        except Exception as e:
                            print(f"Error unpinning routine: {e}")
                    return unpin_routine

                ctk.CTkButton(inner, text="⭐",
                             command=make_unpin_command(),
                             width=45, height=32, font=ctk.CTkFont(size=14, weight="bold"),
                             fg_color=("#fbbf24", "#fbbf24"),
                             text_color=("gray10", "black"),
                             hover_color=("#f59e0b", "#f59e0b"),
                             corner_radius=6).pack(side="right", padx=(8, 0))

                def start_routine(rid=routine_id, rname=routine_name):
                    show_routine_start(parent, db_conn, user, rid, rname)

                ctk.CTkButton(inner, text="Start Workout", command=start_routine,
                             width=100, height=32, font=ctk.CTkFont(size=10, weight="bold"),
                             fg_color=("#2563eb", "#2563eb"),
                             hover_color=("#1d4ed8", "#1d4ed8"),
                             corner_radius=6).pack(side="right", padx=(0, 8))

            # Your routines section - EQUAL HEIGHT
            all_label = ctk.CTkFrame(content_container, fg_color="transparent")
            all_label.pack(fill="x", padx=0, pady=(0, 12))
            
            ctk.CTkLabel(all_label, text="Your Routines", 
                         font=ctk.CTkFont(size=14, weight="bold"),
                         text_color=("gray10", "#ffffff")).pack(anchor="w")

            your_routines_frame = ctk.CTkFrame(content_container, fg_color="transparent")
            your_routines_frame.pack(fill="both", expand=True, padx=0, pady=0)

            render_all_routines(your_routines_frame, all_routines)

        else:
            # No pinned routines - show all routines
            all_label = ctk.CTkFrame(content_container, fg_color="transparent")
            all_label.pack(fill="x", padx=0, pady=(0, 12))
            
            ctk.CTkLabel(all_label, text="Your Routines", 
                         font=ctk.CTkFont(size=14, weight="bold"),
                         text_color=("gray10", "#ffffff")).pack(anchor="w")

            render_all_routines(content_container, all_routines)

    def render_all_routines(parent_frame, routines):
        """Render all routines section - only unpinned routines"""
        routines_frame = ctk.CTkFrame(parent_frame, fg_color="transparent")
        routines_frame.pack(fill="both", expand=True, padx=0, pady=0)

        # Filter out pinned routines
        unpinned_routines = [r for r in routines if not (r.get('is_favorited', 0) if isinstance(r, dict) else (r[4] if len(r) > 4 else 0))]

        if not unpinned_routines:
            empty_frame = ctk.CTkFrame(routines_frame, fg_color="transparent")
            empty_frame.pack(fill="both", expand=True, pady=40)
            ctk.CTkLabel(empty_frame, text="No routines yet", 
                        font=ctk.CTkFont(size=13, weight="bold"),
                        text_color=("gray40", "#808080")).pack()
            ctk.CTkLabel(empty_frame, text="Create one to get started", 
                        text_color=("gray60", "#a0a0a0"), 
                        font=ctk.CTkFont(size=11)).pack(pady=(4, 0))
        else:
            estimated_height = len(unpinned_routines) * 72
            
            if estimated_height > 300:
                routines_scrollable = ctk.CTkScrollableFrame(routines_frame, fg_color="transparent")
                routines_scrollable.pack(fill="both", expand=True)
            else:
                routines_scrollable = ctk.CTkFrame(routines_frame, fg_color="transparent")
                routines_scrollable.pack(fill="both", expand=True)

            for r in unpinned_routines:
                routine_card = ctk.CTkFrame(routines_scrollable, fg_color=("gray95", "#1a1f26"),
                                           corner_radius=12, height=64)
                routine_card.pack(fill="x", pady=8)
                routine_card.pack_propagate(False)

                routine_name = r.get('name', 'Unnamed') if isinstance(r, dict) else r[2]
                routine_id = r.get('id') if isinstance(r, dict) else r[0]
                
                inner = ctk.CTkFrame(routine_card, fg_color="transparent")
                inner.pack(fill="both", expand=True, padx=16, pady=12)

                ctk.CTkLabel(inner, text=routine_name, 
                            font=ctk.CTkFont(size=12, weight="bold"),
                            text_color=("gray10", "#ffffff")).pack(side="left", fill="x", expand=True)

                def make_favorite_toggle(rid=routine_id):
                    def toggle_favorite():
                        try:
                            routinesCrud.favorite_routine(db_conn, rid, user_id)
                            refresh_content()
                        except Exception as e:
                            print(f"Error toggling favorite: {e}")
                    return toggle_favorite

                ctk.CTkButton(inner, text="☆ Pin",
                             command=make_favorite_toggle(),
                             width=80, height=32, font=ctk.CTkFont(size=9, weight="bold"),
                             fg_color=("gray90", "#2a2f36"),
                             text_color=("gray60", "#e0e0e0"),
                             hover_color=("gray80", "#333333"),
                             corner_radius=6).pack(side="right", padx=(8, 0))

                def start_routine(rid=routine_id, rname=routine_name):
                    show_routine_start(parent, db_conn, user, rid, rname)

                ctk.CTkButton(inner, text="Start", command=start_routine,
                             width=80, height=32, font=ctk.CTkFont(size=10, weight="bold"),
                             fg_color=("#2563eb", "#2563eb"),
                             hover_color=("#1d4ed8", "#1d4ed8"),
                             corner_radius=6).pack(side="right", padx=(0, 8))

    # Initial load
    refresh_content()

    return frame


def show_routine_start(parent, db_conn, user, routine_id, routine_name):
    """Display a routine in start mode with workout timer."""
    for w in parent.winfo_children():
        w.destroy()

    frame = ctk.CTkFrame(parent, corner_radius=0, fg_color="transparent")
    frame.pack(fill="both", expand=True, padx=0, pady=0)

    # Define timer state FIRST
    timer_state = {
        "running": False, 
        "paused": False, 
        "elapsed": 0, 
        "rest_remaining": 0, 
        "in_rest": False,
        "timer_job": None
    }

    # Define ALL functions BEFORE creating any UI elements
    def update_timer():
        if timer_state["in_rest"]:
            minutes = timer_state["rest_remaining"] // 60
            seconds = timer_state["rest_remaining"] % 60
        else:
            minutes = timer_state["elapsed"] // 60
            seconds = timer_state["elapsed"] % 60
        
        time_str = f"{minutes:02d}:{seconds:02d}"
        timer_display.configure(text=time_str)

    def tick_timer():
        if timer_state["running"]:
            if not timer_state["paused"]:
                timer_state["elapsed"] += 1
            else:
                if timer_state["in_rest"] and timer_state["rest_remaining"] > 0:
                    timer_state["rest_remaining"] -= 1
                    if timer_state["rest_remaining"] <= 0:
                        timer_state["rest_remaining"] = 0
                        rest_msg.configure(text="Rest complete! Ready?")
            
            update_timer()
            timer_state["timer_job"] = parent.after(1000, tick_timer)

    def start_timer():
        if timer_state["timer_job"]:
            parent.after_cancel(timer_state["timer_job"])
        
        timer_state["running"] = True
        timer_state["paused"] = False
        timer_state["in_rest"] = False
        start_btn.configure(state="disabled")
        pause_btn.configure(state="normal")
        reset_btn.configure(state="normal")
        rest_msg.configure(text="")
        update_timer()
        tick_timer()

    def pause_timer():
        if not timer_state["running"]:
            # Resume mode - restart the timer
            timer_state["running"] = True
            timer_state["paused"] = False
            timer_state["in_rest"] = False
            pause_btn.configure(text="Pause")
            rest_msg.configure(text="")
            tick_timer()
            return
        
        # Pause mode - pause the timer
        timer_state["paused"] = not timer_state["paused"]
        
        if timer_state["paused"]:
            timer_state["in_rest"] = True
            timer_state["rest_remaining"] = 120
            pause_btn.configure(text="Resume")
            rest_msg.configure(text="Take a quick rest between sets")
        else:
            timer_state["in_rest"] = False
            pause_btn.configure(text="Pause")
            rest_msg.configure(text="")
        
        update_timer()

    def reset_timer():
        if timer_state["timer_job"]:
            parent.after_cancel(timer_state["timer_job"])
        
        timer_state["running"] = False
        timer_state["paused"] = False
        timer_state["elapsed"] = 0
        timer_state["rest_remaining"] = 0
        timer_state["in_rest"] = False
        timer_state["timer_job"] = None
        
        update_timer()
        pause_btn.configure(text="Pause")
        start_btn.configure(state="normal")
        pause_btn.configure(state="disabled")
        reset_btn.configure(state="disabled")
        rest_msg.configure(text="")

    def save_workout(elapsed_time):
        """Save workout stats to database"""
        try:
            from datetime import datetime, timedelta
            
            user_id = user.get('id')
            
            cursor = db_conn.cursor()
            cursor.execute("SELECT workouts, total_time, last_login, streak FROM users WHERE id = ?", 
                         (user_id,))
            row = cursor.fetchone()
            
            current_workouts = (row[0] if row[0] else 0) + 1
            current_total_time = (row[1] if row[1] else 0) + elapsed_time
            
            today = datetime.now().date()
            last_login = row[2] if row else None
            current_streak = row[3] if row and len(row) > 3 else 1
            
            if last_login:
                try:
                    last_login_date = datetime.strptime(last_login, "%Y-%m-%d").date()
                    yesterday = today - timedelta(days=1)
                    
                    if last_login_date == yesterday:
                        current_streak = (row[3] if row and len(row) > 3 else 0) + 1
                    elif last_login_date != today:
                        current_streak = 1
                except:
                    current_streak = 1
            
            cursor.execute("""
                UPDATE users 
                SET workouts = ?, total_time = ?, streak = ?, last_login = ?
                WHERE id = ?
            """, (current_workouts, current_total_time, current_streak, today.strftime("%Y-%m-%d"), user_id))
            
            db_conn.commit()
            
            user['workouts'] = current_workouts
            user['total_time'] = current_total_time
            user['streak'] = current_streak
            user['last_login'] = today.strftime("%Y-%m-%d")
            
            root = parent.winfo_toplevel()
            if hasattr(root, 'app_instance'):
                root.app_instance._refresh_sidebar()
            
            for w in parent.winfo_children():
                w.destroy()
            create_home(parent, db_conn, user)
            
        except Exception as e:
            print(f"Error saving workout: {e}")
            import traceback
            traceback.print_exc()

    def finish_workout():
        """Save workout stats and return to home"""
        if timer_state["timer_job"]:
            parent.after_cancel(timer_state["timer_job"])
        
        if timer_state["elapsed"] < 1800:
            minutes = timer_state["elapsed"] // 60
            remaining = 30 - minutes
            
            timer_state["running"] = False
            pause_btn.configure(text="Resume")
            start_btn.configure(state="disabled")
            reset_btn.configure(state="normal")
            
            error_dialog = ctk.CTkToplevel(parent.winfo_toplevel())
            error_dialog.title("Workout Too Short")
            error_dialog.geometry("420x220")
            error_dialog.resizable(False, False)
            error_dialog.grab_set()
            
            error_dialog.update_idletasks()
            root = parent.winfo_toplevel()
            root.update_idletasks()
            x = root.winfo_x() + (root.winfo_width() // 2) - 210
            y = root.winfo_y() + (root.winfo_height() // 2) - 110
            error_dialog.geometry(f"420x220+{x}+{y}")
            
            error_frame = ctk.CTkFrame(error_dialog, fg_color=("gray95", "#1a1f26"), corner_radius=0)
            error_frame.pack(fill="both", expand=True, padx=0, pady=0)
            
            header = ctk.CTkFrame(error_frame, fg_color=("gray85", "#2a3a4a"), corner_radius=0)
            header.pack(fill="x", padx=0, pady=0)
            
            ctk.CTkLabel(header, text="⏱️ Workout Too Short",
                        font=ctk.CTkFont(size=14, weight="bold"),
                        text_color=("gray10", "#ff6b6b")).pack(pady=12, padx=20)
            
            content = ctk.CTkFrame(error_frame, fg_color="transparent")
            content.pack(fill="both", expand=True, padx=24, pady=20)
            
            ctk.CTkLabel(content, text=f"A proper workout lasts more than 30 minutes.",
                        font=ctk.CTkFont(size=11, weight="bold"),
                        text_color=("gray20", "#e0e0e0")).pack(anchor="w", pady=(0, 8))
            
            ctk.CTkLabel(content, text=f"You've exercised for {minutes} minutes.",
                        font=ctk.CTkFont(size=10),
                        text_color=("gray60", "#a0a0a0")).pack(anchor="w", pady=(0, 4))
            
            ctk.CTkLabel(content, text=f"Continue for {remaining} more minutes to complete your workout.",
                        font=ctk.CTkFont(size=10),
                        text_color=("gray60", "#a0a0a0")).pack(anchor="w", pady=(0, 12))
            
            button_frame = ctk.CTkFrame(content, fg_color="transparent")
            button_frame.pack(fill="x", pady=(8, 0))
            
            def finish_anyway():
                error_dialog.destroy()
                save_workout(timer_state["elapsed"])
            
            ctk.CTkButton(button_frame, text="Continue", command=error_dialog.destroy,
                         width=90, height=36, corner_radius=6,
                         font=ctk.CTkFont(size=10, weight="bold"),
                         fg_color=("gray80", "#2a3a4a"),
                         text_color=("gray20", "#e0e0e0"),
                         hover_color=("gray70", "#3a4a5a")).pack(side="left", padx=(0, 8))
            
            ctk.CTkButton(button_frame, text="Still Finish", command=finish_anyway,
                         width=90, height=36, corner_radius=6,
                         font=ctk.CTkFont(size=10, weight="bold"),
                         fg_color=("#ef4444", "#ef4444"),
                         text_color=("white", "white"),
                         hover_color=("#dc2626", "#dc2626")).pack(side="left")
            
            return
        
        save_workout(timer_state["elapsed"])

    # Header
    header = ctk.CTkFrame(frame, fg_color="transparent", height=70)
    header.pack(fill="x", padx=32, pady=(24, 20))
    header.pack_propagate(False)

    def back_to_home():
        if timer_state["timer_job"]:
            parent.after_cancel(timer_state["timer_job"])
        for w in parent.winfo_children():
            w.destroy()
        create_home(parent, db_conn, user)

    ctk.CTkButton(header, text="← Back", command=back_to_home,
                 width=80, height=36, corner_radius=6,
                 font=ctk.CTkFont(size=10, weight="bold"),
                 fg_color=("gray90", "#2a2f36"),
                 text_color=("gray20", "#e0e0e0"),
                 hover_color=("gray80", "#333333")).pack(side="left", padx=(0, 12))
    
    ctk.CTkLabel(header, text=f"▶ {routine_name}", 
                 font=ctk.CTkFont(size=20, weight="bold"),
                 text_color=("gray10", "#ffffff")).pack(side="left")

    # Content area
    content_scroll = ctk.CTkScrollableFrame(frame, fg_color="transparent")
    content_scroll.pack(fill="both", expand=True, padx=32, pady=(0, 32))

    # Timer section
    timer_container = ctk.CTkFrame(content_scroll, fg_color=("gray95", "#1a1f26"), corner_radius=16)
    timer_container.pack(fill="x", pady=(0, 24))

    timer_inner = ctk.CTkFrame(timer_container, fg_color="transparent")
    timer_inner.pack(fill="x", expand=True, padx=28, pady=32)

    ctk.CTkLabel(timer_inner, text="Workout Timer", 
                 font=ctk.CTkFont(size=14, weight="bold"),
                 text_color=("gray10", "#ffffff")).pack(anchor="w", pady=(0, 16))

    timer_display = ctk.CTkLabel(timer_inner, text="00:00", 
                                font=ctk.CTkFont(size=56, weight="bold"),
                                text_color=("#2563eb", "#2563eb"))
    timer_display.pack(pady=20)

    # Button frame
    btn_frame = ctk.CTkFrame(timer_inner, fg_color="transparent")
    btn_frame.pack(pady=20, fill="x")

    start_btn = ctk.CTkButton(btn_frame, text="Start", command=start_timer,
                             width=80, height=40, corner_radius=8,
                             font=ctk.CTkFont(size=11, weight="bold"),
                             fg_color=("#2563eb", "#2563eb"),
                             hover_color=("#1d4ed8", "#1d4ed8"))
    start_btn.pack(side="left", padx=4)

    pause_btn = ctk.CTkButton(btn_frame, text="Pause", command=pause_timer,
                             width=80, height=40, corner_radius=8,
                             font=ctk.CTkFont(size=11, weight="bold"),
                             fg_color=("gray90", "#2a2f36"),
                             text_color=("gray20", "#e0e0e0"),
                             hover_color=("gray80", "#333333"),
                             state="disabled")
    pause_btn.pack(side="left", padx=4)

    reset_btn = ctk.CTkButton(btn_frame, text="Reset", command=reset_timer,
                             width=80, height=40, corner_radius=8,
                             font=ctk.CTkFont(size=11, weight="bold"),
                             fg_color=("#dc2626", "#dc2626"),
                             hover_color=("#b91c1c", "#b91c1c"),
                             state="disabled")
    reset_btn.pack(side="left", padx=4)

    finish_btn = ctk.CTkButton(btn_frame, text="Finish Workout", command=finish_workout,
                              width=100, height=40, corner_radius=8,
                              font=ctk.CTkFont(size=11, weight="bold"),
                              fg_color=("#16a34a", "#16a34a"),
                              hover_color=("#15803d", "#15803d"))
    finish_btn.pack(side="left", padx=4)

    rest_msg = ctk.CTkLabel(timer_inner, text="",
                           font=ctk.CTkFont(size=10),
                           text_color=("gray60", "#a0a0a0"))
    rest_msg.pack(pady=(12, 0))

    # Routine details
    ctk.CTkLabel(content_scroll, text="Routine Details",
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color=("gray10", "#ffffff")).pack(anchor="w", pady=(20, 12), padx=0)

    content_container = ctk.CTkFrame(content_scroll, fg_color=("gray95", "#1a1f26"), corner_radius=12)
    content_container.pack(fill="both", expand=True)

    content_box = ctk.CTkTextbox(content_container, corner_radius=8,
                                font=ctk.CTkFont(size=11),
                                fg_color=("gray95", "#1a1f26"),
                                text_color=("gray20", "#e0e0e0"))
    content_box.pack(fill="both", expand=True, padx=16, pady=16)
    content_box.configure(state="normal")

    try:
        from crud import routinesCrud
        routine_data = routinesCrud.get_routine(db_conn, routine_id)
        if routine_data and routine_data.get('notes'):
            content_box.insert("1.0", routine_data['notes'])
        else:
            content_box.insert("1.0", "No routine details added.")
    except Exception as e:
        content_box.insert("1.0", f"Error loading routine: {e}")

    content_box.configure(state="disabled")

    return frame