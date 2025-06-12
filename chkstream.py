import re
import json
import socket
import ssl
import urllib.request
import random

# For Hong Kong (CN-HK) Region Only
# as a Hong Kong University Student
# 祇限香港地區查詢
# (身為香港大學生)

# The urllib request module was used replacing HTTPie due to the outdated
# insecure renegotiation being used on the EdUHK website.
# 由於EdUHK嘅website仍在使用insecure renegotiation，已經將HTTPie改為urllib request

# config
crawl_timeout = 10
crawl_ua_curl = "curl/8.7.1"
crawl_ua_browser = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"

# Stream Check (Python Version)
# 媒體平台可使用狀態查詢系統 (Python版本)

# functions
# print colours
class pcolour:
    end = "\033[0m"
    bold = "\033[1m"
    red = "\033[31m"
    green = "\033[32m"
    yellow = "\033[33m"
    blue = "\033[34m"

# media cookie (hardcoded)
media_cookie = "grant_type=urn%3Aietf%3Aparams%3Aoauth%3Agrant-type%3Atoken-exchange&latitude=0&longitude=0&platform=browser&subject_token=DISNEYASSERTION&subject_token_type=urn%3Abamtech%3Aparams%3Aoauth%3Atoken-type%3Adevice\n'authorization: Bearer ZGlzbmV5JmJyb3dzZXImMS4wLjA.Cu56AgSfBTDag5NiRA81oLHkDZfu5L3CKadnefEAY84'\n\"AMCVS_CFAF55745DD2611E0A495C82%40AdobeOrg=1; s_pvDate=2021%2F06%2F17; s_cc=true; wowow2_mem_guide=visited; wowow2_MGSID=4440260aa4011f0162393267600028772; wowow2_MGSID_AuthTicket=fd28d6b1349fd2e672af97370c4eaa4d42a4fdf2; demographics=01301; u-demographics=BAD81A3D84A07B32EC333E1BEFE72F10; wowow2_sls=1; wowow2_ext_MGSID=4440260aa4011f0162393267600028772; wod_auth=CfDJ8D-H-2bqdw1AjJk3TVDbKLaZydf2DfrFVw51ktRQdWqpml0TtbTZudBFfOd-ReyghPDX8aTlo8Ys_shmm-Nv7GBeFMrsM-pUufuTmiSYX7yEa5D9h6YDRA7OviqDLyAKDHUpZifwVToT1vKg_A9G1UMaS0exxBx_TcoOe9U_3Ex4HAb98A5106gj-6ztKoSPVxxKEneO1JdtLe3uVCZ_HMqh6oCeJCZvvlOVN_w_lECjchu58NGtZWmV3mE02DZ-SK5X6xT6GTetvr5EvFKJAxNfaNvkHoS_e-20dz-c-8huuTuvXTg3-i5OAQSyG5UQ_VRz-qqMVV-JR2xmRyxPuEifLU3Iy_B0IWvE65YZlexmL2KVEP745nB7-wCRuVzu9zEdO1IRHQ3fruQ_8RJqb0g; wod_secret=1e4c8db631cd4d2f986102a87811e8e5; s_ips=1010; s_sq=%5B%5BB%5D%5D; x_xsrf_token=1623934360j1T6bPwpGswOnPp3IrcHFZ5vPMo8LE; s_gpvPage=www%3Awowow%3Amember%3Alogin.php%3Ard%3Ahttps%3A%2B%2Bwww.wowow.co.jp%2Bsupport%2Bregist_self.php; s_tp=1010; s_ppv=www%253Awowow%253Amember%253Alogin.php%253Ard%253Ahttps%253A%2B%2Bwww.wowow.co.jp%2Bsupport%2Bregist_self.php%2C100%2C100%2C1010%2C1%2C1; s_nr365=1623934367877-Repeat; AMCV_CFAF55745DD2611E0A495C82%40AdobeOrg=-432600572%7CMCIDTS%7C18796%7CMCMID%7C30796674720677405047057880592301178864%7CMCOPTOUT-1623941567s%7CNONE%7CvVersion%7C4.5.2\"\n\"Accept: application/json;pk=BCpkADawqM3ZdH8iYjCnmIpuIRqzCn12gVrtpk_qOePK3J9B6h7MuqOw5T_qIqdzpLvuvb_hTvu7hs-7NsvXnPTYKd9Cgw7YiwI9kFfOOCDDEr20WDEYMjGiLptzWouXXdfE996WWM8myP3Z\"\n{\"device_identifier\":\"2B3BACF5B121715649E5D667D863612E:2ea6\",\"deejay_device_id\":190,\"version\":1,\"all_cdn\":true,\"content_eab_id\":\"EAB::ea0def9a-afa3-4371-b126-964e1c6bea89::60515729::2000604\",\"region\":\"US\",\"xlink_support\":false,\"device_ad_id\":\"7DC1A194-92E0-117A-A072-E22535FD3B8D\",\"limit_ad_tracking\":false,\"ignore_kids_block\":false,\"language\":\"en\",\"guid\":\"2B3BACF5B121715649E5D667D863612E\",\"rv\":838281,\"kv\":451730,\"unencrypted\":true,\"include_t2_revenue_beacon\":\"1\",\"cp_session_id\":\"D5A29AC4-45C5-28EC-2D90-310D8B603665\",\"interface_version\":\"1.11.0\",\"network_mode\":\"wifi\",\"play_intent\":\"resume\",\"lat\":23.1192247,\"long\":113.2199658,\"playback\":{\"version\":2,\"video\":{\"codecs\":{\"values\":[{\"type\":\"H264\",\"width\":1920,\"height\":1080,\"framerate\":60,\"level\":\"4.2\",\"profile\":\"HIGH\"}],\"selection_mode\":\"ONE\"}},\"audio\":{\"codecs\":{\"values\":[{\"type\":\"AAC\"}],\"selection_mode\":\"ONE\"}},\"drm\":{\"values\":[{\"type\":\"WIDEVINE\",\"version\":\"MODULAR\",\"security_level\":\"L3\"},{\"type\":\"PLAYREADY\",\"version\":\"V2\",\"security_level\":\"SL2000\"}],\"selection_mode\":\"ALL\"},\"manifest\":{\"type\":\"DASH\",\"https\":true,\"multiple_cdns\":true,\"patch_updates\":true,\"hulu_types\":true,\"live_dai\":true,\"multiple_periods\":false,\"xlink\":false,\"secondary_audio\":true,\"live_fragment_delay\":3},\"segments\":{\"values\":[{\"type\":\"FMP4\",\"encryption\":{\"mode\":\"CENC\",\"type\":\"CENC\"},\"https\":true}],\"selection_mode\":\"ONE\"}}}\n_h_csrf_id=7409960e2a4c5cacdf4ad0b40d02f1f419ec19a5cf5efde88838f56154d36dab; _hulu_uid=201194534; _hulu_e_id=f49WXX_ScBCK8xPpPfT7JA; _hulu_bluekai_hashed_uid=c0e4c9575742fe7542cbc0eb475f6585; _hulu_dt=CJDtoJLb0AF7xJTRQLO7v6aOJ7I-dqaPkHo8l6LPP1bcLnYA_A--PkyDXJwUJG3o0hWDnKkYILcL_%2FBrDxIXAlyoHDx14NHeeJfctC29Xzsx4tNJedYQZuy1w%2FZLgczSI3qt8nirWwAobE0wmi8OhdO_%2FLmh7Ln7bRqner5sqC0xIsSvDYv%2FkpKdrRyPCzLX0GNhWEcU1sjqGNJhcNySujfMh%2Fq%2FfTe6Gz9vb7rtjpGCRWKNdPWG3vSyNnOKd8J6HLZIWQpVkUuvYqF_D0HrdhVRRAEAu9cpfgW%2F_bPgaG_mWKAt3%2F9_iF0ksf1trvm4Vw01HA1ufRMi1kxTrMfcQ%2FRfmsIL0lVIoUPtdCNWJuQ_xyncNryUK27dYEBI1ZBKpVWk9QO_0F_6XtIjq2etmGLG98e%2Fx74yefigQ7aQACuedPlvDRHOm2Dx7ElxcIBzKGnOBtLt66wPzOHIxa94awZzpjhjBjEJ4JdhngP0DSsaFGzvzXlio9QivBgeAh8FgAl%2F3odQ8mLstQH1Cslz1NiPU9rruTuGmLASk%2F%2FLpYUyOYUOJl%2FfD7K02Xq7nF3MnWv4PTC79Gl5AoxZeGKy9WBFQAVCUKI6OYx_oc3I1McQXBNK1GFkegEHahWO7qUgA6547ucmytiM0llw%2Fyvv8M%2FTuIebc0fGdeV6Ym2AK5ElvBmqMCPVUTrAOP1qK8JC7CkZQ6Cm5U7qw8AEyRrpPfNqdZK00Abne0RAyrbthfzy7bfoMktRMqiP704AgaT3M_YRn9SshQ081Fx8uHI1GE5YmJvo7umw0ZtV0gGxXexxtaZQgqrAx75uyLoWyG2uvuvNCmufWvJrNJ9uEAiXIrghWdtQYYXqbVjFTa6gt4DKKpiDW_J39vf6EeSQyu0jCzlFYrVGmweLDbVXWLk_zeqUBzcbuB4-; _hulu_pid=201194639; _hulu_pname=Bill%20Gates; _hulu_is_p_kids=0; guid=051BDA2EDE200DE1E7C1E48FBE9BE703; AMCVS_0A19F13A598372E90A495D62%40AdobeOrg=1; _hulu_uname=Bill+Gates; _hulu_utype=plus%3Aios; _hulu_pgid=3; _hulu_plid=70828; _hulu_psh=0; _hulu_psvh=0; _csrf_id=75e11783d40cc993792dad9e0816af9443362c9b53e92ef7797f0355a8b95d68; s_cc=true; _hulu_assignments=eyJ2MSI6W3siZSI6OTc5LCJ0IjoyNjk3LCJuIjoiaHVsdV8xMzU3OF93ZWxjb21lX2Jfd2hpdGVfY3RhIn1dfQ%3D%3D; _hulu_hbc=1624194121035; _hulu_session=k2JE4gPqVlM3LtStdErz12jw0U8-lI3d5nWPy2Q8W4tMGGbtzg--atiahdg9XQKv5WqAhkS9t7POnyCifqFVkGE3tpGy6tEMl9UPrfBQ6_RsNDR%2FcGVnz%2FPILVruTsa58eLUq5zdtqFb9nNbvQ53lrRn3WYess8Gs1IMI6Hxj1Zkknh0FbxUcS18um%2FqAeWcyLKTSjJ_FtHwRBzw34fufh0UgyvdcygP_yif9jJ4vLy7W7vhyhRVS_9wLMi206arcdFKfgMNglamSjyxVcBJFEzs91vHiZyK0UEfnpzCpKCujWu38bUIiGbHfpR06kuQ4P80OBp7PXFZ5U3w%2FQT5PzfCdutdQoHbjqw_W8yCdwp0HTzdwmDuRCGKrqBk6KArHtLZA4zFAoovr_d9dKWsZDnWXMc4RjomDzNRP0cjyAa7vXnV_viWf3BoGRuuyBLEwEak%2Fj86fHOW1frY94bdSSQidgZck_8yKl6zHY8Uk_e_TMMrItdSRGO7NwkoWDjl_%2FtbTcahUBhHqVTSOTnVO3U1IzIWW3o8JA0568k92g5roSTKBI6EUD9SktBFcfrzPszL5CJtjt_FuWp9agQyLcQODapMEYhq9USPsnM9MWJatxpHhgY%2FlFmOdOx6z1QK8fBdYuWSK9ExYmr9xYh10DzsO7tYlJn0P6pq65Zv1_US61CVtsHNHOXr4DEsvWuAJGi17f6s2boUrKJiCIxQOuJMwZiJTpjkW2eTH3oeg4nisbUlnb15IrdMdtdwTG26vOGjG5ByHeXZ721mVZfNbm7ghx0nSrKLb_gmM0mdtUM9qyTSB_cyJM5aqQB2LctzuaEaIeLKkUIlXIPGsSiLSDmNX3HGRLdLKuQl1Yoq_7TNkv%2FRXN7t7ybUTTTo6cFsTp7JbbS4%2Ft3HT04m3jY9UhBN80l29hwft0M3eeE2tASFnn90KZs8jd43l0xHu4on9Vbsd2cjHbPi2FyF_utXqI0OUBAQltuNyC9mXW755KbryCErZnb7xkt3VrK5eqdPS70ZdLgfGtID4NGrPCCLgMsPEqNwK4pKbK1kH4exmksjDnwyj5YVIRYywj9LoipgKEnFJzD6IUqhB5ybA8bKLc8qFXPJbUZnmn_u6lEwtUh_heet1mu5; bm_mi=C7288944D1321EF6C7049F7B9FA20378~0QSp6QjTtRiEjeSjIpWX2cS6CplgPGcGlXazUQnps1dJF2Nv2BNe3oqUpw+u+oCKfOR1BMCbrHb3VOpz5cOed+rbDVzxclxodIKKJC/ZXNjTo15F5PC9vIkYqgNSAk5yU4gWV2SaLwT+JBsOydzNcPRwuY+z6+gkCw6eqGSQx0kZQfE/d+xMaJiStH+uUD6tNyCA4nIps5JpeEaNLzWjwuE4EaOuOCC8yZyLh7x8W0AsdEdkeEQEz1GLYgJmwnS0954PSECxwS5zQyqMB2vJSg==; ak_bmsc=72FC22728A28C7F3DC94376C9C3554F3~000000000000000000000000000000~YAAQTXZiaOhghx96AQAAWha6KQwV7/I2tiArb8nII7tGbF20EEmg3lH9OsRYJE/tzpyywpT3eeD2Td/IVRmVmurRrQ5Vp+YIs++zYbvI4XVQKXRtmv7mM0lDDhqOeR+dpM4CRBdT7Vv9eNYchfzID5cd7xzgYLqubfP70LR0zfaTubjfFdjMvawyOIQwAPfaErrsX0iiEpmy4G/nonxdTGB3bBQ7kAYoVpWAtAon8QoYoRx5HCjFzE/c7TKqZ/iDXcUq5tvZjptzNfnF5iChraxr5wlkiDh9eyWWCk/rTJozMeI1tX1HwH+In8iv4T7cTtZJh5MRq+IH/bXrwJtty51jvGu8B5mCaDUsHZKWRtEJpJMp7ta5o1nHrAQuiymFNRMEIPDqxDLbAA==; XSRF-TOKEN=8335e11a-8c68-483e-9a80-2d7f79856b44; AMCV_0A19F13A598372E90A495D62%40AdobeOrg=-408604571%7CMCIDTS%7C18799%7CMCMID%7C59607436576250353666502608938647993204%7CMCAID%7CNONE%7CMCOPTOUT-1624204908s%7CNONE%7CvVersion%7C4.6.0; bm_sv=A5945B0C79D7AA8B5A878BCDD21707C7~uii8SKBBdtZtDcwf0sopMCO3ldEL6L8p4F4PuMBF2DW9zw1kwgQO3b0dRgkojZaH5rNoMisLrt4Fz4c+JeL/zj4YKNr/3DOgt3wK7/tUvEZZPpLFFMlSPjel2Y7D3Gt7N8JMW42t9Gj2gAXFO4nCFA==; _hulu_metrics_context_v1_=%7B%22cookie_session_guid%22%3A%228d152d975a317957990c7d80022cd87c%22%2C%22referrer_url%22%3A%22%22%2C%22curr_page_uri%22%3A%22app%3Awatch%22%2C%22primary_ref_page_uri%22%3A%22urn%3Ahulu%3Ahub%3Ahome%22%2C%22secondary_ref_page_uri%22%3Anull%2C%22curr_page_type%22%3A%22watch%22%2C%22primary_ref_page_type%22%3A%22home%22%2C%22secondary_ref_page_type%22%3Anull%2C%22secondary_ref_click%22%3Anull%2C%22primary_ref_click%22%3A%22Demon%20Slayer%20Kimetsu%20No%20Yaiba%22%2C%22primary_ref_collection%22%3A%22282%22%2C%22secondary_ref_collection%22%3Anull%2C%22primary_ref_collection_source%22%3A%22heimdall%22%2C%22secondary_ref_collection_source%22%3Anull%2C%22ref_collection_position%22%3A0%7D; metrics_tracker_session_manager=%7B%22session_id%22%3A%22051BDA2EDE200DE1E7C1E48FBE9BE703-4040a0e1-3ec2-4b14-b7d2-85115b386d30%22%2C%22creation_time%22%3A1624197697579%2C%22visit_count%22%3A1%2C%22session_seq%22%3A11%2C%22idle_time%22%3A1624197708635%7D\n{\"query\":\"mutation refreshToken($input: RefreshTokenInput!) {\\n            refreshToken(refreshToken: $input) {\\n                activeSession {\\n                    sessionId\\n                }\\n            }\\n        }\",\"variables\":{\"input\":{\"refreshToken\":\"eyJ6aXAiOiJERUYiLCJraWQiOiJLcTYtNW1Ia3BxOXdzLUtsSUUyaGJHYkRIZFduRjU3UjZHY1h6aFlvZi04IiwiY3R5IjoiSldUIiwiZW5jIjoiQzIwUCIsImFsZyI6ImRpciJ9..qnHbUZQXPtEv5n5s.kKfiwHFTT-u6b92OIDNGE8HBbJd_1EsCx3apaucHSvIj44bbLVvwDWkvtnD67qgtqY08_ohitM51nawYdPbLOE45hA2j7d7kaksYtDcj3rVg_Vys_Mxjs_HMdIDn8MdY71SqRl-f9848oDdzTrEswgW-fYqzWjY1Ur7mwmqDTumWWDhzjWCl_-aQWJuHp4CD8UdvfcIr7kVAbJR4_NL0VN69cYCMnBslxo53zNSc8v2MWYsENLxvpU1RD38EoJRjAWCYYmToeqNkxehEemn_qDJNxLdilp40ca4xcLCOCQgjl2hQnLDL4SFj6lIo1Gz2nWI8SOtQECia3Y9Rm778rjfPt2VYsmGux_rnRjipjiCnSSjy2VEjxT_BYFTpfxMU51OqlaqUB5v7xpjAmiQCA20GZcmJBizrHwjRKyFLn7b5jM72_MUE84jruVbgt7PR8XqFAmn76w8SnkgIdZvmnyHHsDB66jGBaRRY91Jrnx5RMyavsYTQRb_JMmCXvNZY1DDpAMuRTOB98uoRdhGsdItROJgKrdY_dyNlmp3BU9mi64Q76JQsRQpqgpIHJParHprX1CSGURa57SP0lo8RUPzwW2c0XJWITicYwvSbpuMGKwFyHECvY7-LqFwrS_VgQzYwv7zxJ_DGSqGGkwLpUAtJgBQ5tZEIeDFUVy_hy8O0Pxu35sHwmOqE3YGvUZagDKU6A_WfXNgP5HX9A9myI57iGxDte2xIEdVjsrEi8OaDByJ9epWMJH97yovmRjw9sv6eJIlfRqHmNi7p9ZFP2seOSaMweVqY4U7gGdNL33kh4VN8QrDD7Iz9l9499lmrB5Zr6jOVDSYJ20PhfXyLWG8WyxY8bPg2kI9xCO295ngti58cyKRteZ_mmGaFoaJjQGNHYKBoFzDCWts4o7T8jgjsMarTx30BjAr09ruyp5zd6C743iaVPQKdhA3gx8gPWlQhpHDoqXx5c6gosiS_Ty8i_pS5eGHuVqiz9Qv4Nb-uZXqgvcWEcbHYxc76dx9sLUzulOY66AdWUWXQc6G6z-XbgkwmK-BpaQrVZcoAhU_Ci69SBHD_XR9eN6XOAUVh2Bsu7Bgb8q5fFJn7gyz2oqujBWpDKM8hraV_IPU8geGOPUQyMetepIFY1SjeOqVM_h6ng9LehWQ0aQiPOn-BDlXhEVCjQDtAmxrW6tj0Hc7InvURGUaL97y22A2MvNh9eaG_h6ztzpm-iBdCkOzdOihrzXZqZmHhaoZADxYgZTL0UDnXBH6CtPuWiBfTycQbXNyjM9nm4y0EsDl14asIUqymDzTq-S9ZYfu2QzLMZXaw4khhLZ7bYsHNaIWd22phXhUxIJQb3Sb_xOlaWlEjWebTw-wWKJ9KQEcroSuKCIKoLLhb21qw_WX8-IN0qlWrk02UJJR1Kz7hoa0Da5QF_yQgkqk4dE_JNn9IxnQOFAEKqASmwORW-3bAH2SqEUhSAUvOIZjVAgO721aUF5TDgiEjLJvfQcEWmETjcHFFwzfnoKVjMRFOj_zHwrsZ-OoPst0D14GT4cs26M4yi7d15Pt28v2CNSHWug4gh89IT5EtkV_wlzuTyBc9hgronT5kN7v6-DHyYPSDh4vfT4BckqzMsi4QxsMBUZ0hYBojdODoW40ckBTncizRf5QqObzfk3WSmv4y7zoseY4c4erV7k6O_O9_op8mcRcVyMDiWchMT4SmrFRP-tBbTmIkp18F3YUIOdPzY1m40c3DdkaP-TrQlNsbpfPSpZURKT97BoZjy3JGofFr--zNvBHUS1lxXxkOkLXCEHSudnBsqSoc5HJP7-qjwfoqCV76E_iZ9zjWNrNN6X3NnYmRfZ8dso8KZfaGBf6u_90qpg6ZBtRa9GzyWS9qBJRi95408UqK5R9m5IDZtQ2B_J7yhMBN2MWXuyBmJoq0_a1BUGXmF50z4avcHbQWQdD-Yf76z1xMD1pLvgb8b9rk6wxxda94XnyvOmX8orY8O7wJXEKSygDm2nKE4gBK1apAi0SbKdXcAdnQfh4hbfcJDmWr5NBjjdKuOzJdnTI8voEFQB4BiUsP2t40orQRFxu-gdmpnGGiApgsojcvCx25ev1TFK0845-NmK0rY2Nvd9o_NBulWnSsWJcGKzODceqi3qaxoQ9U90tOFnipqvJ3lu3BTJWqMedQSrQDzbiUegeAjQd9w2Fz7LLNDSY0V4UO764pCVDJKJBLByifkOuFrkiUJwBVe8LIb7raFYO9P9HOUw1fmcH1rsZajPuWQJQBaQMLm-gon7uJpORZUuYyovv4MBWtJDl_VmIUI4mPwRL8YrzfvuzdMKwCw6ri6zKCbxkBsocALSVBJACPIRvvi4SgeV_F--efROD0.UjQJShStniHGbdb5WwRH5Q\"}}}\n{\"query\":\"mutation refreshToken($input: RefreshTokenInput!) {\\n            refreshToken(refreshToken: $input) {\\n                activeSession {\\n                    sessionId\\n                }\\n            }\\n        }\",\"variables\":{\"input\":{\"refreshToken\":\"ILOVEDISNEY\"}}}\ngrant_type=urn%3Aietf%3Aparams%3Aoauth%3Agrant-type%3Atoken-exchange&latitude=0&longitude=0&platform=browser&subject_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJlM2NkMTFmYi1hZjA4LTQ4Y2UtOGJmNi03ZTVhNDdmNDdmMzUiLCJhdWQiOiJ1cm46YmFtdGVjaDpzZXJ2aWNlOnRva2VuIiwibmJmIjoxNjMwNDIxNDc0LCJpc3MiOiJ1cm46YmFtdGVjaDpzZXJ2aWNlOmRldmljZSIsImV4cCI6MjQ5NDQyMTQ3NCwiaWF0IjoxNjMwNDIxNDc0LCJqdGkiOiI0NGFhNWE4NC01YzdmLTQzOTMtYWFjNy1kN2U5OGM3MzU2NmMifQ.3NIPcVfIPgkDsJJoBD2RS9MK86i-xuIABKcYNl1oCCJJ2bzTiK8cgdPZNrpah7EMzIesVQdVet4Epxpy99jw2w&subject_token_type=urn%3Abamtech%3Aparams%3Aoauth%3Atoken-type%3Adevice\n{\"query\":\"mutation registerDevice($input: RegisterDeviceInput!) {\\n            registerDevice(registerDevice: $input) {\\n                grant {\\n                    grantType\\n                    assertion\\n                }\\n            }\\n        }\",\"variables\":{\"input\":{\"deviceFamily\":\"browser\",\"applicationRuntime\":\"chrome\",\"deviceProfile\":\"windows\",\"deviceLanguage\":\"zh-CN\",\"attributes\":{\"osDeviceIds\":[],\"manufacturer\":\"microsoft\",\"model\":null,\"operatingSystem\":\"windows\",\"operatingSystemVersion\":\"10.0\",\"browserName\":\"chrome\",\"browserVersion\":\"96.0.4664\"}}}}\ngrant_type=urn%3Aietf%3Aparams%3Aoauth%3Agrant-type%3Atoken-exchange&latitude=0&longitude=0&platform=browser&subject_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJjYWJmMDNkMi0xMmEyLTQ0YjYtODJjOS1lOWJkZGNhMzYwNjkiLCJhdWQiOiJ1cm46YmFtdGVjaDpzZXJ2aWNlOnRva2VuIiwibmJmIjoxNjMyMjMwMTY4LCJpc3MiOiJ1cm46YmFtdGVjaDpzZXJ2aWNlOmRldmljZSIsImV4cCI6MjQ5NjIzMDE2OCwiaWF0IjoxNjMyMjMwMTY4LCJqdGkiOiJhYTI0ZWI5Yi1kNWM4LTQ5ODctYWI4ZS1jMDdhMWVhMDgxNzAifQ.8RQ-44KqmctKgdXdQ7E1DmmWYq0gIZsQw3vRL8RvCtrM_hSEHa-CkTGIFpSLpJw8sMlmTUp5ZGwvhghX-4HXfg&subject_token_type=urn%3Abamtech%3Aparams%3Aoauth%3Atoken-type%3Adevice\nauthorization: Bearer eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiJiOTNlZDQyZC00M2RiLTQzNDMtYThjZi1mZTk4YTY2NzVkNTgiLCJpc3MiOiJMaWdodGJveCIsImV4cCI6MTY2NDk3NTExMSwiZGV2aWNlSWQiOiI2NTgzZWU4YmM0YzQwZmJhOTgzMGQ0ZTYwNTM5ZDAzNSIsInBsYXRmb3JtIjoiV2ViIiwiYnJvd3NlciI6IkNocm9tZSIsInRhYiI6MTYzMzQxNzUwNzY4OSwib3MiOiJXaW5kb3dzIDEwLjAiLCJpYXQiOjE2MzM0MTc1MTF9.E7qgVpqsJEPsh0B3lgK9x8hPs7nQ_Bio_FCt1H8mB4XCPrsand4kHVHA5LpiB5rvBLfOaSfJKru-gKuMlgLJhg\n{\"operationName\":\"UpdateAccount\",\"variables\":{\"input\":{\"name\":\"Reid\",\"surname\":\"Hershel\",\"email\":\"restriction.check@gmail.com\",\"password\":\"restriction.check\",\"optIns\":[{\"id\":\"RECEIVE_UPDATES\",\"subscribed\":false}]}},\"query\":\"mutation UpdateAccount($input: AccountInput!, $pin: String) {\\n  account(input: $input, pin: $pin) {\\n    ...AccountFields\\n    __typename\\n  }\\n}\\n\\nfragment AccountFields on Account {\\n  name\\n  surname\\n  email\\n  selectedProfile\\n  hasPin\\n  optIns {\\n    id\\n    text\\n    subscribed\\n    __typename\\n  }\\n  phoneNumbers {\\n    home\\n    mobile\\n    __typename\\n  }\\n  session {\\n    token\\n    __typename\\n  }\\n  profiles {\\n    ...ProfileFields\\n    __typename\\n  }\\n  settings {\\n    requirePinForSwitchProfile\\n    requirePinForManageProfile\\n    tvodPurchaseRestriction\\n    playbackQuality {\\n      ...PlaybackQualityFields\\n      __typename\\n    }\\n    __typename\\n  }\\n  purchases {\\n    totalItems\\n    items {\\n      ...PurchaseFields\\n      __typename\\n    }\\n    __typename\\n  }\\n  cpCustomerID\\n  subscription {\\n    ...SubscriptionInformationFields\\n    __typename\\n  }\\n  __typename\\n}\\n\\nfragment ProfileFields on Profile {\\n  id\\n  name\\n  email\\n  isKid\\n  isDefault\\n  needToConfigure\\n  ageGroup\\n  avatar {\\n    uri\\n    id\\n    __typename\\n  }\\n  closedCaption\\n  maxRating\\n  mobile\\n  __typename\\n}\\n\\nfragment PlaybackQualityFields on PlaybackQuality {\\n  wifi {\\n    id\\n    label\\n    description\\n    bitrate\\n    __typename\\n  }\\n  __typename\\n}\\n\\nfragment PurchaseFields on Purchase {\\n  id\\n  profile {\\n    id\\n    name\\n    __typename\\n  }\\n  contentItem {\\n    ...ContentItemLightFields\\n    __typename\\n  }\\n  product {\\n    id\\n    name\\n    renewable\\n    __typename\\n  }\\n  total\\n  startAvailable\\n  endAvailable\\n  endViewable\\n  __typename\\n}\\n\\nfragment ContentItemLightFields on ContentItem {\\n  id\\n  isRental\\n  ... on Title {\\n    id\\n    ldId\\n    path\\n    title\\n    year\\n    rating {\\n      id\\n      rating\\n      __typename\\n    }\\n    genres\\n    duration\\n    images {\\n      uri\\n      __typename\\n    }\\n    createdAt\\n    products {\\n      id\\n      originalPrice\\n      currentPrice\\n      name\\n      currency\\n      __typename\\n    }\\n    isComingSoon\\n    videoExtras {\\n      ...VideoExtraFields\\n      __typename\\n    }\\n    tile {\\n      image\\n      header\\n      subHeader\\n      badge\\n      contentItem {\\n        id\\n        __typename\\n      }\\n      sortValues {\\n        key\\n        value\\n        __typename\\n      }\\n      playbackInfo {\\n        status\\n        numberMinutesRemaining\\n        numberMinutesWatched\\n        position\\n        __typename\\n      }\\n      rentalInfo {\\n        secondsLeftToStartWatching\\n        secondsLeftToWatch\\n        __typename\\n      }\\n      __typename\\n    }\\n    __typename\\n  }\\n  ... on Series {\\n    title\\n    ldId\\n    genres\\n    path\\n    products {\\n      id\\n      originalPrice\\n      currentPrice\\n      name\\n      currency\\n      __typename\\n    }\\n    seasons {\\n      id\\n      episodes {\\n        id\\n        title\\n        seasonNumber\\n        episodeNumber\\n        __typename\\n      }\\n      __typename\\n    }\\n    images {\\n      uri\\n      __typename\\n    }\\n    createdAt\\n    isComingSoon\\n    videoExtras {\\n      ...VideoExtraFields\\n      __typename\\n    }\\n    tile {\\n      image\\n      header\\n      subHeader\\n      badge\\n      contentItem {\\n        id\\n        __typename\\n      }\\n      sortValues {\\n        key\\n        value\\n        __typename\\n      }\\n      playbackInfo {\\n        status\\n        numberMinutesRemaining\\n        numberMinutesWatched\\n        position\\n        __typename\\n      }\\n      rentalInfo {\\n        secondsLeftToStartWatching\\n        secondsLeftToWatch\\n        __typename\\n      }\\n      __typename\\n    }\\n    __typename\\n  }\\n  ... on Episode {\\n    episodeNumber\\n    seasonNumber\\n    series {\\n      id\\n      title\\n      path\\n      seasons {\\n        episodes {\\n          id\\n          __typename\\n        }\\n        __typename\\n      }\\n      __typename\\n    }\\n    __typename\\n  }\\n  ... on VideoExtra {\\n    contentItems {\\n      id\\n      __typename\\n    }\\n    __typename\\n  }\\n  __typename\\n}\\n\\nfragment VideoExtraFields on VideoExtra {\\n  id\\n  description\\n  images {\\n    id\\n    uri\\n    height\\n    width\\n    __typename\\n  }\\n  tile {\\n    image\\n    __typename\\n  }\\n  start\\n  end\\n  title\\n  videoEncodings {\\n    ...VideoEncodingFields\\n    __typename\\n  }\\n  __typename\\n}\\n\\nfragment VideoEncodingFields on VideoEncoding {\\n  id\\n  format\\n  referenceId\\n  size\\n  offlineEnabled\\n  __typename\\n}\\n\\nfragment SubscriptionInformationFields on SubscriptionInformation {\\n  currentSubscription {\\n    name\\n    sku\\n    endsAt\\n    startsAt\\n    price\\n    features\\n    order {\\n      voucherCode\\n      __typename\\n    }\\n    subscriptionGAType\\n    promotion {\\n      name\\n      price\\n      isSpark\\n      isFreeTrial\\n      expiration\\n      isBridgingOfferPromotion\\n      __typename\\n    }\\n    evSubscriptionStatus\\n    __typename\\n  }\\n  upcomingSubscription {\\n    name\\n    sku\\n    endsAt\\n    startsAt\\n    price\\n    order {\\n      voucherCode\\n      __typename\\n    }\\n    subscriptionGAType\\n    promotion {\\n      name\\n      price\\n      isSpark\\n      isFreeTrial\\n      expiration\\n      __typename\\n    }\\n    evSubscriptionStatus\\n    __typename\\n  }\\n  upcomingFinalBillSubscription {\\n    sku\\n    evSubscriptionStatus\\n    __typename\\n  }\\n  nextPayment {\\n    date\\n    method\\n    type\\n    price\\n    __typename\\n  }\\n  recentPayments {\\n    date\\n    method\\n    type\\n    price\\n    __typename\\n  }\\n  status\\n  renewalStatus\\n  recurringVouchers {\\n    orderDetails {\\n      productName\\n      voucherCode\\n      status\\n      promotion {\\n        endDate\\n        id\\n        amount\\n        isExhausted\\n        __typename\\n      }\\n      __typename\\n    }\\n    __typename\\n  }\\n  dcbSubscriptionInfo {\\n    partnerName\\n    __typename\\n  }\\n  __typename\\n}\\n\"}\nmid=Y1_jFQALAAESwuLfrykcPY44iiIn; ig_did=B755589F-4987-4BED-B6F1-B74C38CDDA46; ig_nrcb=1; fbm_124024574287414=base_domain=.instagram.com; csrftoken=jAYfEUaIhg4JesaPCEw1HaMv20FJ6SZZ; datr=TZ5UYyACdSfnzT1SNWn1oIYE; ds_user_id=56650907390; sessionid=56650907390%3AiPRndDWmoZupKb%3A9%3AAYdsMadARTC9Sys8SCMeMpjqQFWyhnMaVCgPfPyCGw; dpr=1.25"

