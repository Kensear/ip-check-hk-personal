# IP Quality & Stream Restriction Checker (HK)

## IP Quality &amp; Streaming Service Regional Restriction Checker (Hong Kong Region Only)

### IP位址可信程度&流媒體服務可用性測試程式 (祗限香港地區)

### IP质量与流媒体平台解锁测试脚本 (仅限香港地区)

🌎 **README Language/语言:** English | [繁體中文](./README_zh_HK.md) | [简体中文](./README_zh_CN.md)

### ⚠️ Disclaimer
- For personal research🔬 only (apart from just a developer, I am also a researcher!).
- This project is affiliated with neither❌ any local ISP🔌 nor any website🌎 stated.
- This project is only for testing IP address and streaming services. It does not❌ provide other services including VPS servers.
- As a beginner to Cantonese, the Chinese-Traditional (繁體中文) version of README may be incorrect.

### Description

This project is for testing whether streaming services can be used (also known as "流媒体解锁测试" in Mainland) and the quality of the IP address under HK local networks and VPS servers.

As a Hong Kong university student🏫 (and semi-local), **only** the nodes in **Hong Kong region** are used and hence only the checkers of that region were developed (Why? See FAQ below⬇️).

<img width="1250" height="649" alt="440261998-951f4a86-3374-432c-8e69-42de00be0bfe" src="https://github.com/user-attachments/assets/e65b1c55-55d8-43b4-84da-a331a5a83418" /><br>

This was made originally due to an **argument** with the original author about Netflix module, but along with some new features (see below⬇️).

<img width="520" alt="437650943-c26aaf26-9435-43b9-ac4d-2d7f4b49314c-2" src="https://github.com/user-attachments/assets/d5906271-3cd2-4a88-8549-08715fa1ea77" /><br>

**My Personality:**<br>
If my suggestion/PR is rejected by a repo, fork (copy) it ASAP and modify it with my unique suggestions for **personal use**.<br>
Please see bottom⬇️ to learn more.

