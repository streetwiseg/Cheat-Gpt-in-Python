import pandas as pd
from yahoo_fin import stock_info as si
from matplotlib import pyplot as plt

# Yahoo Finance'den THYAO.IS verisini çek
df = si.get_data('THYAO.IS', start_date="2023-01-01")

# İstenen sütunları ve satırları al
df = df[['close']]
df = df.iloc[-30:]  # Son 30 günü al

# Veriyi grafiğe dök
plt.figure(figsize=(12,6))
plt.title('Türk Hava Yolları (THYAO.IS) - Kapanış Fiyatları')
plt.xticks(rotation=45)
plt.plot(df.index, df['close'], 'co-')
plt.grid(color='gray', linestyle='--')
plt.show()
