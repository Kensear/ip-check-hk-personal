# IP位址可信程度及流媒體可用性測試 (HK)

## IP位址可信程度&amp;流媒體服務可用性測試程式 (祗限香港地區)

⚠️ 免責聲明/Disclaimer:
- 祗限個人研究及實驗使用🔬（除身為developer外，我還有researcher的身分）
- 本repo與其中所列明的任何寬頻提供商ISP🔌或網站🌎未有任何聯繫❌
- 本repo祗限測試IP位址及流媒體服務，不會❌供應任何VPS伺服器等其它服務
- 本人正開始學習廣東話及基於廣東話的繁體中文（作為beginner），如本README檔案有任何錯誤，歡迎於Issues報告問題

本repo主要用於測試本港網絡、虛擬服務器VPS等節點是否可使用流媒體服務（內地用戶稱作“流媒體解鎖測試”），以及IP位址可信程度。

身為本港大學生🏫（同semi-local），**只會**使用**香港地區**的節點，故唯有香港地區的測試程式（詳見下面FAQ⬇️）。

<img width="1098" alt="Screenshot 2025-05-02 at 11 52 13 PM" src="https://github.com/user-attachments/assets/34740da8-3a7d-4ad7-80cb-b4a95f2b3b28" /><br>

由於我對於Netflix的建議未能被原repo接納❌，我已按自己idea製作本repo，同時還添加了新功能（詳見下面⬇️）。

<img width="520" alt="Screenshot 2025-04-16 at 4 59 19 PM" src="https://github.com/user-attachments/assets/c26aaf26-9435-43b9-ac4d-2d7f4b49314c" /><br>

**我的特性:**<br>
如果我的建議💬或者PR未能被原repo採用，我將盡快fork📑，然後按自己的idea修改，以供**本人使用**。<br>
如欲了解詳情，請翻到底部查看⬇️

