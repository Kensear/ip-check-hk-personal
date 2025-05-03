# IP Quality & Stream Restriction Checker (HK)

**IP Quality &amp; Streaming Service Regional Restriction Checker (Hong Kong Region Only)**

🌎 README Language/语言:<br>
[繁體中文](./README_zh_HK.md) [简体中文](./README_zh_CN.md)

⚠️ Disclaimer:
- For personal research🔬 only (apart from just a developer, I am also a researcher!).
- This project is affiliated with neither❌ any local ISP🔌 nor any website🌎 stated.
- This project is only for testing IP address and streaming services. It does not❌ provide other services including VPS servers.
- As a beginner to Cantonese, the Chinese-Traditional (繁體中文) version of README may be incorrect.

This project is for testing whether streaming services can be used (also known as "流媒体解锁测试") and the quality of the IP address under HK local networks and VPS servers.

As a Hong Kong university student🏫 (and semi-local), **only** the nodes in **Hong Kong region** are used and hence only the checkers of that region were developed (see FAQ below⬇️).

<img width="1098" alt="Screenshot 2025-05-02 at 11 52 13 PM" src="https://github.com/user-attachments/assets/34740da8-3a7d-4ad7-80cb-b4a95f2b3b28" /><br>

This was made originally due to an **argument** with the original author about Netflix module, but along with some new features (see below⬇️).

<img width="520" alt="Screenshot 2025-04-16 at 4 59 19 PM" src="https://github.com/user-attachments/assets/c26aaf26-9435-43b9-ac4d-2d7f4b49314c" /><br>

**My Personality:**<br>
If my suggestion/PR is rejected by a repo, fork (copy) it ASAP and modify it with my unique suggestions for **personal use**.<br>
Please see bottom⬇️ to learn more.