def plfcolour(status):
    status = status.upper()
    if status == "Y":
        return pcolour.green
    if status == "N" or status == "E":
        return pcolour.red
    return pcolour.blue
def header_to_cookie(header):
    headerlines = str(header).splitlines()
    cookies = {}
    for l in headerlines:
        if l[:10].lower() != "set-cookie":
            continue
        c = l[12:l.index(";")].split("=")
        cookies[c[0]] = c[1]
    return cookies
def cookie_dict_to_str(ckdt):
    cka = []
    for ck, cv in ckdt.items():
        cka.append(str(ck)+"="+str(cv))
    ckstr = "; ".join(cka)
    return ckstr
def load_file(filepath):
    f = open(filepath, "r")
    fl = "".join([l.strip() for l in f.readlines()])
    f.close()
    return fl
def load_file_json(filepath):
    f = open(filepath, "r")
    fl = "".join([l.strip() for l in f.readlines()])
    f.close()
    fd = json.loads(fl)
    return fd
def str_space_l(stro, minlen):
    lendiff = minlen - len(stro)
    if lendiff <= 0:
        return stro
    return stro + " "*lendiff
def plf_print(res_i = -1):
    res_this = test_results[res_i]
    strdisp = ""
    strdisp += str_space_l(res_this["name"], 25)
    strdisp += " | "
    strdisp += plfcolour(res_this["status"]) + res_this["status"] + pcolour.end
    if res_this["region"] != "":
        strdisp += " "
        if res_this["region"] == "HK":
            strdisp += pcolour.blue
        else:
            strdisp += pcolour.red
        strdisp += res_this["region"]
        strdisp += pcolour.end
    else:
        strdisp += "   "
    if res_this["note"] != "":
        strdisp += " ("
        strdisp += res_this["note"]
        strdisp += ")"
    print(strdisp)
def handle_connerr(e):
    errtxt = str(e).lower()
    return_dict = {
        "status": 0, # 0 = error
        "detail": ""
    }
    if "http error" in errtxt:
        return_dict["status"] = int(e.status)
    elif "reset" in errtxt:
        return_dict["detail"] = "Reset"
    elif "closed connection without response" in errtxt:
        return_dict["detail"] = "Empty Reply"
    elif "refused" in errtxt:
        return_dict["detail"] = "Refused"
    elif "timed out" in errtxt:
        return_dict["detail"] = "Timeout"
    elif "nodename nor servname provided" in errtxt:
        return_dict["detail"] = "DNS Error"
    return return_dict

origGetAddrInfo = socket.getaddrinfo
def getAddrInfoWrapper4(host, port, family=0, socktype=0, proto=0, flags=0):
    return origGetAddrInfo(host, port, socket.AF_INET, socktype, proto, flags)
def getAddrInfoWrapper6(host, port, family=0, socktype=0, proto=0, flags=0):
    return origGetAddrInfo(host, port, socket.AF_INET6, socktype, proto, flags)

# force IPv4
socket.getaddrinfo = getAddrInfoWrapper4

test_results = []
# Format
# {"name": "Google Search No CAPTCHA", "status": "Y/W/N/E", "region": "HK", "note": ""}
# Status 狀態代碼:
# Y: Yes / 可使用
# W: Wrong Region (NOT HK) / 地區不對，並非香港地區
# N: No (IP Banned) / 不可使用 (IP被ban咗)
# E: Error (Network Error) / (網路異常)

# Welcome Msg
print(pcolour.bold + "Streaming Restriction Test (HK)" + pcolour.end)
print("By: Ken (Ken's Study Journey)")
print("https://ken.kenstudyjourney.cn")
print("=======================================")
print("")

