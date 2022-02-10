import genshinstats as gs
import requests
from urllib.request import urlopen
from pprint import pprint


def set_cookie():
    with open('cookie.txt') as cook:
        ltoken = cook.readline().replace('\n', '')
        ltuid = cook.readline().replace('\n', '')
        gs.set_cookie(ltuid=ltuid, ltoken=ltoken)


def get_img_from_web(img):
    resource = urlopen(img)
    return resource.read()


def get_time_from_sec(seconds, lang):
    hours, ost = divmod(int(seconds), 3600)
    sec, mins = divmod(ost, 60)
    if lang == 'ru-ru':
        return f'{hours}ч:{mins}м:{sec}с'
    elif lang == 'en-us':
        return f'{hours}h:{mins}m:{sec}s'


def grab_notes(uid, lang):
    response = gs.get_notes(uid, lang=lang)

    res_text = []

    if lang == 'ru-ru':
        res_text.append(f"Сделано дейликов: {response['completed_commissions']}\\{response['total_commissions']}")
        res_text.append(f"Награда за дейлики у Катерины: "
                        f"{'собрана' if response['claimed_commission_reward'] is True else 'не собрана'}")

        res_text.append(f"Зафармлено боссов: "
                        f"{response['max_boss_discounts'] - response['remaining_boss_discounts']}"
                        f"\\{response['max_boss_discounts']}")

        res_text.append(f"Смолы: "
                        f"{response['resin']}\\{response['max_resin']}\n"
                        f"До полного восстановления: "
                        f"{get_time_from_sec(response['until_resin_limit'], lang)}")

        res_text.append(f"Экспедиции: "
                        f"{len(list(filter(lambda exp: exp['remaining_time'] != 0, response['expeditions'])))}"
                        f"\\{response['max_expeditions']}")

        for exp in response['expeditions']:
            res_text.append((get_img_from_web(exp['icon']),
                             f"    Осталось: {get_time_from_sec(exp['remaining_time'], lang)}"))
    return res_text


if __name__ == '__main__':
    set_cookie()
    uid = 705359736
    rus = 'ru-ru'
    pprint(grab_notes(uid, rus))
