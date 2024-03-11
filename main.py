import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def BuyOrSell(MACD, SIGNAL, df):
    Buy = [np.nan]*1000
    Sell = [np.nan]*1000
    PLN = 1000
    crossed, hasActions = False, False
    for i in range(1000):
        if MACD[i] > SIGNAL[i]:
            if crossed is False:
                if PLN > df['Zamkniecie'][i] * 3.7 and 220 < df['Zamkniecie'][i] < 350:
                    PLN -= df['Zamkniecie'][i] * 3.7
                    hasActions = True
                Buy[i] = df['Zamkniecie'][i]
                crossed = True
        elif MACD[i] < SIGNAL[i]:
            if crossed is True:
                if hasActions is True:
                    PLN += df['Zamkniecie'][i] * 3.7
                    hasActions = False
                Sell[i] = df['Zamkniecie'][i]
                crossed = False

    return Buy, Sell, PLN


def ewm(df, MACD, span):
    alpha = 2 / (span + 1)
    vector = [np.nan] * 1000
    value = 0
    divisor = 0
    for i in range(965):
        for j in range(span):
            if MACD == 0:
                value += df['Zamkniecie'][999 - i - j] * pow((1 - alpha), j)
            elif df == 0:
                value += MACD[999 - i - j] * pow((1 - alpha), j)
            divisor += pow((1 - alpha), j)
        vector[999 - i] = value / divisor
        value = 0
        divisor = 0
    return vector


def calcMACD(EMA12, EMA26):
    MACD = [np.nan] * 1000
    for i in range(1000):
        MACD[i] = EMA12[i] - EMA26[i]
    return MACD


data = pd.read_csv("cdr_d.csv")
data = data.set_index(pd.DatetimeIndex(data['Data'].values))

EMA12 = ewm(data, 0, 12)
EMA26 = ewm(data, 0, 26)
MACD = calcMACD(EMA12, EMA26)
signal = ewm(0, MACD, 9)

data['MACD'] = MACD
data['SIGNAL'] = signal
print(data)
print("")



plt.figure(figsize=(12.2, 4.5))
plt.plot(data['MACD'], label='MACD', color='red')
plt.plot(data['SIGNAL'], label='SIGNAL', color='blue')
plt.legend(loc='upper left')
plt.title("Wykres MACD / SIGNAL")
plt.xlabel("Data")

BuySellData = BuyOrSell(MACD, signal, data)
amountOfMoney = BuySellData[2]
income = amountOfMoney - 1000
print("Total amount of money: %.2f PLN" % amountOfMoney)
print("Total income: %.2f PLN" % income)

plt.figure(figsize=(12.2, 4.5))
plt.plot(data['Zamkniecie'], label='Zamkniecie', color='black', alpha=0.35)
plt.scatter(data.index, BuySellData[0], label='Buy', marker='^', color='#4ee44e', s=50)
plt.scatter(data.index, BuySellData[1], label='Sell', marker='v', color='red', s=50)
plt.title("Wykres sygnałów kupna i sprzedaży cen zamknięcia")
plt.xlabel("Data")
plt.legend(loc='upper left')
plt.show()