print("Do you also want to test Mainland websites?")
print("If not, press ENTER directly.")
print("你需要測試內地網站及平台嗎？")
print("如不需要，請直接按ENTER")
c_test_ml = input("(y/N): ").lower() # c_ = choice
print("")
while c_test_ml not in ["", "y", "n"]:
    print("Invalid input. Please type \"Y\" or \"N\":")
    c_test_ml = input().lower()
    print("")

# get ip
print(pcolour.bold + pcolour.blue + "Your IP Address" + pcolour.end + pcolour.end)
try:
    crawl_req = urllib.request.Request("http://ip.sb")
    crawl_req.add_header("User-Agent", crawl_ua_curl)
    crawl_res = urllib.request.urlopen(crawl_req, timeout=crawl_timeout)
    your_ip = crawl_res.read().decode().strip()
    print(your_ip)
except Exception as e:
    print(pcolour.red + "Network Error" + pcolour.end)
    print("Cannot Get your IP Address")
    # print(e)
    continp = input("Still continue checking streaming websites? (y/N): ")
    if continp.strip().lower() != "y":
        exit()
print("")

print(pcolour.bold + pcolour.blue + "Note These Result Letters" + pcolour.end + pcolour.end)
print(pcolour.green + "Y = Yes" + pcolour.end)
print(pcolour.red + "N = No (Banned by Website)" + pcolour.end)
print(pcolour.red + "E = Network Error" + pcolour.end)
print("")

# General Platforms
print(pcolour.bold + pcolour.blue + "General Platforms" + pcolour.end + pcolour.end)

# Google Search No CAPTCHA
try:
    crawl_req = urllib.request.Request("https://www.google.com/search?q=curl&hl=en")
    crawl_req.add_header("User-Agent", crawl_ua_browser)
    crawl_req.add_header("Accept-Language", "en-US,en;q=0.9")
    crawl_req.add_header("Sec-Ch-Ua", "\"Google Chrome\";v=\"135\", \"Not-A.Brand\";v=\"8\", \"Chromium\";v=\"135\"")
    crawl_req.add_header("Sec-Ch-Ua-Mobile", "?0")
    crawl_req.add_header("Sec-Ch-Ua-Model", "\"\"")
    crawl_req.add_header("Sec-Ch-Ua-Platform", "\"Windows\"")
    crawl_req.add_header("Sec-Ch-Ua-Platform-Version", "\"15.0.0\"")
    crawl_req.add_header("Sec-Ch-Ua-Wow64", "?0")
    crawl_req.add_header("Sec-Fetch-Dest", "document")
    crawl_req.add_header("Sec-Fetch-Mode", "navigate")
    crawl_req.add_header("Sec-Fetch-Site", "none")
    crawl_req.add_header("Sec-Fetch-User", "?1")
    crawl_req.add_header("Upgrade-Insecure-Requests", "1")
    crawl_res = urllib.request.urlopen(crawl_req, timeout=crawl_timeout)
    test_results.append({
        "name": "Google Search No CAPTCHA",
        "status": "Y",
        "region": "",
        "note": ""
    })
except Exception as e:
    err_dict = handle_connerr(e)
    if err_dict["status"] == 403 or err_dict["status"] == 429:
        test_results.append({
            "name": "Google Search No CAPTCHA",
            "status": "N",
            "region": "",
            "note": "IP Banned"
        })
    elif err_dict["status"] > 0 and err_dict["status"] != 200:
        test_results.append({
            "name": "Google Search No CAPTCHA",
            "status": "N",
            "region": "",
            "note": "Status: " + str(crawl_res.status)
        })
    else:
        test_results.append({
            "name": "Google Search No CAPTCHA",
            "status": "E",
            "region": "",
            "note": err_dict["detail"]
        })
plf_print()

# Google Play Store
try:
    crawl_req = urllib.request.Request("https://play.google.com/?hl=en")
    crawl_req.add_header("User-Agent", crawl_ua_browser)
    crawl_req.add_header("Accept-Language", "en-US,en;q=0.9")
    crawl_req.add_header("Sec-Ch-Ua", "\"Google Chrome\";v=\"135\", \"Not-A.Brand\";v=\"8\", \"Chromium\";v=\"135\"")
    crawl_req.add_header("Sec-Ch-Ua-Mobile", "?0")
    crawl_req.add_header("Sec-Ch-Ua-Model", "\"\"")
    crawl_req.add_header("Sec-Ch-Ua-Platform", "\"Windows\"")
    crawl_req.add_header("Sec-Ch-Ua-Platform-Version", "\"15.0.0\"")
    crawl_req.add_header("Sec-Ch-Ua-Wow64", "?0")
    crawl_req.add_header("Sec-Fetch-Dest", "document")
    crawl_req.add_header("Sec-Fetch-Mode", "navigate")
    crawl_req.add_header("Sec-Fetch-Site", "none")
    crawl_req.add_header("Sec-Fetch-User", "?1")
    crawl_req.add_header("Upgrade-Insecure-Requests", "1")
    crawl_res = urllib.request.urlopen(crawl_req, timeout=crawl_timeout)
    res_html = "".join([l.strip() for l in crawl_res.read().decode().splitlines()])
    gp_region = re.sub(r".*\"fjF0tb\"\:\s*\"([A-Za-z\-\_\s]+)\".*", r"\1", res_html).strip()
    if gp_region == "CN":
        test_results.append({
            "name": "Google Play Store",
            "status": "N",
            "region": gp_region,
            "note": "Not Available"
        })
    else:
        test_results.append({
            "name": "Google Play Store",
            "status": "Y",
            "region": gp_region,
            "note": ""
        })
except Exception as e:
    err_dict = handle_connerr(e)
    if err_dict["status"] == 403 or err_dict["status"] == 429:
        test_results.append({
            "name": "Google Play Store",
            "status": "N",
            "region": "",
            "note": "IP Banned"
        })
    elif err_dict["status"] > 0 and err_dict["status"] != 200:
        test_results.append({
            "name": "Google Play Store",
            "status": "N",
            "region": "",
            "note": "Status: " + str(crawl_res.status)
        })
    else:
        test_results.append({
            "name": "Google Play Store",
            "status": "E",
            "region": "",
            "note": err_dict["detail"]
        })
plf_print()

# YouTube No Login Required (my creativity & addition)
# On some nodes, it will display (if IP Banned):
# Sign in to confirm you are not a bot
try:
    crawl_req = urllib.request.Request("https://www.youtube.com/watch?v=LXb3EKWsInQ&hl=en")
    crawl_req.add_header("User-Agent", crawl_ua_browser)
    crawl_req.add_header("Accept-Language", "en-US,en;q=0.9")
    crawl_req.add_header("Sec-Ch-Ua", "\"Google Chrome\";v=\"135\", \"Not-A.Brand\";v=\"8\", \"Chromium\";v=\"135\"")
    crawl_req.add_header("Sec-Ch-Ua-Mobile", "?0")
    crawl_req.add_header("Sec-Ch-Ua-Model", "\"\"")
    crawl_req.add_header("Sec-Ch-Ua-Platform", "\"Windows\"")
    crawl_req.add_header("Sec-Ch-Ua-Platform-Version", "\"15.0.0\"")
    crawl_req.add_header("Sec-Ch-Ua-Wow64", "?0")
    crawl_req.add_header("Sec-Fetch-Dest", "document")
    crawl_req.add_header("Sec-Fetch-Mode", "navigate")
    crawl_req.add_header("Sec-Fetch-Site", "none")
    crawl_req.add_header("Sec-Fetch-User", "?1")
    crawl_req.add_header("Upgrade-Insecure-Requests", "1")
    crawl_res = urllib.request.urlopen(crawl_req, timeout=crawl_timeout)
    res_html = "".join([l.strip() for l in crawl_res.read().decode().splitlines()])
    yt_status = re.sub(r".*\"playabilityStatus\"\:\s*\{\s*\"status\"\:\s*\"([A-Za-z\-\_\s]+)\".*", r"\1", res_html).upper().strip()
    yt_region = re.sub(r".*\"detailpage\"\s*\,\s*\"contentRegion\"\:\s*\"([A-Za-z\-\_\s]+)\".*", r"\1", res_html).upper().strip()
    if "www.google.cn" in res_html:
        yt_region = "CN"
    if yt_status == "OK":
        test_results.append({
            "name": "YouTube No Login Required",
            "status": "Y",
            "region": yt_region,
            "note": ""
        })
    else:
        test_results.append({
            "name": "YouTube No Login Required",
            "status": "N",
            "region": yt_region,
            "note": "IP Banned"
        })
except Exception as e:
    err_dict = handle_connerr(e)
    if err_dict["status"] == 403 or err_dict["status"] == 429:
        test_results.append({
            "name": "YouTube No Login Required",
            "status": "N",
            "region": "",
            "note": "IP Banned"
        })
    elif err_dict["status"] > 0 and err_dict["status"] != 200:
        test_results.append({
            "name": "YouTube No Login Required",
            "status": "N",
            "region": "",
            "note": "Status: " + str(crawl_res.status)
        })
    else:
        test_results.append({
            "name": "YouTube No Login Required",
            "status": "E",
            "region": "",
            "note": err_dict["detail"]
        })
plf_print()

# YouTube Premium
try:
    crawl_req = urllib.request.Request("https://www.youtube.com/premium?hl=en")
    crawl_req.add_header("User-Agent", crawl_ua_browser)
    crawl_req.add_header("Accept-Language", "en-US,en;q=0.9")
    crawl_req.add_header("Sec-Ch-Ua", "\"Google Chrome\";v=\"135\", \"Not-A.Brand\";v=\"8\", \"Chromium\";v=\"135\"")
    crawl_req.add_header("Sec-Ch-Ua-Mobile", "?0")
    crawl_req.add_header("Sec-Ch-Ua-Model", "\"\"")
    crawl_req.add_header("Sec-Ch-Ua-Platform", "\"Windows\"")
    crawl_req.add_header("Sec-Ch-Ua-Platform-Version", "\"15.0.0\"")
    crawl_req.add_header("Sec-Ch-Ua-Wow64", "?0")
    crawl_req.add_header("Sec-Fetch-Dest", "document")
    crawl_req.add_header("Sec-Fetch-Mode", "navigate")
    crawl_req.add_header("Sec-Fetch-Site", "none")
    crawl_req.add_header("Sec-Fetch-User", "?1")
    crawl_req.add_header("Upgrade-Insecure-Requests", "1")
    crawl_res = urllib.request.urlopen(crawl_req, timeout=crawl_timeout)
    res_html = "".join([l.strip() for l in crawl_res.read().decode().splitlines()])
    yt_region = re.sub(r".*\"detailpage\"\s*\,\s*\"contentRegion\"\:\s*\"([A-Za-z\-\_\s]+)\".*", r"\1", res_html).upper().strip()
    if "www.google.cn" in res_html:
        yt_region = "CN"
    if "not available in your country" not in res_html:
        test_results.append({
            "name": "YouTube Premium",
            "status": "Y",
            "region": yt_region,
            "note": ""
        })
    else:
        test_results.append({
            "name": "YouTube Premium",
            "status": "N",
            "region": yt_region,
            "note": "Not Available"
        })
except Exception as e:
    err_dict = handle_connerr(e)
    if err_dict["status"] == 403 or err_dict["status"] == 429:
        test_results.append({
            "name": "YouTube Premium",
            "status": "N",
            "region": "",
            "note": "IP Banned"
        })
    elif err_dict["status"] > 0 and err_dict["status"] != 200:
        test_results.append({
            "name": "YouTube Premium",
            "status": "N",
            "region": "",
            "note": "Status: " + str(crawl_res.status)
        })
    else:
        test_results.append({
            "name": "YouTube Premium",
            "status": "E",
            "region": "",
            "note": err_dict["detail"]
        })
plf_print()

# YouTube Music
try:
    crawl_req = urllib.request.Request("https://music.youtube.com/?hl=en")
    crawl_req.add_header("User-Agent", crawl_ua_browser)
    crawl_req.add_header("Accept-Language", "en-US,en;q=0.9")
    crawl_req.add_header("Sec-Ch-Ua", "\"Google Chrome\";v=\"135\", \"Not-A.Brand\";v=\"8\", \"Chromium\";v=\"135\"")
    crawl_req.add_header("Sec-Ch-Ua-Mobile", "?0")
    crawl_req.add_header("Sec-Ch-Ua-Model", "\"\"")
    crawl_req.add_header("Sec-Ch-Ua-Platform", "\"Windows\"")
    crawl_req.add_header("Sec-Ch-Ua-Platform-Version", "\"15.0.0\"")
    crawl_req.add_header("Sec-Ch-Ua-Wow64", "?0")
    crawl_req.add_header("Sec-Fetch-Dest", "document")
    crawl_req.add_header("Sec-Fetch-Mode", "navigate")
    crawl_req.add_header("Sec-Fetch-Site", "none")
    crawl_req.add_header("Sec-Fetch-User", "?1")
    crawl_req.add_header("Upgrade-Insecure-Requests", "1")
    crawl_res = urllib.request.urlopen(crawl_req, timeout=crawl_timeout)
    res_html = "".join([l.strip() for l in crawl_res.read().decode().splitlines()])
    if "not available in your area" not in res_html:
        ym_region = re.sub(r".*\"detailpage\"\s*\,\s*\"contentRegion\"\:\s*\"([A-Za-z\-\_\s]+)\".*", r"\1", res_html).upper().strip()
        test_results.append({
            "name": "YouTube Music",
            "status": "Y",
            "region": ym_region,
            "note": ""
        })
    else:
        test_results.append({
            "name": "YouTube Music",
            "status": "N",
            "region": "",
            "note": "Not Available"
        })
except Exception as e:
    err_dict = handle_connerr(e)
    if err_dict["status"] == 403 or err_dict["status"] == 429:
        test_results.append({
            "name": "YouTube Music",
            "status": "N",
            "region": "",
            "note": "IP Banned"
        })
    elif err_dict["status"] > 0 and err_dict["status"] != 200:
        test_results.append({
            "name": "YouTube Music",
            "status": "N",
            "region": "",
            "note": "Status: " + str(crawl_res.status)
        })
    else:
        test_results.append({
            "name": "YouTube Music",
            "status": "E",
            "region": "",
            "note": err_dict["detail"]
        })
plf_print()

# Bing
try:
    crawl_req = urllib.request.Request("https://www.bing.com/search?q=curl")
    crawl_req.add_header("User-Agent", crawl_ua_browser)
    crawl_res = urllib.request.urlopen(crawl_req, timeout=crawl_timeout)
    res_html = "".join([l.strip() for l in crawl_res.read().decode().splitlines()])
    bg_region = re.sub(r".*\"?Region\"?\:\s*\"([A-Za-z\-\_\s]+)\".*", r"\1", res_html).upper().strip()
    bg_risky = bool(len(re.findall(r"sj\_cook\.set\(\"SRCHHPGUSR\"\s*\,\s*\"HV\"", res_html)))
    if "cn.bing.com" in bg_region:
        bg_region = "CN"
    bg_status = "Y"
    bg_risky_str = ""
    if bg_risky:
        bg_risky_str = "Risky"
    test_results.append({
        "name": "Bing Search",
        "status": bg_status,
        "region": bg_region,
        "note": bg_risky_str
    })
except Exception as e:
    err_dict = handle_connerr(e)
    if err_dict["status"] == 403 or err_dict["status"] == 429:
        test_results.append({
            "name": "Bing Search",
            "status": "N",
            "region": "",
            "note": "IP Banned"
        })
    elif err_dict["status"] > 0 and err_dict["status"] != 200:
        test_results.append({
            "name": "Bing Search",
            "status": "N",
            "region": "",
            "note": "Status: " + str(crawl_res.status)
        })
    else:
        test_results.append({
            "name": "Bing Search",
            "status": "E",
            "region": "",
            "note": err_dict["detail"]
        })
plf_print()

# Apple
try:
    crawl_req = urllib.request.Request("https://gspe1-ssl.ls.apple.com/pep/gcc")
    crawl_req.add_header("User-Agent", crawl_ua_curl)
    crawl_res = urllib.request.urlopen(crawl_req, timeout=crawl_timeout)
    res_html = "".join([l.strip() for l in crawl_res.read().decode().splitlines()]).upper()
    ap_region = res_html
    test_results.append({
        "name": "Apple",
        "status": "Y",
        "region": ap_region,
        "note": ""
    })
except Exception as e:
    err_dict = handle_connerr(e)
    if err_dict["status"] == 403 or err_dict["status"] == 429:
        test_results.append({
            "name": "Apple",
            "status": "N",
            "region": "",
            "note": "IP Banned"
        })
    elif err_dict["status"] > 0 and err_dict["status"] != 200:
        test_results.append({
            "name": "Apple",
            "status": "N",
            "region": "",
            "note": "Status: " + str(crawl_res.status)
        })
    else:
        test_results.append({
            "name": "Apple",
            "status": "E",
            "region": "",
            "note": err_dict["detail"]
        })
plf_print()

# GitHub
try:
    crawl_req = urllib.request.Request("https://github.com")
    crawl_req.add_header("User-Agent", crawl_ua_browser)
    crawl_res = urllib.request.urlopen(crawl_req, timeout=crawl_timeout)
    res_html = "".join([l.strip() for l in crawl_res.read().decode().splitlines()]).upper()
    test_results.append({
        "name": "GitHub",
        "status": "Y",
        "region": "",
        "note": ""
    })
except Exception as e:
    err_dict = handle_connerr(e)
    if err_dict["status"] == 403 or err_dict["status"] == 429:
        test_results.append({
            "name": "GitHub",
            "status": "N",
            "region": "",
            "note": "IP Banned"
        })
    elif err_dict["status"] > 0 and err_dict["status"] != 200:
        test_results.append({
            "name": "GitHub",
            "status": "N",
            "region": "",
            "note": "Status: " + str(crawl_res.status)
        })
    else:
        test_results.append({
            "name": "GitHub",
            "status": "E",
            "region": "",
            "note": err_dict["detail"]
        })
plf_print()

# Wikipedia (my addition)
try:
    crawl_req = urllib.request.Request("https://www.wikipedia.org")
    crawl_req.add_header("User-Agent", crawl_ua_browser)
    crawl_req.add_header("Accept-Language", "zh-CN,zh;q=0.9")
    crawl_req.add_header("Sec-Ch-Ua", "\"Google Chrome\";v=\"135\", \"Not-A.Brand\";v=\"8\", \"Chromium\";v=\"135\"")
    crawl_req.add_header("Sec-Ch-Ua-Mobile", "?0")
    crawl_req.add_header("Sec-Ch-Ua-Model", "\"\"")
    crawl_req.add_header("Sec-Ch-Ua-Platform", "\"Windows\"")
    crawl_req.add_header("Sec-Ch-Ua-Platform-Version", "\"15.0.0\"")
    crawl_req.add_header("Sec-Ch-Ua-Wow64", "?0")
    crawl_req.add_header("Sec-Fetch-Dest", "document")
    crawl_req.add_header("Sec-Fetch-Mode", "navigate")
    crawl_req.add_header("Sec-Fetch-Site", "none")
    crawl_req.add_header("Sec-Fetch-User", "?1")
    crawl_req.add_header("Upgrade-Insecure-Requests", "1")
    crawl_res = urllib.request.urlopen(crawl_req, timeout=crawl_timeout)
    res_html = "".join([l.strip() for l in crawl_res.read().decode().splitlines()]).upper()
    test_results.append({
        "name": "Wikipedia",
        "status": "Y",
        "region": "",
        "note": ""
    })
