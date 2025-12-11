import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, font
from datetime import datetime, timedelta
import storage
from python.models import Film, Salle_info, Representation, Reservation, Utilisateur


class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0, bg='#f5f5f5')
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")


class GUIApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        root.title("CY-NEMA — Interface Graphique")
        root.geometry("1100x700")
        
        # Configure custom theme
        self.setup_theme()

        self.user: Utilisateur | None = None

        # Header with gradient-like effect
        self.header_frame = tk.Frame(root, bg='#1a1a1a', height=80)
        self.header_frame.pack(fill="x", side="top")
        self.header_frame.pack_propagate(False)

        header_title = tk.Label(
            self.header_frame, 
            text="🎬 CY-NEMA", 
            font=("Segoe UI", 32, 'bold'),
            bg='#1a1a1a',
            fg='#00d4ff'
        )
        header_title.pack(pady=15)

        # Main content area
        self.main_frame = tk.Frame(root, bg='#f5f5f5')
        self.main_frame.pack(fill="both", expand=True)

        self.content = tk.Frame(self.main_frame, bg='#f5f5f5')
        self.content.pack(fill="both", expand=True)

        self.build_home()

    def show_success_popup(self, title, message):
        """Affiche un pop-up de succès stylisé"""
        win = tk.Toplevel(self.root)
        win.title(title)
        win.geometry("450x250")
        win.config(bg='#f5f5f5')
        win.resizable(False, False)
        
        # Header
        header = tk.Frame(win, bg='#00d4ff', height=80)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        header_label = tk.Label(
            header,
            text=title,
            font=("Segoe UI", 18, 'bold'),
            bg='#00d4ff',
            fg='#1a1a1a'
        )
        header_label.pack(pady=20)
        
        # Message
        msg_frame = tk.Frame(win, bg='#f5f5f5')
        msg_frame.pack(fill='both', expand=True, padx=30, pady=30)
        
        msg_label = tk.Label(
            msg_frame,
            text=message,
            font=("Segoe UI", 11),
            bg='#f5f5f5',
            fg='#1a1a1a',
            wraplength=350,
            justify='center'
        )
        msg_label.pack(expand=True)
        
        # Button
        btn = tk.Button(
            win,
            text="✅ OK",
            command=win.destroy,
            font=("Segoe UI", 11, 'bold'),
            bg='#00d4ff',
            fg='#1a1a1a',
            border=0,
            padx=30,
            pady=10,
            cursor='hand2',
            activebackground='#00a8cc',
            activeforeground='white'
        )
        btn.pack(pady=15)
        
        win.transient(self.root)
        win.grab_set()
    
    def show_error_popup(self, title, message):
        """Affiche un pop-up d'erreur stylisé"""
        win = tk.Toplevel(self.root)
        win.title(title)
        win.geometry("450x250")
        win.config(bg='#f5f5f5')
        win.resizable(False, False)
        
        # Header
        header = tk.Frame(win, bg='#ff6b6b', height=80)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        header_label = tk.Label(
            header,
            text=title,
            font=("Segoe UI", 18, 'bold'),
            bg='#ff6b6b',
            fg='white'
        )
        header_label.pack(pady=20)
        
        # Message
        msg_frame = tk.Frame(win, bg='#f5f5f5')
        msg_frame.pack(fill='both', expand=True, padx=30, pady=30)
        
        msg_label = tk.Label(
            msg_frame,
            text=message,
            font=("Segoe UI", 11),
            bg='#f5f5f5',
            fg='#1a1a1a',
            wraplength=350,
            justify='center'
        )
        msg_label.pack(expand=True)
        
        # Button
        btn = tk.Button(
            win,
            text="❌ Fermer",
            command=win.destroy,
            font=("Segoe UI", 11, 'bold'),
            bg='#ff6b6b',
            fg='white',
            border=0,
            padx=30,
            pady=10,
            cursor='hand2',
            activebackground='#ff5252',
            activeforeground='white'
        )
        btn.pack(pady=15)
        
        win.transient(self.root)
        win.grab_set()

    def setup_theme(self):
        style = ttk.Style(self.root)
        style.theme_use('clam')
        
        # Define custom colors
        bg_color = "#f5f5f5"
        fg_color = "#1a1a1a"
        accent_color = "#00d4ff"
        button_color = "#2d2d2d"
        
        # Configure styles
        style.configure('TFrame', background=bg_color)
        style.configure('TLabel', background=bg_color, foreground=fg_color, font=('Segoe UI', 10))
        style.configure('TButton', font=('Segoe UI', 10, 'bold'), padding=8)
        style.map('TButton',
            background=[('active', accent_color), ('pressed', '#00a8cc')],
            foreground=[('active', 'white')])
        style.configure('Accent.TButton', background=accent_color, foreground='white')
        style.map('Accent.TButton',
            background=[('active', '#00a8cc'), ('pressed', '#0088aa')])
        style.configure('TEntry', font=('Segoe UI', 10), padding=6)
        style.configure('Treeview', font=('Segoe UI', 9), rowheight=25)

    def clear_content(self):
        for w in self.content.winfo_children():
            w.destroy()

    def build_home(self):
        self.clear_content()
        self.content.config(bg='#f5f5f5')
        
        frame = tk.Frame(self.content, bg='#f5f5f5')
        frame.pack(fill="both", expand=True)

        # Left sidebar with buttons
        left = tk.Frame(frame, bg='#2d2d2d', width=250)
        left.pack(side="left", fill="y")
        left.pack_propagate(False)

        # Sidebar title
        sidebar_title = tk.Label(
            left, 
            text="Menu", 
            font=("Segoe UI", 16, 'bold'),
            bg='#2d2d2d',
            fg='#00d4ff'
        )
        sidebar_title.pack(pady=20)

        buttons_config = [
            ("🎬 Voir les films", lambda: self.show_films()),
            ("👤 Se connecter (User)", self.login_user),
            ("✍️ Créer un compte", self.register_user),
            ("🔐 Panneau Admin", self.login_admin),
            ("❌ Quitter", self.root.quit),
        ]

        for btn_text, cmd in buttons_config:
            btn = tk.Button(
                left,
                text=btn_text,
                command=cmd,
                font=("Segoe UI", 11, 'bold'),
                bg='#00d4ff',
                fg='#1a1a1a',
                border=0,
                padx=15,
                pady=12,
                cursor='hand2',
                activebackground='#00a8cc',
                activeforeground='white'
            )
            btn.pack(fill='x', padx=10, pady=8)

        # Right side with content
        self.home_right = tk.Frame(frame, bg='#f5f5f5')
        self.home_right.pack(side='left', fill='both', expand=True)

        self.show_films_home(parent=self.home_right)

    def show_films_home(self, parent):
        """Affiche les films dans la sidebar de l'accueil (sans bouton retour)"""
        for w in parent.winfo_children():
            w.destroy()

        # Title
        title_frame = tk.Frame(parent, bg='#f5f5f5')
        title_frame.pack(fill='x', padx=20, pady=(20, 10))
        title_label = tk.Label(
            title_frame,
            text="Films disponibles",
            font=("Segoe UI", 16, 'bold'),
            bg='#f5f5f5',
            fg='#1a1a1a'
        )
        title_label.pack(anchor='w')

        sf = ScrollableFrame(parent)
        sf.pack(fill='both', expand=True, padx=15, pady=15)

        films = storage.list_films()
        if not films:
            no_films = tk.Label(
                sf.scrollable_frame,
                text="📭 Aucun film disponible",
                font=("Segoe UI", 12),
                bg='#f5f5f5',
                fg='#999999'
            )
            no_films.pack(pady=40)
            return

        for film in films:
            # Film card
            card = tk.Frame(sf.scrollable_frame, bg='white', relief='flat', bd=0)
            card.pack(fill='x', pady=8, padx=10)
            card.config(highlightthickness=1, highlightbackground='#e0e0e0')

            # Film info
            info_frame = tk.Frame(card, bg='white')
            info_frame.pack(fill='x', padx=12, pady=10)

            title = tk.Label(
                info_frame,
                text=film.titre,
                font=("Segoe UI", 11, 'bold'),
                bg='white',
                fg='#1a1a1a'
            )
            title.pack(anchor='w')

            meta = f"⏱️ {film.duree}min  •  🎭 {film.categorie}  •  🔞 {film.age_min}+"
            meta_label = tk.Label(
                info_frame,
                text=meta,
                font=("Segoe UI", 8),
                bg='white',
                fg='#666666'
            )
            meta_label.pack(anchor='w', pady=(3, 0))

            if film.horaires:
                horaires_text = "Horaires: " + ' • '.join(film.horaires[:2])
                horaires_label = tk.Label(
                    info_frame,
                    text=horaires_text,
                    font=("Segoe UI", 8),
                    bg='white',
                    fg='#00d4ff'
                )
                horaires_label.pack(anchor='w', pady=(3, 0))

    def show_films(self, parent=None):
        # Si parent est None, on est en mode plein écran (depuis l'accueil ou en tant que user)
        if parent is None:
            parent = self.content
            # Détruire tout le contenu
            for w in parent.winfo_children():
                w.destroy()
            is_fullscreen = True
        else:
            # Mode embarqué dans une autre view (ex: panneau admin)
            is_fullscreen = False

        # Top bar with title and back button (seulement en mode plein écran)
        if is_fullscreen:
            top_bar = tk.Frame(parent, bg='#2d2d2d', height=60)
            top_bar.pack(fill='x')
            top_bar.pack_propagate(False)

            title_label = tk.Label(
                top_bar,
                text="🎬 Films disponibles",
                font=("Segoe UI", 16, 'bold'),
                bg='#2d2d2d',
                fg='#00d4ff'
            )
            title_label.pack(side='left', padx=20, pady=15)

            # Back button - always show (with different behavior based on connection)
            def go_back():
                if self.user:
                    self.build_user_dashboard()
                else:
                    self.build_home()

            back_btn = tk.Button(
                top_bar,
                text="← Retour",
                command=go_back,
                font=("Segoe UI", 10, 'bold'),
                bg='#ff6b6b',
                fg='white',
                border=0,
                padx=15,
                pady=10,
                cursor='hand2',
                activebackground='#ff5252',
                activeforeground='white'
            )
            back_btn.pack(side='right', padx=20, pady=10)

            # Content area
            content_frame = tk.Frame(parent, bg='#f5f5f5')
            content_frame.pack(fill='both', expand=True)
        else:
            # Mode embarqué - utiliser directement le parent
            content_frame = parent

        sf = ScrollableFrame(content_frame)
        sf.pack(fill='both', expand=True, padx=15, pady=15)

        films = storage.list_films()
        if not films:
            no_films = tk.Label(
                sf.scrollable_frame,
                text="📭 Aucun film disponible",
                font=("Segoe UI", 14),
                bg='#f5f5f5',
                fg='#999999'
            )
            no_films.pack(pady=40)
            return

        for film in films:
            # Film card with shadow effect
            card = tk.Frame(sf.scrollable_frame, bg='white', relief='flat', bd=0)
            card.pack(fill='x', pady=10, padx=10)
            
            # Add border simulation
            card.config(highlightthickness=1, highlightbackground='#e0e0e0')

            # Film info
            info_frame = tk.Frame(card, bg='white')
            info_frame.pack(fill='x', padx=15, pady=15)

            title = tk.Label(
                info_frame,
                text=film.titre,
                font=("Segoe UI", 14, 'bold'),
                bg='white',
                fg='#1a1a1a'
            )
            title.pack(anchor='w')

            meta = f"⏱️ {film.duree}min  •  🎭 {film.categorie}  •  🔞 {film.age_min}+"
            meta_label = tk.Label(
                info_frame,
                text=meta,
                font=("Segoe UI", 9),
                bg='white',
                fg='#666666'
            )
            meta_label.pack(anchor='w', pady=(5, 0))

            if film.horaires:
                horaires_text = "Horaires: " + ' • '.join(film.horaires)
                horaires_label = tk.Label(
                    info_frame,
                    text=horaires_text,
                    font=("Segoe UI", 9),
                    bg='white',
                    fg='#00d4ff'
                )
                horaires_label.pack(anchor='w', pady=(8, 0))

            btn_frame = tk.Frame(card, bg='white')
            btn_frame.pack(fill='x', padx=15, pady=(0, 15))

            details_btn = tk.Button(
                btn_frame,
                text="📖 Voir détails",
                command=lambda f=film: self.view_film(f),
                font=("Segoe UI", 10, 'bold'),
                bg='#00d4ff',
                fg='#1a1a1a',
                border=0,
                padx=15,
                pady=8,
                cursor='hand2',
                activebackground='#00a8cc',
                activeforeground='white'
            )
            details_btn.pack(anchor='e')

    def view_film(self, film: Film):
        win = tk.Toplevel(self.root)
        win.title(film.titre)
        win.geometry('700x500')
        win.config(bg='#f5f5f5')

        # Header
        header = tk.Frame(win, bg='#1a1a1a', height=60)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        header_label = tk.Label(
            header,
            text=f"🎬 {film.titre}",
            font=("Segoe UI", 18, 'bold'),
            bg='#1a1a1a',
            fg='#00d4ff'
        )
        header_label.pack(pady=15)

        # Content
        frame = tk.Frame(win, bg='#f5f5f5', padx=20, pady=20)
        frame.pack(fill='both', expand=True)

        # Film details
        details_text = f"⏱️ Durée: {film.duree} min\n🎭 Catégorie: {film.categorie}\n🔞 Âge minimum: {film.age_min}+"
        details_label = tk.Label(
            frame,
            text=details_text,
            font=("Segoe UI", 11),
            bg='#f5f5f5',
            fg='#1a1a1a',
            justify='left'
        )
        details_label.pack(anchor='w', pady=(0, 20))

        if film.horaires:
            horaires_title = tk.Label(
                frame,
                text="📅 Horaires disponibles:",
                font=("Segoe UI", 12, 'bold'),
                bg='#f5f5f5',
                fg='#1a1a1a'
            )
            horaires_title.pack(anchor='w', pady=(10, 10))

            for h in film.horaires:
                row = tk.Frame(frame, bg='white', highlightthickness=1, highlightbackground='#e0e0e0')
                row.pack(fill='x', pady=5)
                
                time_label = tk.Label(
                    row,
                    text=f"🕐 {h}",
                    font=("Segoe UI", 11),
                    bg='white',
                    fg='#1a1a1a',
                    padx=15,
                    pady=10
                )
                time_label.pack(side='left', fill='x', expand=True)

                reserve_btn = tk.Button(
                    row,
                    text="Réserver",
                    command=lambda horaire=h, f=film: self.start_reservation(f, horaire),
                    font=("Segoe UI", 10, 'bold'),
                    bg='#00d4ff',
                    fg='#1a1a1a',
                    border=0,
                    padx=15,
                    pady=10,
                    cursor='hand2',
                    activebackground='#00a8cc',
                    activeforeground='white'
                )
                reserve_btn.pack(side='right', padx=10)

    def login_user(self):
        win = tk.Toplevel(self.root)
        win.title("👤 Se connecter")
        win.geometry("450x400")
        win.config(bg='#f5f5f5')
        
        # Header
        header = tk.Frame(win, bg='#1a1a1a', height=80)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        header_label = tk.Label(
            header,
            text="👤 Connexion Utilisateur",
            font=("Segoe UI", 18, 'bold'),
            bg='#1a1a1a',
            fg='#00d4ff'
        )
        header_label.pack(pady=20)
        
        # Main frame
        main = tk.Frame(win, bg='#f5f5f5')
        main.pack(fill='both', expand=True, padx=30, pady=30)
        
        # Email
        tk.Label(main, text="📧 Email", font=("Segoe UI", 11, 'bold'), bg='#f5f5f5', fg='#1a1a1a').pack(anchor='w', pady=(0, 5))
        email_entry = tk.Entry(main, font=("Segoe UI", 11), bg='white', fg='#1a1a1a', border=0, relief='solid')
        email_entry.pack(fill='x', ipady=8, pady=(0, 20))
        
        # Password
        tk.Label(main, text="🔐 Mot de passe", font=("Segoe UI", 11, 'bold'), bg='#f5f5f5', fg='#1a1a1a').pack(anchor='w', pady=(0, 5))
        pwd_entry = tk.Entry(main, font=("Segoe UI", 11), bg='white', fg='#1a1a1a', border=0, relief='solid', show='•')
        pwd_entry.pack(fill='x', ipady=8, pady=(0, 30))
        
        def submit():
            email = email_entry.get().strip()
            pwd = pwd_entry.get()
            if not email or not pwd:
                messagebox.showerror("Erreur", "Tous les champs sont requis")
                return
            u = storage.authenticate_user(email, pwd)
            if u:
                self.user = u
                messagebox.showinfo("Succès", f"✅ Bienvenue {u.prenom} {u.nom}")
                win.destroy()
                self.build_user_dashboard()
            else:
                messagebox.showerror("Erreur", "❌ Email ou mot de passe invalide")
        
        # Buttons
        btn_frame = tk.Frame(main, bg='#f5f5f5')
        btn_frame.pack(fill='x', pady=(10, 0))
        
        login_btn = tk.Button(
            btn_frame,
            text="✅ Se connecter",
            command=submit,
            font=("Segoe UI", 11, 'bold'),
            bg='#00d4ff',
            fg='#1a1a1a',
            border=0,
            padx=25,
            pady=12,
            cursor='hand2',
            activebackground='#00a8cc',
            activeforeground='white'
        )
        login_btn.pack(side='right', padx=(5, 0))
        
        cancel_btn = tk.Button(
            btn_frame,
            text="❌ Annuler",
            command=win.destroy,
            font=("Segoe UI", 11, 'bold'),
            bg='#ff6b6b',
            fg='white',
            border=0,
            padx=25,
            pady=12,
            cursor='hand2',
            activebackground='#ff5252',
            activeforeground='white'
        )
        cancel_btn.pack(side='right', padx=(0, 5))

    def login_admin(self):
        win = tk.Toplevel(self.root)
        win.title("🔐 Admin Login")
        win.geometry("450x400")
        win.config(bg='#f5f5f5')
        
        # Header
        header = tk.Frame(win, bg='#ff9500', height=80)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        header_label = tk.Label(
            header,
            text="🔐 Panneau Administrateur",
            font=("Segoe UI", 18, 'bold'),
            bg='#ff9500',
            fg='white'
        )
        header_label.pack(pady=20)
        
        # Main frame
        main = tk.Frame(win, bg='#f5f5f5')
        main.pack(fill='both', expand=True, padx=30, pady=30)
        
        # Email
        tk.Label(main, text="📧 Email", font=("Segoe UI", 11, 'bold'), bg='#f5f5f5', fg='#1a1a1a').pack(anchor='w', pady=(0, 5))
        email_entry = tk.Entry(main, font=("Segoe UI", 11), bg='white', fg='#1a1a1a', border=0, relief='solid')
        email_entry.pack(fill='x', ipady=8, pady=(0, 20))
        
        # Password
        tk.Label(main, text="🔐 Mot de passe", font=("Segoe UI", 11, 'bold'), bg='#f5f5f5', fg='#1a1a1a').pack(anchor='w', pady=(0, 5))
        pwd_entry = tk.Entry(main, font=("Segoe UI", 11), bg='white', fg='#1a1a1a', border=0, relief='solid', show='•')
        pwd_entry.pack(fill='x', ipady=8, pady=(0, 30))
        
        def submit():
            email = email_entry.get().strip()
            pwd = pwd_entry.get()
            if not email or not pwd:
                messagebox.showerror("Erreur", "Tous les champs sont requis")
                return
            u = storage.authenticate_admin(email, pwd)
            if u:
                self.user = u
                messagebox.showinfo("Succès", f"✅ Bienvenue admin {u.prenom} {u.nom}")
                win.destroy()
                self.build_admin_dashboard()
            else:
                messagebox.showerror("Erreur", "❌ Email ou mot de passe admin invalide")
        
        # Buttons
        btn_frame = tk.Frame(main, bg='#f5f5f5')
        btn_frame.pack(fill='x', pady=(10, 0))
        
        login_btn = tk.Button(
            btn_frame,
            text="✅ Se connecter",
            command=submit,
            font=("Segoe UI", 11, 'bold'),
            bg='#ff9500',
            fg='white',
            border=0,
            padx=25,
            pady=12,
            cursor='hand2',
            activebackground='#ff7700',
            activeforeground='white'
        )
        login_btn.pack(side='right', padx=(5, 0))
        
        cancel_btn = tk.Button(
            btn_frame,
            text="❌ Annuler",
            command=win.destroy,
            font=("Segoe UI", 11, 'bold'),
            bg='#ff6b6b',
            fg='white',
            border=0,
            padx=25,
            pady=12,
            cursor='hand2',
            activebackground='#ff5252',
            activeforeground='white'
        )
        cancel_btn.pack(side='right', padx=(0, 5))

    def register_user(self):
        win = tk.Toplevel(self.root)
        win.title("✍️ Créer un compte")
        win.geometry("500x650")
        win.config(bg='#f5f5f5')
        
        # Header
        header = tk.Frame(win, bg='#1a1a1a', height=80)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        header_label = tk.Label(
            header,
            text="✍️ Créer un compte",
            font=("Segoe UI", 18, 'bold'),
            bg='#1a1a1a',
            fg='#00d4ff'
        )
        header_label.pack(pady=20)
        
        # Main frame
        main = tk.Frame(win, bg='#f5f5f5')
        main.pack(fill='both', expand=True, padx=30, pady=25)
        
        entries = {}
        fields = [
            ("👤 Nom", "nom"),
            ("👤 Prénom", "prenom"),
            ("🎂 Date de naissance (YYYY-MM-DD)", "date"),
            ("📧 Email", "email"),
            ("🔐 Mot de passe", "password")
        ]
        
        for label, key in fields:
            tk.Label(main, text=label, font=("Segoe UI", 10, 'bold'), bg='#f5f5f5', fg='#1a1a1a').pack(anchor='w', pady=(10, 3))
            ent = tk.Entry(
                main, 
                font=("Segoe UI", 10), 
                bg='white', 
                fg='#1a1a1a', 
                border=0, 
                relief='solid',
                show='•' if key == 'password' else ''
            )
            ent.pack(fill='x', ipady=8)
            entries[key] = ent
        
        def submit():
            try:
                nom = entries["nom"].get().strip()
                prenom = entries["prenom"].get().strip()
                dob = entries["date"].get().strip()
                email = entries["email"].get().strip()
                pwd = entries["password"].get()
                
                if not (nom and prenom and dob and email and pwd):
                    messagebox.showerror("Erreur", "❌ Tous les champs sont requis")
                    return
                
                u = storage.create_user(nom=nom, prenom=prenom, date_naissance=dob, email=email, password=pwd)
                messagebox.showinfo("Succès", f"✅ Compte créé: {u.email}")
                win.destroy()
                self.user = u
                self.build_user_dashboard()
            except ValueError as e:
                messagebox.showerror("Erreur", f"❌ {str(e)}")
        
        # Buttons
        btn_frame = tk.Frame(main, bg='#f5f5f5')
        btn_frame.pack(fill='x', pady=(20, 0))
        
        create_btn = tk.Button(
            btn_frame,
            text="✅ Créer un compte",
            command=submit,
            font=("Segoe UI", 11, 'bold'),
            bg='#00d4ff',
            fg='#1a1a1a',
            border=0,
            padx=25,
            pady=12,
            cursor='hand2',
            activebackground='#00a8cc',
            activeforeground='white'
        )
        create_btn.pack(side='right', padx=(5, 0))
        
        cancel_btn = tk.Button(
            btn_frame,
            text="❌ Annuler",
            command=win.destroy,
            font=("Segoe UI", 11, 'bold'),
            bg='#ff6b6b',
            fg='white',
            border=0,
            padx=25,
            pady=12,
            cursor='hand2',
            activebackground='#ff5252',
            activeforeground='white'
        )
        cancel_btn.pack(side='right', padx=(0, 5))

    def build_user_dashboard(self):
        self.clear_content()
        self.content.config(bg='#f5f5f5')
        
        # Top bar
        top = tk.Frame(self.content, bg='#2d2d2d', height=60)
        top.pack(fill='x')
        top.pack_propagate(False)

        user_label = tk.Label(
            top,
            text=f"👤 {self.user.prenom} {self.user.nom}",
            font=("Segoe UI", 12, 'bold'),
            bg='#2d2d2d',
            fg='#00d4ff'
        )
        user_label.pack(side='left', padx=20, pady=15)

        logout_btn = tk.Button(
            top,
            text="🚪 Déconnexion",
            command=self.logout,
            font=("Segoe UI", 10, 'bold'),
            bg='#ff4444',
            fg='white',
            border=0,
            padx=15,
            pady=10,
            cursor='hand2',
            activebackground='#cc0000',
            activeforeground='white'
        )
        logout_btn.pack(side='right', padx=20, pady=10)

        # Navigation
        nav = tk.Frame(self.content, bg='#f5f5f5')
        nav.pack(fill='x', padx=15, pady=10)

        nav_buttons = [
            ("🎬 Voir films", self.show_films),
            ("📋 Mes réservations", self.view_my_reservations),
            ("👨‍💼 Mon profil", self.view_profile),
        ]

        for btn_text, cmd in nav_buttons:
            btn = tk.Button(
                nav,
                text=btn_text,
                command=cmd,
                font=("Segoe UI", 10, 'bold'),
                bg='#00d4ff',
                fg='#1a1a1a',
                border=0,
                padx=15,
                pady=10,
                cursor='hand2',
                activebackground='#00a8cc',
                activeforeground='white'
            )
            btn.pack(side='left', padx=5)

        # Content area for films
        films_container = tk.Frame(self.content, bg='#f5f5f5')
        films_container.pack(fill='both', expand=True)

        # Title
        title_frame = tk.Frame(films_container, bg='#f5f5f5')
        title_frame.pack(fill='x', padx=20, pady=(20, 10))
        title_label = tk.Label(
            title_frame,
            text="Films disponibles",
            font=("Segoe UI", 16, 'bold'),
            bg='#f5f5f5',
            fg='#1a1a1a'
        )
        title_label.pack(anchor='w')

        self.show_films(parent=films_container)

    def build_admin_dashboard(self):
        self.clear_content()
        self.content.config(bg='#f5f5f5')
        
        # Top bar
        top = tk.Frame(self.content, bg='#2d2d2d', height=60)
        top.pack(fill='x')
        top.pack_propagate(False)

        admin_label = tk.Label(
            top,
            text=f"👑 Admin: {self.user.prenom} {self.user.nom}",
            font=("Segoe UI", 12, 'bold'),
            bg='#2d2d2d',
            fg='#ff9500'
        )
        admin_label.pack(side='left', padx=20, pady=15)

        logout_btn = tk.Button(
            top,
            text="🚪 Déconnexion",
            command=self.logout,
            font=("Segoe UI", 10, 'bold'),
            bg='#ff4444',
            fg='white',
            border=0,
            padx=15,
            pady=10,
            cursor='hand2',
            activebackground='#cc0000',
            activeforeground='white'
        )
        logout_btn.pack(side='right', padx=20, pady=10)

        # Navigation
        nav = tk.Frame(self.content, bg='#f5f5f5')
        nav.pack(fill='x', padx=15, pady=10)

        nav_buttons = [
            ("➕ Ajouter film", self.gui_add_film),
            ("🏢 Ajouter salle", self.gui_add_room),
            ("🎬 Ajouter représentation", self.gui_add_representation),
            ("🎯 Assigner représentation", self.gui_assign_representation),
            ("📊 Voir réservations", self.gui_view_all_reservations),
        ]

        for btn_text, cmd in nav_buttons:
            btn = tk.Button(
                nav,
                text=btn_text,
                command=cmd,
                font=("Segoe UI", 10, 'bold'),
                bg='#ff9500',
                fg='white',
                border=0,
                padx=12,
                pady=10,
                cursor='hand2',
                activebackground='#cc7700',
                activeforeground='white'
            )
            btn.pack(side='left', padx=5)

        # Content area for films
        films_container = tk.Frame(self.content, bg='#f5f5f5')
        films_container.pack(fill='both', expand=True)

        # Title
        title_frame = tk.Frame(films_container, bg='#f5f5f5')
        title_frame.pack(fill='x', padx=20, pady=(20, 10))
        title_label = tk.Label(
            title_frame,
            text="Films disponibles",
            font=("Segoe UI", 16, 'bold'),
            bg='#f5f5f5',
            fg='#1a1a1a'
        )
        title_label.pack(anchor='w')

        self.show_films(parent=films_container)

    def logout(self):
        self.user = None
        self.build_home()

    # ----- User actions -----
    def start_reservation(self, film: Film, horaire: str):
        if not self.user:
            messagebox.showinfo("Connexion requise", "Veuillez vous connecter pour réserver")
            return
        
        # Vérifier l'âge minimum du film
        user_age = self.user.calculate_age()
        if user_age < film.age_min:
            messagebox.showerror(
                "Accès refusé",
                f"❌ Vous devez avoir au minimum {film.age_min} ans pour regarder ce film.\nVotre âge: {user_age} ans"
            )
            return

        # find representation
        reps = storage.list_representations()
        rep = None
        for r in reps:
            if r.film_id == film.id and r.horaire == horaire:
                rep = r
                break
        if not rep:
            messagebox.showerror("Erreur", "Aucune représentation trouvée pour cet horaire")
            return

        # find assigned salle
        salles = storage.list_salles()
        salle = None
        for s in salles:
            if rep.id in s.id_representations:
                salle = s
                break
        if not salle:
            messagebox.showerror("Erreur", "Aucune salle assignée à cette représentation")
            return

        salles_entry = storage.get_salle_seating(salle.id, rep.id)
        if not salles_entry or not salles_entry.seating_map:
            messagebox.showerror("Erreur", "Plan de salle non disponible")
            return

        self.open_seat_selection(film, rep, salle, salles_entry.seating_map)

    def open_seat_selection(self, film, rep, salle, seating_map):
        win = tk.Toplevel(self.root)
        win.title(f"🎬 Réserver — {film.titre} à {rep.horaire}")
        win.geometry("950x750")
        win.config(bg='#f5f5f5')

        # Header
        header = tk.Frame(win, bg='#1a1a1a', height=100)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        header_label = tk.Label(
            header,
            text=f"🎬 {film.titre} — {rep.horaire}",
            font=("Segoe UI", 20, 'bold'),
            bg='#1a1a1a',
            fg='#00d4ff'
        )
        header_label.pack(pady=15)
        
        info_label = tk.Label(
            header,
            text=f"Salle {salle.numero}",
            font=("Segoe UI", 12),
            bg='#1a1a1a',
            fg='#ffffff'
        )
        info_label.pack(pady=(0, 10))

        rows = len(seating_map)
        cols = len(seating_map[0]) if rows else 0

        sel = set()

        canvas = tk.Canvas(win, bg='#f5f5f5', highlightthickness=0)
        canvas.pack(side='left', fill='both', expand=True, padx=20, pady=20)
        sbar = ttk.Scrollbar(win, orient='vertical', command=canvas.yview)
        sbar.pack(side='right', fill='y', padx=(0, 20))
        inner = ttk.Frame(canvas)
        canvas.create_window((0, 0), window=inner, anchor='nw')

        def on_config(e):
            canvas.configure(scrollregion=canvas.bbox('all'))

        inner.bind('<Configure>', on_config)
        canvas.configure(yscrollcommand=sbar.set)

        # Legend
        legend_frame = tk.Frame(inner, bg='#f5f5f5')
        legend_frame.pack(pady=(0, 20))
        
        tk.Label(legend_frame, text="🖼️ ÉCRAN", font=("Segoe UI", 13, 'bold'), bg='#f5f5f5', fg='#1a1a1a').pack()
        
        legend_inner = tk.Frame(legend_frame, bg='#f5f5f5')
        legend_inner.pack(pady=(10, 0))
        
        # Legend items with VIP
        legend_items = [
            ('#00d4ff', '💺 Disponible Normal', '9€'),
            ('#d946ef', '⭐ VIP Disponible', '15€'),
            ('#ff3333', '❌ Réservé'),
            ('#ffed4e', '✓ Sélectionné')
        ]
        
        for item in legend_items:
            row = tk.Frame(legend_inner, bg='#f5f5f5')
            row.pack(side='left', padx=15)
            box = tk.Label(row, text='█', font=("Segoe UI", 16), fg=item[0], bg='#f5f5f5')
            box.pack(side='left', padx=(0, 8))
            text = item[1] if len(item) > 2 else item[1]
            price = f"  {item[2]}" if len(item) > 2 else ""
            tk.Label(row, text=text + price, font=("Segoe UI", 9), bg='#f5f5f5', fg='#1a1a1a').pack(side='left')

        # Grid frame
        grid_frame = tk.Frame(inner, bg='#f5f5f5')
        grid_frame.pack(pady=20)

        btns = {}
        
        # Déterminer les rangées VIP
        vip_rows = set(range(salle.nombre_rangees_vip))

        def toggle(r, c):
            key = (r, c)
            if seating_map[r][c] == 'x':
                return
            if key in sel:
                sel.remove(key)
                is_vip = r in vip_rows
                bg_color = '#d946ef' if is_vip else '#00d4ff'
                btns[key].config(bg=bg_color, activebackground='#00a8cc', fg='#1a1a1a')
            else:
                sel.add(key)
                btns[key].config(bg='#ffed4e', activebackground='#fff59d', fg='#1a1a1a')

        for r in range(rows):
            for c in range(cols):
                state = seating_map[r][c]
                txt = f"{chr(65+r)}{c+1}"
                is_vip = r in vip_rows
                
                if state == 'x':
                    b = tk.Button(
                        grid_frame,
                        text=txt,
                        width=6,
                        height=2,
                        font=("Segoe UI", 9, 'bold'),
                        bg='#ff3333',
                        fg='white',
                        border=0,
                        relief='raised',
                        state='disabled',
                        disabledforeground='white'
                    )
                else:
                    bg_color = '#d946ef' if is_vip else '#00d4ff'
                    active_bg = '#ffed4e' if is_vip else '#00a8cc'
                    
                    b = tk.Button(
                        grid_frame,
                        text=txt,
                        width=6,
                        height=2,
                        font=("Segoe UI", 9, 'bold'),
                        bg=bg_color,
                        fg='#1a1a1a',
                        border=0,
                        relief='raised',
                        cursor='hand2',
                        activebackground=active_bg,
                        command=lambda rr=r, cc=c: toggle(rr, cc)
                    )
                
                b.grid(row=r, column=c, padx=3, pady=3)
                btns[(r, c)] = b

        # Bottom frame with stats
        bottom_frame = tk.Frame(inner, bg='#f5f5f5')
        bottom_frame.pack(pady=(20, 0))
        
        selected_label = tk.Label(
            bottom_frame,
            text="Aucun siège sélectionné",
            font=("Segoe UI", 11, 'bold'),
            bg='#f5f5f5',
            fg='#1a1a1a'
        )
        selected_label.pack(pady=(0, 8))
        
        price_label = tk.Label(
            bottom_frame,
            text="",
            font=("Segoe UI", 10, 'bold'),
            bg='#f5f5f5',
            fg='#00d4ff'
        )
        price_label.pack(pady=(0, 15))
        
        def update_label():
            if sel:
                seats_list = sorted([f"{chr(65+r)}{c+1}" for (r, c) in sel])
                selected_label.config(text=f"✓ Sièges sélectionnés: {', '.join(seats_list)}", fg='#00d4ff')
                
                # Calculer le prix
                total_price = 0
                vip_count = 0
                normal_count = 0
                for (r, c) in sel:
                    if r in vip_rows:
                        total_price += 15
                        vip_count += 1
                    else:
                        total_price += 9
                        normal_count += 1
                
                price_text = f"💰 Prix: "
                if normal_count > 0:
                    price_text += f"{normal_count}×9€ "
                if vip_count > 0:
                    price_text += f"{vip_count}×15€ "
                price_text += f"= {total_price}€"
                price_label.config(text=price_text)
            else:
                selected_label.config(text="Aucun siège sélectionné", fg='#ff6b6b')
                price_label.config(text="")

        def confirm():
            if not sel:
                self.show_error_popup('Erreur', 'Aucun siège sélectionné')
                return
            seats = sorted([f"{chr(65+r)}{c+1}" for (r, c) in sel])
            
            # Calculer le prix total
            total_price = sum(15 if (ord(seat[0]) - 65) in vip_rows else 9 for seat in seats)
            
            # create reservation
            reservation = Reservation(
                utilisateur_id=self.user.id,
                salle_id=salle.id,
                film_id=film.id,
                horaire=rep.horaire,
                places=seats
            )
            # mark seats
            for (r, c) in sel:
                seating_map[r][c] = 'x'
            storage.update_salle_seating(salle.id, rep.id, seating_map)
            storage.add_reservation(reservation)
            self.user.nombre_resa += 1
            storage.update_utilisateur(self.user)
            
            self.show_success_popup('✅ Réservation confirmée!', f'Places: {", ".join(seats)}\nPrix total: {total_price}€')
            win.destroy()

        btn_frame = tk.Frame(inner, bg='#f5f5f5')
        btn_frame.pack(fill='x', pady=(10, 0))
        
        confirm_btn = tk.Button(
            btn_frame,
            text="✅ Confirmer la réservation",
            command=confirm,
            font=("Segoe UI", 11, 'bold'),
            bg='#00d4ff',
            fg='#1a1a1a',
            border=0,
            padx=30,
            pady=12,
            cursor='hand2',
            activebackground='#00a8cc',
            activeforeground='white'
        )
        confirm_btn.pack(side='right', padx=(5, 0))
        
        cancel_btn = tk.Button(
            btn_frame,
            text="❌ Annuler",
            command=win.destroy,
            font=("Segoe UI", 11, 'bold'),
            bg='#ff6b6b',
            fg='white',
            border=0,
            padx=30,
            pady=12,
            cursor='hand2',
            activebackground='#ff5252',
            activeforeground='white'
        )
        cancel_btn.pack(side='right', padx=(0, 5))
        
        # Re-bind buttons with label update
        for (r, c), b in btns.items():
            if seating_map[r][c] != 'x':
                b.config(command=lambda rr=r, cc=c: (toggle(rr, cc), update_label()))

    def view_my_reservations(self):
        if not self.user:
            messagebox.showinfo('Info', '❌ Connectez-vous d\'abord')
            return
        win = tk.Toplevel(self.root)
        win.title('📋 Mes réservations')
        win.geometry('700x600')
        win.config(bg='#f5f5f5')

        # Header
        header = tk.Frame(win, bg='#1a1a1a', height=80)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        header_label = tk.Label(
            header,
            text="📋 Mes réservations",
            font=("Segoe UI", 20, 'bold'),
            bg='#1a1a1a',
            fg='#00d4ff'
        )
        header_label.pack(pady=20)

        reservations = storage.get_user_reservations(self.user.id)
        
        # Create scrollable frame
        canvas = tk.Canvas(win, bg='#f5f5f5', highlightthickness=0)
        scrollbar = ttk.Scrollbar(win, orient='vertical', command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#f5f5f5')
        
        scrollable_frame.bind(
            '<Configure>',
            lambda e: canvas.configure(scrollregion=canvas.bbox('all'))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side='left', fill='both', expand=True, padx=15, pady=15)
        scrollbar.pack(side='right', fill='y')
        
        if not reservations:
            no_res = tk.Label(
                scrollable_frame,
                text='📭 Aucune réservation pour le moment',
                font=("Segoe UI", 13, 'bold'),
                bg='#f5f5f5',
                fg='#999999'
            )
            no_res.pack(pady=60)
            return

        for res in reservations:
            card = tk.Frame(scrollable_frame, bg='white', highlightthickness=2, highlightbackground='#00d4ff')
            card.pack(fill='x', pady=10)
            
            # Header de la card
            card_header = tk.Frame(card, bg='#00d4ff')
            card_header.pack(fill='x')
            
            content = tk.Frame(card, bg='white')
            content.pack(fill='x', padx=15, pady=12)

            film = storage.get_film(res.film_id)
            film_title = film.titre if film else 'Film inconnu'
            
            title_label = tk.Label(
                card_header,
                text=f"  🎬 {film_title}",
                font=("Segoe UI", 13, 'bold'),
                bg='#00d4ff',
                fg='#1a1a1a'
            )
            title_label.pack(anchor='w', padx=15, pady=8)
            
            # Infos réservation
            info_label = tk.Label(
                content,
                text=f"🕐 Horaire: {res.horaire}",
                font=("Segoe UI", 11),
                bg='white',
                fg='#1a1a1a'
            )
            info_label.pack(anchor='w', pady=(0, 8))
            
            places_label = tk.Label(
                content,
                text=f"💺 Places: {', '.join(res.places)}",
                font=("Segoe UI", 11),
                bg='white',
                fg='#1a1a1a'
            )
            places_label.pack(anchor='w', pady=(0, 12))

            btn = tk.Button(
                content,
                text="❌ Annuler cette réservation",
                command=lambda r=res: self.cancel_reservation(r, win),
                font=("Segoe UI", 10, 'bold'),
                bg='#ff6b6b',
                fg='white',
                border=0,
                padx=15,
                pady=8,
                cursor='hand2',
                activebackground='#ff5252',
                activeforeground='white'
            )
            btn.pack(anchor='e', pady=(5, 0))

    def cancel_reservation(self, reservation: Reservation, parent_win=None):
        if not messagebox.askyesno('Confirmer', 'Voulez-vous annuler cette réservation ?'):
            return
        # free seats
        rep = None
        for r in storage.list_representations():
            if r.film_id == reservation.film_id and r.horaire == reservation.horaire:
                rep = r
                break
        if rep:
            salles_entry = storage.get_salle_seating(reservation.salle_id, rep.id)
            if salles_entry and salles_entry.seating_map:
                seating_map = salles_entry.seating_map
                for seat in reservation.places:
                    row_letter = seat[0]
                    col_num = int(seat[1:])
                    row_idx = ord(row_letter) - 65
                    col_idx = col_num - 1
                    if 0 <= row_idx < len(seating_map) and 0 <= col_idx < len(seating_map[0]):
                        seating_map[row_idx][col_idx] = 'o'
                storage.update_salle_seating(reservation.salle_id, rep.id, seating_map)

        # remove reservation
        db = storage.load_db()
        db['reservations'] = [r for r in db.get('reservations', []) if r.get('id') != reservation.id]
        storage.save_db(db)
        # update user
        self.user.nombre_resa = max(0, self.user.nombre_resa - 1)
        storage.update_utilisateur(self.user)
        messagebox.showinfo('Succès', 'Réservation annulée')
        if parent_win:
            parent_win.destroy()
            self.view_my_reservations()

    def view_profile(self):
        """Affiche et permet de modifier le profil en une seule fenêtre"""
        if not self.user:
            messagebox.showerror("Erreur", "Vous devez être connecté pour voir votre profil")
            return
            
        # Recharger l'utilisateur depuis la base de données
        current_user = storage.find_user_by_email(self.user.email)
        if current_user:
            self.user = current_user
        
        win = tk.Toplevel(self.root)
        win.title('Mon Profil')
        win.geometry('600x550')
        win.config(bg='#f5f5f5')

        # Header
        header = tk.Frame(win, bg='#1a1a1a', height=70)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        header_label = tk.Label(
            header,
            text="👨‍💼 Mon profil",
            font=("Segoe UI", 20, 'bold'),
            bg='#1a1a1a',
            fg='#00d4ff'
        )
        header_label.pack(pady=20)

        # Main content frame
        main_frm = tk.Frame(win, bg='#f5f5f5')
        main_frm.pack(fill='both', expand=True, padx=20, pady=20)

        # Dictionnaire pour stocker les Entry widgets
        entries = {}

        profile_fields = [
            ("👤 Nom", "nom", self.user.nom),
            ("📝 Prénom", "prenom", self.user.prenom),
            ("📧 Email", "email", self.user.email),
            ("🎂 Date de naissance", "date_naissance", self.user.date_naissance),
        ]

        # Créer les champs éditables
        for display_label, field_key, value_text in profile_fields:
            # Label du champ
            label_widget = tk.Label(
                main_frm,
                text=display_label,
                font=("Segoe UI", 11, 'bold'),
                bg='#f5f5f5',
                fg='#1a1a1a'
            )
            label_widget.pack(anchor='w', pady=(10, 0))
            
            # Entry field (champ éditable)
            entry_widget = tk.Entry(
                main_frm,
                font=("Segoe UI", 11),
                bg='white',
                fg='#1a1a1a',
                border=1,
                relief='solid'
            )
            entry_widget.insert(0, str(value_text))
            entry_widget.pack(fill='x', pady=(5, 0))
            entries[field_key] = entry_widget

        # Frame pour les boutons
        btn_frame = tk.Frame(main_frm, bg='#f5f5f5')
        btn_frame.pack(fill='x', pady=(30, 0))

        def save_profile():
            try:
                # Mettre à jour l'objet utilisateur
                self.user.nom = entries['nom'].get().strip()
                self.user.prenom = entries['prenom'].get().strip()
                self.user.email = entries['email'].get().strip()
                self.user.date_naissance = entries['date_naissance'].get().strip()
                
                # Sauvegarder dans la base de données
                storage.update_utilisateur(self.user)
                
                # Message de succès
                messagebox.showinfo('Succès', '✅ Profil mis à jour avec succès!')
                win.destroy()
                
                # Rafraîchir le dashboard pour appliquer les changements partout
                if self.user.role == 'client':
                    self.build_user_dashboard()
                elif self.user.role == 'admin':
                    self.build_admin_dashboard()
            except Exception as e:
                messagebox.showerror('Erreur', f'Erreur lors de la sauvegarde: {str(e)}')

        # Bouton Enregistrer
        save_btn = tk.Button(
            btn_frame,
            text="💾 Enregistrer",
            command=save_profile,
            font=("Segoe UI", 11, 'bold'),
            bg='#00d4ff',
            fg='#1a1a1a',
            border=0,
            padx=25,
            pady=12,
            cursor='hand2',
            activebackground='#00a8cc',
            activeforeground='white'
        )
        save_btn.pack(side='right', padx=(5, 0))

        # Bouton Annuler
        cancel_btn = tk.Button(
            btn_frame,
            text="❌ Annuler",
            command=win.destroy,
            font=("Segoe UI", 11, 'bold'),
            bg='#ff6b6b',
            fg='white',
            border=0,
            padx=25,
            pady=12,
            cursor='hand2',
            activebackground='#e55555',
            activeforeground='white'
        )
        cancel_btn.pack(side='right')

    def edit_profile(self, parent):
        """Méthode obsolète - kept for compatibility"""
        pass

    # ----- Admin actions -----
    def gui_add_film(self):
        win = tk.Toplevel(self.root)
        win.title('Ajouter film')
        win.geometry('600x450')
        win.config(bg='#f5f5f5')

        # Header
        header = tk.Frame(win, bg='#ff9500', height=60)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        header_label = tk.Label(
            header,
            text="➕ Ajouter un nouveau film",
            font=("Segoe UI", 16, 'bold'),
            bg='#ff9500',
            fg='white'
        )
        header_label.pack(pady=15)

        frm = tk.Frame(win, bg='#f5f5f5', padx=20, pady=20)
        frm.pack(fill='both', expand=True)

        entries = {}
        for label in ('Titre', 'Durée (min)', 'Catégorie', 'Âge min', 'Horaires (séparés par ,)'):
            row = tk.Frame(frm, bg='#f5f5f5')
            row.pack(fill='x', pady=10)
            
            label_widget = tk.Label(
                row,
                text=label,
                font=("Segoe UI", 10, 'bold'),
                bg='#f5f5f5',
                fg='#1a1a1a',
                width=25
            )
            label_widget.pack(side='left')
            
            ent = tk.Entry(
                row,
                font=("Segoe UI", 10),
                bg='white',
                fg='#1a1a1a',
                border=1,
                relief='solid'
            )
            ent.pack(side='left', fill='x', expand=True, padx=(10, 0))
            entries[label] = ent

        def submit():
            titre = entries['Titre'].get().strip()
            try:
                duree = int(entries['Durée (min)'].get())
            except Exception:
                messagebox.showerror('Erreur', '❌ Durée invalide')
                return
            categorie = entries['Catégorie'].get().strip()
            try:
                age_min = int(entries['Âge min'].get())
            except Exception:
                age_min = 0
            horaires = [h.strip() for h in entries['Horaires (séparés par ,)'].get().split(',') if h.strip()]
            film = Film(titre=titre, duree=duree, categorie=categorie, age_min=age_min, horaires=horaires)
            storage.add_film(film)
            messagebox.showinfo('Succès', f'✅ Film "{titre}" ajouté')
            win.destroy()

        submit_btn = tk.Button(
            frm,
            text="✅ Ajouter",
            command=submit,
            font=("Segoe UI", 10, 'bold'),
            bg='#ff9500',
            fg='white',
            border=0,
            padx=15,
            pady=10,
            cursor='hand2',
            activebackground='#cc7700',
            activeforeground='white'
        )
        submit_btn.pack(anchor='e', pady=(20, 0))

    def gui_add_room(self):
        win = tk.Toplevel(self.root)
        win.title('Ajouter salle')
        win.geometry('600x450')
        win.config(bg='#f5f5f5')

        # Header
        header = tk.Frame(win, bg='#ff9500', height=60)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        header_label = tk.Label(
            header,
            text="🏢 Ajouter une nouvelle salle",
            font=("Segoe UI", 16, 'bold'),
            bg='#ff9500',
            fg='white'
        )
        header_label.pack(pady=15)

        frm = tk.Frame(win, bg='#f5f5f5', padx=20, pady=20)
        frm.pack(fill='both', expand=True)

        entries = {}
        for label in ('Numéro', 'Nombre rangées total', 'Nombre rangées VIP', 'Nombre colonnes'):
            row = tk.Frame(frm, bg='#f5f5f5')
            row.pack(fill='x', pady=10)
            
            label_widget = tk.Label(
                row,
                text=label,
                font=("Segoe UI", 10, 'bold'),
                bg='#f5f5f5',
                fg='#1a1a1a',
                width=25
            )
            label_widget.pack(side='left')
            
            ent = tk.Entry(
                row,
                font=("Segoe UI", 10),
                bg='white',
                fg='#1a1a1a',
                border=1,
                relief='solid'
            )
            ent.pack(side='left', fill='x', expand=True, padx=(10, 0))
            entries[label] = ent

        def submit():
            try:
                numero = int(entries['Numéro'].get())
                nbr_r = int(entries['Nombre rangées total'].get())
                nbr_vip = int(entries['Nombre rangées VIP'].get())
                nbr_col = int(entries['Nombre colonnes'].get())
            except Exception:
                messagebox.showerror('Erreur', '❌ Valeurs invalides')
                return
            if nbr_vip > nbr_r:
                messagebox.showerror('Erreur', '❌ Rangées VIP > total')
                return
            salle = Salle_info(numero=numero, nombre_rangees_total=nbr_r, nombre_rangees_vip=nbr_vip, nombre_colonnes=nbr_col)
            storage.add_salle(salle)
            messagebox.showinfo('Succès', f'✅ Salle {numero} ajoutée')
            win.destroy()

        submit_btn = tk.Button(
            frm,
            text="✅ Ajouter",
            command=submit,
            font=("Segoe UI", 10, 'bold'),
            bg='#ff9500',
            fg='white',
            border=0,
            padx=15,
            pady=10,
            cursor='hand2',
            activebackground='#cc7700',
            activeforeground='white'
        )
        submit_btn.pack(anchor='e', pady=(20, 0))

    def gui_add_representation(self):
        win = tk.Toplevel(self.root)
        win.title('Ajouter représentation')
        win.geometry('600x400')
        win.config(bg='#f5f5f5')

        # Header
        header = tk.Frame(win, bg='#ff9500', height=60)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        header_label = tk.Label(
            header,
            text="🎬 Ajouter une représentation",
            font=("Segoe UI", 16, 'bold'),
            bg='#ff9500',
            fg='white'
        )
        header_label.pack(pady=15)

        frm = tk.Frame(win, bg='#f5f5f5', padx=20, pady=20)
        frm.pack(fill='both', expand=True)

        films = storage.list_films()
        if not films:
            messagebox.showerror('Erreur', '❌ Aucun film disponible')
            return

        # Film selection
        film_frame = tk.Frame(frm, bg='#f5f5f5')
        film_frame.pack(fill='x', pady=10)
        
        film_label = tk.Label(
            film_frame,
            text="Film",
            font=("Segoe UI", 10, 'bold'),
            bg='#f5f5f5',
            fg='#1a1a1a'
        )
        film_label.pack(side='left', padx=(0, 10))

        film_var = tk.StringVar()
        film_menu = ttk.Combobox(
            film_frame,
            values=[f.titre for f in films],
            textvariable=film_var,
            state='readonly',
            font=("Segoe UI", 10)
        )
        film_menu.pack(side='left', fill='x', expand=True)

        # Time selection
        time_frame = tk.Frame(frm, bg='#f5f5f5')
        time_frame.pack(fill='x', pady=10)
        
        time_label = tk.Label(
            time_frame,
            text="Horaire (HH:MM)",
            font=("Segoe UI", 10, 'bold'),
            bg='#f5f5f5',
            fg='#1a1a1a'
        )
        time_label.pack(side='left', padx=(0, 10))

        horaire_ent = tk.Entry(
            time_frame,
            font=("Segoe UI", 10),
            bg='white',
            fg='#1a1a1a',
            border=1,
            relief='solid'
        )
        horaire_ent.pack(side='left', fill='x', expand=True)

        def submit():
            titre = film_var.get()
            horaire = horaire_ent.get().strip()
            film = next((f for f in films if f.titre == titre), None)
            if not film:
                messagebox.showerror('Erreur', '❌ Film invalide')
                return
            try:
                horaire_fin = (datetime.strptime(horaire, '%H:%M') + timedelta(minutes=film.duree)).strftime('%H:%M')
            except:
                messagebox.showerror('Erreur', '❌ Format d\'horaire invalide (HH:MM)')
                return
            rep_id = f"{film.id}_{horaire}_{horaire_fin}"
            if storage.get_representation(rep_id):
                messagebox.showerror('Erreur', '❌ Représentation existe déjà')
                return
            rep = Representation(film_id=film.id, horaire=horaire, id=rep_id, horaire_fin=horaire_fin)
            storage.add_representation(rep)
            messagebox.showinfo('Succès', '✅ Représentation ajoutée')
            win.destroy()
            self.build_admin_dashboard()  # Rafraîchir le tableau de bord admin

        submit_btn = tk.Button(
            frm,
            text="✅ Ajouter",
            command=submit,
            font=("Segoe UI", 10, 'bold'),
            bg='#ff9500',
            fg='white',
            border=0,
            padx=15,
            pady=10,
            cursor='hand2',
            activebackground='#cc7700',
            activeforeground='white'
        )
        submit_btn.pack(anchor='e', pady=(30, 0))

    def gui_assign_representation(self):
        win = tk.Toplevel(self.root)
        win.title('Assigner représentation')
        win.geometry('600x400')
        win.config(bg='#f5f5f5')

        # Header
        header = tk.Frame(win, bg='#ff9500', height=60)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        header_label = tk.Label(
            header,
            text="🎯 Assigner une représentation",
            font=("Segoe UI", 16, 'bold'),
            bg='#ff9500',
            fg='white'
        )
        header_label.pack(pady=15)

        frm = tk.Frame(win, bg='#f5f5f5', padx=20, pady=20)
        frm.pack(fill='both', expand=True)

        reps = storage.list_representations()
        salles = storage.list_salles()
        if not reps or not salles:
            messagebox.showerror('Erreur', '❌ Représentations ou salles manquantes')
            return

        # Representation selection
        rep_frame = tk.Frame(frm, bg='#f5f5f5')
        rep_frame.pack(fill='x', pady=10)
        
        rep_label = tk.Label(
            rep_frame,
            text="Représentation",
            font=("Segoe UI", 10, 'bold'),
            bg='#f5f5f5',
            fg='#1a1a1a'
        )
        rep_label.pack(side='left', padx=(0, 10))

        rep_var = tk.StringVar()
        rep_menu = ttk.Combobox(
            rep_frame,
            values=[f"{storage.get_film(r.film_id).titre} — {r.horaire}" for r in reps],
            textvariable=rep_var,
            state='readonly',
            font=("Segoe UI", 10)
        )
        rep_menu.pack(side='left', fill='x', expand=True)

        # Salle selection
        salle_frame = tk.Frame(frm, bg='#f5f5f5')
        salle_frame.pack(fill='x', pady=10)
        
        salle_label = tk.Label(
            salle_frame,
            text="Salle",
            font=("Segoe UI", 10, 'bold'),
            bg='#f5f5f5',
            fg='#1a1a1a'
        )
        salle_label.pack(side='left', padx=(0, 10))

        salle_var = tk.StringVar()
        salle_menu = ttk.Combobox(
            salle_frame,
            values=[f"Salle {s.numero}" for s in salles],
            textvariable=salle_var,
            state='readonly',
            font=("Segoe UI", 10)
        )
        salle_menu.pack(side='left', fill='x', expand=True)

        def submit():
            sel_rep = rep_menu.get()
            sel_salle = salle_menu.get()
            if not sel_rep or not sel_salle:
                messagebox.showerror('Erreur', '❌ Sélection invalide')
                return
            rep_idx = rep_menu.current()
            salle_idx = salle_menu.current()
            rep = reps[rep_idx]
            salle = salles[salle_idx]
            success, err = storage.assign_representation_to_room(rep.id, salle.id)
            if success:
                messagebox.showinfo('Succès', '✅ Assignation effectuée')
                win.destroy()
                self.build_admin_dashboard()  # Rafraîchir le tableau de bord admin
            else:
                messagebox.showerror('Erreur', f"❌ {err}")

        submit_btn = tk.Button(
            frm,
            text="✅ Assigner",
            command=submit,
            font=("Segoe UI", 10, 'bold'),
            bg='#ff9500',
            fg='white',
            border=0,
            padx=15,
            pady=10,
            cursor='hand2',
            activebackground='#cc7700',
            activeforeground='white'
        )
        submit_btn.pack(anchor='e', pady=(30, 0))

    def gui_view_all_reservations(self):
        win = tk.Toplevel(self.root)
        win.title('Toutes les réservations')
        win.geometry('700x600')
        win.config(bg='#f5f5f5')

        # Header
        header = tk.Frame(win, bg='#ff9500', height=60)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        header_label = tk.Label(
            header,
            text="📊 Toutes les réservations",
            font=("Segoe UI", 16, 'bold'),
            bg='#ff9500',
            fg='white'
        )
        header_label.pack(pady=15)

        frm = tk.Frame(win, bg='#f5f5f5', padx=15, pady=15)
        frm.pack(fill='both', expand=True)

        reservations = storage.list_reservations()
        if not reservations:
            no_res = tk.Label(
                frm,
                text='📭 Aucune réservation',
                font=("Segoe UI", 12),
                bg='#f5f5f5',
                fg='#999999'
            )
            no_res.pack(pady=40)
            return

        # Scrollable list
        sf = ScrollableFrame(frm)
        sf.pack(fill='both', expand=True)

        for r in reservations:
            card = tk.Frame(sf.scrollable_frame, bg='white', highlightthickness=1, highlightbackground='#e0e0e0')
            card.pack(fill='x', pady=8)
            
            content = tk.Frame(card, bg='white')
            content.pack(fill='x', padx=15, pady=12)

            film = storage.get_film(r.film_id)
            film_title = film.titre if film else 'Film inconnu'
            
            # Find user
            user_obj = None
            for u in storage.list_utilisateurs():
                if u.id == r.utilisateur_id:
                    user_obj = u
                    break
            
            user_name = f"{user_obj.prenom} {user_obj.nom}" if user_obj else 'Utilisateur inconnu'
            
            title_label = tk.Label(
                content,
                text=f"🎬 {film_title}",
                font=("Segoe UI", 12, 'bold'),
                bg='white',
                fg='#1a1a1a'
            )
            title_label.pack(anchor='w')

            info_label = tk.Label(
                content,
                text=f"👤 {user_name}  •  🕐 {r.horaire}  •  💺 Places: {', '.join(r.places)}",
                font=("Segoe UI", 10),
                bg='white',
                fg='#666666'
            )
            info_label.pack(anchor='w', pady=(5, 0))


def main():
    root = tk.Tk()
    app = GUIApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()
