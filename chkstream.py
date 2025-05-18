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

# Bloomberg Anywhere
try:
    crawl_req = urllib.request.Request("https://bba.bloomberg.net/?utm_source=bloomberg-menu&utm_medium=terminal")
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
        "name": "Bloomberg Anywhere",
        "status": "Y",
        "region": "",
        "note": ""
    })
except Exception as e:
    err_dict = handle_connerr(e)
    if err_dict["status"] == 403 or err_dict["status"] == 429:
        test_results.append({
            "name": "Bloomberg Anywhere",
            "status": "N",
            "region": "",
            "note": "IP Banned"
        })
    elif err_dict["status"] > 0 and err_dict["status"] != 200:
        test_results.append({
            "name": "Bloomberg Anywhere",
            "status": "N",
            "region": "",
            "note": "Status: " + str(crawl_res.status)
        })
    else:
        test_results.append({
            "name": "Bloomberg Anywhere",
            "status": "E",
            "region": "",
            "note": err_dict["detail"]
        })
plf_print()

# ResearchGate
rsg_urls = [
    "https://www.researchgate.net/publication/343820813_A_Systematic_Review_of_Transition_from_IPV4_To_IPV6",
    "https://www.researchgate.net/publication/354992184_Research_on_the_Application_of_the_IPv6_Network_Protocol",
    "https://www.researchgate.net/publication/263856140_A_Comparative_Review_Of_Internet_Protocol_Version_4_IPv4_and_Internet_Protocol_Version_6_IPv6",
    "https://www.researchgate.net/publication/45816107_Social_and_Ethical_Aspects_of_IPv6",
    "https://www.researchgate.net/publication/319143290_How_HTTP2_pushes_the_web_An_empirical_study_of_HTTP2_server_push",
]
try:
    crawl_req = urllib.request.Request(random.choice(rsg_urls))
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
        "name": "ResearchGate",
        "status": "Y",
        "region": "",
        "note": ""
    })
except Exception as e:
    err_dict = handle_connerr(e)
    if err_dict["status"] == 403 or err_dict["status"] == 429:
        test_results.append({
            "name": "ResearchGate",
            "status": "N",
            "region": "",
            "note": "IP Banned"
        })
    elif err_dict["status"] > 0 and err_dict["status"] != 200:
        test_results.append({
            "name": "ResearchGate",
            "status": "N",
            "region": "",
            "note": "Status: " + str(crawl_res.status)
        })
    else:
        test_results.append({
            "name": "ResearchGate",
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
    # Get Media Token
    crawl_req_mc = urllib.request.Request("https://raw.githubusercontent.com/lmc999/RegionRestrictionCheck/main/cookies")
    crawl_req_mc.add_header("User-Agent", crawl_ua_browser)
    crawl_res_mc = urllib.request.urlopen(crawl_req_mc, timeout=crawl_timeout)
    # STEP 1
    media_cookie = crawl_res_mc.read().decode()
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

# V2EX (my addition)
# The website may return an "Access Denied" page
# with 403 HTTP Status Code on some nodes.
try:
    crawl_req = urllib.request.Request("https://www.v2ex.com")
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
    res_html = "".join([l.strip() for l in crawl_res.read().decode().splitlines()]).upper()
    test_results.append({
        "name": "V2EX",
        "status": "Y",
        "region": "",
        "note": ""
    })
except Exception as e:
    err_dict = handle_connerr(e)
    if err_dict["status"] == 403 or err_dict["status"] == 429:
        test_results.append({
            "name": "V2EX",
            "status": "N",
            "region": "",
            "note": "IP Banned"
        })
    elif err_dict["status"] > 0 and err_dict["status"] != 200:
        test_results.append({
            "name": "V2EX",
            "status": "N",
            "region": "",
            "note": "Status: " + str(crawl_res.status)
        })
    else:
        test_results.append({
            "name": "V2EX",
            "status": "E",
            "region": "",
            "note": err_dict["detail"]
        })
plf_print()

# Stack Overflow
try:
    crawl_req = urllib.request.Request("https://stackoverflow.com")
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
    res_html = "".join([l.strip() for l in crawl_res.read().decode().splitlines()]).upper()
    test_results.append({
        "name": "Stack Overflow",
        "status": "Y",
        "region": "",
        "note": ""
    })
except Exception as e:
    err_dict = handle_connerr(e)
    if err_dict["status"] == 403 or err_dict["status"] == 429:
        test_results.append({
            "name": "Stack Overflow",
            "status": "N",
            "region": "",
            "note": "IP Banned"
        })
    elif err_dict["status"] > 0 and err_dict["status"] != 200:
        test_results.append({
            "name": "Stack Overflow",
            "status": "N",
            "region": "",
            "note": "Status: " + str(crawl_res.status)
        })
    else:
        test_results.append({
            "name": "Stack Overflow",
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
    if mts_region == "HK":
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
