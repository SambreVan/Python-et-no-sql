import tkinter as tk
from tkinter import ttk, Menu, PhotoImage
import tkinter.simpledialog as simpledialog
from internet_data import InternetDataFetcher
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class MainApplication(tk.Frame):
    def __init__(self, parent, db, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.db = db
        self.create_widgets()
        self.graph_canvas = None
        self.parent.title("Application de Gestion de Données")
        self.parent.geometry("800x600")  # Taille de la fenêtre

    def create_widgets(self):
        self.set_background()
        self.set_menu()
        self.set_treeview()
        self.set_buttons()

    def set_background(self):
        background = Image.open(r'C:\Users\Pinta\Desktop\Projet final python\ressources\images\background.png')
        self.background_image = ImageTk.PhotoImage(background)
        background_label = tk.Label(self, image=self.background_image)
        background_label.place(x=800, y=0, relwidth=1, relheight=1)

    def set_menu(self):
        menubar = Menu(self.parent)
        self.parent.config(menu=menubar)

        options_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Options", menu=options_menu)
        options_menu.add_command(label="Effacer les Données", command=self.clear_data)
        options_menu.add_command(label="Nouvelles données", command=self.refresh_data)

    def set_treeview(self):
        style = ttk.Style()
        style.theme_use("clam")  # Utiliser un thème pour un look plus moderne
        style.configure("Treeview",
                        background="#E8E8E8",
                        foreground="black",
                        rowheight=25,
                        fieldbackground="#E8E8E8")
        style.map('Treeview', background=[('selected', '#3498db')])  # Couleur de sélection

        # Police et couleur des en-têtes
        style.configure("Treeview.Heading",
                        font=('Calibri', 11, 'bold'),
                        background="#D3D3D3",
                        foreground="black")
        style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])  # Enlever la bordure

        tree_frame = tk.Frame(self)
        tree_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=10)

        # Création et configuration du Treeview
        self.tree = ttk.Treeview(tree_frame, style="Treeview")
        self.config_treeview()
        self.tree.pack(expand=True, fill=tk.BOTH)

    def config_treeview(self):
        # Configuration des colonnes du Treeview
        self.tree["columns"] = ("id", "url", "width", "height")
        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.column("id", width=100, anchor=tk.CENTER)
        self.tree.column("url", width=200, anchor=tk.W)
        self.tree.column("width", width=80, anchor=tk.CENTER)
        self.tree.column("height", width=80, anchor=tk.CENTER)

        # Configuration des en-têtes
        self.tree.heading("id", text="ID", anchor=tk.W)
        self.tree.heading("url", text="URL", anchor=tk.W)
        self.tree.heading("width", text="Width", anchor=tk.CENTER)
        self.tree.heading("height", text="Height", anchor=tk.CENTER)

    def set_buttons(self):
        buttons_frame = tk.Frame(self, bg='white')
        buttons_frame.pack(pady=10)

        # Bouton pour charger les données
        self.load_data_image = PhotoImage(file=r'C:\Users\Pinta\Desktop\Projet final python\ressources\images\button_load-image.png')
        self.load_data_button = tk.Button(buttons_frame, image=self.load_data_image, command=self.load_data)
        self.load_data_button.image = self.load_data_image  # Garder une référence
        self.load_data_button.pack(side=tk.LEFT, padx=5)

        # Bouton pour afficher le graphique
        self.show_graph_image = PhotoImage(file=r'C:\Users\Pinta\Desktop\Projet final python\ressources\images\button_graphique.png')
        self.show_graph_button = tk.Button(buttons_frame, image=self.show_graph_image, command=self.show_graph)
        self.show_graph_button.image = self.show_graph_image  # Garder une référence
        self.show_graph_button.pack(side=tk.LEFT, padx=5)







    def clear_data(self):
        self.db.clear_table()
        for i in self.tree.get_children():
            self.tree.delete(i)

    def load_data(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        data = self.db.fetch_all_entries()
        for row in data:
            self.tree.insert("", tk.END, values=row)


    def show_graph(self):
        average_height = self.db.get_average_height()
        average_width = self.db.get_average_width()
        all_sizes = self.db.get_all_sizes()

        if average_height is not None and average_width is not None and all_sizes:
            fig, ax = plt.subplots(figsize=(8, 6))

            if self.graph_canvas:
                self.graph_canvas.get_tk_widget().destroy()

            for width, height in all_sizes:
                ax.scatter(width, height, color='red')

            ax.set_xlabel("Largeur")
            ax.set_ylabel("Hauteur")
            ax.set_title("Analyse des Images")

            # Lignes de moyenne
            height_line = ax.axhline(y=average_height, color='blue', linestyle='--')
            width_line = ax.axvline(x=average_width, color='green', linestyle='--')

            # Couleur de fond correspondante
            ax.set_facecolor('#4618A7')  # Couleur de fond blanche
            fig.set_facecolor('#4618A7')

            # Ajout de la légende avec des étiquettes
            ax.legend([height_line, width_line], [f'Moyenne des Hauteurs: {average_height:.2f}', f'Moyenne des Largeurs: {average_width:.2f}'], loc='center left', bbox_to_anchor=(1, 0.5))

            fig.tight_layout()

            self.graph_canvas = FigureCanvasTkAgg(fig, master=self)
            canvas_widget = self.graph_canvas.get_tk_widget()
            canvas_widget.pack()
            self.graph_canvas.draw()
        else:
            print("Aucune donnée disponible pour le graphique")

    def refresh_data(self):
        number = simpledialog.askinteger("Nouvelles données", "Nombre d'images à télécharger:",
                                        parent=self.parent, minvalue=1, maxvalue=100)
        if number is not None:
            for _ in range(number):
                fetcher = InternetDataFetcher("https://api.thecatapi.com/v1/images/search")
                json_data = fetcher.fetch_json()

                if json_data and len(json_data) > 0:
                    item = json_data[0]
                    self.db.insert_cat_image(item['id'], item['url'], item['width'], item['height'])

            self.load_data()