except Exception as e:
    err_dict = handle_connerr(e)
    if err_dict["status"] == 403 or err_dict["status"] == 429:
        test_results.append({
            "name": "Wikipedia",
            "status": "N",
            "region": "",
            "note": "IP Banned"
        })
    elif err_dict["status"] > 0 and err_dict["status"] != 200:
        test_results.append({
            "name": "Wikipedia",
            "status": "N",
            "region": "",
            "note": "Status: " + str(crawl_res.status)
        })
    else:
        test_results.append({
            "name": "Wikipedia",
            "status": "E",
            "region": "",
            "note": err_dict["detail"]
        })
plf_print()

# Wikipedia Editing
# IP Address Labelled as VPN/Proxy can be Banned for Several (1~5) Years!
# If IP banned, open this URL in your browser to learn more.
try:
    crawl_req = urllib.request.Request("https://zh.wikipedia.org/w/index.php?title=Wikipedia%3A%E6%B2%99%E7%9B%92&action=edit")
    crawl_req.add_header("User-Agent", crawl_ua_browser)
    crawl_req.add_header("Accept-Language", "zh-CN,zh;q=0.9")
    crawl_req.add_header("Sec-Ch-Ua", "\"Google Chrome\";v=\"135\", \"Not-A.Brand\";v=\"8\", \"Chromium\";v=\"135\"")
    crawl_req.add_header("Sec-Ch-Ua-Mobile", "?0")
    crawl_req.add_header("Sec-Ch-Ua-Model", "\"\"")
    crawl_req.add_header("Sec-Ch-Ua-Platform", "\"Windows\"")
    crawl_req.add_header("Sec-Ch-Ua-Platform-Version", "\"15.0.0\"")
    crawl_req.add_header("Sec-Ch-Ua-Wow64", "?0")
    crawl_req.add_header("Sec-Fetch-Dest", "document")
    crawl_req.add_header("Sec-Fetch-Mode", "navigate")
    crawl_req.add_header("Sec-Fetch-Site", "none")
    crawl_req.add_header("Sec-Fetch-User", "?1")
    crawl_req.add_header("Upgrade-Insecure-Requests", "1")
    crawl_res = urllib.request.urlopen(crawl_req, timeout=crawl_timeout)
    res_html = "".join([l.strip() for l in crawl_res.read().decode().splitlines()])
    not_available = bool(len(re.findall(r"Banned", res_html)))
    if not not_available:
        test_results.append({
            "name": "Wikipedia Editing",
            "status": "Y",
            "region": "",
            "note": ""
        })
    else:
        test_results.append({
            "name": "Wikipedia Editing",
            "status": "N",
            "region": "",
            "note": "IP Banned"
        })
except Exception as e:
    err_dict = handle_connerr(e)
    if err_dict["status"] == 403 or err_dict["status"] == 429:
        test_results.append({
            "name": "Wikipedia Editing",
            "status": "N",
            "region": "",
            "note": "IP Banned"
        })
    elif err_dict["status"] > 0 and err_dict["status"] != 200:
        test_results.append({
            "name": "Wikipedia Editing",
            "status": "N",
            "region": "",
            "note": "Status: " + str(crawl_res.status)
        })
    else:
        test_results.append({
            "name": "Wikipedia Editing",
            "status": "E",
            "region": "",
            "note": err_dict["detail"]
        })
plf_print()

print("")

# Academic & Research Platforms
print(pcolour.bold + pcolour.blue + "Academic & Research Platforms" + pcolour.end + pcolour.end)

# Google Scholar
try:
    crawl_req = urllib.request.Request("https://scholar.google.com/?hl=en")
    crawl_req.add_header("User-Agent", crawl_ua_browser)
    crawl_req.add_header("Accept-Language", "en-US,en;q=0.9")
    crawl_req.add_header("Sec-Ch-Ua", "\"Google Chrome\";v=\"135\", \"Not-A.Brand\";v=\"8\", \"Chromium\";v=\"135\"")
    crawl_req.add_header("Sec-Ch-Ua-Mobile", "?0")
    crawl_req.add_header("Sec-Ch-Ua-Model", "\"\"")
    crawl_req.add_header("Sec-Ch-Ua-Platform", "\"Windows\"")
    crawl_req.add_header("Sec-Ch-Ua-Platform-Version", "\"15.0.0\"")
    crawl_req.add_header("Sec-Ch-Ua-Wow64", "?0")
    crawl_req.add_header("Sec-Fetch-Dest", "document")
    crawl_req.add_header("Sec-Fetch-Mode", "navigate")
    crawl_req.add_header("Sec-Fetch-Site", "none")
    crawl_req.add_header("Sec-Fetch-User", "?1")
    crawl_req.add_header("Upgrade-Insecure-Requests", "1")
    crawl_res = urllib.request.urlopen(crawl_req, timeout=crawl_timeout)
    test_results.append({
        "name": "Google Scholar",
        "status": "Y",
        "region": "",
        "note": ""
    })
except Exception as e:
    err_dict = handle_connerr(e)
    if err_dict["status"] == 403 or err_dict["status"] == 429:
        test_results.append({
            "name": "Google Scholar",
            "status": "N",
            "region": "",
            "note": "IP Banned"
        })
    elif err_dict["status"] > 0 and err_dict["status"] != 200:
        test_results.append({
            "name": "Google Scholar",
            "status": "N",
            "region": "",
            "note": "Status: " + str(crawl_res.status)
        })
    else:
        test_results.append({
            "name": "Google Scholar",
            "status": "E",
            "region": "",
            "note": err_dict["detail"]
        })
plf_print()

# Google Colab
try:
    crawl_req = urllib.request.Request("https://colab.research.google.com/?hl=en")
    crawl_req.add_header("User-Agent", crawl_ua_browser)
    crawl_req.add_header("Accept-Language", "en-US,en;q=0.9")
    crawl_req.add_header("Sec-Ch-Ua", "\"Google Chrome\";v=\"135\", \"Not-A.Brand\";v=\"8\", \"Chromium\";v=\"135\"")
    crawl_req.add_header("Sec-Ch-Ua-Mobile", "?0")
    crawl_req.add_header("Sec-Ch-Ua-Model", "\"\"")
    crawl_req.add_header("Sec-Ch-Ua-Platform", "\"Windows\"")
    crawl_req.add_header("Sec-Ch-Ua-Platform-Version", "\"15.0.0\"")
    crawl_req.add_header("Sec-Ch-Ua-Wow64", "?0")
    crawl_req.add_header("Sec-Fetch-Dest", "document")
    crawl_req.add_header("Sec-Fetch-Mode", "navigate")
    crawl_req.add_header("Sec-Fetch-Site", "none")
    crawl_req.add_header("Sec-Fetch-User", "?1")
    crawl_req.add_header("Upgrade-Insecure-Requests", "1")
    crawl_res = urllib.request.urlopen(crawl_req, timeout=crawl_timeout)
    test_results.append({
        "name": "Google Colab",
        "status": "Y",
        "region": "",
        "note": ""
    })
except Exception as e:
    err_dict = handle_connerr(e)
    if err_dict["status"] == 403 or err_dict["status"] == 429:
        test_results.append({
            "name": "Google Colab",
            "status": "N",
            "region": "",
            "note": "IP Banned"
        })
    elif err_dict["status"] > 0 and err_dict["status"] != 200:
        test_results.append({
            "name": "Google Colab",
            "status": "N",
            "region": "",
            "note": "Status: " + str(crawl_res.status)
        })
    else:
        test_results.append({
            "name": "Google Colab",
            "status": "E",
            "region": "",
            "note": err_dict["detail"]
        })
plf_print()

print("")

# Streaming Platforms
print(pcolour.bold + pcolour.blue + "Streaming Platforms" + pcolour.end + pcolour.end)

# iqiyi Oversea
try:
    crawl_req = urllib.request.Request("https://www.iq.com")
    crawl_req.add_header("User-Agent", crawl_ua_browser)
    crawl_res = urllib.request.urlopen(crawl_req, timeout=crawl_timeout)
    res_html = "".join([l.strip() for l in crawl_res.read().decode().splitlines()])
    iq_region = re.sub(r".*mod\=([A-Za-z\-\_\s]+).*", r"\1", res_html).upper().strip()
    if iq_region == "NTW":
        iq_region = "TW"
    test_results.append({
        "name": "iqiyi Oversea",
        "status": "Y",
        "region": iq_region,
        "note": ""
    })
except Exception as e:
    err_dict = handle_connerr(e)
    if err_dict["status"] == 403 or err_dict["status"] == 429:
        test_results.append({
            "name": "iqiyi Oversea",
            "status": "N",
            "region": "",
            "note": "IP Banned"
        })
    elif err_dict["status"] > 0 and err_dict["status"] != 200:
        test_results.append({
            "name": "iqiyi Oversea",
            "status": "N",
            "region": "",
            "note": "Status: " + str(crawl_res.status)
        })
    else:
        test_results.append({
            "name": "iqiyi Oversea",
            "status": "E",
            "region": "",
            "note": err_dict["detail"]
        })
plf_print()

# Netflix
try:
    crawl_req = urllib.request.Request("https://www.netflix.com/title/70143836")
    crawl_req.add_header("User-Agent", crawl_ua_browser)
    crawl_req.add_header("Host", "www.netflix.com")
    crawl_req.add_header("Accept-Language", "en-US,en;q=0.9")
    crawl_req.add_header("Sec-Ch-Ua", "\"Google Chrome\";v=\"135\", \"Not-A.Brand\";v=\"8\", \"Chromium\";v=\"135\"")
    crawl_req.add_header("Sec-Ch-Ua-Mobile", "?0")
    crawl_req.add_header("Sec-Ch-Ua-Model", "\"\"")
    crawl_req.add_header("Sec-Ch-Ua-Platform", "\"Windows\"")
    crawl_req.add_header("Sec-Ch-Ua-Platform-Version", "\"15.0.0\"")
    crawl_req.add_header("Sec-Ch-Ua-Wow64", "?0")
    crawl_req.add_header("Sec-Fetch-Dest", "document")
    crawl_req.add_header("Sec-Fetch-Mode", "navigate")
    crawl_req.add_header("Sec-Fetch-Site", "none")
    crawl_req.add_header("Sec-Fetch-User", "?1")
    crawl_res = urllib.request.urlopen(crawl_req, timeout=crawl_timeout)
    res_html = "".join([l.strip() for l in crawl_res.read().decode().splitlines()])
    nf_region = re.sub(r".*\"country\"\:\s*\"([A-Za-z\-\_\s]+)\"\,\s*\"language\".*", r"\1", res_html).upper().strip()
    not_available = bool(len(re.findall(r"\<div\s*data\-uia\=\"locally-unavailable\"", res_html)))
    if not not_available:
        test_results.append({
            "name": "Netflix",
            "status": "Y",
            "region": nf_region,
            "note": ""
        })
    else:
        test_results.append({
            "name": "Netflix",
            "status": "N",
            "region": nf_region,
            "note": "Originals Only"
        })
except Exception as e:
    err_dict = handle_connerr(e)
    if err_dict["status"] == 403 or err_dict["status"] == 429:
        test_results.append({
            "name": "Netflix",
            "status": "N",
            "region": "",
            "note": "IP Banned"
        })
    if err_dict["status"] == 404:
        test_results.append({
            "name": "Netflix",
            "status": "N",
            "region": "",
            "note": "Originals Only"
        })
    elif err_dict["status"] > 0 and err_dict["status"] != 200:
        test_results.append({
            "name": "Netflix",
            "status": "N",
            "region": "",
            "note": "Status: " + str(crawl_res.status)
        })
    else:
        test_results.append({
            "name": "Netflix",
            "status": "E",
            "region": "",
            "note": err_dict["detail"]
        })
plf_print()

# Amazon Prime Video
try:
    crawl_req = urllib.request.Request("https://www.primevideo.com")
    crawl_req.add_header("User-Agent", crawl_ua_browser)
    crawl_req.add_header("Accept-Language", "en-US,en;q=0.9")
    crawl_req.add_header("Sec-Ch-Ua", "\"Google Chrome\";v=\"135\", \"Not-A.Brand\";v=\"8\", \"Chromium\";v=\"135\"")
    crawl_req.add_header("Sec-Ch-Ua-Mobile", "?0")
    crawl_req.add_header("Sec-Ch-Ua-Model", "\"\"")
    crawl_req.add_header("Sec-Ch-Ua-Platform", "\"Windows\"")
    crawl_req.add_header("Sec-Ch-Ua-Platform-Version", "\"15.0.0\"")
    crawl_req.add_header("Sec-Ch-Ua-Wow64", "?0")
    crawl_req.add_header("Sec-Fetch-Dest", "document")
    crawl_req.add_header("Sec-Fetch-Mode", "navigate")
    crawl_req.add_header("Sec-Fetch-Site", "none")
    crawl_req.add_header("Sec-Fetch-User", "?1")
    crawl_res = urllib.request.urlopen(crawl_req, timeout=crawl_timeout)
    res_html = "".join([l.strip() for l in crawl_res.read().decode().splitlines()])
    apv_region = re.sub(r".*\"currentTerritory\"\:\s*\"([A-Za-z\-\_\s]+)\".*", r"\1", res_html).upper().strip()
    not_available = bool(len(re.findall(r"isServiceRestricted", res_html)))
    if not not_available:
        test_results.append({
            "name": "Amazon Prime Video",
            "status": "Y",
            "region": apv_region,
            "note": ""
        })
    else:
        test_results.append({
            "name": "Amazon Prime Video",
            "status": "N",
            "region": apv_region,
            "note": "Service Unavailable"
        })
except Exception as e:
    err_dict = handle_connerr(e)
    if err_dict["status"] == 403 or err_dict["status"] == 429:
        test_results.append({
            "name": "Amazon Prime Video",
            "status": "N",
            "region": "",
            "note": "IP Banned"
        })
    elif err_dict["status"] > 0 and err_dict["status"] != 200:
        test_results.append({
            "name": "Amazon Prime Video",
            "status": "N",
            "region": "",
            "note": "Status: " + str(crawl_res.status)
        })
    else:
        test_results.append({
            "name": "Amazon Prime Video",
            "status": "E",
            "region": "",
            "note": err_dict["detail"]
        })
plf_print()

# Spotify (my addition)
try:
    crawl_req = urllib.request.Request("https://open.spotify.com")
    crawl_req.add_header("User-Agent", crawl_ua_browser)
    crawl_req.add_header("Accept-Language", "en-US,en;q=0.9")
    crawl_req.add_header("Sec-Ch-Ua", "\"Google Chrome\";v=\"135\", \"Not-A.Brand\";v=\"8\", \"Chromium\";v=\"135\"")
    crawl_req.add_header("Sec-Ch-Ua-Mobile", "?0")
    crawl_req.add_header("Sec-Ch-Ua-Model", "\"\"")
    crawl_req.add_header("Sec-Ch-Ua-Platform", "\"Windows\"")
    crawl_req.add_header("Sec-Ch-Ua-Platform-Version", "\"15.0.0\"")
    crawl_req.add_header("Sec-Ch-Ua-Wow64", "?0")
    crawl_req.add_header("Sec-Fetch-Dest", "document")
    crawl_req.add_header("Sec-Fetch-Mode", "navigate")
    crawl_req.add_header("Sec-Fetch-Site", "none")
    crawl_req.add_header("Sec-Fetch-User", "?1")
    crawl_res = urllib.request.urlopen(crawl_req, timeout=crawl_timeout)
    res_html = "".join([l.strip() for l in crawl_res.read().decode().splitlines()]).upper()
    test_results.append({
        "name": "Spotify",
        "status": "Y",
        "region": "",
        "note": ""
    })
except Exception as e:
    err_dict = handle_connerr(e)
    if err_dict["status"] == 403 or err_dict["status"] == 429:
        test_results.append({
            "name": "Spotify",
            "status": "N",
            "region": "",
            "note": "IP Banned"
        })
    elif err_dict["status"] > 0 and err_dict["status"] != 200:
        test_results.append({
            "name": "Spotify",
            "status": "N",
            "region": "",
            "note": "Status: " + str(crawl_res.status)
        })
    else:
        test_results.append({
            "name": "Spotify",
            "status": "E",
            "region": "",
            "note": err_dict["detail"]
        })
plf_print()

# Spotify Registration
try:
    crawl_post_param = "birth_day=11&birth_month=11&birth_year=2000&collect_personal_info=undefined&creation_flow=&creation_point=https%3A%2F%2Fwww.spotify.com%2Fhk-en%2F&displayname=Gay%20Lord&gender=male&iagree=1&key=a1e486e2729f46d6bb368d6b2bcda326&platform=www&referrer=&send-email=0&thirdpartyemail=0&identifier_token=AgE6YTvEzkReHNfJpO114514"
    crawl_req = urllib.request.Request("https://spclient.wg.spotify.com/signup/public/v1/account", data=crawl_post_param.encode(), method="POST")
    crawl_req.add_header("User-Agent", crawl_ua_browser)
    crawl_req.add_header("Accept-Language", "en")
    crawl_req.add_header("Content-Type", "application/x-www-form-urlencoded")
    crawl_res = urllib.request.urlopen(crawl_req, timeout=crawl_timeout)
    res_dict = json.loads(crawl_res.read())
    rg_status = res_dict["status"]
    if rg_status == 311:
        sp_region = res_dict["country"].strip().upper()
        test_results.append({
            "name": "Spotify Registration",
            "status": "Y",
            "region": sp_region,
            "note": ""
        })
    elif rg_status == 120:
        sp_region = res_dict["country"].strip().upper()
        test_results.append({
            "name": "Spotify Registration",
            "status": "N",
            "region": sp_region,
            "note": "Not Available"
        })
    elif rg_status == 320:
        test_results.append({
            "name": "Spotify Registration",
            "status": "N",
            "region": "",
            "note": "IP Banned"
        })
    else:
        test_results.append({
            "name": "Spotify Registration",
            "status": "N",
            "region": "",
            "note": "Status: " + str(rg_status)
        })
except Exception as e:
    err_dict = handle_connerr(e)
    if err_dict["status"] == 403 or err_dict["status"] == 429:
        test_results.append({
            "name": "Spotify Registration",
            "status": "N",
            "region": "",
            "note": "IP Banned"
        })
    elif err_dict["status"] > 0 and err_dict["status"] != 200:
        test_results.append({
            "name": "Spotify Registration",
            "status": "N",
            "region": "",
            "note": "Status: " + str(crawl_res.status)
        })
    else:
        test_results.append({
            "name": "Spotify Registration",
            "status": "E",
            "region": "",
            "note": err_dict["detail"]
        })
plf_print()

