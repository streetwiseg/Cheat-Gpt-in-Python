import yfinance as yf
import time
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk, StringVar
from threading import Thread
import matplotlib.backends.backend_tkagg as tkagg
from matplotlib.patches import FancyArrowPatch

stop_thread = False

# Örnek portföy
portfoy = {
    "THYAO.IS": [245.28, 784],
    # Diğer hisseler...
}

def draw_graph(labels, values, colors, current_prices, canvas):
    plt.clf()
    bars = plt.bar(range(len(labels)), values, color=colors, tick_label=labels)
    plt.ylabel("Kar/Zarar Oranı (%)")
    plt.title("Hisse Senedi Kar/Zarar Oranı")

    for i, (bar, hisse, current_price, kar_zarar) in enumerate(zip(bars, labels, current_prices, values)):
        height = bar.get_height()

        # Anlık fiyat
        plt.text(i, -7, f'{current_price:.2f}₺', ha='center', va='top', fontsize=20, color='black', fontweight='bold')

        # Ok işaretlerini ekleyelim
        if height > 0:
            arrow = FancyArrowPatch((i, height+1), (i, height+2), mutation_scale=15, color='white', arrowstyle='->')
        else:
            arrow = FancyArrowPatch((i, height-1), (i, height-2), mutation_scale=15, color='white', arrowstyle='->')
            plt.gca().add_patch(arrow)

        # Kar/Zarar metni
        if kar_zarar > 0:
            text = f"%{kar_zarar:.2f} Kar"
            plt.text(i, -12, text, ha='center', va='top', fontsize=15, color='green', fontweight='bold')
        else:
            text = f"%{-kar_zarar:.2f} Zarar"  # Negatif değer pozitife çevrilir.
            plt.text(i, -12, text, ha='center', va='top', fontsize=15, color='red', fontweight='bold')

    canvas.draw()

def hisse_takip(refresh_time: str, canvas: tkagg.FigureCanvasTkAgg):
    global stop_thread

    while not stop_thread:
        labels, values, colors, current_prices = [], [], [], []
        for hisse, detay in portfoy.items():
            alis_fiyati, miktar = detay
            try:
                data = yf.Ticker(hisse)
                anlik_fiyat = data.history(period="1d")["Close"].iloc[-1]
                kar_zarar_orani = ((anlik_fiyat - alis_fiyati) / alis_fiyati) * 100

                labels.append(hisse)
                values.append(kar_zarar_orani)
                colors.append('g' if kar_zarar_orani > 0 else 'r')
                current_prices.append(anlik_fiyat)
            except Exception as e:
                print(f"{hisse} için veri çekilemedi: {e}")

        draw_graph(labels, values, colors, current_prices, canvas)
        time.sleep(int(refresh_time))

# Tkinter Penceresi
root = tk.Tk()
root.title("Hisse Senedi Takip")
root.geometry("390x812")
root.resizable(True, True)

# Yenileme süresi girişi
refresh_time_var = StringVar(value="5")
refresh_time_label = ttk.Label(root, text="Yenileme Süresi (örn: 5 saniye):")
refresh_time_label.grid(row=0, column=0, sticky="w", padx=20)
refresh_time_entry = ttk.Entry(root, textvariable=refresh_time_var)
refresh_time_entry.grid(row=0, column=1, sticky="ew", pady=10, padx=20)

# Alarm başlat düğmesi
alarm_baslat_button = ttk.Button(root, text="Alarm Başlat", command=lambda: Thread(target=hisse_takip, args=(refresh_time_var.get(), canvas)).start(), width=15)
alarm_baslat_button.grid(row=3, column=0, pady=20, padx=20, sticky="ew")

# Alarm bitir düğmesi
alarm_bitir_button = ttk.Button(root, text="Alarm Bitir", command=lambda: setattr(root, 'stop_thread', True), width=15)
alarm_bitir_button.grid(row=4, column=0, pady=10, padx=20, sticky="ew")

# Grafik widget'i
fig = plt.figure(figsize=(7, 5), facecolor='white')  # Arka plan rengi beyaz olarak ayarlandı
canvas = tkagg.FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(row=1, column=0, columnspan=2, pady=60, sticky="nsew")

root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(1, weight=1)

# Temalar
temalar = {
    'Açık': {
        'bg': 'white',
        'fg': 'black',
        'btn': 'lightgrey',
        'highlight': 'blue'
    },
    'Koyu': {
        'bg': 'black',
        'fg': 'red',
        'btn': 'grey',
        'highlight': 'cyan'
    }
}

# Mevcut tema
mevcut_tema = 'Açık'

def tema_degistir(tema_adı):
    global mevcut_tema
    mevcut_tema = tema_adı
    tema = temalar[tema_adı]

    root.configure(bg=tema['bg'])

    style = ttk.Style()

    style.configure('TLabel', background=tema['bg'], foreground=tema['fg'])
    style.configure('TButton', background=tema['btn'], foreground=tema['fg'])

    for widget in root.winfo_children():
        if isinstance(widget, tk.Label):
            widget.configure(bg=tema['bg'], fg=tema['fg'])
        elif isinstance(widget, tk.Button):
            widget.configure(bg=tema['btn'], fg=tema['fg'], activebackground=tema['highlight'])

def ayarlar_penceresi():
    ayarlar = tk.Toplevel(root)
    ayarlar.title('Ayarlar')

    ttk.Label(ayarlar, text="Tema Seçin:").grid(row=0, column=0, padx=10, pady=5, sticky='w')
    tema_secim = ttk.Combobox(ayarlar, values=list(temalar.keys()), state="readonly", width=15)
    tema_secim.grid(row=0, column=1, padx=10, pady=5)
    tema_secim.set(mevcut_tema)

    def uygula():
        tema_degistir(tema_secim.get())
        ayarlar.destroy()

    uygula_butonu = ttk.Button(ayarlar, text="Uygula", command=uygula)
    uygula_butonu.grid(row=1, column=0, columnspan=2, pady=10)

    ayarlar.mainloop()

# Ayarlar Butonu
ayarlar_butonu = ttk.Button(root, text="Ayarlar", command=ayarlar_penceresi)
ayarlar_butonu.grid(row=5, column=0, pady=10, padx=10, sticky="ew")

# İlk temayı uygula
tema_degistir(mevcut_tema)

root.mainloop()