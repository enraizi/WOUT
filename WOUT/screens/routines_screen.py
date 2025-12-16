import customtkinter as ctk
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from WOUT.crud import routines_crud

def create_routines(parent, db_conn, user=None):
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
    
    ctk.CTkLabel(header, text="Routines", 
                 font=ctk.CTkFont(size=28, weight="bold"),
                 text_color=("gray10", "#ffffff")).pack(anchor="w")
    
    ctk.CTkLabel(header, text="Create and manage your workout routines", 
                 font=ctk.CTkFont(size=12),
                 text_color=("gray60", "#a0a0a0")).pack(anchor="w", pady=(4, 0))

    # Main content area
    main_content = ctk.CTkFrame(frame, fg_color="transparent")
    main_content.pack(fill="both", expand=True, padx=32, pady=(0, 32))

    # Create routine section - premium card
    create_section = ctk.CTkFrame(main_content, fg_color="transparent")
    create_section.pack(fill="x", padx=0, pady=(0, 16))

    create_container = ctk.CTkFrame(create_section, fg_color=("gray95", "#1a1f26"), corner_radius=12)
    create_container.pack(fill="x")

    create_border = ctk.CTkFrame(create_container, fg_color=("gray75", "#ffd700"), corner_radius=12)
    create_border.pack(fill="x", expand=True, padx=1, pady=1)

    create_inner = ctk.CTkFrame(create_border, fg_color=("gray95", "#1a1f26"), corner_radius=11)
    create_inner.pack(fill="x", expand=True, padx=0, pady=0, ipadx=16, ipady=12)

    ctk.CTkLabel(create_inner, text="   ➕ Create New Routine", 
                 font=ctk.CTkFont(size=12, weight="bold"),
                 text_color=("gray10", "#ffd700")).pack(anchor="w", pady=(0, 12))

    routine_name_entry = ctk.CTkEntry(create_inner, placeholder_text="Routine name",
                                      height=36, border_width=1,
                                      border_color=("gray80", "#333333"),
                                      fg_color=("gray90", "#2a2f36"))
    routine_name_entry.pack(fill="x", pady=(0, 10))

    notes_entry = ctk.CTkTextbox(create_inner, height=80, corner_radius=8,
                                 fg_color=("gray90", "#2a2f36"),
                                 border_width=1,
                                 border_color=("gray80", "#333333"))
    notes_entry.pack(fill="x", pady=(0, 12))

    error_label = ctk.CTkLabel(create_inner, text="", 
                              font=ctk.CTkFont(size=9),
                              text_color=("#dc2626", "#ff6b6b"))
    error_label.pack(pady=(0, 10))

    def create_routine():
        name = routine_name_entry.get().strip()
        notes = notes_entry.get("1.0", "end").strip()

        if not name:
            error_label.configure(text="Please enter a routine name")
            return

        try:
            routines_crud.create_routine(db_conn, user_id=user_id, name=name, notes=notes)
            routine_name_entry.delete(0, "end")
            notes_entry.delete("1.0", "end")
            error_label.configure(text="")
            
            refresh_routines()
        except Exception as e:
            error_label.configure(text=f"Error creating routine: {str(e)}")

    create_btn = ctk.CTkButton(create_inner, text="Create Routine", command=create_routine,
                              height=40, font=ctk.CTkFont(size=11, weight="bold"),
                              fg_color=("#2563eb", "#2563eb"),
                              hover_color=("#1d4ed8", "#1d4ed8"),
                              corner_radius=8)
    create_btn.pack(fill="x")

    # Routines list section header
    routines_label = ctk.CTkFrame(main_content, fg_color="transparent")
    routines_label.pack(fill="x", padx=0, pady=(0, 12))
    
    ctk.CTkLabel(routines_label, text="Your Routines", 
                 font=ctk.CTkFont(size=14, weight="bold"),
                 text_color=("gray10", "#ffffff")).pack(anchor="w")

    # Scrollable routines container
    routines_container = ctk.CTkScrollableFrame(main_content, fg_color="transparent", corner_radius=0)
    routines_container.pack(fill="both", expand=True, padx=0, pady=0)

    def refresh_routines():
        for w in routines_container.winfo_children():
            w.destroy()

        try:
            routines = routines_crud.get_routines(db_conn, user_id=user_id)
        except Exception as e:
            print(f"Error fetching routines: {e}")
            routines = []

        if not routines:
            empty_frame = ctk.CTkFrame(routines_container, fg_color="transparent")
            empty_frame.pack(fill="both", expand=True, pady=40)
            ctk.CTkLabel(empty_frame, text="No routines yet", 
                        font=ctk.CTkFont(size=13, weight="bold"),
                        text_color=("gray40", "#808080")).pack()
            ctk.CTkLabel(empty_frame, text="Create one above to get started", 
                        text_color=("gray60", "#a0a0a0"), 
                        font=ctk.CTkFont(size=11)).pack(pady=(4, 0))
        else:
            for r in routines:
                routine_card = ctk.CTkFrame(routines_container, fg_color=("gray95", "#1a1f26"),
                                           corner_radius=12, height=70)
                routine_card.pack(fill="x", pady=8)
                routine_card.pack_propagate(False)

                routine_border = ctk.CTkFrame(routine_card, fg_color=("gray75", "#ffd700"), corner_radius=12)
                routine_border.pack(fill="both", expand=True, padx=1, pady=1)

                routine_inner = ctk.CTkFrame(routine_border, fg_color=("gray95", "#1a1f26"), corner_radius=11)
                routine_inner.pack(fill="both", expand=True, padx=0, pady=0, ipadx=16, ipady=12)

                routine_name = r.get('name', 'Unnamed') if isinstance(r, dict) else r[2]
                routine_id = r.get('id') if isinstance(r, dict) else r[0]
                
                inner = ctk.CTkFrame(routine_inner, fg_color="transparent")
                inner.pack(fill="both", expand=True)

                # Routine info
                info_frame = ctk.CTkFrame(inner, fg_color="transparent")
                info_frame.pack(side="left", fill="both", expand=True)

                ctk.CTkLabel(info_frame, text=f"    💪 {routine_name}", 
                            font=ctk.CTkFont(size=13, weight="bold"),
                            text_color=("gray10", "#ffd700")).pack(anchor="w", pady=(0, 4))

                ctk.CTkLabel(info_frame, text="         Tap to manage your workout routine", 
                            font=ctk.CTkFont(size=9),
                            text_color=("gray50", "#90caf9")).pack(anchor="w")

                # Action buttons
                button_frame = ctk.CTkFrame(inner, fg_color="transparent")
                button_frame.pack(side="right", padx=(12, 0))

                def make_delete_command(rid=routine_id):
                    def delete_routine():
                        try:
                            routines_crud.delete_routine(db_conn, rid)
                            refresh_routines()
                        except Exception as e:
                            print(f"Error deleting routine: {e}")
                    return delete_routine

                def make_edit_command(rid=routine_id, rname=routine_name):
                    def edit_routine():
                        try:
                            routine_data = routines_crud.get_routine(db_conn, rid)
                            
                            root = parent.winfo_toplevel()
                            modal = ctk.CTkToplevel(root)
                            modal.title("Edit Routine")
                            modal.geometry("480x500")
                            modal.resizable(False, False)
                            modal.grab_set()
                            
                            modal.update_idletasks()
                            root.update_idletasks()
                            x = root.winfo_x() + (root.winfo_width() // 2) - 240
                            y = root.winfo_y() + (root.winfo_height() // 2) - 250
                            modal.geometry(f"+{x}+{y}")
                            
                            modal_frame = ctk.CTkFrame(modal, fg_color=("gray95", "#1a1f26"), corner_radius=0)
                            modal_frame.pack(fill="both", expand=True, padx=0, pady=0)
                            
                            bordered_card = ctk.CTkFrame(modal_frame, fg_color=("gray75", "#ffd700"), corner_radius=12)
                            bordered_card.pack(fill="both", expand=True, padx=16, pady=16)
                            
                            card_inner = ctk.CTkFrame(bordered_card, fg_color=("gray95", "#1a1f26"), corner_radius=11)
                            card_inner.pack(fill="both", expand=True, padx=1, pady=1)
                            
                            header = ctk.CTkFrame(card_inner, fg_color=("gray88", "#2a3a4a"), corner_radius=0)
                            header.pack(fill="x", padx=0, pady=0)
                            
                            ctk.CTkLabel(header, text="✏️ Edit Routine",
                                        font=ctk.CTkFont(size=15, weight="bold"),
                                        text_color=("gray10", "#ffd700")).pack(anchor="w", padx=20, pady=14)
                            
                            content = ctk.CTkFrame(card_inner, fg_color="transparent")
                            content.pack(fill="both", expand=True, padx=20, pady=16)
                            
                            ctk.CTkLabel(content, text="Routine Name",
                                        font=ctk.CTkFont(size=11, weight="bold"),
                                        text_color=("gray20", "#e0e0e0")).pack(anchor="w", pady=(0, 6))
                            
                            name_var = ctk.StringVar(value=rname)
                            name_entry = ctk.CTkEntry(content, textvariable=name_var,
                                                      height=40, border_width=2,
                                                      border_color=("gray70", "#ffd700"),
                                                      fg_color=("white", "#2a2f36"),
                                                      text_color=("gray10", "#ffd700"),
                                                      font=ctk.CTkFont(size=11))
                            name_entry.pack(fill="x", pady=(0, 14))
                            
                            ctk.CTkLabel(content, text="Notes",
                                        font=ctk.CTkFont(size=11, weight="bold"),
                                        text_color=("gray20", "#e0e0e0")).pack(anchor="w", pady=(0, 6))
                            
                            notes_text = ctk.CTkTextbox(content, height=120, corner_radius=8,
                                                       fg_color=("white", "#2a2f36"),
                                                       border_width=2,
                                                       border_color=("gray70", "#ffd700"),
                                                       text_color=("gray10", "#ffffff"),
                                                       font=ctk.CTkFont(size=11))
                            notes_text.pack(fill="both", expand=True, pady=(0, 14))
                            

                            if routine_data and routine_data.get('notes'):
                                notes_text.insert("1.0", routine_data['notes'])
                            
                            error_msg = ctk.CTkLabel(content, text="",
                                                    font=ctk.CTkFont(size=9),
                                                    text_color=("#dc2626", "#ff6b6b"))
                            error_msg.pack(anchor="w", pady=(0, 12))
                            
                            button_frame = ctk.CTkFrame(content, fg_color="transparent")
                            button_frame.pack(fill="x")
                            
                            def save_changes():
                                new_name = name_var.get().strip()
                                new_notes = notes_text.get("1.0", "end").strip()
                                
                                if not new_name:
                                    error_msg.configure(text="Routine name cannot be empty")
                                    return
                                
                                try:
                                    routines_crud.update_routine(db_conn, rid, new_name, new_notes)
                                    modal.destroy()
                                    refresh_routines()
                                except Exception as e:
                                    error_msg.configure(text=f"Error: {str(e)[:40]}")
                            

                            ctk.CTkButton(button_frame, text="Cancel",
                                         command=modal.destroy,
                                         width=100, height=40,
                                         fg_color=("gray80", "#2a3a4a"),
                                         text_color=("gray20", "#e0e0e0"),
                                         hover_color=("gray70", "#3a4a5a"),
                                         corner_radius=8,
                                         font=ctk.CTkFont(size=11, weight="bold")).pack(side="left", padx=(0, 10))
                            

                            ctk.CTkButton(button_frame, text="Save",
                                         command=save_changes,
                                         width=100, height=40,
                                         fg_color=("#2563eb", "#2563eb"),
                                         text_color=("white", "white"),
                                         hover_color=("#1d4ed8", "#1d4ed8"),
                                         corner_radius=8,
                                         font=ctk.CTkFont(size=11, weight="bold")).pack(side="left")
                        except Exception as e:
                            print(f"Error opening edit modal: {e}")
                    return edit_routine

                ctk.CTkButton(button_frame, text="Delete",
                             command=make_delete_command(),
                             width=70, height=32,
                             fg_color=("#ef4444", "#ef4444"),
                             hover_color=("#dc2626", "#dc2626"),
                             corner_radius=6,
                             font=ctk.CTkFont(size=9, weight="bold")).pack(side="right", padx=(4, 0))

                ctk.CTkButton(button_frame, text="Edit",
                             command=make_edit_command(),
                             width=70, height=32,
                             fg_color=("#2563eb", "#2563eb"),
                             hover_color=("#1d4ed8", "#1d4ed8"),
                             corner_radius=6,
                             font=ctk.CTkFont(size=9, weight="bold")).pack(side="right")

    refresh_routines()

    return frame