# ...existing code...
import customtkinter as ctk
from crud import routinesCrud

def create_routines(parent, db_conn, user=None):
    frame = ctk.CTkFrame(parent, corner_radius=0, fg_color="transparent")
    frame.pack(fill="both", expand=True, padx=0, pady=0)

    # Header section
    header = ctk.CTkFrame(frame, fg_color=("gray88", "#1a1a1a"), height=80, corner_radius=0)
    header.pack(fill="x", padx=0, pady=0)
    header.pack_propagate(False)

    ctk.CTkLabel(header, text="Routines", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=(16, 8))
    ctk.CTkLabel(header, text="Manage and create your workout routines", font=ctk.CTkFont(size=12), text_color="gray").pack(pady=(0, 12))

    if not user:
        ctk.CTkLabel(frame, text="Please log in to manage routines.").pack()
        return frame

    user_id = user.get("id") if isinstance(user, dict) else None
    if not user_id:
        ctk.CTkLabel(frame, text="Error: Invalid user data.").pack()
        return frame

    # Container for list and detail/create panels
    main_container = ctk.CTkFrame(frame, fg_color="transparent", corner_radius=0)
    main_container.pack(fill="both", expand=True, padx=0, pady=0)

    # Left: List of routines with scrollbar (persistent)
    list_frame = ctk.CTkFrame(main_container, fg_color=("white", "#1f1f1f"), corner_radius=0)
    list_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)

    # Border for list frame
    list_border = ctk.CTkFrame(list_frame, fg_color=("gray75", "#3a3a3a"), corner_radius=12)
    list_border.pack(fill="both", expand=True, padx=1, pady=1)

    list_inner = ctk.CTkFrame(list_border, fg_color=("white", "#1f1f1f"), corner_radius=11)
    list_inner.pack(fill="both", expand=True, padx=0, pady=0)

    ctk.CTkLabel(list_inner, text="My Routines", font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", padx=16, pady=(16, 12))

    # Scrollable frame for routines list
    routines_scrollable = ctk.CTkScrollableFrame(list_inner, fg_color="transparent", corner_radius=0)
    routines_scrollable.pack(fill="both", expand=True, padx=16, pady=(0, 16))

    # Right: Content area (switches between create and detail views)
    content_container = ctk.CTkFrame(main_container, fg_color=("white", "#1f1f1f"), corner_radius=0, width=360)
    content_container.pack_propagate(False)
    content_container.pack(side="right", fill="y", padx=(0, 20), pady=20)

    # Border for content frame
    content_border = ctk.CTkFrame(content_container, fg_color=("gray75", "#3a3a3a"), corner_radius=12)
    content_border.pack(fill="both", expand=True, padx=1, pady=1)

    content_inner = ctk.CTkFrame(content_border, fg_color=("white", "#1f1f1f"), corner_radius=11)
    content_inner.pack(fill="both", expand=True, padx=0, pady=0)

    def show_create_view():
        """Show the create new routine panel"""
        for w in content_inner.winfo_children():
            w.destroy()

        ctk.CTkLabel(content_inner, text="New Routine", font=ctk.CTkFont(size=13, weight="bold")).pack(pady=(16, 12), padx=16)

        routine_name_var = ctk.StringVar()
        name_entry = ctk.CTkEntry(content_inner, placeholder_text="Routine name", textvariable=routine_name_var, width=300)
        name_entry.pack(pady=(0, 12), padx=16)

        create_status = ctk.CTkLabel(content_inner, text="", text_color="red", font=ctk.CTkFont(size=10))
        create_status.pack(pady=4, padx=16)

        def handle_create():
            name = routine_name_var.get().strip()
            if not name:
                create_status.configure(text="Enter a routine name")
                return
            try:
                routine_id = routinesCrud.create_routine(db_conn, user_id=user_id, name=name, notes=None)
                if routine_id:
                    create_status.configure(text="Routine created!", text_color="green")
                    routine_name_var.set("")
                    refresh_routines()
                    show_create_view()
                else:
                    create_status.configure(text="Failed to create routine", text_color="red")
            except Exception as e:
                create_status.configure(text=f"Error: {str(e)}", text_color="red")

        ctk.CTkButton(content_inner, text="Create routine", command=handle_create, width=300, height=40, corner_radius=8).pack(pady=16, padx=16)

    def show_detail_view(routine_id, routine_name):
        """Show the routine detail/edit panel"""
        for w in content_inner.winfo_children():
            w.destroy()

        header = ctk.CTkFrame(content_inner, fg_color="transparent")
        header.pack(fill="x", pady=(16, 12), padx=16)

        ctk.CTkButton(header, text="← Back", command=show_create_view, width=60, height=32, corner_radius=6).pack(side="left")
        ctk.CTkLabel(header, text=f"{routine_name}", font=ctk.CTkFont(size=12, weight="bold")).pack(side="left", padx=8)

        content_area = ctk.CTkFrame(content_inner, fg_color="transparent")
        content_area.pack(fill="both", expand=True, pady=(0, 16), padx=16)

        ctk.CTkLabel(content_area, text="Details", font=ctk.CTkFont(size=11, weight="bold")).pack(anchor="w", pady=(4, 8))
        
        # Content box with border
        box_container = ctk.CTkFrame(content_area, fg_color=("gray95", "#2a2a2a"), corner_radius=8)
        box_container.pack(fill="both", expand=True, pady=(0, 12))

        box_border = ctk.CTkFrame(box_container, fg_color=("gray70", "#3a3a3a"), corner_radius=8)
        box_border.pack(fill="both", expand=True, padx=1, pady=1)

        box_inner = ctk.CTkFrame(box_border, fg_color=("gray95", "#2a2a2a"), corner_radius=7)
        box_inner.pack(fill="both", expand=True, padx=0, pady=0)

        content_box = ctk.CTkTextbox(box_inner, corner_radius=6)
        content_box.pack(fill="both", expand=True, padx=8, pady=8)

        try:
            routine_data = routinesCrud.get_routine(db_conn, routine_id)
            if routine_data and routine_data.get('notes'):
                content_box.insert("1.0", routine_data['notes'])
        except Exception as e:
            print(f"Error loading routine: {e}")

        save_status = ctk.CTkLabel(content_area, text="", text_color="green", font=ctk.CTkFont(size=9))
        save_status.pack(pady=2)

        def save_content():
            content = content_box.get("1.0", "end-1c")
            try:
                routinesCrud.update_routine(db_conn, routine_id, notes=content)
                save_status.configure(text="✓ Saved!", text_color="green")
                content_area.after(2000, lambda: save_status.configure(text="") if content_area.winfo_exists() else None)
            except Exception as e:
                save_status.configure(text=f"Error: {str(e)}", text_color="red")

        ctk.CTkButton(content_area, text="Save routine", command=save_content, width=300, height=36, corner_radius=8).pack(pady=4)

    def refresh_routines():
        """Refresh the routines list"""
        for w in routines_scrollable.winfo_children():
            w.destroy()
        
        try:
            routines = routinesCrud.get_routines(db_conn, user_id=user_id)
        except Exception as e:
            print(f"Error fetching routines: {e}")
            routines = []

        if not routines:
            ctk.CTkLabel(routines_scrollable, text="No routines yet.", text_color="gray").pack(pady=20)
        else:
            for r in routines:
                routine_frame = ctk.CTkFrame(routines_scrollable, fg_color=("gray92", "#2a2a2a"), corner_radius=8)
                routine_frame.pack(fill="x", padx=0, pady=6)

                # Add subtle border to routine card
                routine_border = ctk.CTkFrame(routine_frame, fg_color=("gray70", "#3a3a3a"), corner_radius=8)
                routine_border.pack(fill="x", expand=True, padx=1, pady=1)

                routine_inner = ctk.CTkFrame(routine_border, fg_color=("gray92", "#2a2a2a"), corner_radius=7)
                routine_inner.pack(fill="x", expand=True, padx=0, pady=0)
                
                routine_name = r.get('name', 'Unnamed')
                name_label = ctk.CTkLabel(routine_inner, text=routine_name, font=ctk.CTkFont(size=11, weight="bold"), anchor="w")
                name_label.pack(fill="x", padx=12, pady=(8, 2))

                routine_id = r.get('id')

                def view_routine(rid=routine_id, rname=routine_name):
                    show_detail_view(rid, rname)

                def delete_routine(rid=routine_id):
                    try:
                        routinesCrud.delete_routine(db_conn, rid)
                        refresh_routines()
                    except Exception as e:
                        print(f"Delete error: {e}")

                btn_frame = ctk.CTkFrame(routine_inner, fg_color="transparent")
                btn_frame.pack(fill="x", padx=12, pady=(2, 8))
                ctk.CTkButton(btn_frame, text="View", command=view_routine, width=50, height=24, font=ctk.CTkFont(size=9), corner_radius=5).pack(side="left", padx=2)
                ctk.CTkButton(btn_frame, text="Delete", command=delete_routine, width=50, height=24, fg_color="#ef4444", font=ctk.CTkFont(size=9), corner_radius=5).pack(side="left", padx=2)

    # Initialize
    refresh_routines()
    show_create_view()

    return frame
# ...existing code...