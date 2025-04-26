import re
import json
import socket
# import ssl
import urllib.request

# config
crawl_timeout = 10
crawl_ua_curl = "curl/8.7.1"
crawl_ua_browser = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Trailer/93.3.8652.5"

# IP Quality Check (Python Version)

# Anti-scraping Techniques Deployed on:
# - Ping0 (ping0.cc)
# - AbuseIPDB (www.abuseipdb.com)
# You need to **manually** visit them in your web browser.

# constants
ipt_err_dict = {
    "success": False,
    "ip_type": "Error",
    "company_type": "Error",
    "is_server": "", # Y/N
    "is_proxy": "", # Y/N
    "is_relay": "", # Y/N
    "is_vpn": "", # Y/N
    "is_tor": "", # Y/N
    "is_abuser": "" # Y/N
}
ipq_err_dict = {
    "success": False,
    "risk_score": -1.0 # -1.0 = ERROR
}

# variables
your_ip = ""
ip_as = ""
ip_isp = ""
ip_region = ""
ip_regregions = []
ip_regregions_str = ""
ipt_res = {
    "ipinfo": ipt_err_dict,
    "ipdata": ipt_err_dict,
    "ip2location": ipt_err_dict,
    "ipregistry": ipt_err_dict,
    "ipapi": ipt_err_dict,
}
ipr_res = {
    "scamalytics": ipq_err_dict,
    "ipapi": ipq_err_dict,
    "cloudflare": ipq_err_dict,
    "dbip": ipq_err_dict,
    "ipdata": ipq_err_dict,
}

# functions
# print colours
class pcolour:
    end = "\033[0m"
    bold = "\033[1m"
    red = "\033[31m"
    green = "\033[32m"
    yellow = "\033[33m"
    blue = "\033[34m"

# IP type colours
def iptcolour(iptype):
    iptype = iptype.lower()
    if iptype == "isp" or iptype == "mobile" or iptype == "isp/mobile":
        return pcolour.green
    elif iptype == "hosting" or iptype == "error":
        return pcolour.red
    return pcolour.blue
def ippcolour(ipprivacy):
    ipprivacy = ipprivacy.upper()
    if ipprivacy == "Y":
        return pcolour.red
    elif ipprivacy == "N":
        return pcolour.green
    return pcolour.blue
def iprcolour(iprisk):
    if 0 <= iprisk < 50:
        return pcolour.green
    elif 50 <= iprisk < 80:
        return pcolour.yellow
    return pcolour.red
def bool_str(boolval):
    if boolval or boolval == "true":
        return "Y"
    return "N"
def boolstr_bool(boolstr):
    boolstr = boolstr.strip().lower()
    if boolstr == "true":
        return True
    return False
def iptype_cap(typestr):
    typestr = typestr.strip().lower()
    if typestr == "isp/mob" or  typestr == "isp/mobile":
        return "ISP/Mobile"
    if typestr == "isp":
        return typestr.upper()
    return typestr.capitalize()
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
def ipt_print(disp_name, dict_k):
    ipt_res_this = ipt_res[dict_k]
    strdisp = ""
    strdisp += str_space_l(disp_name, 11)
    strdisp += " | "
    strdisp += iptcolour(ipt_res_this["ip_type"]) + str_space_l(ipt_res_this["ip_type"], 10) + pcolour.end
    strdisp += " | "
    strdisp += iptcolour(ipt_res_this["company_type"]) + str_space_l(ipt_res_this["company_type"], 10) + pcolour.end
    print(strdisp)
def ipp_print(disp_name, dict_k):
    ipt_res_this = ipt_res[dict_k]
    strdisp = ""
    strdisp += str_space_l(disp_name, 11)
    strdisp += " |  "
    strdisp += ippcolour(ipt_res_this["is_server"]) + str_space_l(ipt_res_this["is_server"], 1) + pcolour.end
    strdisp += "   "
    strdisp += ippcolour(ipt_res_this["is_vpn"]) + str_space_l(ipt_res_this["is_vpn"], 1) + pcolour.end
    strdisp += "   "
    strdisp += ippcolour(ipt_res_this["is_proxy"]) + str_space_l(ipt_res_this["is_proxy"], 1) + pcolour.end
    strdisp += "   "
    strdisp += ippcolour(ipt_res_this["is_relay"]) + str_space_l(ipt_res_this["is_relay"], 1) + pcolour.end
    strdisp += "   "
    strdisp += ippcolour(ipt_res_this["is_tor"]) + str_space_l(ipt_res_this["is_tor"], 1) + pcolour.end
    strdisp += "   "
    strdisp += ippcolour(ipt_res_this["is_abuser"]) + str_space_l(ipt_res_this["is_abuser"], 1) + pcolour.end
    print(strdisp)
