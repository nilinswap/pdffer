import requests
def test():
    # test healthcheck
    r = requests.get('http://127.0.0.1:8000/api/healthcheck/')
    print(r.text, r.status_code)
    with open('test.html', 'a+') as f:
        f.write(r.text)
    assert(r.status_code == 200)

    r = requests.get('http://127.0.0.1:8000/api/find-shops/?productname=pedigree')
    assert(r.status_code == 200)
    print(r.json())

    r = requests.get('http://127.0.0.1:8000/api/items-in-shop/?shopid=7')
    assert(r.status_code == 200)
    print(r.json())

test()