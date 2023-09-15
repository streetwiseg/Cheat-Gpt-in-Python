import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Flatten, Attention
from tensorflow.keras.layers import Input
from sklearn.preprocessing import RobustScaler


def create_dataset(dataset, time_step=1):
    X, Y = [], []
    for i in range(len(dataset) - time_step - 1):
        X.append(dataset[i:(i + time_step), 0])
        Y.append(dataset[i + time_step, 0])
    return np.array(X), np.array(Y)

# Veri indirme ve ön işleme
data = yf.download("THYAO.IS", start="2020-01-01", end="2023-12-12")
data = data["Close"]
data = data.values.reshape(data.shape[0], 1)

scaler = RobustScaler()
data = scaler.fit_transform(data)

time_step = 100
X, y = create_dataset(data, time_step)

# Model oluşturma
query_input = Input(shape=(time_step, 1))
value_input = Input(shape=(time_step, 1))
attention = Attention()([query_input, value_input])
attention_flattened = Flatten()(attention)  # Eklenen kısım
output = Dense(1)(attention_flattened)

model = Model(inputs=[query_input, value_input], outputs=output)

model.compile(loss="huber", optimizer="rmsprop")
model.fit([X, X], y, epochs=100, batch_size=64, verbose=1)

# Son günlerin verilerini al
input_data = data[-time_step:].reshape(1, -1, 1)
query_input_data = input_data
value_input_data = input_data

# Geleceğe dönük tahminleri al
predictions = []
for i in range(30):  # 30 gün tahmin
    predicted_value = model.predict([query_input_data, value_input_data])
    predictions.append(predicted_value[0, 0])
    
    # Tahmin edilen değeri giriş verisine ekleyip ilk girişi atma
    query_input_data = np.concatenate((query_input_data[0, 1:, :], predicted_value.reshape(1, -1)), axis=0).reshape(1, time_step, 1)
    value_input_data = query_input_data


# Eksik olan kısımlar
actual_prices = scaler.inverse_transform(data[-30:])
predicted_prices = scaler.inverse_transform(np.array(predictions).reshape(-1, 1))

# Plot a graph of the real and predicted prices
plt.figure(figsize=(10, 6))
plt.plot(range(len(actual_prices)), actual_prices, label="Gerçek")
plt.plot(range(len(actual_prices), len(actual_prices) + len(predicted_prices)), predicted_prices, label="Tahmin", color="red")
plt.legend()
plt.title("THYAO.IS Stock Price Prediction")
plt.xlabel("Gün")
plt.ylabel("Fiyat (TL)")
plt.grid(True)
plt.show()
