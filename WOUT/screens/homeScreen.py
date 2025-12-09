# ...existing code...
import customtkinter as ctk
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from crud import routinesCrud

def create_home(parent, db_conn, user=None):
    frame = ctk.CTkFrame(parent, corner_radius=0, fg_color="transparent")
    frame.pack(fill="both", expand=True, padx=0, pady=0)

    # Header section
    header = ctk.CTkFrame(frame, fg_color=("gray88", "#1a1a1a"), height=80, corner_radius=0)
    header.pack(fill="x", padx=0, pady=0)
    header.pack_propagate(False)

    if not user:
        ctk.CTkLabel(header, text="Error: No user data.", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=20)
        return frame

    name = user.get("display_name") if isinstance(user, dict) else None
    username = user.get("username") if isinstance(user, dict) else str(user)
    title_text = f"Welcome back, {name or username}!"
    ctk.CTkLabel(header, text=title_text, font=ctk.CTkFont(size=18, weight="bold")).pack(pady=(16, 8))
    ctk.CTkLabel(header, text="Let's get to work! 💪", font=ctk.CTkFont(size=12), text_color="gray").pack(pady=(0, 12))

    # Content area - Main container
    main_content = ctk.CTkFrame(frame, fg_color="transparent", corner_radius=0)
    main_content.pack(fill="both", expand=True, padx=0, pady=0)

    # Your Routines section
    routines_label_frame = ctk.CTkFrame(main_content, fg_color="transparent")
    routines_label_frame.pack(fill="x", padx=20, pady=(20, 12))
    
    ctk.CTkLabel(routines_label_frame, text="Your Routines", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w")

    routines_container = ctk.CTkFrame(main_content, fg_color=("white", "#1f1f1f"), corner_radius=12)
    routines_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    # Add subtle border effect with frame
    border_frame = ctk.CTkFrame(routines_container, fg_color=("gray75", "#3a3a3a"), corner_radius=12)
    border_frame.pack(fill="both", expand=True, padx=1, pady=1)

    routines_inner = ctk.CTkFrame(border_frame, fg_color=("white", "#1f1f1f"), corner_radius=11)
    routines_inner.pack(fill="both", expand=True, padx=0, pady=0)

    user_id = user.get("id") if isinstance(user, dict) else None
    
    try:
        routines = routinesCrud.get_routines(db_conn, user_id=user_id)
    except Exception as e:
        print(f"Error fetching routines: {e}")
        routines = []

    if not routines:
        # Empty state
        empty_frame = ctk.CTkFrame(routines_inner, fg_color="transparent")
        empty_frame.pack(fill="both", expand=True, pady=40)
        ctk.CTkLabel(empty_frame, text="📝 No routines yet", font=ctk.CTkFont(size=12, weight="bold")).pack()
        ctk.CTkLabel(empty_frame, text="Create one to get started!", text_color="gray", font=ctk.CTkFont(size=11)).pack(pady=(4, 0))
    else:
        # Determine if we need scrolling based on number of routines
        estimated_height = len(routines) * 80
        
        # Use scrollable frame only if content might exceed available space
        if estimated_height > 400:
            routines_scrollable = ctk.CTkScrollableFrame(routines_inner, fg_color="transparent", corner_radius=0)
            routines_scrollable.pack(fill="both", expand=True, padx=16, pady=16)
        else:
            # Use regular frame if content fits
            routines_scrollable = ctk.CTkFrame(routines_inner, fg_color="transparent", corner_radius=0)
            routines_scrollable.pack(fill="both", expand=True, padx=16, pady=16)

        for r in routines:
            routine_card = ctk.CTkFrame(routines_scrollable, fg_color=("gray92", "#2a2a2a"), corner_radius=10)
            routine_card.pack(fill="x", padx=0, pady=6)

            # Add subtle border to card
            card_border = ctk.CTkFrame(routine_card, fg_color=("gray70", "#3a3a3a"), corner_radius=10)
            card_border.pack(fill="x", expand=False, padx=1, pady=1)

            card_inner = ctk.CTkFrame(card_border, fg_color=("gray92", "#2a2a2a"), corner_radius=9)
            card_inner.pack(fill="x", expand=True, padx=0, pady=0)

            routine_name = r.get('name', 'Unnamed')
            
            # Header row with name and button
            header_row = ctk.CTkFrame(card_inner, fg_color="transparent")
            header_row.pack(fill="x", padx=12, pady=10)

            name_label = ctk.CTkLabel(header_row, text=routine_name, font=ctk.CTkFont(size=12, weight="bold"), anchor="w")
            name_label.pack(side="left", fill="x", expand=True)

            def start_routine(routine_id=r.get('id'), routine_name=routine_name):
                show_routine_start(parent, db_conn, user, routine_id, routine_name)

            ctk.CTkButton(header_row, text="▶ Start", command=start_routine, width=90, height=32, 
                         font=ctk.CTkFont(size=10, weight="bold"), corner_radius=6).pack(side="right", padx=(12, 0))

    return frame


def show_routine_start(parent, db_conn, user, routine_id, routine_name):
    """Display a routine in start mode with workout timer."""
    for w in parent.winfo_children():
        w.destroy()

    frame = ctk.CTkFrame(parent, corner_radius=0, fg_color="transparent")
    frame.pack(fill="both", expand=True, padx=0, pady=0)

    # Header
    header = ctk.CTkFrame(frame, fg_color=("gray88", "#1a1a1a"), height=70, corner_radius=0)
    header.pack(fill="x", padx=0, pady=0)
    header.pack_propagate(False)

    def back_to_home():
        from screens import homeScreen
        # Cancel any pending timer
        if timer_state["timer_job"]:
            parent.after_cancel(timer_state["timer_job"])
        for w in parent.winfo_children():
            w.destroy()
        homeScreen.create_home(parent, db_conn, user)

    ctk.CTkButton(header, text="← Back to Home", command=back_to_home, width=120, height=36, 
                 corner_radius=6, font=ctk.CTkFont(size=11, weight="bold")).pack(side="left", padx=16, pady=17)
    ctk.CTkLabel(header, text=f"▶ {routine_name}", font=ctk.CTkFont(size=16, weight="bold")).pack(side="left", padx=12)

    # Content area
    content_scroll = ctk.CTkScrollableFrame(frame, fg_color="transparent", corner_radius=0)
    content_scroll.pack(fill="both", expand=True, padx=0, pady=0)

    content_area = ctk.CTkFrame(content_scroll, fg_color="transparent")
    content_area.pack(fill="both", expand=True, padx=20, pady=20)

    # Timer section
    timer_container = ctk.CTkFrame(content_area, fg_color=("white", "#1f1f1f"), corner_radius=12)
    timer_container.pack(fill="x", pady=(0, 20))

    timer_border = ctk.CTkFrame(timer_container, fg_color=("gray75", "#3a3a3a"), corner_radius=12)
    timer_border.pack(fill="both", expand=True, padx=1, pady=1)

    timer_inner = ctk.CTkFrame(timer_border, fg_color=("white", "#1f1f1f"), corner_radius=11)
    timer_inner.pack(fill="both", expand=True, padx=0, pady=0, ipadx=20, ipady=20)

    ctk.CTkLabel(timer_inner, text="Workout Timer", font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w")

    # Timer display
    timer_display = ctk.CTkLabel(timer_inner, text="00:00", font=ctk.CTkFont(size=48, weight="bold"), 
                                 text_color=("gray20", "#2563eb"))
    timer_display.pack(pady=20)

    # Timer state management
    timer_state = {
        "running": False, 
        "paused": False, 
        "elapsed": 0, 
        "rest_remaining": 0, 
        "in_rest": False,
        "timer_job": None
    }

    def update_timer():
        """Update timer display"""
        if timer_state["in_rest"]:
            minutes = timer_state["rest_remaining"] // 60
            seconds = timer_state["rest_remaining"] % 60
        else:
            minutes = timer_state["elapsed"] // 60
            seconds = timer_state["elapsed"] % 60
        
        time_str = f"{minutes:02d}:{seconds:02d}"
        timer_display.configure(text=time_str)

    def tick_timer():
        """Tick the timer - only schedule one update at a time"""
        if timer_state["running"]:
            if not timer_state["paused"]:
                # Workout mode - increment elapsed
                timer_state["elapsed"] += 1
            else:
                # Rest mode - decrement rest time
                if timer_state["in_rest"] and timer_state["rest_remaining"] > 0:
                    timer_state["rest_remaining"] -= 1
                    if timer_state["rest_remaining"] <= 0:
                        timer_state["rest_remaining"] = 0
                        rest_msg.configure(text="Rest complete! Ready to continue? 💪")
            
            update_timer()
            # Schedule next tick in exactly 1000ms
            timer_state["timer_job"] = parent.after(1000, tick_timer)

    def start_timer():
        """Start the workout timer"""
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
        """Pause and start rest period"""
        if not timer_state["running"]:
            return
        
        timer_state["paused"] = not timer_state["paused"]
        
        if timer_state["paused"]:
            # Enter rest mode
            timer_state["in_rest"] = True
            timer_state["rest_remaining"] = 120  # 2 minutes in seconds
            pause_btn.configure(text="Resume")
            rest_msg.configure(text="💡 Optimal rest is between 1-2 minutes per set", 
                              text_color=("gray60", "#9ca3af"))
        else:
            # Resume workout
            timer_state["in_rest"] = False
            pause_btn.configure(text="Pause")
            rest_msg.configure(text="")
        
        update_timer()

    def reset_timer():
        """Reset the timer"""
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

    # Control buttons
    btn_frame = ctk.CTkFrame(timer_inner, fg_color="transparent")
    btn_frame.pack(pady=12)

    start_btn = ctk.CTkButton(btn_frame, text="▶ Start", command=start_timer, width=90, height=36, 
                             corner_radius=6, font=ctk.CTkFont(size=11, weight="bold"))
    start_btn.pack(side="left", padx=6)

    pause_btn = ctk.CTkButton(btn_frame, text="⏸ Pause", command=pause_timer, width=90, height=36, 
                             fg_color=("gray80", "#2a2a2a"), text_color=("black", "white"),
                             hover_color=("gray65", "#3a3a3a"), corner_radius=6, 
                             font=ctk.CTkFont(size=11, weight="bold"), state="disabled")
    pause_btn.pack(side="left", padx=6)

    reset_btn = ctk.CTkButton(btn_frame, text="🔄 Reset", command=reset_timer, width=90, height=36,
                             fg_color=("#ef4444"), hover_color=("#dc2626"), corner_radius=6,
                             font=ctk.CTkFont(size=11, weight="bold"), state="disabled")
    reset_btn.pack(side="left", padx=6)

    # Rest message
    rest_msg = ctk.CTkLabel(timer_inner, text="", font=ctk.CTkFont(size=10), wraplength=400)
    rest_msg.pack(pady=(8, 0))

    # Routine content section
    ctk.CTkLabel(content_area, text="Routine Details", font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", pady=(0, 12))

    # Content box with border
    content_container = ctk.CTkFrame(content_area, fg_color=("white", "#1f1f1f"), corner_radius=10)
    content_container.pack(fill="both", expand=True, pady=(0, 12))

    border = ctk.CTkFrame(content_container, fg_color=("gray75", "#3a3a3a"), corner_radius=10)
    border.pack(fill="both", expand=True, padx=1, pady=1)

    content_inner = ctk.CTkFrame(border, fg_color=("white", "#1f1f1f"), corner_radius=9)
    content_inner.pack(fill="both", expand=True, padx=0, pady=0)

    content_box = ctk.CTkTextbox(content_inner, corner_radius=8, font=ctk.CTkFont(size=11))
    content_box.pack(fill="both", expand=True, padx=12, pady=12)
    content_box.configure(state="normal")

    try:
        routine_data = routinesCrud.get_routine(db_conn, routine_id)
        if routine_data and routine_data.get('notes'):
            content_box.insert("1.0", routine_data['notes'])
        else:
            content_box.insert("1.0", "No routine details added yet.")
    except Exception as e:
        content_box.insert("1.0", f"Error loading routine: {e}")

    content_box.configure(state="disabled")

    return frame
# ...existing code...