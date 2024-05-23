import os
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox

import matplotlib.pyplot as plt
import psutil
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class SwiftGuideApp:
    def __init__(self, master):
        self.master = master
        master.title("SwiftGuide")

        # Ustawienia języka
        self.language = 'en'
        self.translations = {
            'en': {
                'title': "SwiftGuide",
                'cpu_usage': "CPU Usage:",
                'ram_usage': "RAM Usage:",
                'disk_usage': "Disk Usage:",
                'cpu_temp': "CPU Temperature:",
                'memory_temp': "Memory Temperature:",
                'update_packages': "Update Packages",
                'update_system': "Update System",
                'optimize_system': "Optimize System",
                'refresh_mirrors': "Refresh Mirrors",
                'manage_drivers': "Manage Drivers",
                'refresh_devices': "Refresh Devices",
                'device': "Device",
                'driver': "Driver",
                'update_drivers': "Update Drivers",
                'install_dedicated_drivers': "Install Dedicated Drivers",
                'install_open_source_drivers': "Install Open-Source Drivers",
                'distribution_unknown': "Unknown Distribution"
            },
            'de': {
                'title': "SwiftGuide",
                'cpu_usage': "CPU-Auslastung:",
                'ram_usage': "RAM-Auslastung:",
                'disk_usage': "Festplattennutzung:",
                'cpu_temp': "CPU-Temperatur:",
                'memory_temp': "Speichertemperatur:",
                'update_packages': "Pakete aktualisieren",
                'update_system': "System aktualisieren",
                'optimize_system': "System optimieren",
                'refresh_mirrors': "Spiegel aktualisieren",
                'manage_drivers': "Treiber verwalten",
                'refresh_devices': "Geräte aktualisieren",
                'device': "Gerät",
                'driver': "Treiber",
                'update_drivers': "Treiber aktualisieren",
                'install_dedicated_drivers': "Dedizierte Treiber installieren",
                'install_open_source_drivers': "Open-Source-Treiber installieren",
                'distribution_unknown': "Unbekannte Distribution"
            },
            'pl': {
                'title': "SwiftGuide",
                'cpu_usage': "Zużycie CPU:",
                'ram_usage': "Zużycie RAM:",
                'disk_usage': "Zużycie dysku:",
                'cpu_temp': "Temperatura CPU:",
                'memory_temp': "Temperatura pamięci:",
                'update_packages': "Aktualizuj pakiety",
                'update_system': "Aktualizuj system",
                'optimize_system': "Optymalizuj system",
                'refresh_mirrors': "Odśwież serwery lustrzane",
                'manage_drivers': "Zarządzaj sterownikami",
                'refresh_devices': "Odśwież urządzenia",
                'device': "Urządzenie",
                'driver': "Sterownik",
                'update_drivers': "Aktualizuj sterowniki",
                'install_dedicated_drivers': "Zainstaluj dedykowane sterowniki",
                'install_open_source_drivers': "Zainstaluj sterowniki open-source",
                'distribution_unknown': "Nieznana dystrybucja"
            },
            'fr': {
                'title': "SwiftGuide",
                'cpu_usage': "Utilisation du CPU:",
                'ram_usage': "Utilisation de la RAM:",
                'disk_usage': "Utilisation du disque:",
                'cpu_temp': "Température du CPU:",
                'memory_temp': "Température de la mémoire:",
                'update_packages': "Mettre à jour les paquets",
                'update_system': "Mettre à jour le système",
                'optimize_system': "Optimiser le système",
                'refresh_mirrors': "Rafraîchir les miroirs",
                'manage_drivers': "Gérer les pilotes",
                'refresh_devices': "Rafraîchir les appareils",
                'device': "Appareil",
                'driver': "Pilote",
                'update_drivers': "Mettre à jour les pilotes",
                'install_dedicated_drivers': "Installer des pilotes dédiés",
                'install_open_source_drivers': "Installer des pilotes open-source",
                'distribution_unknown': "Distribution inconnue"
            }
        }

        # Tworzenie interfejsu
        self.create_gui()

        # Inicjalizacja odświeżania zasobów
        self.update_interval = 200  # Interwał odświeżania w milisekundach
        self.refresh_resources()

    def create_gui(self):
        # Menu zmiany języka
        self.language_menu = tk.Menu(self.master)
        self.master.config(menu=self.language_menu)

        self.languages = [
            ("English", 'en'),
            ("Deutsch", 'de'),
            ("Polski", 'pl'),
            ("Français", 'fr')
        ]

        lang_menu = tk.Menu(self.language_menu, tearoff=0)
        for lang, code in self.languages:
            lang_menu.add_command(
                label=lang,
                command=lambda c=code: self.change_language(c)
            )

        self.language_menu.add_cascade(label="Language", menu=lang_menu)

        # Etykieta na nazwę dystrybucji
        self.label_distribution = tk.Label(self.master, text="", font=("Helvetica", 24), fg="green", underline=True,
                                           relief=tk.GROOVE)
        self.label_distribution.pack(pady=10)

        # Ramka na zasoby systemowe
        self.frame_resources = tk.Frame(self.master)
        self.frame_resources.pack(pady=10)

        # Etykiety na zasoby systemowe
        self.label_cpu_usage = tk.Label(self.frame_resources, font=("Helvetica", 12))
        self.label_cpu_usage.grid(row=0, column=0, padx=10, sticky="w")
        self.label_ram_usage = tk.Label(self.frame_resources, font=("Helvetica", 12))
        self.label_ram_usage.grid(row=1, column=0, padx=10, sticky="w")
        self.label_disk_usage = tk.Label(self.frame_resources, font=("Helvetica", 12))
        self.label_disk_usage.grid(row=2, column=0, padx=10, sticky="w")
        self.label_cpu_temp = tk.Label(self.frame_resources, font=("Helvetica", 12))
        self.label_cpu_temp.grid(row=3, column=0, padx=10, sticky="w")
        self.label_memory_temp = tk.Label(self.frame_resources, font=("Helvetica", 12))
        self.label_memory_temp.grid(row=4, column=0, padx=10, sticky="w")

        # Wykres kołowy
        self.figure = plt.Figure(figsize=(5, 5), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.ax.set_title("Resource Usage")
        self.chart = FigureCanvasTkAgg(self.figure, master=self.master)
        self.chart.get_tk_widget().pack(pady=10)

        # Dodatkowe opcje
        self.additional_options_frame = tk.Frame(self.master)
        self.additional_options_frame.pack(pady=10)

        # Stylizacja przycisków
        button_style = {'relief': tk.RAISED, 'bd': 3, 'font': ("Helvetica", 12)}

        # Przycisk aktualizacji pakietów
        self.button_update_packages = tk.Button(self.additional_options_frame, bg="lightblue", **button_style,
                                                command=self.update_packages)
        self.button_update_packages.grid(row=0, column=0, padx=10)
        self.button_update_packages.bind("<Enter>", lambda e: self.show_tooltip(e, self.translate(
            "Requires root password to update packages in terminal")))

        # Przycisk aktualizacji systemu
        self.button_update_system = tk.Button(self.additional_options_frame, bg="lightgreen", **button_style,
                                              command=self.update_system)
        self.button_update_system.grid(row=0, column=1, padx=10)
        self.button_update_system.bind("<Enter>", lambda e: self.show_tooltip(e, self.translate(
            "Requires root password to update system in terminal")))

        # Przycisk optymalizacji systemu
        self.button_optimize_system = tk.Button(self.additional_options_frame, bg="lightcoral", **button_style,
                                                command=self.optimize_system)
        self.button_optimize_system.grid(row=0, column=2, padx=10)
        self.button_optimize_system.bind("<Enter>", lambda e: self.show_tooltip(e, self.translate(
            "Requires root password to optimize system in terminal")))

        # Przycisk odświeżania serwerów lustrzanych
        self.button_refresh_mirrors = tk.Button(self.additional_options_frame, bg="lightgoldenrod", **button_style,
                                                command=self.refresh_mirrors)
        self.button_refresh_mirrors.grid(row=0, column=3, padx=10)
        self.button_refresh_mirrors.bind("<Enter>", lambda e: self.show_tooltip(e, self.translate(
            "Requires root password to refresh mirrors in terminal")))

        # Nowy przycisk do zarządzania sterownikami
        self.button_manage_drivers = tk.Button(self.additional_options_frame, bg="lightgrey", **button_style,
                                               command=self.manage_drivers)
        self.button_manage_drivers.grid(row=0, column=4, padx=10)
        self.button_manage_drivers.bind("<Enter>",
                                        lambda e: self.show_tooltip(e, self.translate("Manage and update drivers")))

        # Ukrywanie podpowiedzi po opuszczeniu przycisku
        self.additional_options_frame.bind("<Leave>", self.hide_tooltip)

        # Aktualizacja tekstu GUI zgodnie z językiem
        self.update_texts()

    def update_texts(self):
        self.master.title(self.translate('title'))
        self.label_cpu_usage.config(text=self.translate('cpu_usage'))
        self.label_ram_usage.config(text=self.translate('ram_usage'))
        self.label_disk_usage.config(text=self.translate('disk_usage'))
        self.label_cpu_temp.config(text=self.translate('cpu_temp'))
        self.label_memory_temp.config(text=self.translate('memory_temp'))
        self.button_update_packages.config(text=self.translate('update_packages'))
        self.button_update_system.config(text=self.translate('update_system'))
        self.button_optimize_system.config(text=self.translate('optimize_system'))
        self.button_refresh_mirrors.config(text=self.translate('refresh_mirrors'))
        self.button_manage_drivers.config(text=self.translate('manage_drivers'))

    def change_language(self, lang_code):
        self.language = lang_code
        self.update_texts()
        self.display_distribution_name()
        self.display_system_resources()

    def translate(self, text):
        return self.translations.get(self.language, {}).get(text, text)

    def show_tooltip(self, event, text):
        self.tooltip = tk.Toplevel(self.master)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{event.x_root + 10}+{event.y_root + 10}")
        label = tk.Label(self.tooltip, text=text, font=("Helvetica", 10), bg="yellow", relief=tk.SOLID, borderwidth=1)
        label.pack()

    def hide_tooltip(self, event):
        if hasattr(self, 'tooltip'):
            self.tooltip.destroy()

    def display_distribution_name(self):
        try:
            with open('/etc/os-release') as f:
                for line in f:
                    if line.startswith('PRETTY_NAME'):
                        dist_name = line.split('=')[1].strip().strip('"')
                        self.label_distribution.config(text=dist_name)
                        break
        except FileNotFoundError:
            self.label_distribution.config(text=self.translate('distribution_unknown'))

    def refresh_resources(self):
        self.display_system_resources()
        self.master.after(self.update_interval, self.refresh_resources)

    def display_system_resources(self):
        # Pobieranie informacji o zasobach systemowych
        cpu_usage = psutil.cpu_percent()
        ram_usage = psutil.virtual_memory().percent
        disk_usage = psutil.disk_usage('/').percent
        cpu_temp = self.get_cpu_temperature()
        memory_temp = self.get_memory_temperature()

        # Aktualizacja etykiet z zasobami systemowymi
        self.label_cpu_usage.config(text=f"{self.translate('cpu_usage')} {cpu_usage}%")
        self.label_ram_usage.config(text=f"{self.translate('ram_usage')} {ram_usage}%")
        self.label_disk_usage.config(text=f"{self.translate('disk_usage')} {disk_usage}%")
        self.label_cpu_temp.config(text=f"{self.translate('cpu_temp')} {cpu_temp}°C")
        self.label_memory_temp.config(text=f"{self.translate('memory_temp')} {memory_temp}°C")

        # Aktualizacja wykresu kołowego
        labels = ['CPU', 'RAM', 'Disk']
        sizes = [cpu_usage, ram_usage, disk_usage]
        self.ax.clear()
        self.ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
        self.chart.draw()

    def get_cpu_temperature(self):
        # Symulacja odczytu temperatury procesora
        return 45

    def get_memory_temperature(self):
        # Symulacja odczytu temperatury pamięci
        return 37

    def run_command_in_terminal(self, command):
        desktop_session = os.environ.get('XDG_CURRENT_DESKTOP') or os.environ.get('DESKTOP_SESSION')

        if 'GNOME' in desktop_session or 'Unity' in desktop_session:
            terminal = 'gnome-terminal'
            term_command = [terminal, '--', 'bash', '-c', f"{command}; read -p 'Press Enter to close terminal...'"]
        elif 'KDE' in desktop_session:
            terminal = 'konsole'
            term_command = [terminal, '--hold', '-e',
                            f"bash -c \"{command}; read -p 'Press Enter to close terminal...'\""]
        elif 'XFCE' in desktop_session:
            terminal = 'xfce4-terminal'
            term_command = [terminal, '--hold', '-e',
                            f"bash -c \"{command}; read -p 'Press Enter to close terminal...'\""]
        elif 'LXDE' in desktop_session:
            terminal = 'lxterminal'
            term_command = [terminal, '-e', f"bash -c \"{command}; read -p 'Press Enter to close terminal...'\""]
        else:
            terminal = 'x-terminal-emulator'  # fallback option
            term_command = [terminal, '-e', f"bash -c \"{command}; read -p 'Press Enter to close terminal...'\""]

        try:
            subprocess.run(term_command)
        except FileNotFoundError:
            messagebox.showerror("Error", f"Could not find terminal: {terminal}")

    def update_packages(self):
        self.run_command_in_terminal("sudo pacman -Syu")

    def update_system(self):
        self.run_command_in_terminal("sudo pacman -Syu")

    def optimize_system(self):
        self.run_command_in_terminal(
            "sudo pacman -Scc && sudo pacman -Rns $(pacman -Qtdq) && sudo fstrim -av && sudo pacman-mirrors --fasttrack")

    def refresh_mirrors(self):
        self.run_command_in_terminal("sudo pacman-mirrors --fasttrack")

    def manage_drivers(self):
        driver_window = tk.Toplevel(self.master)
        driver_window.title(self.translate("Manage Drivers"))
        driver_window.geometry("600x400")

        # List of devices and drivers
        self.tree = ttk.Treeview(driver_window)
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree['columns'] = ("Device", "Driver")

        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.column("Device", anchor=tk.W, width=300)
        self.tree.column("Driver", anchor=tk.W, width=300)

        self.tree.heading("#0", text="", anchor=tk.W)
        self.tree.heading("Device", text=self.translate("device"), anchor=tk.W)
        self.tree.heading("Driver", text=self.translate("driver"), anchor=tk.W)

        # Adding data to the treeview (example data)
        self.refresh_device_list()

        # Buttons for driver actions
        frame_buttons = tk.Frame(driver_window)
        frame_buttons.pack(fill=tk.X, pady=10)

        button_update_drivers = tk.Button(frame_buttons, text=self.translate("update_drivers"),
                                          command=self.update_drivers, bg="lightblue", font=("Helvetica", 12))
        button_update_drivers.pack(side=tk.LEFT, padx=10)

        button_install_dedicated = tk.Button(frame_buttons, text=self.translate("install_dedicated_drivers"),
                                             command=self.install_dedicated_drivers, bg="lightgreen",
                                             font=("Helvetica", 12))
        button_install_dedicated.pack(side=tk.LEFT, padx=10)

        button_install_open_source = tk.Button(frame_buttons, text=self.translate("install_open_source_drivers"),
                                               command=self.install_open_source_drivers, bg="lightcoral",
                                               font=("Helvetica", 12))
        button_install_open_source.pack(side=tk.LEFT, padx=10)

        button_refresh_devices = tk.Button(frame_buttons, text=self.translate("refresh_devices"),
                                           command=self.refresh_device_list, bg="lightyellow", font=("Helvetica", 12))
        button_refresh_devices.pack(side=tk.LEFT, padx=10)

    def refresh_device_list(self):
        # Example list of devices and drivers
        devices_drivers = [("Graphics Card", "NVIDIA Driver"), ("Network Card", "Intel Driver"),
                           ("Sound Card", "Realtek Driver"),
                           ("USB Controller", "Generic USB Driver"), ("Bluetooth Adapter", "BlueZ Driver")]
        for item in self.tree.get_children():
            self.tree.delete(item)
        for device, driver in devices_drivers:
            self.tree.insert("", tk.END, values=(device, driver))

    def update_drivers(self):
        self.run_command_in_terminal("sudo pacman -Syu")

    def install_dedicated_drivers(self):
        self.run_command_in_terminal("sudo mhwd -a pci nonfree 0300")

    def install_open_source_drivers(self):
        self.run_command_in_terminal("sudo mhwd -a pci free 0300")


def main():
    root = tk.Tk()
    app = SwiftGuideApp(root)
    app.display_distribution_name()
    root.mainloop()


if __name__ == "__main__":
    main()