# Dazn
try:
    crawl_post_param = "{\"LandingPageKey\":\"generic\",\"languages\":\"en-US,en\",\"Platform\":\"web\",\"PlatformAttributes\":{},\"Manufacturer\":\"\",\"PromoCode\":\"\",\"Version\":\"2\"}"
    crawl_req = urllib.request.Request("https://startup.core.indazn.com/misl/v5/Startup", data=crawl_post_param.encode(), method="POST")
    crawl_req.add_header("User-Agent", crawl_ua_browser)
    crawl_req.add_header("Content-Type", "application/json")
    crawl_res = urllib.request.urlopen(crawl_req, timeout=crawl_timeout)
    res_dict = json.loads(crawl_res.read())
    rg_success = res_dict["Region"]["isAllowed"]
    if rg_success:
        dz_region = res_dict["Region"]["GeolocatedCountry"].strip().upper()
        test_results.append({
            "name": "Dazn",
            "status": "Y",
            "region": dz_region,
            "note": ""
        })
    else:
        test_results.append({
            "name": "Dazn",
            "status": "N",
            "region": "",
            "note": "Not Available"
        })
except Exception as e:
    err_dict = handle_connerr(e)
    if err_dict["status"] == 403 or err_dict["status"] == 429:
        test_results.append({
            "name": "Dazn",
            "status": "N",
            "region": "",
            "note": "IP Banned"
        })
    elif err_dict["status"] > 0 and err_dict["status"] != 200:
        test_results.append({
            "name": "Dazn",
            "status": "N",
            "region": "",
            "note": "Status: " + str(crawl_res.status)
        })
    else:
        test_results.append({
            "name": "Dazn",
            "status": "E",
            "region": "",
            "note": err_dict["detail"]
        })
plf_print()

# Disney+
# Most Challenging One (4 Steps!)
try:
    # STEP 1
    crawl_post_param_1 = "{\"deviceFamily\":\"browser\",\"applicationRuntime\":\"chrome\",\"deviceProfile\":\"windows\",\"attributes\":{}}"
    crawl_req_1 = urllib.request.Request("https://disney.api.edge.bamgrid.com/devices", data=crawl_post_param_1.encode(), method="POST")
    crawl_req_1.add_header("User-Agent", crawl_ua_browser)
    crawl_req_1.add_header("Content-Type", "application/json; charset=UTF-8")
    crawl_req_1.add_header("Authorization", "Bearer ZGlzbmV5JmJyb3dzZXImMS4wLjA.Cu56AgSfBTDag5NiRA81oLHkDZfu5L3CKadnefEAY84")
    crawl_res_1 = urllib.request.urlopen(crawl_req_1, timeout=crawl_timeout)
    # STEP 1 Result
    res_json_1 = crawl_res_1.read().decode().strip()
    res_dict_1 = json.loads(res_json_1)
    dp_assertion = res_dict_1["assertion"]
    # STEP 2
    crawl_post_param_2 = media_cookie.splitlines()[0].replace("DISNEYASSERTION", dp_assertion)
    crawl_req_2 = urllib.request.Request("https://disney.api.edge.bamgrid.com/token", data=crawl_post_param_2.encode(), method="POST")
    crawl_req_2.add_header("User-Agent", crawl_ua_browser)
    crawl_req_2.add_header("Content-Type", "application/x-www-form-urlencoded")
    crawl_req_2.add_header("Authorization", "Bearer ZGlzbmV5JmJyb3dzZXImMS4wLjA.Cu56AgSfBTDag5NiRA81oLHkDZfu5L3CKadnefEAY84")
    crawl_res_2 = urllib.request.urlopen(crawl_req_2, timeout=crawl_timeout)
    # STEP 2 Result
    res_json_2 = crawl_res_2.read().decode().strip()
    res_dict_2 = json.loads(res_json_2)
    dp_refresh_token = res_dict_2["refresh_token"]
    # STEP 3
    crawl_post_param_3 = media_cookie.splitlines()[7].replace("ILOVEDISNEY", dp_refresh_token)
    crawl_req_3 = urllib.request.Request("https://disney.api.edge.bamgrid.com/graph/v1/device/graphql", data=crawl_post_param_3.encode(), method="POST")
    crawl_req_3.add_header("User-Agent", crawl_ua_browser)
    crawl_req_3.add_header("Content-Type", "application/x-www-form-urlencoded")
    crawl_req_3.add_header("Authorization", "Bearer ZGlzbmV5JmJyb3dzZXImMS4wLjA.Cu56AgSfBTDag5NiRA81oLHkDZfu5L3CKadnefEAY84")
    crawl_res_3 = urllib.request.urlopen(crawl_req_3, timeout=crawl_timeout)
    # STEP 3 Result
    res_json_3 = crawl_res_3.read().decode().strip()
    res_dict_3 = json.loads(res_json_3)
    dp_success = res_dict_3["extensions"]["sdk"]["session"]["inSupportedLocation"]
    if dp_success:
        dp_region = res_dict_3["extensions"]["sdk"]["session"]["location"]["countryCode"]
        # STEP 4: Official Website
        crawl_req_4 = urllib.request.Request("https://disneyplus.com")
        crawl_req_4.add_header("User-Agent", crawl_ua_browser)
        crawl_res_4 = urllib.request.urlopen(crawl_req_4, timeout=crawl_timeout)
        # STEP 4 Result
        res_html_4 = "".join([l.strip() for l in crawl_res_4.read().decode().splitlines()])
        dp_preview_success = bool(len(re.findall(r"preview|unavailable", res_html_4, re.IGNORECASE)))
        if dp_preview_success:
            test_results.append({
                "name": "Disney+",
                "status": "Y",
                "region": dp_region,
                "note": ""
            })
        else:
            test_results.append({
                "name": "Disney+",
                "status": "N",
                "region": dp_region,
                "note": "No Preview"
            })
    else:
        test_results.append({
            "name": "Disney+",
            "status": "N",
            "region": "",
            "note": "Not Available"
        })
except Exception as e:
    err_dict = handle_connerr(e)
    if err_dict["status"] == 400 or err_dict["status"] == 403 or err_dict["status"] == 429:
        test_results.append({
            "name": "Disney+",
            "status": "N",
            "region": "",
            "note": "IP Banned"
        })
    elif err_dict["status"] > 0 and err_dict["status"] != 200:
        test_results.append({
            "name": "Disney+",
            "status": "N",
            "region": "",
            "note": "Status: " + str(crawl_res.status)
        })
    else:
        test_results.append({
            "name": "Disney+",
            "status": "E",
            "region": "",
            "note": err_dict["detail"]
        })
plf_print()

# HBO Max
try:
    crawl_req = urllib.request.Request("https://www.max.com/")
    crawl_req.add_header("User-Agent", crawl_ua_browser)
    crawl_res = urllib.request.urlopen(crawl_req, timeout=crawl_timeout)
    res_html = "".join([l.strip() for l in crawl_res.read().decode().splitlines()])
    max_has_region = bool(len(re.findall(r"\"userCountry\"\:\s*\"([A-Za-z\-\_\s]+)\"", res_html, re.IGNORECASE)))
    if max_has_region:
        max_region = re.sub(r".*\"userCountry\"\:\s*\"([A-Za-z\-\_\s]+)\".*", r"\1", res_html, re.IGNORECASE).strip().upper()
        max_regionlist_u = re.findall(r"\"url\"\:\s*\"\/[a-z]{2}\/[a-z]{2}\"", res_html, re.IGNORECASE)
        max_regionlist = [re.sub(r"\"url\"\:\s*\"\/([A-Za-z]{2})\/[A-Za-z]{2}\"", r"\1", i).upper() for i in max_regionlist_u]
        max_regionlist = list(set(max_regionlist)) # remove duplicates
        max_regionlist.sort()
        if max_region in max_regionlist:
            test_results.append({
                "name": "HBO Max",
                "status": "Y",
                "region": max_region,
                "note": ""
            })
        else:
            test_results.append({
                "name": "HBO Max",
                "status": "N",
                "region": max_region,
                "note": "Not Available"
            })
    else:
        test_results.append({
            "name": "HBO Max",
            "status": "N",
            "region": "",
            "note": "Not Available"
        })
except Exception as e:
    err_dict = handle_connerr(e)
    if err_dict["status"] == 403 or err_dict["status"] == 429:
        test_results.append({
            "name": "HBO Max",
            "status": "N",
            "region": "",
            "note": "IP Banned"
        })
    elif err_dict["status"] > 0 and err_dict["status"] != 200:
        test_results.append({
            "name": "HBO Max",
            "status": "N",
            "region": "",
            "note": "Status: " + str(crawl_res.status)
        })
    else:
        test_results.append({
            "name": "HBO Max",
            "status": "E",
            "region": "",
            "note": err_dict["detail"]
        })
plf_print()

print("")

# HK Local Platforms
print(pcolour.bold + pcolour.blue + "Social Platforms" + pcolour.end + pcolour.end)

# Facebook (my addition)
try:
    crawl_req = urllib.request.Request("https://www.facebook.com")
    crawl_req.add_header("User-Agent", crawl_ua_browser)
    crawl_req.add_header("Accept-Language", "en-US,en;q=0.9")
    crawl_req.add_header("Sec-Ch-Ua", "\"Google Chrome\";v=\"135\", \"Not-A.Brand\";v=\"8\", \"Chromium\";v=\"135\"")
    crawl_req.add_header("Sec-Ch-Ua-Mobile", "?0")
    crawl_req.add_header("Sec-Ch-Ua-Model", "\"\"")
    crawl_req.add_header("Sec-Ch-Ua-Platform", "\"Windows\"")
    crawl_req.add_header("Sec-Ch-Ua-Platform-Version", "\"15.0.0\"")
    crawl_req.add_header("Sec-Ch-Ua-Wow64", "?0")
    crawl_req.add_header("Sec-Fetch-Dest", "document")
    crawl_req.add_header("Sec-Fetch-Mode", "navigate")
    crawl_req.add_header("Sec-Fetch-Site", "none")
    crawl_req.add_header("Sec-Fetch-User", "?1")
    crawl_req.add_header("Upgrade-Insecure-Requests", "1")
    crawl_res = urllib.request.urlopen(crawl_req, timeout=crawl_timeout)
    res_html = "".join([l.strip() for l in crawl_res.read().decode().splitlines()])
    test_results.append({
        "name": "Facebook",
        "status": "Y",
        "region": "",
        "note": ""
    })
except Exception as e:
    err_dict = handle_connerr(e)
    if err_dict["status"] == 403 or err_dict["status"] == 429:
        test_results.append({
            "name": "Facebook",
            "status": "N",
            "region": "",
            "note": "IP Banned"
        })
    elif err_dict["status"] > 0 and err_dict["status"] != 200:
        test_results.append({
            "name": "Facebook",
            "status": "N",
            "region": "",
            "note": "Status: " + str(crawl_res.status)
        })
    else:
        test_results.append({
            "name": "Facebook",
            "status": "E",
            "region": "",
            "note": err_dict["detail"]
        })
plf_print()

# X (Twitter) (my addition)
try:
    crawl_req = urllib.request.Request("https://x.com")
    crawl_req.add_header("User-Agent", crawl_ua_browser)
    crawl_req.add_header("Accept-Language", "en-US,en;q=0.9")
    crawl_req.add_header("Sec-Ch-Ua", "\"Google Chrome\";v=\"135\", \"Not-A.Brand\";v=\"8\", \"Chromium\";v=\"135\"")
    crawl_req.add_header("Sec-Ch-Ua-Mobile", "?0")
    crawl_req.add_header("Sec-Ch-Ua-Model", "\"\"")
    crawl_req.add_header("Sec-Ch-Ua-Platform", "\"Windows\"")
    crawl_req.add_header("Sec-Ch-Ua-Platform-Version", "\"15.0.0\"")
    crawl_req.add_header("Sec-Ch-Ua-Wow64", "?0")
    crawl_req.add_header("Sec-Fetch-Dest", "document")
    crawl_req.add_header("Sec-Fetch-Mode", "navigate")
    crawl_req.add_header("Sec-Fetch-Site", "none")
    crawl_req.add_header("Sec-Fetch-User", "?1")
    crawl_req.add_header("Upgrade-Insecure-Requests", "1")
    crawl_res = urllib.request.urlopen(crawl_req, timeout=crawl_timeout)
    res_html = "".join([l.strip() for l in crawl_res.read().decode().splitlines()])
    x_region = re.sub(r".*\"country\"\:\s*\"([A-Za-z\-\_\s]+)\".*", r"\1", res_html).upper().strip()
    test_results.append({
        "name": "X (Twitter)",
        "status": "Y",
        "region": x_region,
        "note": ""
    })
except Exception as e:
    err_dict = handle_connerr(e)
    if err_dict["status"] == 403 or err_dict["status"] == 429:
        test_results.append({
            "name": "X (Twitter)",
            "status": "N",
            "region": "",
            "note": "IP Banned"
        })
    elif err_dict["status"] > 0 and err_dict["status"] != 200:
        test_results.append({
            "name": "X (Twitter)",
            "status": "N",
            "region": "",
            "note": "Status: " + str(crawl_res.status)
        })
    else:
        test_results.append({
            "name": "X (Twitter)",
            "status": "E",
            "region": "",
            "note": err_dict["detail"]
        })
plf_print()

# Instagram (my addition)
# Based on my past experiences, the server may return
# 429 HTTP Status Code on some nodes
try:
    crawl_req = urllib.request.Request("https://www.instagram.com")
    crawl_req.add_header("User-Agent", crawl_ua_browser)
    crawl_req.add_header("Accept-Language", "en-US,en;q=0.9")
    crawl_req.add_header("Sec-Ch-Ua", "\"Google Chrome\";v=\"135\", \"Not-A.Brand\";v=\"8\", \"Chromium\";v=\"135\"")
    crawl_req.add_header("Sec-Ch-Ua-Mobile", "?0")
    crawl_req.add_header("Sec-Ch-Ua-Model", "\"\"")
    crawl_req.add_header("Sec-Ch-Ua-Platform", "\"Windows\"")
    crawl_req.add_header("Sec-Ch-Ua-Platform-Version", "\"15.0.0\"")
    crawl_req.add_header("Sec-Ch-Ua-Wow64", "?0")
    crawl_req.add_header("Sec-Fetch-Dest", "document")
    crawl_req.add_header("Sec-Fetch-Mode", "navigate")
    crawl_req.add_header("Sec-Fetch-Site", "none")
    crawl_req.add_header("Sec-Fetch-User", "?1")
    crawl_req.add_header("Upgrade-Insecure-Requests", "1")
    crawl_res = urllib.request.urlopen(crawl_req, timeout=crawl_timeout)
    res_html = "".join([l.strip() for l in crawl_res.read().decode().splitlines()])
    ins_region = re.sub(r".*\"country_code\"\:\s*\"([A-Za-z\-\_\s]+)\".*", r"\1", res_html).upper().strip()
    test_results.append({
        "name": "Instagram",
        "status": "Y",
        "region": ins_region,
        "note": ""
    })
except Exception as e:
    err_dict = handle_connerr(e)
    if err_dict["status"] == 403 or err_dict["status"] == 429:
        test_results.append({
            "name": "Instagram",
            "status": "N",
            "region": "",
            "note": "IP Banned"
        })
    elif err_dict["status"] > 0 and err_dict["status"] != 200:
        test_results.append({
            "name": "Instagram",
            "status": "N",
            "region": "",
            "note": "Status: " + str(crawl_res.status)
        })
    else:
        test_results.append({
            "name": "Instagram",
            "status": "E",
            "region": "",
            "note": err_dict["detail"]
        })
plf_print()

# Reddit
try:
    crawl_req = urllib.request.Request("https://www.reddit.com")
    crawl_req.add_header("User-Agent", crawl_ua_browser)
    crawl_req.add_header("Accept-Language", "en-US,en;q=0.9")
    crawl_req.add_header("Sec-Ch-Ua", "\"Google Chrome\";v=\"135\", \"Not-A.Brand\";v=\"8\", \"Chromium\";v=\"135\"")
    crawl_req.add_header("Sec-Ch-Ua-Mobile", "?0")
    crawl_req.add_header("Sec-Ch-Ua-Model", "\"\"")
    crawl_req.add_header("Sec-Ch-Ua-Platform", "\"Windows\"")
    crawl_req.add_header("Sec-Ch-Ua-Platform-Version", "\"15.0.0\"")
    crawl_req.add_header("Sec-Ch-Ua-Wow64", "?0")
    crawl_req.add_header("Sec-Fetch-Dest", "document")
    crawl_req.add_header("Sec-Fetch-Mode", "navigate")
    crawl_req.add_header("Sec-Fetch-Site", "none")
    crawl_req.add_header("Sec-Fetch-User", "?1")
    crawl_req.add_header("Upgrade-Insecure-Requests", "1")
    crawl_res = urllib.request.urlopen(crawl_req, timeout=crawl_timeout)
    res_html = "".join([l.strip() for l in crawl_res.read().decode().splitlines()])
    res_html = "".join([l.strip() for l in crawl_res.read().decode().splitlines()])
    rd_region = re.sub(r".*country\=\"([A-Za-z\-\_\s]+)\".*", r"\1", res_html).upper().strip()
    test_results.append({
        "name": "Reddit",
        "status": "Y",
        "region": rd_region,
        "note": ""
    })
except Exception as e:
    err_dict = handle_connerr(e)
    if err_dict["status"] == 403 or err_dict["status"] == 429:
        test_results.append({
            "name": "Reddit",
            "status": "N",
            "region": "",
            "note": "IP Banned"
        })
    elif err_dict["status"] > 0 and err_dict["status"] != 200:
        test_results.append({
            "name": "Reddit",
            "status": "N",
            "region": "",
            "note": "Status: " + str(crawl_res.status)
        })
    else:
        test_results.append({
            "name": "Reddit",
            "status": "E",
            "region": "",
            "note": err_dict["detail"]
        })
plf_print()

print("")

# HK Local Platforms
print(pcolour.bold + pcolour.blue + "HK Local Platforms" + pcolour.end + pcolour.end)

# Now E
try:
    crawl_post_param = "{\"contentId\":\"202310181863841\",\"contentType\":\"Vod\",\"pin\":\"\",\"deviceName\":\"Browser\",\"deviceId\":\"w-678913af-3998-3998-3998-39983998\",\"deviceType\":\"WEB\",\"secureCookie\":null,\"callerReferenceNo\":\"W17370372345461425\",\"profileId\":null,\"mupId\":null,\"trackId\":\"738296446.226.1737037103860.2\",\"sessionId\":\"c39f03e6-9e74-4d24-a82f-e0d0f328bb70\"}"
    crawl_req = urllib.request.Request("https://webtvapi.nowe.com/16/1/getVodURL", data=crawl_post_param.encode(), method="POST")
    crawl_req.add_header("User-Agent", crawl_ua_browser)
    crawl_req.add_header("Accept", "application/json, text/javascript, */*; q=0.01")
    crawl_req.add_header("Accept-Language", "en-US,en;q=0.9")
    crawl_req.add_header("Content-Type", "text/plain")
    crawl_req.add_header("Sec-Fetch-Dest", "empty")
    crawl_req.add_header("Sec-Fetch-Mode", "cors")
    crawl_req.add_header("Sec-Fetch-Site", "same-site")
    crawl_req.add_header("Priority", "u=1, i")
    crawl_req.add_header("Origin", "https://www.nowe.com")
    crawl_req.add_header("Referer", "https://www.nowe.com/")
    crawl_res = urllib.request.urlopen(crawl_req, timeout=crawl_timeout)
    res_dict = json.loads(crawl_res.read())
    if res_dict["OTTAPI_ResponseCode"] == "SUCCESS":
        test_results.append({
            "name": "Now E",
            "status": "Y",
            "region": "",
            "note": ""
        })
    elif res_dict["OTTAPI_ResponseCode"] == "GEO_CHECK_FAIL":
        test_results.append({
            "name": "Now E",
            "status": "N",
            "region": "",
            "note": "Not Available"
        })
    else:
        test_results.append({
            "name": "Now E",
            "status": "N",
            "region": "",
            "note": "Status: " + str(res_dict["OTTAPI_ResponseCode"])
        })