Inspired by and modified from:
- [https://doc.theojs.cn/vps/tools/streaming-unlocked](https://doc.theojs.cn/vps/tools/streaming-unlocked)
- [https://doc.theojs.cn/vps/tools/ipquality](https://doc.theojs.cn/vps/tools/ipquality)

## Personal Version - No Contribution or Discussion Allowed

This repository is **only for my personal sharing**📤 as used on Kensear articles & videos.

Any interactions, including but not limited to Issues and Pull Requests, will be **ignored** in this repository.

I may consider opening a Public Version for public contribution (possibly with more regions) in the coming weeks/months.

However, you are welcome to contact me if you have questions/suggestions:
https://www.kensear.com/en/contact/

## Running

Simply download and run the corresponding .py files in Python.

> [!CAUTION]
> **Do Not** run the same type of script (Check IP or Stream) too many times🔂  under the **same IP address** in a day, or it may result in IP Ban⛔️ by the services tested.

### Test IP Quality

```
# Choose one based on your device/emulator.
python3 ./chkip.py
python ./chkip.py
```

Be mindful of the following CAPITAL letters:

|Letters|Meaning|
|-------|-------|
|LC|Location (Region) Code of the IP Address|
|SRV|Whether Labelled as a Server / Data Centre|
|VPN|Whether Labelled as a VPN Server|
|PXY|Whether Labelled as a Proxy Server|
|RLY|Whether Labelled as a Relay Server|
|TOR|Whether Labelled as a Tor Server|
|ABU|Whether Labelled as an Abuser|

**Non-HK**❌ regions ("LC" column) labelled by each IP address information provider will be 🔴**red** for quicker checking☑️.

### Test Streaming/Local Services

```
# Choose one based on your device/emulator.
python3 ./chkstream.py
python ./chkstream.py
```

Press "Y" and then "Enter" to also test Mainland websites, or press "Enter" otherwise.

Be mindful of the following result letters:

|Letter|Colour|Result|
|------|------|------|
|Y|🟢Green|Yes|
|N|🔴Red|No (IP Banned or Not Available)|
|E|🔴Red|Network Error, Unable to Test|

## New Features

This script adds the following features (improvements) from the reference repo above⬆️:

- Check if Sign-in🪪 Required for YouTube (i.e., "Sign in to confirm that you're not a bot🤖")
- Check Academic & Research🔬 Websites (e.g., Google Scholar & Colab)
- Check HK University🏫 Websites
- Check HK Bank🤑 Websites
- Check Mainland Websites (optional)

YouTube "Sign in to confirm that you're not a bot" Screen:

<img width="650" alt="437651374-37708650-8917-4ed1-930b-6bc99c37843d-2" src="https://github.com/user-attachments/assets/cc776b24-daed-4849-941f-cad862315644" /><br>

## Tech Principles of Testing

The following table shows the technical working principles🛠️ of the testing of some services for the ease of understanding by developers and researchers.

Please note that the actual test scripts use **keyword scanning**🔍.

|Test Name|Test URL|Result|
|---------|--------|------|
|Google Search No CAPTCHA|Search anything (e.g., curl):<br>[https://www.google.com/search?q=curl](https://www.google.com/search?q=curl)|✅ Search Results<br>❌ CAPTCHA (I'm not a robot) Popup|
|YouTube No Login Required|Watch any video (e.g., a 4K video):<br>[https://www.youtube.com/watch?v=LXb3EKWsInQ](https://www.youtube.com/watch?v=LXb3EKWsInQ)|✅ Video or Ad Playing<br>❌ Sign in to confirm that you're not a bot|
|Google Scholar|[https://scholar.google.com](https://scholar.google.com)|✅ Google Scholar Search Page<br>❌ “We're sorry” or 403 Error Page|
|Netflix|[https://www.netflix.com/title/70143836](https://www.netflix.com/title/70143836)|✅ Movie Information<br>❌ Yellow Banner "isn't available to watch" at the Top|
 
## FAQ (Frequently Asked Questions)

### Why Use Python?

It can also be used in the following OS (including mobile phones) apart from just Linux and VPS (Virtual Private Servers):
- iOS (with iSH app)
- Android (with Termux app)
- Windows
- macOS

Python is also one of my current skills.

### Why Only HK Region Nodes and Test Script?

As a HK university student🏫 (and semi-local), only HK nodes are required for local services and content.

Switching to many different regions in a very short time will trigger **account login security alerts**⚠️ on some websites/services and may even lead to **account ban**🚫.

Using node(s) of other regions for a long time can also lead to **account region change🔁**.

### Why Red/Blue "Wrong Region" Colours?

This is for quicker check☑️ whether the node is in HK region.

### Why Limited the Width of Display?

This is for testing and display on mobile phones📲 with much smaller screens than computers🖥️.

### Why you also Use it on Mobile Phones?

This is for my personal research and experiments🔬, testing various WiFi🛜 among different places in HK.

### Why you Need this Test (and why Residential IP)?

As a HK university student📝, services like Google Scholar/Colab and WhatsApp are the essentials.

In Mainland, however, they are not directly accessible🚧 without a dedicated line impacting studies and coursework.

However, some nodes are not ISP, Business or Education types (majorly Hosting🗃️) or reused🔂 by hundreds or thousands of other users, making certain services (like Netflix) inaccessible🚧 (i.e., IP Ban).

Using a node with many abusers⚠️ may also lead to account ban🚫.

This is why a Residential IP (or relevant VPS servers) is also an essential.

> [!NOTE]
> This project is only for testing IP address and streaming services. It **does not**❌ provide other services including VPS servers, Residential IPs and dedicated lines.

## My Personal Research

Apart from a programmer🧑‍💻 and software developer🛠️, I am also a **researcher**🔬 diving into the technical working principles behind.

I did a lot of personal research and experiments🧪 about the Residential IPs and local ISPs around HK.

### Common HK ISPs

I researched🔬 about some common ISPs in HK and their AS (Autonomous System) numbers with the following ways:
- Residential IP🏡 (a.k.a., 住宅IP) providers
- HK local network🛜 at different places (including Mobile Data, University Campus WiFi and Public WiFi in various shopping malls)

While free WiFi around HK usually have time limits⏳ per day/session (like 15 to 30 mins, but with **unlimited free WiFi** under a small probability), the tests only take around **3 mins** to complete.

For example only. This is not an exhaustive list.<br>
- H = Home Broadband🏡
- B = Business Broadband🏢
- M = Mobile Data📲

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

- Block All **Bank** Websites/Apps (including HK and other Banks)
- Block All **ICP-Registered** Websites/Apps (even if they have servers outside Mainland)

<img width="400" alt="437651118-2b711d91-c64a-4ae4-bc13-a4b7f5321e31" src="https://github.com/user-attachments/assets/f28d71e8-cf6a-478e-9218-aa8b6a19326b" /><br>

### Issue: IP Labelled as Mainland by Google

Due to some users in Mainland using Google with Location Services📍 (like GPS) enabled, some IP addresses were labelled as Mainland by Google even if it is not❌ the actual IP address location.

You will see that all Google and YouTube services will have the "CN" region displayed in the test scripts.

<img width="700" alt="440264204-e0febc8b-d2a7-4b0d-bfe7-1866ef77a02c" src="https://github.com/user-attachments/assets/d2526ec5-1c4e-4e70-b362-4083ca0cb906" /><br>

From my test and experiment results, **none**❌ of the HK local networks, including Mobile Data📲, University "eduroam" WiFi🏫 and Free WiFi🛜, appeared to have this result (probability: 0%).

To "pull" an IP address back to HK🔙, keep doing the following for 1 to 30 days⏳ (several times per day):
1. Connect🔌 to the same server when **physically** in HK
2. Turn on (Allow) Location Services on your device/browser
3. Search🔍 anything on Google or use Google Maps🧭
4. After searching/opening, update/report your location📍 at the bottom

Based on my experiment, **three (3)** of the IP addresses previously labelled as Mainland by Google (plus **one (1)** for Instagram) were **successfully** "pulled back"✅ to HK.

To learn more, please visit: [https://www.tjsky.net/tutorial/546](https://www.tjsky.net/tutorial/546) (just a reference, not my article)

### HK Local Broadband Test Result

When testing under HK local network (under the ISPs mentioned above⬆️), all testing were passed including the ISP incorrectly labelled as Hosting by IPinfo.

- For IP Quality Check:
  - IP Usage Type Table majorly have the 🟢**Green** "**ISP**" or 🔵**Blue** "**Business**" or "**Education**" displayed✅ *
  - IP Privacy Table majorly have the 🟢**Green** "**N**" displayed✅ *
  - IP Risk Table all have the 🟢**Green** low-risk values displayed✅
- For Stream Restriction Check:
  - All Tests have the 🟢**Green** "**Y**" displayed✅

\* Except the ISP incorrectly labelled as Hosting by IPinfo, where **only** some IP database results are incorrect.

## My Unique Personality

As a dedicated but technical student, my personality is **very different from over 99% of others**💘. I always **uphold my unique ideas and opinions** in my personal and self-led group projects.

I am currently experiencing mental stress with Autism Spectrum Disorder (ASD), Asperger Syndrome😡 and **hardship** for accepting other's opinions and ideas.

Please visit Kensear website🌎 (https://www.kensear.com/en/unique-personality/) to learn more.

Thanks for your understanding.
