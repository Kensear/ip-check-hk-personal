# IP位址可信程度及流媒體可用性測試 (HK)

**IP位址可信程度&amp;流媒體服務可用性測試程序 (祗限香港地區)**

Disclaimer:
- 祗限Personal Research🔬（除身為developer外，我仲有researcher的身分）
- 本repo與其中所列明的任何寬頻提供商ISP或網站未有任何聯繫

由於我對於Netflix的建議未能被原repo接納，我已按自己idea製作本repo。

<img width="520" alt="Screenshot 2025-04-16 at 4 59 19 PM" src="https://github.com/user-attachments/assets/c26aaf26-9435-43b9-ac4d-2d7f4b49314c" /><br>

**我的特性:**<br>
如果我的建議或者PR未能被原repo採用，我將盡快fork，然後按自己的idea修改，以供**本人使用**。<br>
如欲了解詳情，請翻到底部查看⬇️

基於以下資料修改：
- [https://doc.theojs.cn/vps/tools/streaming-unlocked](https://doc.theojs.cn/vps/tools/streaming-unlocked)
- [https://doc.theojs.cn/vps/tools/ipquality](https://doc.theojs.cn/vps/tools/ipquality)

身為本港大學生，**只會**使用**香港地區**的節點，故唯有香港地區的測試程序。

為什麼？因為短時間內頻繁切換region可能會引起網站服務的登入安全警報 (security alert)，甚至被封鎖戶口。

**Note:**
由於Spotify註冊功能（即Spotify Registration）會就**latency**對是否使用代理做出判斷，其測試結論可能會在高網絡延遲下不準確。

## 程序運行

測試時，只需要下載對應Python (.py)程序，然後運行即可。

**切勿**在一日內用**相同的IP位址**太多次運行本repo中相同類型的程序（即IP或者Stream測試），否則可能因太多次請求導致IP位址被服務封鎖。

IP位址可信程度測試
```
# 根據自己裝置選定以下其中一個command
python3 ./chkip.py
python ./chkip.py
```

流媒體及本港服務可用性測試
```
# 根據自己裝置選定以下其中一個command
python3 ./chkstream.py
python ./chkstream.py
```

## 新增功能

本程序已在上列參考的repo的基礎之上做出改善與新增功能：

- 測試YouTube是否強制Sign-in才可收看影片（即“請登入以確認你並非機械人”提示畫面）
- 測試本港各大學官方網站可否使用
- 測試本港各銀行網站可否使用
- 測試內地網站/服務可否使用（可選項）

本repo最初為Python版本（連同**urllib**模組）。除Linux系統外，還可用於iOS（連同iSH app）、Windows、macOS等系統。

YouTube "請登入以確認你並非機械人" 提示畫面：
<img width="700" alt="Screenshot 2025-04-09 at 4 08 59 PM" src="https://github.com/user-attachments/assets/37708650-8917-4ed1-930b-6bc99c37843d" />

## 我的研究

除programmer🧑‍💻同software developer🛠️的身分以外，我還有**researcher**🔬的身分，了解更多技術內部運作原理。

前段時間我已做過許多有關Residential IP同本港寬頻提供商的研究和實驗🧪。

### 本港常見寬頻提供商

我已透過以下方法研究🔬、搜尋本港常見的寬頻提供商及其AS（自治系統）編碼：
- Residential IP（內地稱作“住宅IP”）提供商
- 位於本港不同地方的免費WiFi熱點

本表格僅為樣例，可能還有更多表格內未列明的ISP<br>
H = 家用寬頻 Home; B = 商業寬頻 Business

|名稱|Hostname最後部分|AS編碼|類別|
|----|--|--|----|
|HKT 香港電訊|netvigator.com|AS4760|H|
|HKT Enterprise|imsbiz.com|AS4515|B|
|HK Cable TV 有線寬頻|hkcable.com.hk|AS9908|H|
|SmarTone 數碼通||AS17924|H|
|CMHK 中國移動香港|hk.chinamobile.com|AS9231<br>AS137872|H|
|HKBN 香港寬頻|ctinets.com|AS10103|H|
|HKBN Enterprise <sup>1</sup>||AS9381|B|
|HGC 和記環球電訊||AS9304|H/B|
|Hutchison (3/Three)||AS10118|H|
|JUCC 大學聯合電腦中心 (祗限University) <sup>2</sup><br>||AS3662|B|

Note:
1. 被IPinfo標錯為**Hosting**（甚至有**VPN**）類別；我已聯絡IPinfo，而由於IPinfo此前已通過**mass port scanning**確認為server同VPN類別，我的appeal**未獲接納**（回覆郵件有提供掃描程式的evidence）
2. 連同每個大學（downstream）的AS自治系統編碼

根據我自己的研究與實驗結論，有大學使用了HGC或者HKBN Enterprise的寬頻，而非JUCC（即自己的AS編碼）。

### Residential IP提供商特性

根據實驗結論，一些Residential IP提供商有以下特性：

- 封鎖**銀行**網站同App（包括本港同其他地區銀行）
- 封鎖所有持**內地ICP備案編號**的網站同App（包括持有非內地server的服務）

<img width="400" alt="Screenshot 2025-04-26 at 8 23 12 AM" src="https://github.com/user-attachments/assets/2b711d91-c64a-4ae4-bc13-a4b7f5321e31" />

### 本港寬頻測試實驗結論

在本港不同地點多個網路（即上方⬆️所列明的寬頻提供商ISP）測試後，所有測試都已通過（顯示**綠色的"Y"**），包括被IPinfo標錯為Hosting的IP位址。

## 我的特性

身為一名專注、有技術能力的學生，我的性格不同於超過99%的其他同學。我在personal project同由本人領導的group project都想始終**按自己的idea完成**。

我目前存在自閉症(ASD)、阿斯伯格綜合症等症狀，故**未能**接納其他人的idea同opinion。

儘管如此，歡迎在Issues中提出自己的idea📩，但盡量避免oppose我的unique idea。

如欲了解詳情，請瀏覽我的個人主頁🌎（https://ken.kenstudyjourney.cn）。

感謝你的理解。