def ipr_print(disp_name, dict_k, dispts = False):
    ipr_res_this = ipr_res[dict_k]
    ipr_risk_score = ipr_res_this["risk_score"]
    ipr_error = ipr_risk_score == -1.0
    strdisp = ""
    strdisp += str_space_l(disp_name, 11)
    strdisp += " | "
    if not ipr_error:
        strdisp += iprcolour(ipr_risk_score) + str(ipr_risk_score) + pcolour.end
        if dispts: # Display Trust Score (100 - risk)
            strdisp += " "
            strdisp += "(Trust: " + iprcolour(ipr_risk_score) + str(100.0 - ipr_risk_score) + pcolour.end + ")"
    else:
        strdisp += iprcolour(ipr_risk_score) + "Error" + pcolour.end
    print(strdisp)

origGetAddrInfo = socket.getaddrinfo
def getAddrInfoWrapper4(host, port, family=0, socktype=0, proto=0, flags=0):
    return origGetAddrInfo(host, port, socket.AF_INET, socktype, proto, flags)
def getAddrInfoWrapper6(host, port, family=0, socktype=0, proto=0, flags=0):
    return origGetAddrInfo(host, port, socket.AF_INET, socktype, proto, flags)

# force IPv4
socket.getaddrinfo = getAddrInfoWrapper4

# Welcome Msg
print(pcolour.bold + "IP Quality Test" + pcolour.end)
print("By: Ken (Ken's Study Journey)")
print("https://ken.kenstudyjourney.cn")
print("=======================================")
print("")

# get ip
try:
    crawl_req = urllib.request.Request("http://ip.sb")
    crawl_req.add_header("User-Agent", crawl_ua_curl)
    crawl_res = urllib.request.urlopen(crawl_req, timeout=crawl_timeout)
    your_ip = crawl_res.read().decode().strip()
    print(pcolour.bold + pcolour.blue + "Your IP Address" + pcolour.end + pcolour.end)
    print(your_ip)
    print("")
except Exception as e:
    print(pcolour.red + "Network Error" + pcolour.end)
    print(pcolour.bold + pcolour.blue + "Your IP Address" + pcolour.end + pcolour.end)
    print("Cannot Get your IP Address")
    print(e)
    print("")
    print("Cannot Continue - Cannot Get your IP Address")
    print("Please Check with `curl ip.sb` and Try Again")
    exit()

# ipinfo.io (general)
try:
    crawl_req = urllib.request.Request("https://ipinfo.io/widget/demo/" + your_ip)
    crawl_req.add_header("User-Agent", crawl_ua_browser)
    crawl_res = urllib.request.urlopen(crawl_req, timeout=crawl_timeout)
    res_dict = json.loads(crawl_res.read())
    ip_as = res_dict["data"]["asn"]["asn"]
    ip_isp = res_dict["data"]["asn"]["name"]
    ip_region = res_dict["data"]["country"]
    ipinfo_comtype = ""
    if "company" in res_dict["data"].keys():
        ipinfo_comtype = iptype_cap(res_dict["data"]["company"]["type"])
    ipt_res["ipinfo"] = {
        "success": True,
        "ip_type": iptype_cap(res_dict["data"]["asn"]["type"]),
        "company_type": ipinfo_comtype,
        "is_server": bool_str(res_dict["data"]["privacy"]["hosting"]),
        "is_proxy": bool_str(res_dict["data"]["privacy"]["proxy"]),
        "is_relay": bool_str(res_dict["data"]["privacy"]["relay"]),
        "is_vpn": bool_str(res_dict["data"]["privacy"]["vpn"]),
        "is_tor": bool_str(res_dict["data"]["privacy"]["tor"]),
        "is_abuser": "",
    }
except Exception as e:
    print(pcolour.red + "Network Error" + pcolour.end)
    print("Cannot Get IPinfo Database")
    print(e)
    print("")
    pass