except Exception as e:
    err_dict = handle_connerr(e)
    if err_dict["status"] == 403 or err_dict["status"] == 429:
        test_results.append({
            "name": "Now E",
            "status": "N",
            "region": "",
            "note": "IP Banned"
        })
    elif err_dict["status"] > 0 and err_dict["status"] != 200:
        test_results.append({
            "name": "Now E",
            "status": "N",
            "region": "",
            "note": "Status: " + str(crawl_res.status)
        })
    else:
        test_results.append({
            "name": "Now E",
            "status": "E",
            "region": "",
            "note": err_dict["detail"]
        })
plf_print()

# Viu.com
try:
    crawl_req = urllib.request.Request("https://www.viu.com")
    crawl_req.add_header("User-Agent", crawl_ua_browser)
    crawl_res = urllib.request.urlopen(crawl_req, timeout=crawl_timeout)
    res_html = "".join([l.strip() for l in crawl_res.read().decode().splitlines()])
    has_region = bool(len(re.findall(r"\"country\"\:\s*\{\s*\"code\"\:\s*\"([A-Za-z\-\_\s]+)\"", res_html, re.IGNORECASE)))
    if has_region:
        viucom_region = re.sub(r".*\"country\"\:\s*\{\s*\"code\"\:\s*\"([A-Za-z\-\_\s]+)\".*", r"\1", res_html, re.IGNORECASE).strip().upper()
        if viucom_region != "NO-SERVICE":
            test_results.append({
                "name": "Viu.com",
                "status": "Y",
                "region": viucom_region,
                "note": ""
            })
        else:
            test_results.append({
                "name": "Viu.com",
                "status": "N",
                "region": "",
                "note": "Not Available"
            })
    else:
        test_results.append({
            "name": "Viu.com",
            "status": "N",
            "region": "",
            "note": "Not Available"
        })
except Exception as e:
    err_dict = handle_connerr(e)
    if err_dict["status"] == 403 or err_dict["status"] == 429:
        test_results.append({
            "name": "Viu.com",
            "status": "N",
            "region": "",
            "note": "IP Banned"
        })
    elif err_dict["status"] > 0 and err_dict["status"] != 200:
        test_results.append({
            "name": "Viu.com",
            "status": "N",
            "region": "",
            "note": "Status: " + str(crawl_res.status)
        })
    else:
        test_results.append({
            "name": "Viu.com",
            "status": "E",
            "region": "",
            "note": err_dict["detail"]
        })
plf_print()

# Viu.TV
try:
    crawl_post_param = "{\"callerReferenceNo\":\"20210726112323\",\"contentId\":\"099\",\"contentType\":\"Channel\",\"channelno\":\"099\",\"mode\":\"prod\",\"deviceId\":\"29b3cb117a635d5b56\",\"deviceType\":\"ANDROID_WEB\"}"
    crawl_req = urllib.request.Request("https://api.viu.now.com/p8/3/getLiveURL", data=crawl_post_param.encode(), method="POST")
    crawl_req.add_header("User-Agent", crawl_ua_browser)
    crawl_req.add_header("Content-Type", "application/json")
    crawl_res = urllib.request.urlopen(crawl_req, timeout=crawl_timeout)
    res_dict = json.loads(crawl_res.read())
    viutv_rc = res_dict["responseCode"]
    if viutv_rc == "SUCCESS":
        test_results.append({
            "name": "Viu.TV",
            "status": "Y",
            "region": "",
            "note": ""
        })
    elif viutv_rc == "GEO_CHECK_FAIL":
        test_results.append({
            "name": "Viu.TV",
            "status": "N",
            "region": "",
            "note": "Not Available"
        })
    else:
        test_results.append({
            "name": "Viu.TV",
            "status": "N",
            "region": "",
            "note": "Status: " + str(viutv_rc)
        })
except Exception as e:
    err_dict = handle_connerr(e)
    if err_dict["status"] == 403 or err_dict["status"] == 429:
        test_results.append({
            "name": "Viu.TV",
            "status": "N",
            "region": "",
            "note": "IP Banned"
        })
    elif err_dict["status"] > 0 and err_dict["status"] != 200:
        test_results.append({
            "name": "Viu.TV",
            "status": "N",
            "region": "",
            "note": "Status: " + str(crawl_res.status)
        })
    else:
        test_results.append({
            "name": "Viu.TV",
            "status": "E",
            "region": "",
            "note": err_dict["detail"]
        })
plf_print()

# MyTVSuper
try:
    crawl_req = urllib.request.Request("https://www.mytvsuper.com/api/auth/getSession/self/")
    crawl_req.add_header("User-Agent", crawl_ua_browser)
    crawl_res = urllib.request.urlopen(crawl_req, timeout=crawl_timeout)
    res_dict = json.loads(crawl_res.read())
    mts_region = res_dict["country_code"].strip().upper()
    mts_supported = bool(res_dict["supported_country"])
    if mts_region == "ZP":
        test_results.append({
            "name": "MyTVSuper",
            "status": "N",
            "region": mts_region,
            "note": "IP Banned"
        })
    elif mts_supported:
        test_results.append({
            "name": "MyTVSuper",
            "status": "Y",
            "region": mts_region,
            "note": ""
        })
    else:
        test_results.append({
            "name": "MyTVSuper",
            "status": "N",
            "region": mts_region,
            "note": "Not Available"
        })
except Exception as e:
    err_dict = handle_connerr(e)
    if err_dict["status"] == 403 or err_dict["status"] == 429:
        test_results.append({
            "name": "MyTVSuper",
            "status": "N",
            "region": "",
            "note": "IP Banned"
        })
    elif err_dict["status"] > 0 and err_dict["status"] != 200:
        test_results.append({
            "name": "MyTVSuper",
            "status": "N",
            "region": "",
            "note": "Status: " + str(crawl_res.status)
        })
    else:
        test_results.append({
            "name": "MyTVSuper",
            "status": "E",
            "region": "",
            "note": err_dict["detail"]
        })
plf_print()

# Bilibili HK/MO/TW
# Sometimes, the web version (www.bilibili.tv) may return
# a Block Page on some nodes.
try:
    crawl_session_1 = ""
    crawl_session_chars = "0123456789abcdef"
    for _ in range(32):
        crawl_session_1 += crawl_session_chars[random.randint(0, len(crawl_session_chars)-1)]
    crawl_req_1 = urllib.request.Request("https://api.bilibili.com/pgc/player/web/playurl?avid=18281381&cid=29892777&qn=0&type=&otype=json&ep_id=183799&fourk=1&fnver=0&fnval=16&session=" + str(crawl_session_1) + "&module=bangumi")
    crawl_req_1.add_header("User-Agent", crawl_ua_browser)
    crawl_res_1 = urllib.request.urlopen(crawl_req_1, timeout=crawl_timeout)
    res_dict_1 = json.loads(crawl_res_1.read())
    bl_code = int(res_dict_1["code"])
    if bl_code == 0:
        crawl_req_2 = urllib.request.Request("https://www.bilibili.tv")
        crawl_req_2.add_header("User-Agent", crawl_ua_browser)
        crawl_res_2 = urllib.request.urlopen(crawl_req_2, timeout=crawl_timeout)
        test_results.append({
            "name": "Bilibili HK/MO/TW",
            "status": "Y",
            "region": "",
            "note": ""
        })
    elif bl_code == -10403:
        test_results.append({
            "name": "Bilibili HK/MO/TW",
            "status": "N",
            "region": "",
            "note": "Not Available"
        })
    else:
        test_results.append({
            "name": "Bilibili HK/MO/TW",
            "status": "N",
            "region": "",
            "note": "Code: " + str(bl_code)
        })
except Exception as e:
    err_dict = handle_connerr(e)
    if err_dict["status"] == 403 or err_dict["status"] == 429:
        test_results.append({
            "name": "Bilibili HK/MO/TW",
            "status": "N",
            "region": "",
            "note": "IP Banned"
        })
    elif err_dict["status"] > 0 and err_dict["status"] != 200:
        test_results.append({
            "name": "Bilibili HK/MO/TW",
            "status": "N",
            "region": "",
            "note": "Status: " + str(crawl_res.status)
        })
    else:
        test_results.append({
            "name": "Bilibili HK/MO/TW",
            "status": "E",
            "region": "",
            "note": err_dict["detail"]
        })
plf_print()

# Bahamut Anime
ba_sn = "37783"
try:
    crawl_req_1 = urllib.request.Request("https://ani.gamer.com.tw/ajax/getdeviceid.php")
    crawl_req_1.add_header("User-Agent", crawl_ua_curl)
    crawl_res_1 = urllib.request.urlopen(crawl_req_1, timeout=crawl_timeout)
    crawl_cookie_r_1 = header_to_cookie(crawl_res_1.headers)
    res_dict_1 = json.loads(crawl_res_1.read())
    ba_device_id = res_dict_1["deviceid"]
    crawl_cookie_2 = crawl_cookie_r_1
    crawl_req_2 = urllib.request.Request("https://ani.gamer.com.tw/ajax/token.php?adID=89422&sn=" + str(ba_sn) + "&device=" + str(ba_device_id))
    crawl_req_2.add_header("User-Agent", crawl_ua_curl)
    crawl_req_2.add_header("Cookie", cookie_dict_to_str(crawl_cookie_2))
    crawl_res_2 = urllib.request.urlopen(crawl_req_2, timeout=crawl_timeout)
    res_html_2 = "".join([l.strip() for l in crawl_res_2.read().decode().splitlines()])
    if "animeSn" not in res_html_2:
        test_results.append({
            "name": "Bahamut Anime",
            "status": "N",
            "region": "",
            "note": ""
        })
    else:
        crawl_cookie_3 = crawl_cookie_r_1
        crawl_req_3 = urllib.request.Request("https://ani.gamer.com.tw/")
        crawl_req_3.add_header("User-Agent", crawl_ua_browser)
        crawl_req_3.add_header("Cookie", cookie_dict_to_str(crawl_cookie_3))
        crawl_req_3.add_header("Accept", "*/*;q=0.8,application/signed-exchange;v=b3;q=0.7")
        crawl_req_3.add_header("Accept-Language", "zh-CN,zh;q=0.9")
        crawl_req_3.add_header("Sec-Ch-Ua", "\"Google Chrome\";v=\"135\", \"Not-A.Brand\";v=\"8\", \"Chromium\";v=\"135\"")
        crawl_req_3.add_header("Sec-Ch-Ua-Mobile", "?0")
        crawl_req_3.add_header("Sec-Ch-Ua-Model", "\"\"")
        crawl_req_3.add_header("Sec-Ch-Ua-Platform", "\"Windows\"")
        crawl_req_3.add_header("Sec-Ch-Ua-Platform-Version", "\"15.0.0\"")
        crawl_req_3.add_header("Sec-Fetch-Dest", "document")
        crawl_req_3.add_header("Sec-Fetch-Mode", "navigate")
        crawl_req_3.add_header("Sec-Fetch-Site", "none")
        crawl_req_3.add_header("Sec-Fetch-User", "?1")
        crawl_res_3 = urllib.request.urlopen(crawl_req_3, timeout=crawl_timeout)
        res_html_3 = "".join([l.strip() for l in crawl_res_3.read().decode().splitlines()])
        ba_region = re.sub(r".*data\-geo\=\"([A-Za-z\-\_\s]+)\".*", r"\1", res_html_3).strip().upper()
        test_results.append({
            "name": "Bahamut Anime",
            "status": "Y",
            "region": ba_region,
            "note": ""
        })
except Exception as e:
    err_dict = handle_connerr(e)
    if err_dict["status"] == 403 or err_dict["status"] == 429:
        test_results.append({
            "name": "Bahamut Anime",
            "status": "N",
            "region": "",
            "note": "IP Banned"
        })
    elif err_dict["status"] > 0 and err_dict["status"] != 200:
        test_results.append({
            "name": "Bahamut Anime",
            "status": "N",
            "region": "",
            "note": "Status: " + str(crawl_res.status)
        })
    else:
        test_results.append({
            "name": "Bahamut Anime",
            "status": "E",
            "region": "",
            "note": err_dict["detail"]
        })
plf_print()

# HK01
try:
    crawl_req = urllib.request.Request("https://www.hk01.com")
    crawl_req.add_header("User-Agent", crawl_ua_browser)
    crawl_res = urllib.request.urlopen(crawl_req, timeout=crawl_timeout)
    test_results.append({
        "name": "HK01",
        "status": "Y",
        "region": "",
        "note": ""
    })
except Exception as e:
    err_dict = handle_connerr(e)
    if err_dict["status"] == 403 or err_dict["status"] == 429:
        test_results.append({
            "name": "HK01",
            "status": "N",
            "region": "",
            "note": "IP Banned"
        })
    elif err_dict["status"] > 0 and err_dict["status"] != 200:
        test_results.append({
            "name": "HK01",
            "status": "N",
            "region": "",
            "note": "Status: " + str(crawl_res.status)
        })
    else:
        test_results.append({
            "name": "HK01",
            "status": "E",
            "region": "",
            "note": err_dict["detail"]
        })
plf_print()

# HK Observatory
try:
    crawl_req = urllib.request.Request("https://www.weather.gov.hk")
    crawl_req.add_header("User-Agent", crawl_ua_browser)
    crawl_res = urllib.request.urlopen(crawl_req, timeout=crawl_timeout)
    test_results.append({
        "name": "HK Observatory",
        "status": "Y",
        "region": "",
        "note": ""
    })
except Exception as e:
    err_dict = handle_connerr(e)
    if err_dict["status"] == 403 or err_dict["status"] == 429:
        test_results.append({
            "name": "HK Observatory",
            "status": "N",
            "region": "",
            "note": "IP Banned"
        })
    elif err_dict["status"] > 0 and err_dict["status"] != 200:
        test_results.append({
            "name": "HK Observatory",
            "status": "N",
            "region": "",
            "note": "Status: " + str(crawl_res.status)
        })
    else:
        test_results.append({
            "name": "HK Observatory",
            "status": "E",
            "region": "",
            "note": err_dict["detail"]
        })
plf_print()

print("")

# HK Universities
print(pcolour.bold + pcolour.blue + "HK Universities" + pcolour.end + pcolour.end)

# HKU
try:
    crawl_req = urllib.request.Request("http://hku.hk")
    crawl_req.add_header("User-Agent", crawl_ua_browser)
    crawl_res = urllib.request.urlopen(crawl_req, timeout=crawl_timeout)
    test_results.append({
        "name": "HKU",
        "status": "Y",
        "region": "",
        "note": ""
    })
except Exception as e:
    err_dict = handle_connerr(e)
    if err_dict["status"] == 403 or err_dict["status"] == 429:
        test_results.append({
            "name": "HKU",
            "status": "N",
            "region": "",
            "note": "IP Banned"
        })
    elif err_dict["status"] > 0 and err_dict["status"] != 200:
        test_results.append({
            "name": "HKU",
            "status": "N",
            "region": "",
            "note": "Status: " + str(crawl_res.status)
        })
    else:
        test_results.append({
            "name": "HKU",
            "status": "E",
            "region": "",
            "note": err_dict["detail"]
        })
plf_print()

# HKUST
try:
    crawl_req = urllib.request.Request("http://hkust.edu.hk")
    crawl_req.add_header("User-Agent", crawl_ua_browser)
    crawl_res = urllib.request.urlopen(crawl_req, timeout=crawl_timeout)
    test_results.append({
        "name": "HKUST",
        "status": "Y",
        "region": "",
        "note": ""
    })
except Exception as e:
    err_dict = handle_connerr(e)
    if err_dict["status"] == 403 or err_dict["status"] == 429:
        test_results.append({
            "name": "HKUST",
            "status": "N",
            "region": "",
            "note": "IP Banned"
        })
    elif err_dict["status"] > 0 and err_dict["status"] != 200:
        test_results.append({
            "name": "HKUST",
            "status": "N",
            "region": "",
            "note": "Status: " + str(crawl_res.status)
        })
    else:
        test_results.append({
            "name": "HKUST",
            "status": "E",
            "region": "",
            "note": err_dict["detail"]
        })
plf_print()

# CUHK
try:
    crawl_req = urllib.request.Request("http://cuhk.edu.hk")
    crawl_req.add_header("User-Agent", crawl_ua_browser)
    crawl_res = urllib.request.urlopen(crawl_req, timeout=crawl_timeout)
    test_results.append({
        "name": "CUHK",
        "status": "Y",
        "region": "",
        "note": ""
    })
except Exception as e:
    err_dict = handle_connerr(e)
    if err_dict["status"] == 403 or err_dict["status"] == 429:
        test_results.append({
            "name": "CUHK",
            "status": "N",
            "region": "",
            "note": "IP Banned"
        })
    elif err_dict["status"] > 0 and err_dict["status"] != 200:
        test_results.append({
            "name": "CUHK",
            "status": "N",
            "region": "",
            "note": "Status: " + str(crawl_res.status)
        })
    else:
        test_results.append({
            "name": "CUHK",
            "status": "E",
            "region": "",
            "note": err_dict["detail"]
        })
plf_print()

# HKBU
try:
    crawl_req = urllib.request.Request("http://hkbu.edu.hk")
    crawl_req.add_header("User-Agent", crawl_ua_browser)
    crawl_res = urllib.request.urlopen(crawl_req, timeout=crawl_timeout)
    test_results.append({
        "name": "HKBU",
        "status": "Y",
        "region": "",
        "note": ""
    })
except Exception as e:
    err_dict = handle_connerr(e)
    if err_dict["status"] == 403 or err_dict["status"] == 429:
        test_results.append({
            "name": "HKBU",
            "status": "N",
            "region": "",
            "note": "IP Banned"
        })
    elif err_dict["status"] > 0 and err_dict["status"] != 200:
        test_results.append({
            "name": "HKBU",
            "status": "N",
            "region": "",
            "note": "Status: " + str(crawl_res.status)
        })
    else:
        test_results.append({
            "name": "HKBU",
            "status": "E",
            "region": "",
            "note": err_dict["detail"]
        })
plf_print()

# CityU
try:
    crawl_req = urllib.request.Request("http://cityu.edu.hk")
    crawl_req.add_header("User-Agent", crawl_ua_browser)
    crawl_res = urllib.request.urlopen(crawl_req, timeout=crawl_timeout)
    test_results.append({
        "name": "CityU",
        "status": "Y",
        "region": "",
        "note": ""
    })
except Exception as e:
    err_dict = handle_connerr(e)
    if err_dict["status"] == 403 or err_dict["status"] == 429:
        test_results.append({
            "name": "CityU",
            "status": "N",
            "region": "",
            "note": "IP Banned"
        })
    elif err_dict["status"] > 0 and err_dict["status"] != 200:
        test_results.append({
            "name": "CityU",
            "status": "N",
            "region": "",
            "note": "Status: " + str(crawl_res.status)
        })
    else:
        test_results.append({
            "name": "CityU",
            "status": "E",
            "region": "",
            "note": err_dict["detail"]
        })
plf_print()

