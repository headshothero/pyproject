import tkinter as tk
from tkinter import filedialog, messagebox
import csv

# Initialisation de l'interface graphique
root = tk.Tk()
root.title("Convertisseur de noms d'hôtes")

# Définir les couleurs
bg_color = "#000000"  # Noir
fg_color = "#FFA500"  # Orange
hover_bg_color = "#FF8C00"  # Orange plus clair pour le survol
button_font = ("Arial", 14, "bold")  # Police plus grande et en gras

# Appliquer les couleurs à la fenêtre principale
root.config(bg=bg_color)

# Variable pour stocker le chemin du fichier et le choix
file_path = None
suffix_choice = tk.StringVar(value="GW")  # Valeur par défaut

# Suffixes selon le choix
suffixes = {
    "GW": ".rouen.francetelecom.fr",
    "BRMC": ".nor.fr.gin.intraorange"
}

def import_csv():
    global file_path
    file_path = filedialog.askopenfilename(
        filetypes=[("CSV Files", "*.csv")], 
        title="Choisissez un fichier CSV"
    )
    if file_path:
        messagebox.showinfo("Fichier importé", f"Fichier importé avec succès : {file_path}")

def convert_hosts():
    if not file_path:
        messagebox.showwarning("Avertissement", "Veuillez importer un fichier CSV d'abord.")
        return

    # Suffixe à ajouter selon le choix
    suffix = suffixes[suffix_choice.get()]

    # Lecture du fichier CSV et extraction des noms d'hôtes
    try:
        with open(file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter=';')
            hostnames = []
            for i, row in enumerate(reader):
                if i == 0:  # Ignore la première ligne si elle est un en-tête
                    continue
                hostnames.append(row[0])  # On suppose que le nom d'hôte est dans la première colonne

        # Ajout du suffixe aux noms d'hôtes
        full_hostnames = [hostname + suffix for hostname in hostnames]

        # Affichage des résultats
        result_text.delete("1.0", tk.END)  # Effacer le texte existant
        result_text.insert(tk.END, " ".join(full_hostnames))
        messagebox.showinfo("Conversion terminée", "Les noms d'hôtes ont été convertis avec succès !")
    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur est survenue lors de la conversion : {e}")

# Fonction pour changer la couleur de fond au survol
def on_enter(event, button):
    button.config(bg=hover_bg_color)

def on_leave(event, button):
    button.config(bg=bg_color)

# Interface graphique
import_button = tk.Button(root, text="Importer CSV", command=import_csv, bg=bg_color, fg=fg_color, relief="solid", font=button_font, height=2, width=20)
convert_button = tk.Button(root, text="Convertir", command=convert_hosts, bg=bg_color, fg=fg_color, relief="solid", font=button_font, height=2, width=20)

# Ajout des effets de survol
import_button.bind("<Enter>", lambda event: on_enter(event, import_button))
import_button.bind("<Leave>", lambda event: on_leave(event, import_button))

convert_button.bind("<Enter>", lambda event: on_enter(event, convert_button))
convert_button.bind("<Leave>", lambda event: on_leave(event, convert_button))

# Menu déroulant pour sélectionner le type de suffixe
choice_label = tk.Label(root, text="Choisissez le type :", bg=bg_color, fg=fg_color, font=("Arial", 12))
choice_menu = tk.OptionMenu(root, suffix_choice, *suffixes.keys())
choice_menu.config(bg=bg_color, fg=fg_color, font=("Arial", 12), width=15)

# Zone de texte pour les résultats
result_text = tk.Text(root, wrap="word", height=10, width=80, bg=bg_color, fg=fg_color, insertbackground="white", font=("Arial", 12))

# Positionnement des éléments
choice_label.pack(pady=10)
choice_menu.pack(pady=10)
import_button.pack(pady=20)
convert_button.pack(pady=20)
result_text.pack(pady=10)

# Lancement de la boucle principale
root.mainloop()