# ipinfo.io (whois)
try:
    crawl_req = urllib.request.Request("https://ipinfo.io/widget/demo/" + your_ip + "?dataset=whois")
    crawl_req.add_header("User-Agent", crawl_ua_browser)
    crawl_res = urllib.request.urlopen(crawl_req, timeout=crawl_timeout)
    res_dict = json.loads(crawl_res.read())
    ip_regregions_recarr = res_dict["records"]
    ip_regregions_arr = list(set(map(lambda r: r["country"], ip_regregions_recarr)))
    ip_regregions_arr.sort()
    ip_regregions_str = ", ".join(ip_regregions_arr)
except Exception as e:
    print(pcolour.red + "Network Error" + pcolour.end)
    print("Cannot Get IPinfo WHOIS Database")
    print(e)
    print("")

# ip type check

# IPData
try:
    # IPData Demo API strictly checks Origin request header
    # API Key is fixed, for demo only
    crawl_req = urllib.request.Request("https://api.ipdata.co/" + your_ip + "?api-key=eca677b284b3bac29eb72f5e496aa9047f26543605efe99ff2ce35c9")
    crawl_req.add_header("User-Agent", crawl_ua_browser)
    crawl_req.add_header("Origin", "https://ipdata.co")
    crawl_req.add_header("Referer", "https://ipdata.co")
    crawl_res = urllib.request.urlopen(crawl_req, timeout=crawl_timeout)
    res_dict = json.loads(crawl_res.read())
    ip_type = ""
    if "asn" in res_dict.keys():
        ip_type = res_dict["asn"]["type"]
    ipt_res["ipdata"] = {
        "success": True,
        "ip_type": iptype_cap(ip_type),
        "company_type": iptype_cap(res_dict["company"]["type"]),
        "is_server": bool_str(res_dict["threat"]["is_datacenter"]),
        "is_proxy": bool_str(res_dict["threat"]["is_proxy"]),
        "is_relay": bool_str(res_dict["threat"]["is_icloud_relay"]),
        "is_vpn": bool_str(res_dict["threat"]["is_vpn"]),
        "is_tor": bool_str(res_dict["threat"]["is_tor"]),
        "is_abuser": bool_str(res_dict["threat"]["is_known_attacker"] or res_dict["threat"]["is_known_abuser"] or res_dict["threat"]["is_threat"])
    }
    ipr_res["ipdata"] = {
        "success": True,
        "risk_score": float(100 - res_dict["threat"]["scores"]["trust_score"])
    }
except Exception as e:
    print(pcolour.red + "Network Error" + pcolour.end)
    print("Cannot Get IPData Database")
    print(e)
    print("")

# IP2Location
try:
    crawl_req = urllib.request.Request("https://www.ip2location.io/" + your_ip)
    crawl_req.add_header("User-Agent", crawl_ua_browser)
    crawl_res = urllib.request.urlopen(crawl_req, timeout=crawl_timeout)
    res_html = "".join([l.strip() for l in crawl_res.read().decode().splitlines()])
    is_server = boolstr_bool(re.sub(r".*\"is_data_center\"\:\s?(true|false).*", r"\1", res_html))
    # Proxy = Public Proxy || Web Proxy || Residential Proxy
    is_proxy = boolstr_bool(re.sub(r".*\"is_public_proxy\"\:\s?(true|false).*", r"\1", res_html)) or boolstr_bool(re.sub(r".*\"is_web_proxy\"\:\s?(true|false).*", r"\1", res_html)) or boolstr_bool(re.sub(r".*\"is_residential_proxy\"\:\s?(true|false).*", r"\1", res_html))
    is_vpn = boolstr_bool(re.sub(r".*\"is_vpn\"\:\s?(true|false).*", r"\1", res_html))
    is_tor = boolstr_bool(re.sub(r".*\"is_tor\"\:\s?(true|false).*", r"\1", res_html))
    # Abuser = Spammer || Scanner || Botnet
    is_abuser = boolstr_bool(re.sub(r".*\"is_spammer\"\:\s?(true|false).*", r"\1", res_html)) or boolstr_bool(re.sub(r".*\"is_scanner\"\:\s?(true|false).*", r"\1", res_html)) or boolstr_bool(re.sub(r".*\"is_botnet\"\:\s?(true|false).*", r"\1", res_html))
    # IP Type (conversion for "ISP" omitted)
    ip2l_iptype = re.sub(r"\\\/", "/", re.sub(r".*\"usage_type\"\:\s?\"([A-Za-z0-9\\\/]*)\".*", r"\1", res_html)).strip().upper()
    if ip2l_iptype in ["COM", "GOV", "ORG", "MIL", "LIB"]:
        ip2l_iptype = "Business"
    elif ip2l_iptype in ["DCH", "CDN", "SES"]:
        ip2l_iptype = "Hosting"
    elif ip2l_iptype == "EDU":
        ip2l_iptype = "Education"
    elif ip2l_iptype == "MOB":
        ip2l_iptype = "Mobile"
    elif ip2l_iptype == "RSV":
        ip2l_iptype = "Reserved"
    ipt_res["ip2location"] = {
        "success": True,
        "ip_type": iptype_cap(ip2l_iptype),
        "company_type": "",
        "is_server": bool_str(is_server),
        "is_proxy": bool_str(is_proxy),
        "is_relay": "",
        "is_vpn": bool_str(is_vpn),
        "is_tor": bool_str(is_tor),
        "is_abuser": bool_str(is_abuser)
    }