# PolyU
try:
    crawl_req = urllib.request.Request("http://polyu.edu.hk")
    crawl_req.add_header("User-Agent", crawl_ua_browser)
    crawl_res = urllib.request.urlopen(crawl_req, timeout=crawl_timeout)
    test_results.append({
        "name": "PolyU",
        "status": "Y",
        "region": "",
        "note": ""
    })
except Exception as e:
    err_dict = handle_connerr(e)
    if err_dict["status"] == 403 or err_dict["status"] == 429:
        test_results.append({
            "name": "PolyU",
            "status": "N",
            "region": "",
            "note": "IP Banned"
        })
    elif err_dict["status"] > 0 and err_dict["status"] != 200:
        test_results.append({
            "name": "PolyU",
            "status": "N",
            "region": "",
            "note": "Status: " + str(crawl_res.status)
        })
    else:
        test_results.append({
            "name": "PolyU",
            "status": "E",
            "region": "",
            "note": err_dict["detail"]
        })
plf_print()

# EdUHK
try:
    crawl_ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    crawl_ctx.options |= 0x4  # OP_LEGACY_SERVER_CONNECT
    crawl_req = urllib.request.Request("http://eduhk.hk", data=crawl_post_param.encode(), method="POST")
    crawl_req.add_header("User-Agent", crawl_ua_browser)
    crawl_res = urllib.request.urlopen(crawl_req, context=crawl_ctx, timeout=crawl_timeout)
    test_results.append({
        "name": "EdUHK",
        "status": "Y",
        "region": "",
        "note": ""
    })
except Exception as e:
    err_dict = handle_connerr(e)
    if err_dict["status"] == 403 or err_dict["status"] == 429:
        test_results.append({
            "name": "EdUHK",
            "status": "N",
            "region": "",
            "note": "IP Banned"
        })
    elif err_dict["status"] > 0 and err_dict["status"] != 200:
        test_results.append({
            "name": "EdUHK",
            "status": "N",
            "region": "",
            "note": "Status: " + str(crawl_res.status)
        })
    else:
        test_results.append({
            "name": "EdUHK",
            "status": "E",
            "region": "",
            "note": err_dict["detail"]
        })
plf_print()

# LingU
try:
    crawl_req = urllib.request.Request("http://ln.edu.hk")
    crawl_req.add_header("User-Agent", crawl_ua_browser)
    crawl_req.add_header("Accept-Language", "en-US,en;q=0.9")
    crawl_req.add_header("Sec-Ch-Ua", "\"Google Chrome\";v=\"135\", \"Not-A.Brand\";v=\"8\", \"Chromium\";v=\"135\"")
    crawl_req.add_header("Sec-Ch-Ua-Mobile", "?0")
    crawl_req.add_header("Sec-Ch-Ua-Model", "\"\"")
    crawl_req.add_header("Sec-Ch-Ua-Platform", "\"Windows\"")
    crawl_req.add_header("Sec-Ch-Ua-Platform-Version", "\"15.0.0\"")
    crawl_req.add_header("Sec-Ch-Ua-Wow64", "?0")
    crawl_req.add_header("Sec-Fetch-Dest", "document")
    crawl_req.add_header("Sec-Fetch-Mode", "navigate")
    crawl_req.add_header("Sec-Fetch-Site", "none")
    crawl_req.add_header("Sec-Fetch-User", "?1")
    crawl_req.add_header("Upgrade-Insecure-Requests", "1")
    crawl_res = urllib.request.urlopen(crawl_req, timeout=crawl_timeout)
    test_results.append({
        "name": "LingU",
        "status": "Y",
        "region": "",
        "note": ""
    })
except Exception as e:
    err_dict = handle_connerr(e)
    if err_dict["status"] == 403 or err_dict["status"] == 429:
        test_results.append({
            "name": "LingU",
            "status": "N",
            "region": "",
            "note": "IP Banned"
        })
    elif err_dict["status"] > 0 and err_dict["status"] != 200:
        test_results.append({
            "name": "LingU",
            "status": "N",
            "region": "",
            "note": "Status: " + str(crawl_res.status)
        })
    else:
        test_results.append({
            "name": "LingU",
            "status": "E",
            "region": "",
            "note": err_dict["detail"]
        })
plf_print()

# HKMU
try:
    crawl_req = urllib.request.Request("http://www.hkmu.edu.hk")
    crawl_req.add_header("User-Agent", crawl_ua_browser)
    crawl_res = urllib.request.urlopen(crawl_req, timeout=crawl_timeout)
    test_results.append({
        "name": "HKMU",
        "status": "Y",
        "region": "",
        "note": ""
    })
except Exception as e:
    err_dict = handle_connerr(e)
    if err_dict["status"] == 403 or err_dict["status"] == 429:
        test_results.append({
            "name": "HKMU",
            "status": "N",
            "region": "",
            "note": "IP Banned"
        })
    elif err_dict["status"] > 0 and err_dict["status"] != 200:
        test_results.append({
            "name": "HKMU",
            "status": "N",
            "region": "",
            "note": "Status: " + str(crawl_res.status)
        })
    else:
        test_results.append({
            "name": "HKMU",
            "status": "E",
            "region": "",
            "note": err_dict["detail"]
        })
plf_print()

# Hang Seng University
try:
    crawl_req = urllib.request.Request("https://www.hsu.edu.hk")
    crawl_req.add_header("User-Agent", crawl_ua_browser)
    crawl_res = urllib.request.urlopen(crawl_req, timeout=crawl_timeout)
    test_results.append({
        "name": "Hang Seng University",
        "status": "Y",
        "region": "",
        "note": ""
    })
except Exception as e:
    err_dict = handle_connerr(e)
    if err_dict["status"] == 403 or err_dict["status"] == 429:
        test_results.append({
            "name": "Hang Seng University",
            "status": "N",
            "region": "",
            "note": "IP Banned"
        })
    elif err_dict["status"] > 0 and err_dict["status"] != 200:
        test_results.append({
            "name": "Hang Seng University",
            "status": "N",
            "region": "",
            "note": "Status: " + str(crawl_res.status)
        })
    else:
        test_results.append({
            "name": "Hang Seng University",
            "status": "E",
            "region": "",
            "note": err_dict["detail"]
        })
plf_print()

print("")

# HK University Libraries
print(pcolour.bold + pcolour.blue + "HK University Libraries" + pcolour.end + pcolour.end)

# HKU Library
try:
    crawl_req = urllib.request.Request("https://lib.hku.hk")
    crawl_req.add_header("User-Agent", crawl_ua_browser)
    crawl_res = urllib.request.urlopen(crawl_req, timeout=crawl_timeout)
    test_results.append({
        "name": "HKU Library",
        "status": "Y",
        "region": "",
        "note": ""
    })
except Exception as e:
    err_dict = handle_connerr(e)
    if err_dict["status"] == 403 or err_dict["status"] == 429:
        test_results.append({
            "name": "HKU Library",
            "status": "N",
            "region": "",
            "note": "IP Banned"
        })
    elif err_dict["status"] > 0 and err_dict["status"] != 200:
        test_results.append({
            "name": "HKU Library",
            "status": "N",
            "region": "",
            "note": "Status: " + str(crawl_res.status)
        })
    else:
        test_results.append({
            "name": "HKU Library",
            "status": "E",
            "region": "",
            "note": err_dict["detail"]
        })
plf_print()

# HKUST Library
try:
    crawl_req = urllib.request.Request("https://library.hkust.edu.hk")
    crawl_req.add_header("User-Agent", crawl_ua_browser)
    crawl_res = urllib.request.urlopen(crawl_req, timeout=crawl_timeout)
    test_results.append({
        "name": "HKUST Library",
        "status": "Y",
        "region": "",
        "note": ""
    })
except Exception as e:
    err_dict = handle_connerr(e)
    if err_dict["status"] == 403 or err_dict["status"] == 429:
        test_results.append({
            "name": "HKUST Library",
            "status": "N",
            "region": "",
            "note": "IP Banned"
        })
    elif err_dict["status"] > 0 and err_dict["status"] != 200:
        test_results.append({
            "name": "HKUST Library",
            "status": "N",
            "region": "",
            "note": "Status: " + str(crawl_res.status)
        })
    else:
        test_results.append({
            "name": "HKUST Library",
            "status": "E",
            "region": "",
            "note": err_dict["detail"]
        })
plf_print()

# CUHK Library
try:
    crawl_req = urllib.request.Request("https://www.lib.cuhk.edu.hk/")
    crawl_req.add_header("User-Agent", crawl_ua_browser)
    crawl_res = urllib.request.urlopen(crawl_req, timeout=crawl_timeout)
    test_results.append({
        "name": "CUHK Library",
        "status": "Y",
        "region": "",
        "note": ""
    })
except Exception as e:
    err_dict = handle_connerr(e)
    if err_dict["status"] == 403 or err_dict["status"] == 429:
        test_results.append({
            "name": "CUHK Library",
            "status": "N",
            "region": "",
            "note": "IP Banned"
        })
    elif err_dict["status"] > 0 and err_dict["status"] != 200:
        test_results.append({
            "name": "CUHK Library",
            "status": "N",
            "region": "",
            "note": "Status: " + str(crawl_res.status)
        })
    else:
        test_results.append({
            "name": "CUHK Library",
            "status": "E",
            "region": "",
            "note": err_dict["detail"]
        })
plf_print()

print("")

# HK Banks (HTTPS)
# Some proxy providers (like Cliproxy) ban all bank websites/apps,
# regardless of whether they are HK banks.
print(pcolour.bold + pcolour.blue + "HK Banks" + pcolour.end + pcolour.end)

# HSBC (HK)
try:
    crawl_req = urllib.request.Request("https://www.hsbc.com.hk")
    crawl_req.add_header("User-Agent", crawl_ua_browser)
    crawl_res = urllib.request.urlopen(crawl_req, timeout=crawl_timeout)
    test_results.append({
        "name": "HSBC (HK)",
        "status": "Y",
        "region": "",
        "note": ""
    })
except Exception as e:
    err_dict = handle_connerr(e)
    if err_dict["status"] == 403 or err_dict["status"] == 429:
        test_results.append({
            "name": "HSBC (HK)",
            "status": "N",
            "region": "",
            "note": "IP Banned"
        })
    elif err_dict["status"] > 0 and err_dict["status"] != 200:
        test_results.append({
            "name": "HSBC (HK)",
            "status": "N",
            "region": "",
            "note": "Status: " + str(crawl_res.status)
        })
    else:
        test_results.append({
            "name": "HSBC (HK)",
            "status": "E",
            "region": "",
            "note": err_dict["detail"]
        })
plf_print()

# Hang Seng Bank (HK)
try:
    crawl_req = urllib.request.Request("https://www.hangseng.com")
    crawl_req.add_header("User-Agent", crawl_ua_browser)
    crawl_res = urllib.request.urlopen(crawl_req, timeout=crawl_timeout)
    test_results.append({
        "name": "Hang Seng Bank (HK)",
        "status": "Y",
        "region": "",
        "note": ""
    })
except Exception as e:
    err_dict = handle_connerr(e)
    if err_dict["status"] == 403 or err_dict["status"] == 429:
        test_results.append({
            "name": "Hang Seng Bank (HK)",
            "status": "N",
            "region": "",
            "note": "IP Banned"
        })
    elif err_dict["status"] > 0 and err_dict["status"] != 200:
        test_results.append({
            "name": "Hang Seng Bank (HK)",
            "status": "N",
            "region": "",
            "note": "Status: " + str(crawl_res.status)
        })
    else:
        test_results.append({
            "name": "Hang Seng Bank (HK)",
            "status": "E",
            "region": "",
            "note": err_dict["detail"]
        })
plf_print()

# Bank of China (HK)
try:
    crawl_req = urllib.request.Request("https://www.bochk.com")
    crawl_req.add_header("User-Agent", crawl_ua_browser)
    crawl_res = urllib.request.urlopen(crawl_req, timeout=crawl_timeout)
    test_results.append({
        "name": "Bank of China (HK)",
        "status": "Y",
        "region": "",
        "note": ""
    })
except Exception as e:
    err_dict = handle_connerr(e)
    if err_dict["status"] == 403 or err_dict["status"] == 429:
        test_results.append({
            "name": "Bank of China (HK)",
            "status": "N",
            "region": "",
            "note": "IP Banned"
        })
    elif err_dict["status"] > 0 and err_dict["status"] != 200:
        test_results.append({
            "name": "Bank of China (HK)",
            "status": "N",
            "region": "",
            "note": "Status: " + str(crawl_res.status)
        })
    else:
        test_results.append({
            "name": "Bank of China (HK)",
            "status": "E",
            "region": "",
            "note": err_dict["detail"]
        })
plf_print()

# Standard Chartered (HK)
try:
    crawl_req = urllib.request.Request("https://www.sc.com/hk/")
    crawl_req.add_header("User-Agent", crawl_ua_browser)
    crawl_res = urllib.request.urlopen(crawl_req, timeout=crawl_timeout)
    test_results.append({
        "name": "Standard Chartered (HK)",
        "status": "Y",
        "region": "",
        "note": ""
    })
except Exception as e:
    err_dict = handle_connerr(e)
    if err_dict["status"] == 403 or err_dict["status"] == 429:
        test_results.append({
            "name": "Standard Chartered (HK)",
            "status": "N",
            "region": "",
            "note": "IP Banned"
        })
    elif err_dict["status"] > 0 and err_dict["status"] != 200:
        test_results.append({
            "name": "Standard Chartered (HK)",
            "status": "N",
            "region": "",
            "note": "Status: " + str(crawl_res.status)
        })
    else:
        test_results.append({
            "name": "Standard Chartered (HK)",
            "status": "E",
            "region": "",
            "note": err_dict["detail"]
        })
plf_print()

# Citibank (HK)
try:
    crawl_req = urllib.request.Request("https://www.citibank.com.hk")
    crawl_req.add_header("User-Agent", crawl_ua_browser)
    crawl_res = urllib.request.urlopen(crawl_req, timeout=crawl_timeout)
    test_results.append({
        "name": "Citibank (HK)",
        "status": "Y",
        "region": "",
        "note": ""
    })
except Exception as e:
    err_dict = handle_connerr(e)
    if err_dict["status"] == 403 or err_dict["status"] == 429:
        test_results.append({
            "name": "Citibank (HK)",
            "status": "N",
            "region": "",
            "note": "IP Banned"
        })
    elif err_dict["status"] > 0 and err_dict["status"] != 200:
        test_results.append({
            "name": "Citibank (HK)",
            "status": "N",
            "region": "",
            "note": "Status: " + str(crawl_res.status)
        })
    else:
        test_results.append({
            "name": "Citibank (HK)",
            "status": "E",
            "region": "",
            "note": err_dict["detail"]
        })
plf_print()

print("")

# Mainland Websites
# Some proxy providers (like IP2World) ban all Mainland ICP-Registered websites.