Inspired by and modified from:
- [https://doc.theojs.cn/vps/tools/streaming-unlocked](https://doc.theojs.cn/vps/tools/streaming-unlocked)
- [https://doc.theojs.cn/vps/tools/ipquality](https://doc.theojs.cn/vps/tools/ipquality)

## Running

Simply download and run the corresponding .py files in Python.

It's **not recommended** to run the same type of script (Check IP or Stream) many times under the **same IP address** in a day, or it may result in IP Ban.

Test IP Quality:
```
# Choose one based on your device/emulator.
python3 ./chkip.py
python ./chkip.py
```

Test Streaming/Local Websites:
```
# Choose one based on your device/emulator.
python3 ./chkstream.py
python ./chkstream.py
```

## New Features

This script adds the following features (improvements):

- Check if Sign-in Required for YouTube (i.e., "Sign in to confirm that you're not a bot")
- Check HK University Websites
- Check HK Bank Websites
- Check Mainland Websites (optional)

It's initially a Python version (with **urllib** module) so that it can be used on iOS (with iSH app), Windows, macOS, etc. apart from just Linux servers.

YouTube "Sign in to confirm that you're not a bot" Screen:

<img width="700" alt="Screenshot 2025-04-09 at 4 08 59 PM" src="https://github.com/user-attachments/assets/37708650-8917-4ed1-930b-6bc99c37843d" /><br>

## My Previous Research

Apart from a programmer🧑‍💻 and software developer🛠️, I am also a **researcher**🔬 diving into the technical working principles behind.

I did a lot of personal research and experiments🧪 about the Residential IPs and local ISPs around HK.

### Common HK ISPs

Whether from Residential IP providers or real local network (like WiFi in some places), I researched🔬 about some common ISPs and their AS (Autonomous System) numbers.

For example only. This is not an exhaustive list.<br>
H = Home; B = Business

|Name|Hostname Suffix<sup>1</sup>|AS Number|Type|
|----|--|--|----|
|HKT|netvigator.com|AS4760|H|
|HKT Enterprise|imsbiz.com|AS4515|B|
|HK Cable TV|hkcable.com.hk|AS9908|H|
|SmarTone||AS17924|H|
|CMHK|hk.chinamobile.com|AS9231<br>AS137872|H|
|HKBN|ctinets.com|AS10103|H|
|HKBN Enterprise <sup>2</sup>||AS9381|B|
|HGC||AS9304|H/B|
|Hutchison (3/Three)||AS10118|H|
|JUCC (University Only) <sup>3</sup><br>||AS3662|B|

Notes:
1. Results from `nslookup` command searching🔍 for Hostname of each IP address
2. Incorrectly❌ labelled as **"Hosting"** (and even **VPN**) Type on IPinfo even if only used in normal WiFi, but I **failed the appeal (rejected)** (I contacted it📩 before) due to its previous **mass port scanning**🔍 evidence (in its email reply). Stream service accessibility is **not affected**✅.
3. Including downstream AS numbers for each university.

From my personal research and experiment, the WiFi of some universities may use HGC or HKBN Enterprise broadbands instead of JUCC (its own AS number).

HGC (and sometimes HKT) are the commonly-used ISPs for HK Residential IP server providers.

### "Personality" of Residential IP Providers

Some Residential IP providers may have the following "personality":

- Ban **Bank** Websites/Apps (including HK and other Banks)
- Ban All **ICP-Registered** Websites/Apps (regardless of whether the servers are in Mainland or not)

<img width="400" alt="Screenshot 2025-04-26 at 8 23 12 AM" src="https://github.com/user-attachments/assets/2b711d91-c64a-4ae4-bc13-a4b7f5321e31" /><br>

### Issue: IP Labelled as Mainland by Google

Due to some users using Google with Location Services📍 (like GPS) enabled, some IP addresses were labelled as Mainland by Google even if it is not❌ the actual IP address location.

You will see that all Google and YouTube services will have the "CN" region displayed in the test scripts.

<img width="601" alt="Screenshot 2025-05-03 at 12 05 43 PM" src="https://github.com/user-attachments/assets/7e12b2f8-078d-47d6-b9b3-df9d4656bf48" /><br>

From my test and experiment results, **none**❌ of the HK local networks, including Mobile Data📲, University "eduroam" WiFi🏫 and Free WiFi🛜, appeared to have this result (probability: 0%).

To "pull" an IP address back to HK🔙, keep doing the following for 1 to 30 days⏳ (several times per day):
1. Connect🔌 to the corresponding node when **physically** in HK
2. Turn on (Allow) Location Services on your device/browser
3. Search🔍 anything on Google or use Google Maps🧭
4. After searching/opening, update/report your location📍 at the bottom

Based on my experiment, **two (2)** of the IP addresses previously labelled as Mainland by Google were **successfully** "pulled back"✅ to HK.

To learn more, please visit: [https://www.tjsky.net/tutorial/546](https://www.tjsky.net/tutorial/546) (just a reference, not my article)

### HK Local Broadband Test Result

When testing under HK local network (under the ISPs mentioned above⬆️), all testing were passed including the ISP incorrectly labelled as Hosting by IPinfo.

- For IP Quality Check:
  - IP Usage Type Table majorly have the 🟢**Green** "**ISP**" or 🔵**Blue** "**Business**" or "**Education**" displayed✅ *
  - IP Privacy Table majorly have the 🟢**Green** "**N**" displayed✅ *
  - IP Risk Table all have the 🟢**Green** low-risk values displayed✅
- For Stream Restriction Check:
  - All Tests have the 🟢**Green** "**Y**" displayed✅

\* Except the ISP incorrectly labelled as Hosting by IPinfo, where **only** the IPinfo results are incorrect.

## My Unique Personality

As a dedicated but technical student, my personality is **very different from over 99% of others**💘. I always **uphold my unique ideas and opinions** in my personal and self-led group projects.

I am currently experiencing mental stress with Autism Spectrum Disorder (ASD), Asperger Syndrome😡 and **hardship** for accepting other's opinions and ideas.

However, you are still welcome to drop your ideas📩 to Issues and my contacts.
Do not try to oppose my unique idea and opinions when making suggestions.

Please visit my personal website🌎 (https://ken.kenstudyjourney.cn) to learn more.

Thanks for your understanding.