基於以下資料修改：
- [https://doc.theojs.cn/vps/tools/streaming-unlocked](https://doc.theojs.cn/vps/tools/streaming-unlocked)
- [https://doc.theojs.cn/vps/tools/ipquality](https://doc.theojs.cn/vps/tools/ipquality)

## 程式運行

測試時，只需要下載對應Python (.py)程式，然後運行即可。

> [!CAUTION]
> **切勿**在一日內用**相同的IP位址**太多次運行🔂本repo中相同類型的程式（即IP或者Stream測試），否則可能因太多次請求導致IP位址被服務封鎖⛔️。

### IP位址可信程度測試

該程式將從不同IP位址數據庫提供商取得IP位址地區🌎、風險評值⚠️等訊息。

```
# 根據自己裝置選定以下其中一個command
python3 ./chkip.py
python ./chkip.py
```

留意以下結果字母簡寫含義：

|字母簡寫|含義|
|------|-------|
|LC|IP位址所在地區ISO編碼|
|VPN|是否被標為VPN Server|
|PXY|是否被標為Proxy Server|
|RLY|是否被標為Relay Server|
|TOR|是否被標為Tor Server|
|ABU|是否被標為濫用者 (abuser)|

如果IP位址被一些數據庫標為**非香港地區**❌，表格內LC一列對應的地方會以**紅色**顯示，幫助更快判斷。

### 流媒體及本港服務可用性測試

該程式將測試不同的搜尋引擎🔍、學術資料搜尋服務📝、流媒體服務🎬、本港大學🏫等網站/服務的可用性。

```
# 根據自己裝置選定以下其中一個command
python3 ./chkstream.py
python ./chkstream.py
```

在流媒體及本港服務可用性測試程式中，如欲測試內地服務可用性，請按Y然後Enter，否則直接Enter即可

留意以下結果字母含義：

|字母|顏色|結果|
|------|------|------|
|Y|🟢綠色|可使用|
|W|🔵藍色|可使用，但地區不對（並非香港地區）|
|N|🔴紅色|不可使用 (IP已經被ban)|
|E|🔴紅色|網絡錯誤，未能查詢|

## 新增功能

本程式已在上列⬆️參考的repo的基礎之上做出改善與新增功能：

- 測試YouTube是否強制登入🪪才可收看影片（即“請登入以確認你並非機械人🤖”提示畫面）
- 測試學術和科研🔬網站可否使用 (例如Google Scholar同Colab)
- 測試本港各大學🏫官方網站可否使用
- 測試本港各銀行🤑網站可否使用
- 測試內地網站/服務可否使用（可選項）

YouTube "請登入以確認你並非機械人" 提示畫面：

<img width="700" alt="Screenshot 2025-04-09 at 4 08 59 PM" src="https://github.com/user-attachments/assets/37708650-8917-4ed1-930b-6bc99c37843d" />

## 常見服務測試原理

為方便developer同researcher了解運作原理，已將部份服務的測試原理詳列下表，但會通過keyword scan來測試。

|測試項|測試連結|測試結果|
|-----|-------|-------|
|Google Search No CAPTCHA|搜尋任意關鍵字，例如curl：<br>[https://www.google.com/search?q=curl](https://www.google.com/search?q=curl)|✅ 正常顯示curl的搜尋結果<br>❌ 彈出CAPTCHA (I'm not a robot)|
|YouTube No Signin Required|觀看任意影片，例如一部4K影片：<br>[https://www.youtube.com/watch?v=LXb3EKWsInQ](https://www.youtube.com/watch?v=LXb3EKWsInQ)|✅ 正常顯示影片或廣告<br>❌ 請登入以確認你並非機械人|
|Google Scholar|[https://scholar.google.com](https://scholar.google.com)|✅ 正常顯示Google學術搜尋畫面<br>❌ “We're sorry”或者403錯誤畫面|
|Netflix|[https://www.netflix.com/title/70143836](https://www.netflix.com/title/70143836)|✅ 正常顯示影片資訊<br>❌ 最上面有黃色“這部影片目前無法在您的國家/地區觀賞”提示|

## FAQ/常見問題

### 為什麼用Python？

本repo最初為Python版本（連同**urllib**模組）。除Linux系統外，還可用於以下類別的OS（包括流動電話裝置）：
- iOS（連同iSH app）
- Android（連同Termux app）
- Windows
- macOS

Python也是我現在的其中一個skill。

### 為什麼你只需要港區節點，只有港區測試程式？

作為本港的大學生🏫（semi-local），只需要用到香港地區的節點，以使用/觀看本港服務及內容。

因為短時間內頻繁切換region可能會引起網站服務的登入安全警報⚠️ (security alert)，甚至被封鎖戶口🚫。

另外，如長時間使用其它地區的出口IP節點，還會導致戶口被標為/轉到🔁其它地區。

### 為什麼要增加紅色/藍色“地區不對 (Wrong Region)”的提示？

該提示可以讓自己更加快速判斷☑️是否為香港地區。

### 為什麼限制了程式顯示的寬度？

這樣是為了方便自己在流動電話📲裝置上使用、測試，而流動電話的屏幕不會像電腦🖥️一樣闊，會特別窄。

### 為什麼還會在流動電話裝置上使用？

供本人研究及實驗🔬使用，這樣會方便自己快速測試全港不同地方的WiFi熱點🛜。

### 為什麼要進行這種測試？

作為本港的大學生，溫習📝期間需要用到Google Scholar/Colab、WhatsApp等服務。

但在內地不可直接使用🚧這些服務，需要使用專綫連同Residential IP（或者其VPS伺服器）節點，否則溫習將受妨礙。

但是，部份節點並非ISP、Business或Education類別（一般為Hosting🗃️），或者很多人用同一個IP位址🔂，就會造成部份網站和Netflix等流媒體服務不可使用🚧（即IP位址被封鎖）。

另外，如果一個IP位址內有太多濫用者 (abuser)⚠️，還有可能會導致被封鎖戶口🚫。

## 我的研究

除programmer🧑‍💻同software developer🛠️的身分以外，我還有**researcher**🔬的身分，了解更多技術內部運作原理。

前段空閒時間我已做過許多有關Residential IP及本港寬頻提供商(ISP)的研究和實驗🧪。

### 本港常見寬頻提供商

我已透過以下方法研究🔬、搜尋本港常見的寬頻提供商(ISP)及其AS（自治系統）編碼：
- Residential🏡 IP（內地稱作“住宅IP”）提供商
- 全港不同地點的網絡🛜（例如流動數據、大學校園WiFi及不同商場的免費WiFi）

本港的免費WiFi熱點一般會限制每日/每節使用時間⏳（例如15-30分鐘，但很小概率會有**不限時**的免費WiFi），但本測試只需**約3分鐘**即可完成。

本表格僅為樣例，可能還有更多表格內未列明的ISP<br>
- H = 家用寬頻 Home Broadband🏡
- B = 商業寬頻 Business Broadband🏢
- M = 流動數據 Mobile Data📲

|名稱|Hostname最尾部分<sup>1</sup>|AS編碼|類別|
|----|--|--|----|
|HKT 香港電訊|netvigator.com|AS4760|H|
|HKT Enterprise|imsbiz.com|AS4515|B|
|HKCSL GPRS Network|pccw-hkt.com|AS38819|M|
|HK Cable TV 有線寬頻|hkcable.com.hk|AS9908|H|
|SmarTone 數碼通||AS17924|H/M|
|CMHK 中國移動香港|hk.chinamobile.com|AS9231<br>AS137872|H/M|
|HKBN 香港寬頻|ctinets.com|AS10103|H/B|
|HKBN Enterprise<sup>2</sup>||AS9381|B|
|HGC 和記環球電訊||AS9304|H/B|
|Hutchison (3/Three)||AS10118|M|
|JUCC 大學聯合電腦中心 (祗限大學)<sup>3</sup><br>||AS3662|B|

Note:
1. 透過`nslookup`指令查詢🔍IP位址對應的Hostname得出
2. 被IPinfo標錯❌為**Hosting**（甚至有**VPN**）類別；我已聯絡IPinfo📩，而由於IPinfo此前已通過**mass port scanning**🔍確認為server同VPN類別，我的appeal**未獲接納**（回覆郵件有提供掃描程式的證據）；但**並未影響✅**流媒體可使用性
3. 連同每個大學（downstream，下聯）的AS自治系統編碼

根據我自己的研究與實驗結論，部份本港大學使用了HGC或者HKBN Enterprise的寬頻，而非JUCC（即大學自己的AS編碼）。

常見本港Residential IP的VPS提供商使用了HGC（有時會有HKT）寬頻提供商的綫路。

### Residential IP提供商特性

根據實驗結論，一些Residential IP提供商有以下特性（其中一個）：

- 封鎖**銀行**網站同App（包括本港同其他地區銀行）
- 封鎖所有持**ICP備案編號**的網站同App（包括持有非內地server的服務）

<img width="400" alt="Screenshot 2025-04-26 at 8 23 12 AM" src="https://github.com/user-attachments/assets/2b711d91-c64a-4ae4-bc13-a4b7f5321e31" /><br>

### IP位址被Google標為內地問題

由於部份用戶在啟用Location Service📍（即GPS）時使用Google，部份節點的IP位址已被Google標為內地，即使該IP位址並非❌位於該地區。

在運行測試程式時，就會看到Google同YouTube的地區顯示為CN（內地）。

<img width="601" alt="Screenshot 2025-05-03 at 12 05 43 PM" src="https://github.com/user-attachments/assets/7e12b2f8-078d-47d6-b9b3-df9d4656bf48" /><br>

我在全港範圍內的網絡（包括流動數據📲、大學校園"eduroam" WiFi🏫及免費WiFi熱點🛜）進行測試和實驗時，**並未出現過**該情況（概率為0%）❌。

要將節點IP位址拉回🔙到本港，只需持續1-30日⏳做這些事情即可：
1. 在全港範圍內連結🔌到該節點
2. 在你的裝置及瀏覽器中啟用Location
3. 使用Google搜尋🔍任意內容，或者打開Google Maps🧭
4. 滾動到底部，並上報/更新自己GPS位置📍

根據我的實驗結果，其中兩個被Google標為內地的節點IP位址**已成功**拉回✅到本港。

如欲了解詳情，請參考：[https://www.tjsky.net/tutorial/546](https://www.tjsky.net/tutorial/546)（只供參考，並非我的文章）

### 本港寬頻測試實驗結論

在本港不同地點多個網絡熱點（即上方⬆️所列明的寬頻提供商ISP）測試後，所有測試都已通過，包括被IPinfo標錯為Hosting的IP位址，例如：
- IP位址可信程度測試程式內：
  - IP Usage Type的表格基本顯示🟢**綠色的**"**ISP**"或者**藍色的**"**Business**"或"**Education**"✅ *
  - IP Privacy的表格基本顯示🟢**綠色的**"**N**"✅ *
  - IP Risk的表格所有都以🟢**綠色**顯示特別低的數值✅
- 流媒體可用性測試程式內：
  - 所有測試均顯示🟢**綠色的**"**Y**"✅

\* 被IPinfo標錯為Hosting的ISP除外，但**僅有**IPinfo這一行出現錯誤

內地用戶會將這種結果稱作“**流媒體全解鎖**”✅，也是他們期望的結果。

## 我的特性

身為一名專注、有技術技能的學生，我的性格**不同於超過99%的其他同學💘**。我在personal project及由本人領導的group project都想始終**按自己的idea完成**。

我目前存在自閉症(ASD)、阿斯伯格綜合症😡等症狀，故**未能**接納其他人的idea同opinion。

儘管如此，歡迎在Issues中提出自己的idea📩，但盡量避免oppose我的unique idea。

如欲了解詳情，請瀏覽我的個人主頁🌎 ([https://ken.kenstudyjourney.cn](https://ken.kenstudyjourney.cn))。

感謝你的理解。