if c_test_ml == "y":
    print(pcolour.bold + pcolour.blue + "Mainland Websites" + pcolour.end + pcolour.end)
    print("(Accessibility Only; No Restriction Check)")

    # Tencent/QQ News
    try:
        crawl_req = urllib.request.Request("https://www.qq.com")
        crawl_req.add_header("User-Agent", crawl_ua_browser)
        crawl_res = urllib.request.urlopen(crawl_req, timeout=crawl_timeout)
        test_results.append({
            "name": "Tencent/QQ News",
            "status": "Y",
            "region": "",
            "note": ""
        })
    except Exception as e:
        err_dict = handle_connerr(e)
        if err_dict["status"] == 403 or err_dict["status"] == 429:
            test_results.append({
                "name": "Tencent/QQ News",
                "status": "N",
                "region": "",
                "note": "IP Banned"
            })
        elif err_dict["status"] > 0 and err_dict["status"] != 200:
            test_results.append({
                "name": "Tencent/QQ News",
                "status": "N",
                "region": "",
                "note": "Status: " + str(crawl_res.status)
            })
        else:
            test_results.append({
                "name": "Tencent/QQ News",
                "status": "E",
                "region": "",
                "note": err_dict["detail"]
            })
    plf_print()

    # QQ Mail
    try:
        crawl_req = urllib.request.Request("https://mail.qq.com")
        crawl_req.add_header("User-Agent", crawl_ua_browser)
        crawl_res = urllib.request.urlopen(crawl_req, timeout=crawl_timeout)
        test_results.append({
            "name": "QQ Mail",
            "status": "Y",
            "region": "",
            "note": ""
        })
    except Exception as e:
        err_dict = handle_connerr(e)
        if err_dict["status"] == 403 or err_dict["status"] == 429:
            test_results.append({
                "name": "QQ Mail",
                "status": "N",
                "region": "",
                "note": "IP Banned"
            })
        elif err_dict["status"] > 0 and err_dict["status"] != 200:
            test_results.append({
                "name": "QQ Mail",
                "status": "N",
                "region": "",
                "note": "Status: " + str(crawl_res.status)
            })
        else:
            test_results.append({
                "name": "QQ Mail",
                "status": "E",
                "region": "",
                "note": err_dict["detail"]
            })
    plf_print()

    # Weixin (Mainland)
    try:
        crawl_req = urllib.request.Request("https://weixin.qq.com")
        crawl_req.add_header("User-Agent", crawl_ua_browser)
        crawl_res = urllib.request.urlopen(crawl_req, timeout=crawl_timeout)
        test_results.append({
            "name": "Weixin (Mainland)",
            "status": "Y",
            "region": "",
            "note": ""
        })
    except Exception as e:
        err_dict = handle_connerr(e)
        if err_dict["status"] == 403 or err_dict["status"] == 429:
            test_results.append({
                "name": "Weixin (Mainland)",
                "status": "N",
                "region": "",
                "note": "IP Banned"
            })
        elif err_dict["status"] > 0 and err_dict["status"] != 200:
            test_results.append({
                "name": "Weixin (Mainland)",
                "status": "N",
                "region": "",
                "note": "Status: " + str(crawl_res.status)
            })
        else:
            test_results.append({
                "name": "Weixin (Mainland)",
                "status": "E",
                "region": "",
                "note": err_dict["detail"]
            })
    plf_print()

    # Baidu Search No CAPTCHA
    try:
        crawl_req = urllib.request.Request("https://www.baidu.com/s?wd=curl")
        crawl_req.add_header("User-Agent", crawl_ua_browser)
        crawl_req.add_header("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7")
        crawl_req.add_header("Accept-Language", "en-US,en;q=0.9")
        crawl_req.add_header("Accept-Encoding", "gzip, deflate, br, zstd")
        crawl_req.add_header("Host", "www.baidu.com")
        crawl_req.add_header("Sec-Ch-Ua", "\"Google Chrome\";v=\"135\", \"Not-A.Brand\";v=\"8\", \"Chromium\";v=\"135\"")
        crawl_req.add_header("Sec-Ch-Ua-Mobile", "?0")
        crawl_req.add_header("Sec-Ch-Ua-Model", "\"\"")
        crawl_req.add_header("Sec-Ch-Ua-Platform", "\"Windows\"")
        crawl_req.add_header("Sec-Ch-Ua-Platform-Version", "\"15.0.0\"")
        crawl_req.add_header("Sec-Ch-Ua-Wow64", "?0")
        crawl_req.add_header("Sec-Fetch-Dest", "document")
        crawl_req.add_header("Sec-Fetch-Mode", "navigate")
        crawl_req.add_header("Sec-Fetch-Site", "none")
        crawl_req.add_header("Sec-Fetch-User", "?1")
        crawl_req.add_header("Upgrade-Insecure-Requests", "1")
        crawl_res = urllib.request.urlopen(crawl_req, timeout=crawl_timeout)
        res_html = "".join([l.strip() for l in crawl_res.read().decode().splitlines()])
        if "百度安全验证" not in res_html:
            test_results.append({
                "name": "Baidu Search No CAPTCHA",
                "status": "Y",
                "region": "",
                "note": ""
            })
        else:
            test_results.append({
                "name": "Baidu Search No CAPTCHA",
                "status": "N",
                "region": "",
                "note": "IP Banned"
            })
    except Exception as e:
        # ignore brotli and gzip errors
        errtxt = str(e).lower()
        if "can't decode byte" in errtxt:
            test_results.append({
                "name": "Baidu Search No CAPTCHA",
                "status": "Y",
                "region": "",
                "note": ""
            })
        else:
            err_dict = handle_connerr(e)
            if err_dict["status"] == 403 or err_dict["status"] == 429:
                test_results.append({
                    "name": "Baidu Search No CAPTCHA",
                    "status": "N",
                    "region": "",
                    "note": "IP Banned"
                })
            elif err_dict["status"] > 0 and err_dict["status"] != 200:
                test_results.append({
                    "name": "Baidu Search No CAPTCHA",
                    "status": "N",
                    "region": "",
                    "note": "Status: " + str(crawl_res.status)
                })
            else:
                test_results.append({
                    "name": "Baidu Search No CAPTCHA",
                    "status": "E",
                    "region": "",
                    "note": err_dict["detail"]
                })
    plf_print()

    # JD (Jingdong)
    try:
        crawl_req = urllib.request.Request("https://www.jd.com")
        crawl_req.add_header("User-Agent", crawl_ua_browser)
        crawl_res = urllib.request.urlopen(crawl_req, timeout=crawl_timeout)
        test_results.append({
            "name": "JD (Jingdong)",
            "status": "Y",
            "region": "",
            "note": ""
        })
    except Exception as e:
        err_dict = handle_connerr(e)
        if err_dict["status"] == 403 or err_dict["status"] == 429:
            test_results.append({
                "name": "JD (Jingdong)",
                "status": "N",
                "region": "",
                "note": "IP Banned"
            })
        elif err_dict["status"] > 0 and err_dict["status"] != 200:
            test_results.append({
                "name": "JD (Jingdong)",
                "status": "N",
                "region": "",
                "note": "Status: " + str(crawl_res.status)
            })
        else:
            test_results.append({
                "name": "JD (Jingdong)",
                "status": "E",
                "region": "",
                "note": err_dict["detail"]
            })
    plf_print()

    # Taobao
    try:
        crawl_req = urllib.request.Request("https://www.taobao.com")
        crawl_req.add_header("User-Agent", crawl_ua_browser)
        crawl_res = urllib.request.urlopen(crawl_req, timeout=crawl_timeout)
        test_results.append({
            "name": "Taobao",
            "status": "Y",
            "region": "",
            "note": ""
        })
    except Exception as e:
        err_dict = handle_connerr(e)
        if err_dict["status"] == 403 or err_dict["status"] == 429:
            test_results.append({
                "name": "Taobao",
                "status": "N",
                "region": "",
                "note": "IP Banned"
            })
        elif err_dict["status"] > 0 and err_dict["status"] != 200:
            test_results.append({
                "name": "Taobao",
                "status": "N",
                "region": "",
                "note": "Status: " + str(crawl_res.status)
            })
        else:
            test_results.append({
                "name": "Taobao",
                "status": "E",
                "region": "",
                "note": err_dict["detail"]
            })
    plf_print()

    # NetEase (163) News
    try:
        crawl_req = urllib.request.Request("https://www.163.com")
        crawl_req.add_header("User-Agent", crawl_ua_browser)
        crawl_res = urllib.request.urlopen(crawl_req, timeout=crawl_timeout)
        test_results.append({
            "name": "NetEase (163) News",
            "status": "Y",
            "region": "",
            "note": ""
        })
    except Exception as e:
        err_dict = handle_connerr(e)
        if err_dict["status"] == 403 or err_dict["status"] == 429:
            test_results.append({
                "name": "NetEase (163) News",
                "status": "N",
                "region": "",
                "note": "IP Banned"
            })
        elif err_dict["status"] > 0 and err_dict["status"] != 200:
            test_results.append({
                "name": "NetEase (163) News",
                "status": "N",
                "region": "",
                "note": "Status: " + str(crawl_res.status)
            })
        else:
            test_results.append({
                "name": "NetEase (163) News",
                "status": "E",
                "region": "",
                "note": err_dict["detail"]
            })
    plf_print()

    # NetEase (163) Music
    try:
        crawl_req = urllib.request.Request("https://music.163.com")
        crawl_req.add_header("User-Agent", crawl_ua_browser)
        crawl_res = urllib.request.urlopen(crawl_req, timeout=crawl_timeout)
        test_results.append({
            "name": "NetEase (163) Music",
            "status": "Y",
            "region": "",
            "note": ""
        })
    except Exception as e:
        err_dict = handle_connerr(e)
        if err_dict["status"] == 403 or err_dict["status"] == 429:
            test_results.append({
                "name": "NetEase (163) Music",
                "status": "N",
                "region": "",
                "note": "IP Banned"
            })
        elif err_dict["status"] > 0 and err_dict["status"] != 200:
            test_results.append({
                "name": "NetEase (163) Music",
                "status": "N",
                "region": "",
                "note": "Status: " + str(crawl_res.status)
            })
        else:
            test_results.append({
                "name": "NetEase (163) Music",
                "status": "E",
                "region": "",
                "note": err_dict["detail"]
            })
    plf_print()

    # Kugou Music
    try:
        crawl_req = urllib.request.Request("https://www.kugou.com")
        crawl_req.add_header("User-Agent", crawl_ua_browser)
        crawl_res = urllib.request.urlopen(crawl_req, timeout=crawl_timeout)
        test_results.append({
            "name": "Kugou Music",
            "status": "Y",
            "region": "",
            "note": ""
        })
    except Exception as e:
        err_dict = handle_connerr(e)
        if err_dict["status"] == 403 or err_dict["status"] == 429:
            test_results.append({
                "name": "Kugou Music",
                "status": "N",
                "region": "",
                "note": "IP Banned"
            })
        elif err_dict["status"] > 0 and err_dict["status"] != 200:
            test_results.append({
                "name": "Kugou Music",
                "status": "N",
                "region": "",
                "note": "Status: " + str(crawl_res.status)
            })
        else:
            test_results.append({
                "name": "Kugou Music",
                "status": "E",
                "region": "",
                "note": err_dict["detail"]
            })
    plf_print()

    # Weibo
    try:
        crawl_req = urllib.request.Request("https://www.weibo.com")
        crawl_req.add_header("User-Agent", crawl_ua_browser)
        crawl_res = urllib.request.urlopen(crawl_req, timeout=crawl_timeout)
        test_results.append({
            "name": "Weibo",
            "status": "Y",
            "region": "",
            "note": ""
        })
    except Exception as e:
        err_dict = handle_connerr(e)
        if err_dict["status"] == 403 or err_dict["status"] == 429:
            test_results.append({
                "name": "Weibo",
                "status": "N",
                "region": "",
                "note": "IP Banned"
            })
        elif err_dict["status"] > 0 and err_dict["status"] != 200:
            test_results.append({
                "name": "Weibo",
                "status": "N",
                "region": "",
                "note": "Status: " + str(crawl_res.status)
            })
        else:
            test_results.append({
                "name": "Weibo",
                "status": "E",
                "region": "",
                "note": err_dict["detail"]
            })
    plf_print()

    # rednote (Xiaohongshu)
    try:
        crawl_req = urllib.request.Request("https://www.xiaohongshu.com")
        crawl_req.add_header("User-Agent", crawl_ua_browser)
        crawl_res = urllib.request.urlopen(crawl_req, timeout=crawl_timeout)
        test_results.append({
            "name": "rednote (Xiaohongshu)",
            "status": "Y",
            "region": "",
            "note": ""
        })
    except Exception as e:
        err_dict = handle_connerr(e)
        if err_dict["status"] == 403 or err_dict["status"] == 429:
            test_results.append({
                "name": "rednote (Xiaohongshu)",
                "status": "N",
                "region": "",
                "note": "IP Banned"
            })
        elif err_dict["status"] > 0 and err_dict["status"] != 200:
            test_results.append({
                "name": "rednote (Xiaohongshu)",
                "status": "N",
                "region": "",
                "note": "Status: " + str(crawl_res.status)
            })
        else:
            test_results.append({
                "name": "rednote (Xiaohongshu)",
                "status": "E",
                "region": "",
                "note": err_dict["detail"]
            })
    plf_print()

    # bilibili (Mainland)
    try:
        crawl_req = urllib.request.Request("https://www.bilibili.com")
        crawl_req.add_header("User-Agent", crawl_ua_browser)
        crawl_res = urllib.request.urlopen(crawl_req, timeout=crawl_timeout)
        test_results.append({
            "name": "bilibili (Mainland)",
            "status": "Y",
            "region": "",
            "note": ""
        })
    except Exception as e:
        err_dict = handle_connerr(e)
        if err_dict["status"] == 403 or err_dict["status"] == 429:
            test_results.append({
                "name": "bilibili (Mainland)",
                "status": "N",
                "region": "",
                "note": "IP Banned"
            })
        elif err_dict["status"] > 0 and err_dict["status"] != 200:
            test_results.append({
                "name": "bilibili (Mainland)",
                "status": "N",
                "region": "",
                "note": "Status: " + str(crawl_res.status)
            })
        else:
            test_results.append({
                "name": "bilibili (Mainland)",
                "status": "E",
                "region": "",
                "note": err_dict["detail"]
            })
    plf_print()

    # Dazhong Dianping
    try:
        crawl_req = urllib.request.Request("https://www.dianping.com")
        crawl_req.add_header("User-Agent", crawl_ua_browser)
        crawl_res = urllib.request.urlopen(crawl_req, timeout=crawl_timeout)
        test_results.append({
            "name": "Dazhong Dianping",
            "status": "Y",
            "region": "",
            "note": ""
        })
    except Exception as e:
        err_dict = handle_connerr(e)
        if err_dict["status"] == 403 or err_dict["status"] == 429:
            test_results.append({
                "name": "Dazhong Dianping",
                "status": "N",
                "region": "",
                "note": "IP Banned"
            })
        elif err_dict["status"] > 0 and err_dict["status"] != 200:
            test_results.append({
                "name": "Dazhong Dianping",
                "status": "N",
                "region": "",
                "note": "Status: " + str(crawl_res.status)
            })
        else:
            test_results.append({
                "name": "Dazhong Dianping",
                "status": "E",
                "region": "",
                "note": err_dict["detail"]
            })
    plf_print()

    # Ctrip (Xiecheng)
    try:
        crawl_req = urllib.request.Request("https://ctrip.com")
        crawl_req.add_header("User-Agent", crawl_ua_browser)
        crawl_res = urllib.request.urlopen(crawl_req, timeout=crawl_timeout)
        test_results.append({
            "name": "Ctrip (Xiecheng)",
            "status": "Y",
            "region": "",
            "note": ""
        })
    except Exception as e:
        err_dict = handle_connerr(e)
        if err_dict["status"] == 403 or err_dict["status"] == 429:
            test_results.append({
                "name": "Ctrip (Xiecheng)",
                "status": "N",
                "region": "",
                "note": "IP Banned"
            })
        elif err_dict["status"] > 0 and err_dict["status"] != 200:
            test_results.append({
                "name": "Ctrip (Xiecheng)",
                "status": "N",
                "region": "",
                "note": "Status: " + str(crawl_res.status)
            })
        else:
            test_results.append({
                "name": "Ctrip (Xiecheng)",
                "status": "E",
                "region": "",
                "note": err_dict["detail"]
            })
    plf_print()

    # Douban
    try:
        crawl_req = urllib.request.Request("https://www.douban.com")
        crawl_req.add_header("User-Agent", crawl_ua_browser)
        crawl_res = urllib.request.urlopen(crawl_req, timeout=crawl_timeout)
        test_results.append({
            "name": "Douban",
            "status": "Y",
            "region": "",
            "note": ""
        })
    except Exception as e:
        err_dict = handle_connerr(e)
        if err_dict["status"] == 403 or err_dict["status"] == 429:
            test_results.append({
                "name": "Douban",
                "status": "N",
                "region": "",
                "note": "IP Banned"
            })
        elif err_dict["status"] > 0 and err_dict["status"] != 200:
            test_results.append({
                "name": "Douban",
                "status": "N",
                "region": "",
                "note": "Status: " + str(crawl_res.status)
            })
        else:
            test_results.append({
                "name": "Douban",
                "status": "E",
                "region": "",
                "note": err_dict["detail"]
            })
    plf_print()

    # Zhihu
    try:
        crawl_req = urllib.request.Request("https://www.zhihu.com")
        crawl_req.add_header("User-Agent", crawl_ua_browser)
        crawl_res = urllib.request.urlopen(crawl_req, timeout=crawl_timeout)
        test_results.append({
            "name": "Zhihu",
            "status": "Y",
            "region": "",
            "note": ""
        })
    except Exception as e:
        err_dict = handle_connerr(e)
        if err_dict["status"] == 403 or err_dict["status"] == 429:
            test_results.append({
                "name": "Zhihu",
                "status": "N",
                "region": "",
                "note": "IP Banned"
            })
        elif err_dict["status"] > 0 and err_dict["status"] != 200:
            test_results.append({
                "name": "Zhihu",
                "status": "N",
                "region": "",
                "note": "Status: " + str(crawl_res.status)
            })
        else:
            test_results.append({
                "name": "Zhihu",
                "status": "E",
                "region": "",
                "note": err_dict["detail"]
            })
    plf_print()

    # 12306 Railway
    try:
        crawl_req = urllib.request.Request("https://www.12306.cn")
        crawl_req.add_header("User-Agent", crawl_ua_browser)
        crawl_res = urllib.request.urlopen(crawl_req, timeout=crawl_timeout)
        test_results.append({
            "name": "12306 Railway",
            "status": "Y",
            "region": "",
            "note": ""
        })
    except Exception as e:
        err_dict = handle_connerr(e)
        if err_dict["status"] == 403 or err_dict["status"] == 429:
            test_results.append({
                "name": "12306 Railway",
                "status": "N",
                "region": "",
                "note": "IP Banned"
            })
        elif err_dict["status"] > 0 and err_dict["status"] != 200:
            test_results.append({
                "name": "12306 Railway",
                "status": "N",
                "region": "",
                "note": "Status: " + str(crawl_res.status)
            })
        else:
            test_results.append({
                "name": "12306 Railway",
                "status": "E",
                "region": "",
                "note": err_dict["detail"]
            })
    plf_print()

    print("")

# Ken's Study Journey
print(pcolour.bold + pcolour.blue + "Ken's Study Journey" + pcolour.end + pcolour.end)

# Ken's Study Journey
try:
    crawl_req = urllib.request.Request("https://www.kenstudyjourney.cn/en/")
    crawl_req.add_header("User-Agent", crawl_ua_browser)
    crawl_res = urllib.request.urlopen(crawl_req, timeout=crawl_timeout)
    crawl_headers_onel = " ".join([l.strip() for l in str(crawl_res.headers).splitlines()])
    ksj_region = re.sub(r".*(Ken\-)?Server\-Node\:\s*([A-Za-z]{3}\-)?([A-Za-z]{2}\-[A-Za-z]{3}).*", r"\3", crawl_headers_onel).upper()
    test_results.append({
        "name": "Ken's Study Journey",
        "status": "Y",
        "region": "",
        "note": "Node: " + ksj_region
    })
except Exception as e:
    err_dict = handle_connerr(e)
    if err_dict["status"] == 403 or err_dict["status"] == 429:
        test_results.append({
            "name": "Ken's Study Journey",
            "status": "N",
            "region": "",
            "note": "IP Banned"
        })
    elif err_dict["status"] > 0 and err_dict["status"] != 200:
        test_results.append({
            "name": "Ken's Study Journey",
            "status": "N",
            "region": "",
            "note": "Status: " + str(crawl_res.status)
        })
    else:
        test_results.append({
            "name": "Ken's Study Journey",
            "status": "E",
            "region": "",
            "note": err_dict["detail"]
        })
plf_print()

# Ken's Study Planner
try:
    crawl_req = urllib.request.Request("https://planner.kenstudyjourney.cn/en/")
    crawl_req.add_header("User-Agent", crawl_ua_browser)
    crawl_res = urllib.request.urlopen(crawl_req, timeout=crawl_timeout)
    crawl_headers_onel = " ".join([l.strip() for l in str(crawl_res.headers).splitlines()])
    ksj_region = re.sub(r".*(Ken\-)?Server\-Node\:\s*([A-Za-z]{3}\-)?([A-Za-z]{2}\-[A-Za-z]{3}).*", r"\3", crawl_headers_onel).upper()
    test_results.append({
        "name": "Ken's Study Planner",
        "status": "Y",
        "region": "",
        "note": "Node: " + ksj_region
    })
except Exception as e:
    err_dict = handle_connerr(e)
    if err_dict["status"] == 403 or err_dict["status"] == 429:
        test_results.append({
            "name": "Ken's Study Planner",
            "status": "N",
            "region": "",
            "note": "IP Banned"
        })
    elif err_dict["status"] > 0 and err_dict["status"] != 200:
        test_results.append({
            "name": "Ken's Study Planner",
            "status": "N",
            "region": "",
            "note": "Status: " + str(crawl_res.status)
        })
    else:
        test_results.append({
            "name": "Ken's Study Planner",
            "status": "E",
            "region": "",
            "note": err_dict["detail"]
        })
plf_print()

# Ken Deng (Personal Site)
try:
    crawl_req = urllib.request.Request("https://ken.kenstudyjourney.cn/en/")
    crawl_req.add_header("User-Agent", crawl_ua_browser)
    crawl_res = urllib.request.urlopen(crawl_req, timeout=crawl_timeout)
    crawl_headers_onel = " ".join([l.strip() for l in str(crawl_res.headers).splitlines()])
    ksj_region = re.sub(r".*(Ken\-)?Server\-Node\:\s*([A-Za-z]{3}\-)?([A-Za-z]{2}\-[A-Za-z]{3}).*", r"\3", crawl_headers_onel).upper()
    test_results.append({
        "name": "Ken Deng (Personal Site)",
        "status": "Y",
        "region": "",
        "note": "Node: " + ksj_region
    })
except Exception as e:
    err_dict = handle_connerr(e)
    if err_dict["status"] == 403 or err_dict["status"] == 429:
        test_results.append({
            "name": "Ken Deng (Personal Site)",
            "status": "N",
            "region": "",
            "note": "IP Banned"
        })
    elif err_dict["status"] > 0 and err_dict["status"] != 200:
        test_results.append({
            "name": "Ken Deng (Personal Site)",
            "status": "N",
            "region": "",
            "note": "Status: " + str(crawl_res.status)
        })
    else:
        test_results.append({
            "name": "Ken Deng (Personal Site)",
            "status": "E",
            "region": "",
            "note": err_dict["detail"]
        })
plf_print()

print("")
