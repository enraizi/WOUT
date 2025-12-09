import customtkinter as ctk
import random

def create_sidebar(parent, on_nav=None, is_logged_in=False, current_page=None, db=None, user_id=None):
    """Create sidebar with navigation"""
    
    # Define quotes list
    quotes = [
        ("The only way to do great work is to love what you do.", "Steve Jobs"),
        ("Believe you can and you're halfway there.", "Theodore Roosevelt"),
        ("Don't watch the clock; do what it does. Keep going.", "Sam Levenson"),
        ("The future belongs to those who believe in the beauty of their dreams.", "Eleanor Roosevelt"),
        ("It is during our darkest moments that we must focus to see the light.", "Aristotle"),
        ("The only impossible journey is the one you never begin.", "Tony Robbins"),
        ("Success is not final, failure is not fatal.", "Winston Churchill"),
        ("You are never too old to set another goal or to dream a new dream.", "C.S. Lewis"),
        ("The best time to plant a tree was 20 years ago. The second best time is now.", "Chinese Proverb"),
        ("Your limitation—it's only your imagination.", "Unknown"),
        ("Great things never come from comfort zones.", "Unknown"),
        ("Success doesn't just find you. You have to go out and get it.", "Unknown"),
        ("The harder you work for something, the greater you'll feel when you achieve it.", "Unknown"),
        ("Dream bigger. Do bigger.", "Unknown"),
        ("Don't stop when you're tired. Stop when you're done.", "Unknown"),
    ]
    
    sidebar_frame = ctk.CTkFrame(parent, fg_color=("gray96", "#0d1b2a"), corner_radius=0)
    sidebar_frame.pack(fill="both", expand=True, padx=0, pady=0)

    if not is_logged_in:
        # Login state - premium welcome section
        # Top gradient bar
        top_bar = ctk.CTkFrame(sidebar_frame, fg_color=("gray70", "#ffd700"), height=4)
        top_bar.pack(fill="x", padx=0, pady=0)
        
        # Welcome section with icon
        welcome_container = ctk.CTkFrame(sidebar_frame, fg_color="transparent")
        welcome_container.pack(fill="both", expand=True, padx=0, pady=0)
        
        welcome_frame = ctk.CTkFrame(welcome_container, fg_color="transparent")
        welcome_frame.pack(fill="x", padx=14, pady=(12, 0))
        
        # Logo emoji
        ctk.CTkLabel(welcome_frame, text="💪", 
                     font=ctk.CTkFont(size=48, weight="bold")).pack(anchor="w", pady=(0, 6))
        
        ctk.CTkLabel(welcome_frame, text="Welcome to", 
                     font=ctk.CTkFont(size=16, weight="bold"),
                     text_color=("gray40", "#90caf9")).pack(anchor="w", pady=(0, 2))
        
        ctk.CTkLabel(welcome_frame, text="WOUT", 
                     font=ctk.CTkFont(size=40, weight="bold"),
                     text_color=("gray10", "#ffd700")).pack(anchor="w", pady=(0, 16))
        
        # Features list
        features_label = ctk.CTkLabel(welcome_frame, text="Get Started", 
                                     font=ctk.CTkFont(size=15, weight="bold"),
                                     text_color=("gray50", "#90caf9"))
        features_label.pack(anchor="w", pady=(0, 10))
        
        features = [
            ("✓", "Track workouts", "Build habits"),
            ("✓", "Analyze progress", "See improvements"),
            ("✓", "Stay motivated", "Reach goals"),
        ]
        
        for icon, text, subtext in features:
            feature_row = ctk.CTkFrame(welcome_frame, fg_color="transparent")
            feature_row.pack(fill="x", pady=4)
            
            ctk.CTkLabel(feature_row, text=icon, 
                        font=ctk.CTkFont(size=14, weight="bold"),
                        text_color=("gray20", "#ffd700")).pack(side="left", padx=(0, 8))
            
            text_frame = ctk.CTkFrame(feature_row, fg_color="transparent")
            text_frame.pack(side="left", fill="x", expand=True)
            
            ctk.CTkLabel(text_frame, text=text, 
                        font=ctk.CTkFont(size=13, weight="bold"),
                        text_color=("gray30", "#ffffff")).pack(anchor="w")
            
            ctk.CTkLabel(text_frame, text=subtext, 
                        font=ctk.CTkFont(size=11),
                        text_color=("gray60", "#a0a0a0")).pack(anchor="w")
        
        # Spacer
        spacer = ctk.CTkFrame(welcome_container, fg_color="transparent")
        spacer.pack(fill="both", expand=True)
        
        # Bottom info section
        bottom_frame = ctk.CTkFrame(welcome_container, fg_color="transparent")
        bottom_frame.pack(fill="x", padx=14, pady=8)
        
        sep_line = ctk.CTkFrame(bottom_frame, height=2, fg_color=("gray70", "#ffd700"))
        sep_line.pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(bottom_frame, text="Login Required", 
                     font=ctk.CTkFont(size=14, weight="bold"),
                     text_color=("gray20", "#ffd700")).pack(anchor="w", pady=(0, 4))
        
        ctk.CTkLabel(bottom_frame, text="Sign in to access your", 
                     font=ctk.CTkFont(size=11),
                     text_color=("gray60", "#a0a0a0")).pack(anchor="w")
        
        ctk.CTkLabel(bottom_frame, text="workouts and analytics", 
                     font=ctk.CTkFont(size=11),
                     text_color=("gray60", "#a0a0a0")).pack(anchor="w")
        
        # Version footer
        version_footer = ctk.CTkFrame(sidebar_frame, fg_color="transparent")
        version_footer.pack(fill="x", padx=12, pady=6)
        
        version_border = ctk.CTkFrame(version_footer, fg_color=("gray70", "#ffd700"), corner_radius=6)
        version_border.pack(fill="x", padx=0, pady=0)
        
        version_inner = ctk.CTkFrame(version_border, fg_color=("gray85", "#0d1b2a"), corner_radius=5)
        version_inner.pack(fill="x", padx=1, pady=1, ipadx=6, ipady=4)
        
        version_content = ctk.CTkFrame(version_inner, fg_color="transparent")
        version_content.pack(expand=True)
        
        ctk.CTkLabel(version_content, text="WOUT v1.0", 
                     font=ctk.CTkFont(size=9, weight="bold"),
                     text_color=("gray20", "#ffd700")).pack()

        return sidebar_frame

    # Logged in state - enhanced navigation
    # Top gradient bar
    top_bar = ctk.CTkFrame(sidebar_frame, fg_color=("gray70", "#ffd700"), height=4)
    top_bar.pack(fill="x", padx=0, pady=0)

    # Header section
    header_frame = ctk.CTkFrame(sidebar_frame, fg_color="transparent")
    header_frame.pack(fill="x", padx=12, pady=(14, 8))
    
    ctk.CTkLabel(header_frame, text="WOUT", 
                 font=ctk.CTkFont(size=16, weight="bold"),
                 text_color=("gray10", "#ffd700")).pack(anchor="w", pady=(0, 2))
    
    ctk.CTkLabel(header_frame, text="Navigation", 
                 font=ctk.CTkFont(size=10),
                 text_color=("gray50", "#90caf9")).pack(anchor="w")

    # Separator
    sep = ctk.CTkFrame(header_frame, height=2, fg_color=("gray70", "#ffd700"))
    sep.pack(fill="x", pady=(6, 0))

    # Navigation section - premium buttons
    nav_frame = ctk.CTkFrame(sidebar_frame, fg_color="transparent")
    nav_frame.pack(fill="x", padx=8, pady=12)

    nav_items = [
        ("🏠", "Home", "home"),
        ("⚙️", "Routines", "routines"),
        ("👤", "Profile", "profile"),
    ]

    for emoji, label, key in nav_items:
        is_active = current_page == key
        
        nav_btn = ctk.CTkButton(
            nav_frame, 
            text=f"{emoji}  {label}",
            command=lambda nav_key=key: on_nav(nav_key) if on_nav else None,
            fg_color=("gray80", "#1a2940") if is_active else ("gray88", "#0d1b2a"),
            text_color=("gray10", "#ffd700") if is_active else ("gray50", "#90caf9"),
            hover_color=("gray70", "#2a3a4a"),
            corner_radius=8,
            height=42,
            font=ctk.CTkFont(size=11, weight="bold"),
            border_width=2 if is_active else 0,
            border_color=("gray70", "#ffd700") if is_active else ("gray88", "#0d1b2a")
        )
        nav_btn.pack(fill="x", padx=0, pady=4)

    # Middle frame with stats (no scrolling needed)
    middle_frame = ctk.CTkFrame(sidebar_frame, fg_color="transparent")
    middle_frame.pack(fill="both", expand=True, padx=0, pady=8)

    # Stats section
    stats_frame = ctk.CTkFrame(middle_frame, fg_color="transparent")
    stats_frame.pack(fill="both", expand=True, padx=12, pady=0)
    
    ctk.CTkLabel(stats_frame, text="📊 Stats", 
                 font=ctk.CTkFont(size=11, weight="bold"),
                 text_color=("gray40", "#90caf9")).pack(anchor="w", pady=(0, 8))
    
    # Fetch user stats from database
    workouts_count = "0"
    streak_count = "0"
    total_time = "0 min"
    
    try:
        if user_id and db:
            cursor = db.cursor()
            cursor.execute("SELECT workouts, streak, total_time FROM users WHERE id = ?", (user_id,))
            stats_row = cursor.fetchone()
            if stats_row:
                workouts_count = str(stats_row[0] if stats_row[0] else 0)
                streak_count = str(stats_row[1] if stats_row[1] else 0)
                total_seconds = stats_row[2] if stats_row[2] else 0
                
                hours = total_seconds // 3600
                minutes = (total_seconds % 3600) // 60
                if hours > 0:
                    total_time = f"{hours}h {minutes}m"
                else:
                    total_time = f"{minutes}m" if minutes > 0 else "0 min"
    except Exception as e:
        print(f"Error fetching stats: {e}")
    
    stat_items = [
        ("     🏋️", "Workouts", workouts_count),
        ("🔥", "Streak", f"{streak_count} days"),
        ("⏱️", "Time", total_time),
    ]
    
    for emoji, title, value in stat_items:
        stat_card = ctk.CTkFrame(stats_frame, fg_color=("gray88", "#0d1b2a"), corner_radius=6)
        stat_card.pack(fill="x", pady=2)
        
        stat_border = ctk.CTkFrame(stat_card, fg_color=("gray70", "#ffd700"), corner_radius=6)
        stat_border.pack(fill="x", padx=1, pady=1)
        
        stat_inner = ctk.CTkFrame(stat_border, fg_color=("gray88", "#0d1b2a"), corner_radius=5)
        stat_inner.pack(fill="both", expand=True, padx=0, pady=0, ipadx=8, ipady=6)
        
        # Emoji centered
        ctk.CTkLabel(stat_inner, text=emoji, 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="center", pady=(1, 2))
        
        # Title centered
        ctk.CTkLabel(stat_inner, text=title, 
                    font=ctk.CTkFont(size=10, weight="bold"),
                    text_color=("gray50", "#90caf9")).pack(anchor="center")
        
        # Value centered
        ctk.CTkLabel(stat_inner, text=value, 
                    font=ctk.CTkFont(size=11, weight="bold"),
                    text_color=("gray30", "#ffd700")).pack(anchor="center")

    # Bottom separator
    bottom_sep = ctk.CTkFrame(sidebar_frame, height=2, fg_color=("gray70", "#ffd700"))
    bottom_sep.pack(fill="x", padx=8, pady=(4, 6))

    # Logout button
    logout_btn = ctk.CTkButton(
        sidebar_frame, 
        text="🚪 Logout",
        command=lambda: on_nav("logout") if on_nav else None,
        fg_color=("#ef4444", "#ef4444"),
        text_color=("white", "white"),
        hover_color=("#dc2626", "#dc2626"),
        corner_radius=6,
        height=40,
        font=ctk.CTkFont(size=10, weight="bold")
    )
    logout_btn.pack(fill="x", padx=8, pady=(0, 6))

    # Version footer
    version_footer = ctk.CTkFrame(sidebar_frame, fg_color="transparent")
    version_footer.pack(fill="x", padx=12, pady=6)
    
    version_border = ctk.CTkFrame(version_footer, fg_color=("gray70", "#ffd700"), corner_radius=6)
    version_border.pack(fill="x", padx=0, pady=0)
    
    version_inner = ctk.CTkFrame(version_border, fg_color=("gray85", "#0d1b2a"), corner_radius=5)
    version_inner.pack(fill="x", padx=1, pady=1, ipadx=6, ipady=4)
    
    version_content = ctk.CTkFrame(version_inner, fg_color="transparent")
    version_content.pack(expand=True)
    
    ctk.CTkLabel(version_content, text="WOUT v1.0", 
                 font=ctk.CTkFont(size=9, weight="bold"),
                 text_color=("gray20", "#ffd700")).pack()

    return sidebar_frame