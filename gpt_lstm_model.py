import yfinance
import numpy as np
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Dense, LSTM
from sklearn.preprocessing import MinMaxScaler

def create_dataset(dataset, time_step=1):
    X, Y = [], []
    for i in range(len(dataset) - time_step - 1):
        X.append(dataset[i:(i + time_step), 0])
        Y.append(dataset[i + time_step, 0])
    return np.array(X), np.array(Y)

# Veri indirme ve ön işleme
data = yfinance.download("THYAO.IS", start="2021-01-01", end="2023-12-12")
data = data["Close"]
data = data.values.reshape(data.shape[0], 1)

scaler = MinMaxScaler(feature_range=(0, 1))
data = scaler.fit_transform(data)

time_step = 100
X, y = create_dataset(data, time_step)
X = X.reshape(X.shape[0], X.shape[1], 1)

# Model oluşturma
model = Sequential()
model.add(LSTM(50, return_sequences=True, input_shape=(time_step, 1)))
model.add(LSTM(50, return_sequences=True))
model.add(LSTM(50))
model.add(Dense(1))
model.compile(loss="mse", optimizer="adam")
model.fit(X, y, epochs=100, batch_size=64, verbose=1)

# Son günlerin verilerini al
input_data = data[-time_step:].reshape(1, -1)
input_data = input_data.reshape((1, time_step, 1))

# Geleceğe dönük tahminleri al
predictions = []
for i in range(30):  # 30 gün tahmin
    predicted_value = model.predict(input_data)
    predictions.append(predicted_value[0, 0])
    input_data = np.append(input_data[0, 1:, 0], predicted_value).reshape(1, time_step, 1)

predicted_prices = scaler.inverse_transform(np.array(predictions).reshape(-1, 1))
actual_prices = scaler.inverse_transform(data)

plt.plot(range(len(actual_prices)), actual_prices, label="Gerçek")
plt.plot(range(len(actual_prices)-1, len(actual_prices)+len(predicted_prices)-1), predicted_prices, label="Tahmin", color="red")
plt.legend()
plt.show()
