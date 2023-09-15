import yfinance as yf
from prophet import Prophet
import matplotlib.pyplot as plt
import numpy as np

# THYAO.IS verilerini çek
df = yf.download("THYAO.IS", start="2020-01-01", end="2023-09-14")

# Veriyi Prophet formatına uygun hale getir
df.reset_index(inplace=True)
df = df[['Date', 'Close']].copy()
df.rename(columns={'Date': 'ds', 'Close': 'y'}, inplace=True)

# Prophet modelini oluştur
model = Prophet(daily_seasonality=True)
model.fit(df)

# Gelecek 30 gün için tahmin yap
future = model.make_future_dataframe(periods=30)
forecast = model.predict(future)

# MAPE hesaplama
def mean_absolute_percentage_error(y_true, y_pred): 
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100

# Geçmiş veriler üzerinden hata oranını hesaplama
MAPE = mean_absolute_percentage_error(df['y'], forecast['yhat'][:len(df)])
print(f"MAPE: {MAPE:.2f}%")

# Prophet'in kendi plot fonksiyonu ile grafik oluşturma
fig1 = model.plot(forecast)
plt.title("THYAO.IS Tahmini")
plt.xlabel("Tarih")
plt.ylabel("Kapanış Fiyatı")

# Ekstra olarak direkt matplotlib ile çizdirme
plt.figure(figsize=(10,6))
plt.plot(forecast["ds"], forecast["yhat"], label="Tahmin")
plt.plot(df["ds"], df["y"], label="Gerçek Veriler")
plt.title("THYAO.IS Tahmini")
plt.xlabel("Tarih")
plt.ylabel("Kapanış Fiyatı")
plt.legend()
plt.show()
