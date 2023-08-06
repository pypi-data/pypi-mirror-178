import requests

# get key on https://currate.ru/account
key = 'df65788972e526c662489c020fba320b'


def get_course(render='BTCRUB', valut=False, key_list=False):
    if key_list:
        url = f'https://currate.ru/api/?get=currency_list&key={key}'
        req = requests.get(url).json()
        cours = req['data']
        return cours
    else:
        url = f'https://currate.ru/api/?get=rates&pairs={render.upper()}&key={key}'
        req = requests.get(url).json()
        cours = float(req['data'][render.upper()])
        cours = round(cours, 2)

        if valut:
            return str(cours) + f' {render[3:].lower()}'
        return cours