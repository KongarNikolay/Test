#Импорт библиотек.
import requests
import numpy as np
from datetime import datetime
'''
Задаю время начала работы программы для дальнейшего отделения работы за час.
Обращаюсь к api платформы binance для получения актуальных данных о ценах eth и btc.
Переменные stat- для записи цен на протяжении всего часа.
Переменные prices- для записи цен с целью нахождения коэффициента корреляции.
'''
np.seterr(divide='ignore', invalid='ignore')
startmin = datetime.now().minute
startsec = datetime.now().second
url_eth = 'https://api.binance.com/api/v3/ticker/price?symbol=ETHUSDT'
url_btc = 'https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT'
ethstat, btcstat = [float(requests.get(url_eth).json()['price'])], [float(requests.get(url_btc).json()['price'])]
ethprices, btcprices = [float(requests.get(url_eth).json()['price'])], [float(requests.get(url_btc).json()['price'])]

#Начало бесконечного цикла с проверкой времени.
while True:
    if startmin == datetime.now().minute and startsec//10 == datetime.now().second:
        ethstat, btcstat = [float(requests.get(url_eth).json()['price'])], [float(requests.get(url_btc).json()['price'])]

#Вложенный цикл для фиксации цен и нахождением коэффициента корреляции.
    while len(ethprices) != 10:
        ethprice, btcprice = float(requests.get(url_eth).json()['price']), float(requests.get(url_btc).json()['price'])
        ethprices.append(ethprice)
        btcprices.append(btcprice)
        ethstat.append(ethprice)
        btcstat.append(btcprice)
        corr = np.corrcoef(ethprices, btcprices)[0][1]

#Часть цикла, отвечающая за корректировку цены с учетом корреляции.
        if np.isnan(corr):
            corr = 0
        if ethstat[-1] >= ethstat[-2]:
            ethstat[-1] = ethstat[-2] + (ethstat[-1]-ethstat[-2])*(1-abs(corr))
        else:
            ethstat[-1] = ethstat[-2]-(ethstat[-2]-ethstat[-1])*(1-abs(corr))

#Вывод сообщения в терминал.
        if ethstat[-1] > ethstat[0]+ethstat[0]*0.01:
            print(f'Произошло повышение цены на {(ethstat[-1]-ethstat[0])/ethstat[0]}%')
        elif ethstat[-1] < ethstat[0]-ethstat[0]*0.01:
            print(f'Произошло понижение цены на {(ethstat[0]-ethstat[-1])/ethstat[0]}%')

#Очистка самого старого элемента для заполнения актуальными данными.
    del(ethprices[0])
    del(btcprices[0])