except Exception as e:
    print(pcolour.red + "Network Error" + pcolour.end)
    print("Cannot Get IP2Location Database")
    print(e)
    print("")

# IPRegistry
try:
    # IPRegistry Demo API strictly checks Origin request header
    # API Key is fixed, for demo only
    crawl_req = urllib.request.Request("https://api.ipregistry.co/" + your_ip + "?hostname=true&key=sb69ksjcajfs4c")
    crawl_req.add_header("User-Agent", crawl_ua_browser)
    crawl_req.add_header("Origin", "https://ipregistry.co")
    crawl_req.add_header("Referer", "https://ipregistry.co")
    crawl_res = urllib.request.urlopen(crawl_req, timeout=crawl_timeout)
    res_dict = json.loads(crawl_res.read())
    ipt_res["ipregistry"] = {
        "success": True,
        "ip_type": iptype_cap(res_dict["connection"]["type"]),
        "company_type": iptype_cap(res_dict["company"]["type"]),
        "is_server": bool_str(res_dict["security"]["is_cloud_provider"]),
        "is_proxy": bool_str(res_dict["security"]["is_proxy"]),
        "is_relay": bool_str(res_dict["security"]["is_relay"]),
        "is_vpn": bool_str(res_dict["security"]["is_vpn"]),
        "is_tor": bool_str(res_dict["security"]["is_tor"] or res_dict["security"]["is_tor_exit"]),
        "is_abuser": bool_str(res_dict["security"]["is_abuser"] or res_dict["security"]["is_attacker"] or res_dict["security"]["is_threat"])
    }
except Exception as e:
    print(pcolour.red + "Network Error" + pcolour.end)
    print("Cannot Get IPRegistry Database")
    print(e)
    print("")

# IPAPI
try:
    crawl_req = urllib.request.Request("https://api.ipapi.is/?q=" + your_ip)
    crawl_req.add_header("User-Agent", crawl_ua_browser)
    crawl_res = urllib.request.urlopen(crawl_req, timeout=crawl_timeout)
    res_dict = json.loads(crawl_res.read())
    ipt_res["ipapi"] = {
        "success": True,
        "ip_type": iptype_cap(res_dict["asn"]["type"]),
        "company_type": iptype_cap(res_dict["company"]["type"]),
        "is_server": bool_str(res_dict["is_datacenter"]),
        "is_proxy": bool_str(res_dict["is_proxy"]),
        "is_relay": "",
        "is_vpn": bool_str(res_dict["is_vpn"]),
        "is_tor": bool_str(res_dict["is_tor"]),
        "is_abuser": bool_str(res_dict["is_abuser"])
    }
    ipr_res["ipapi"] = {
        "success": True,
        "risk_score": float(re.sub(r"([0-9\.]*)\s*\([A-Za-z\s]*\)", r"\1", res_dict["company"]["abuser_score"]))
    }
except Exception as e:
    print(pcolour.red + "Network Error" + pcolour.end)
    print("Cannot Get IPAPI Database")
    print(e)
    print("")

# Scamalytics
try:
    crawl_req = urllib.request.Request("https://www.scamalytics.com/ip/" + your_ip)
    crawl_req.add_header("User-Agent", crawl_ua_browser)
    crawl_req.add_header("Origin", "https://scamalytics.com")
    crawl_req.add_header("Referer", "https://scamalytics.com")
    crawl_res = urllib.request.urlopen(crawl_req, timeout=crawl_timeout)
    res_html = "".join([l.strip() for l in crawl_res.read().decode().splitlines()])
    risk_score = float(re.sub(r".*Fraud\s*Score\:\s*([0-9]*).*", r"\1", res_html))
    ipr_res["scamalytics"] = {
        "success": True,
        "risk_score": risk_score
    }
