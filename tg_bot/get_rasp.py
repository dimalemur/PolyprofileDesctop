import requests

headers = {"accept": "*/*",
           "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36",
           "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
           "cookie": "_ym_uid=1579441743129118070; _ym_d=1579441743; _ym_isad=1; group=181-362",
           "referer": "https://rasp.dmami.ru/session"}


def get_rasp(group):
    res = []
    session = requests.Session()
    try:
        r = session.get('https://rasp.dmami.ru/site/group?group=' + str(group) + '&session=1', headers=headers).json()
        for i in r["grid"]:  # по датам
            num = 0
            for j in r["grid"][i]:  # По непустум датам
                num += 1
                if r["grid"][i][j]:
                    para = r["grid"][i][j][0]['subject']
                    teacher = r["grid"][i][j][0]['teacher']
                    auditory = r["grid"][i][j][0]['auditories'][0]['title']
                    para_type = r["grid"][i][j][0]['type']
                    date = i
                    res.append(
                        {'para': para,
                         'teacher': teacher,
                         'auditory': auditory,
                         'para_type': para_type,
                         'date': date,
                         'num': num})
    except:
        pass
    return res

