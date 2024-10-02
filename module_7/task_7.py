"""
Приложение должно отдавать курс валюты к доллару используя стороннее
АПИ https://api.exchangerate-api.com/v4/latest/{currency} Например, в ответ
на http://localhost:8000/USD должен возвращаться ответ вида:

{
"provider":"https://www.exchangerate-api.com",
"WARNING_UPGRADE_TO_V6":"https://www.exchangerate-api.com/docs/free",
"terms":"https://www.exchangerate-api.com/terms",
"base":"USD",
"date":"2024-09-18",
"time_last_updated":1726617601,
"rates":{"USD":1,"AED":3.67,"AFN":69.45,"ALL":89.49,"AMD":387.39,"ANG":1.79,"AOA":939.8,"ARS":962.42,"AUD":1.48,"AWG":1.79,"AZN":1.7,"BAM":1.76,"BBD":2,"BDT":119.52,"BGN":1.76,"BHD":0.376,"BIF":2903.25,"BMD":1,"BND":1.3,"BOB":6.92,"BRL":5.5,"BSD":1,"BTN":83.83,"BWP":13.26,"BYN":3.24,"BZD":2,"CAD":1.36,"CDF":2848.38,"CHF":0.846,"CLP":923.71,"CNY":7.1,"COP":4229.19,"CRC":516.75,"CUP":24,"CVE":99.13,"CZK":22.58,"DJF":177.72,"DKK":6.71,"DOP":59.96,"DZD":132.26,"EGP":48.41,"ERN":15,"ETB":113.97,"EUR":0.899,"FJD":2.21,"FKP":0.759,"FOK":6.71,"GBP":0.759,"GEL":2.7,"GGP":0.759,"GHS":15.91,"GIP":0.759,"GMD":70.63,"GNF":8672.54,"GTQ":7.73,"GYD":209.23,"HKD":7.79,"HNL":24.8,"HRK":6.77,"HTG":131.88,"HUF":354.62,"IDR":15349.46,"ILS":3.77,"IMP":0.759,"INR":83.83,"IQD":1308.4,"IRR":42066.63,"ISK":136.88,"JEP":0.759,"JMD":157.06,"JOD":0.709,"JPY":141.61,"KES":129.1,"KGS":84.07,"KHR":4064.68,"KID":1.48,"KMF":442.29,"KRW":1320.78,"KWD":0.305,"KYD":0.833,"KZT":479.94,"LAK":21948.89,"LBP":89500,"LKR":301.69,"LRD":199.89,"LSL":17.61,"LYD":4.77,"MAD":9.74,"MDL":17.47,"MGA":4531.21,"MKD":55.28,"MMK":2100.62,"MNT":3394.43,"MOP":8.03,"MRU":39.77,"MUR":45.75,"MVR":15.43,"MWK":1742.74,"MXN":19.2,"MYR":4.27,"MZN":63.92,"NAD":17.61,"NGN":1641.54,"NIO":36.8,"NOK":10.6,"NPR":134.13,"NZD":1.62,"OMR":0.384,"PAB":1,"PEN":3.77,"PGK":3.91,"PHP":55.72,"PKR":278.24,"PLN":3.84,"PYG":7794.13,"QAR":3.64,"RON":4.47,"RSD":105.24,"RUB":90.71,"RWF":1349.97,"SAR":3.75,"SBD":8.48,"SCR":14.44,"SDG":449.19,"SEK":10.19,"SGD":1.3,"SHP":0.759,"SLE":22.6,"SLL":22599.88,"SOS":571.95,"SRD":29.74,"SSP":2803.95,"STN":22.03,"SYP":13132.3,"SZL":17.61,"THB":33.34,"TJS":10.63,"TMT":3.5,"TND":3.04,"TOP":2.32,"TRY":34.08,"TTD":6.77,"TVD":1.48,"TWD":31.9,"TZS":2713.62,"UAH":41.46,"UGX":3719.28,"UYU":40.91,"UZS":12723.87,"VES":36.77,"VND":24604.09,"VUV":117.99,"WST":2.71,"XAF":589.72,"XCD":2.7,"XDR":0.739,"XOF":589.72,"XPF":107.28,"YER":250.3,"ZAR":17.61,"ZMW":26.39,"ZWL":13.96}
}

Данные, соответственно, для доллара должны браться
из https://api.exchangerate-api.com/v4/latest/USD
"""
import re
from http.client import HTTPException

import aiohttp
from aiohttp import ClientSession


async def fetch_request(session: ClientSession, currency: str):
    """ Функция делает запрос по API """
    async with session.get(f"https://api.exchangerate-api.com/v4/latest/{currency}") as resp:
        if resp.status != 200:
            raise HTTPException({"status": resp.status, "error": resp.json()})
        return await resp.json()


async def app(scope: dict, receive, send):
    """ Типа ASGI функция """
    ___ = """
    scope: <class 'dict'> # Словарь с инфой по запросу
    {
        'type': 'http', 
        'asgi': {'version': '3.0', 'spec_version': '2.4'}, 
        'http_version': '1.1', 
        'server': ('127.0.0.1', 8000), 
        'client': ('127.0.0.1', 39730), 
        'scheme': 'http', 
        'method': 'GET', 
        'root_path': '', 
        'path': '/favicon.ico', 
        'raw_path': b'/favicon.ico', 
        'query_string': b'', 
        'headers': [
            (b'host', b'localhost:8000'), 
            (b'connection', b'keep-alive'), 
            (b'sec-ch-ua', b'"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"'), 
            (b'dnt', b'1'), 
            (b'sec-ch-ua-mobile', b'?0'), 
            (b'user-agent', b'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'), 
            (b'sec-ch-ua-platform', b'"Linux"'), 
            (b'accept', b'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8'), 
            (b'sec-fetch-site', b'same-origin'), 
            (b'sec-fetch-mode', b'no-cors'), 
            (b'sec-fetch-dest', b'image'), 
            (b'referer', b'http://localhost:8000/USD'), 
            (b'accept-encoding', b'gzip, deflate, br, zstd'), 
            (b'accept-language', b'ru,ru-RU;q=0.9,en;q=0.8')
        ], 
        'state': {}
    }
    receive: <class 'method'> <bound method RequestResponseCycle.receive of <uvicorn.protocols.http.h11_impl.RequestResponseCycle object at 0x78b64cff1ed0>> # Кортеж с типами или функцией для приема данных
    send: <class 'method'> <bound method RequestResponseCycle.send of <uvicorn.protocols.http.h11_impl.RequestResponseCycle object at 0x78b64cff1ed0>> # Кортеж с типами или функцией для отправки данных
    """  # Это дает uvicorn с запроса в браузере.  # noqa

    if scope.get("type") != "http":
        raise ValueError("Request type not supported")

    if scope.get("method") not in ("GET",):
        raise ValueError("Request method not supported")

    headers = scope.get("headers")

    async with aiohttp.ClientSession() as session:
        decode_headers = dict()

        for header in headers:
            decode_headers[header[0].decode()] = header[1].decode()

        param = decode_headers.get("referer")

        if param:  # При запросе param = None
            result = str(await fetch_request(session, param.split("/")[-1]))
        else:
            result = "No params"

    await send({
        "type": "http.response.start",
        "status": 200,
        "headers": [(b"Content-Type", "application/json".encode()),
                    (b"Content-Length", str(len(result)).encode())],
    })

    await send({
        "type": "http.response.body",
        "body": str(result).encode(),
    })


if __name__ == '__main__':
    import uvicorn  # http://localhost:8000/USD
    uvicorn.run(app=app, host="0.0.0.0", port=8000)