except Exception as e:
    print(pcolour.red + "Network Error" + pcolour.end)
    print("Cannot Get Scamalytics Database")
    print(e)
    print("")

# CloudFlare (via Nodeget)
try:
    crawl_req = urllib.request.Request("https://ip.nodeget.com/json")
    crawl_req.add_header("User-Agent", crawl_ua_curl)
    crawl_res = urllib.request.urlopen(crawl_req, timeout=crawl_timeout)
    res_dict = json.loads(crawl_res.read())
    risk_score = float(res_dict["ip"]["riskScore"])
    ipr_res["cloudflare"] = {
        "success": True,
        "risk_score": risk_score
    }
except Exception as e:
    print(pcolour.red + "Network Error" + pcolour.end)
    print("Cannot Get CloudFlare Database")
    print(e)
    print("")

# DBIP
try:
    crawl_req = urllib.request.Request("https://db-ip.com/demo/home.php?s=" + your_ip)
    crawl_req.add_header("User-Agent", crawl_ua_browser)
    crawl_res = urllib.request.urlopen(crawl_req, timeout=crawl_timeout)
    res_dict = json.loads(crawl_res.read())
    # if `status` != "ok", rate limit reached
    if res_dict["status"] == "ok":
        risk_score_l = res_dict["demoInfo"]["threatLevel"]
        risk_score = 0.0
        if risk_score_l == "medium":
            risk_score = 50.0
        elif risk_score_l == "high":
            risk_score = 100.0
        ipr_res["dbip"] = {
            "success": True,
            "risk_score": risk_score
        }
    else:
        print(pcolour.red + "Network Error" + pcolour.end)
        print("Cannot Get DBIP Database")
        print("Status: " + str(res_dict["status"]))
        # print(str(crawl_res.read()))
        print("")
except Exception as e:
    print(pcolour.red + "Network Error" + pcolour.end)
    print("Cannot Get DBIP Database")
    print(e)
    print("")

print(pcolour.bold + pcolour.blue + "More IP Info" + pcolour.end + pcolour.end)
print(pcolour.blue + "AS Number:         " + pcolour.end + ip_as)
print(pcolour.blue + "ISP:               " + pcolour.end + ip_isp)
print(pcolour.blue + "IP Region:         " + pcolour.end + ip_region)
print(pcolour.blue + "Registered Region: " + pcolour.end + ip_regregions_str)
# if len(ip_regregions_arr) > 1 or ip_regregions_arr[0] != ip_region:
if ip_region not in ip_regregions_arr:
    print(pcolour.blue + "IP Region Type:    " + pcolour.red + "Broadcasted IP" + pcolour.end)
else:
    print(pcolour.blue + "IP Region Type:    " + pcolour.green + "Native IP" + pcolour.end)
print("")

print(pcolour.blue + pcolour.bold + "IP Usage Type" + pcolour.end + pcolour.end)
print("Provider    | IP         | Company")
ipt_print("IPinfo", "ipinfo")
ipt_print("IPData", "ipdata")
ipt_print("IPRegistry", "ipregistry")
ipt_print("IPAPI", "ipapi")
ipt_print("IP2Location", "ip2location")
print("")

print(pcolour.blue + pcolour.bold + "IP Privacy" + pcolour.end + pcolour.end)
print("Provider    | SRV VPN PXY RLY TOR ABU")
ipp_print("IPinfo", "ipinfo")
ipp_print("IPData", "ipdata")
ipp_print("IPRegistry", "ipregistry")
ipp_print("IPAPI", "ipapi")
ipp_print("IP2Location", "ip2location")
print("")

print(pcolour.blue + pcolour.bold + "IP Risk" + pcolour.end + pcolour.end)
print("Provider    | Risk")
ipr_print("Scamalytics", "scamalytics")
# ipr_print("IPQS", "ipqs")
ipr_print("CloudFlare", "cloudflare")
ipr_print("DBIP", "dbip")
ipr_print("IPData", "ipdata", True)
ipr_print("IPAPI", "ipapi")
print("")
