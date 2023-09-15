import yfinance as yf
from prophet import Prophet
import plotly.graph_objs as go
import pandas as pd

def get_stock_data(symbol, start_date, end_date):
    try:
        data = yf.download(symbol, start=start_date, end=end_date)
        return data
    except Exception as e:
        print(f"Veri indirilemedi: {e}")
        exit()

def preprocess_data(data):
    data['Close'].fillna(method='bfill', inplace=True)
    data = data.reset_index()
    data = data[data['Date'].dt.weekday < 5]
    return data[['Date', 'Close']].rename(columns={"Date": "ds", "Close": "y"})

def plot_prophet_forecast(data, forecast):
    fig = go.Figure()

    # Actual past closing prices
    fig.add_trace(go.Scatter(x=data['ds'], y=data['y'], mode='lines+markers', name='Gerçek Fiyat'))

    fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat'], mode='lines', name='Tahmin Edilen Fiyat'))
    fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat_lower'], mode='lines', name='Alt Güven Aralığı', line=dict(dash='dash')))
    fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat_upper'], mode='lines', name='Üst Güven Aralığı', line=dict(dash='dash')))
    
    fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['trend'], mode='lines', name='Trend'))
    fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yearly'], mode='lines', name='Yıllık Mevsimsellik'))
    fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['weekly'], mode='lines', name='Haftalık Mevsimsellik'))

    fig.update_layout(title='Prophet Modeli ile Tahmin', xaxis_title="Tarih", yaxis_title="Fiyat")
    fig.show()

symbol = "THYAO.IS"
start_date = "2015-01-01"
end_date = "2023-12-31"  # Bu tarihi son kapanış tarihi olarak güncelledik.

raw_data = get_stock_data(symbol, start_date, end_date)
data = preprocess_data(raw_data)

# Prophet modelini oluşturma ve eğitme
model = Prophet(daily_seasonality=True, yearly_seasonality=True, weekly_seasonality=True)
model.add_seasonality(name='monthly', period=30.5, fourier_order=5)
model.fit(data)

# Kapanış tarihinden itibaren 01.01.2024'e kadar olan iş günleri için tahminde bulunuyoruz.
from datetime import datetime
last_date_in_data = data['ds'].iloc[-1]
days_to_predict = (datetime(2024, 1, 1) - last_date_in_data).days

future = model.make_future_dataframe(periods=days_to_predict, freq='B')
forecast = model.predict(future)

# Tahminleri görselleştirme
plot_prophet_forecast(data, forecast)
