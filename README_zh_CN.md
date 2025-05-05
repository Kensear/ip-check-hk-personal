# IP质量与流媒体解锁测试 (HK)

## IP质量与流媒体平台解锁测试脚本 (仅限香港地区)

### ⚠️ 免责声明/Disclaimer
- 仅限本人研究和实验使用🔬（除程序员/开发者外，我还有研究人员的身份哦！）
- 本项目与其中列出的任何宽带提供商ISP🔌或网站🌎均没有任何关联❌
- 本项目只能测试IP质量和流媒体解锁，不提供❌任何VPS服务器等其它产品/服务
- 本人作为粤语的初学者，繁体中文版的README说明文件可能不太准确，敬请谅解

### 项目介绍

本项目主要用于测试香港本地网络、虚拟服务器VPS等节点的IP地址质量和流媒体解锁情况（即“IP质量检测”和“流媒体解锁测试”）。

作为一名香港的大学生🏫（和semi-local），**只会**用到**香港地区**的节点，因此只有香港地区的测试脚本（为什么？详见下方FAQ常见问题⬇️）。

<img width="1250" alt="Screenshot 2025-05-05 at 12 32 37 PM" src="https://github.com/user-attachments/assets/951f4a86-3374-432c-8e69-42de00be0bfe" /><br>

由于我之前关于Netflix的建议未被原第三方项目采纳❌，我已完全按照自己想法制作本项目，同时还添加了一些新功能（详见下方⬇️）。

<img width="520" alt="Screenshot 2025-04-16 at 4 59 19 PM" src="https://github.com/user-attachments/assets/c26aaf26-9435-43b9-ac4d-2d7f4b49314c" /><br>

**我的性格：**<br>
如果我的建议💬或拉取请求PR未被原项目采纳，将尽快复制一份(fork)📑，然后完全按照自己的想法修改，以便**本人使用**。<br>
更多信息请查看本文底部⬇️

基于以下项目修改：
- [https://doc.theojs.cn/vps/tools/streaming-unlocked](https://doc.theojs.cn/vps/tools/streaming-unlocked)
- [https://doc.theojs.cn/vps/tools/ipquality](https://doc.theojs.cn/vps/tools/ipquality)

## 脚本运行

测试时，只需下载对应的Python (.py)程序，然后运行即可。

> [!CAUTION]
> **不要**一天内在**同一个IP地址下**运行太多次🔂相同类型的脚本（即IP质量或流媒体解锁测试），否则可能会因太多次请求导致IP地址被相关服务封禁⛔️哦！

### IP地址质量测试

该脚本将从不同的IP地址数据库提供商获取IP地址所在地区🌎、风险值⚠️等信息。

```
# 根据自己的设备类型，运行以下其中一条命令
python3 ./chkip.py
python ./chkip.py
```

测试时，留意以下结果字母简写的意思：

|字母简写|意思|
|------|-------|
|LC|IP地址所在地区代码|
|SRV|是否已被标记为机房/服务器类型|
|VPN|是否已被标记为VPN服务器|
|PXY|是否已被标记为普通代理(Proxy)服务器|
|RLY|是否已被标记为中继代理(Relay)服务器|
|TOR|是否已被标记为Tor节点|
|ABU|是否已被标记为滥用(abuser)|

为帮助自己更快判断☑️，被标为**非香港区**❌的对应数据库的“LC”位置一栏会以🔴**红色**显示。

### 流媒体和香港本地服务解锁测试

该脚本将测试不同的搜索引擎🔍、学术信息搜索引擎📝、流媒体平台🎬、香港不同大学🏫等网站/服务是否可用。

```
# 根据自己的设备类型，运行以下其中一条命令
python3 ./chkstream.py
python ./chkstream.py
```

如需测试内地服务是否可用，请按Y然后Enter回车键，否则直接Enter回车即可

测试时，留意以下结果字母的意思：

|字母|颜色|测试结果|
|------|------|------|
|Y|🟢绿色|解锁成功|
|N|🔴红色|解锁失败 (IP已被封禁)|
|E|🔴红色|网络异常，查询失败|

## 新功能

本脚本已在上列⬆️参考项目的基础上修改、新增部分功能：

- 测试YouTube是否强制登录账号🪪才能看视频（即“请登录，以便我们确认你不是聊天机器人🤖”提示界面）
- 测试学术和科研🔬网站是否可用（如Google Scholar和Colab）
- 测试香港不同大学🏫的官方网站是否可用
- 测试香港不同银行🤑的网站是否可用
- 测试内地网站/服务是否可用（选测项）

YouTube“请登录，以便我们确认你不是聊天机器人”提示界面：

<img width="700" alt="Screenshot 2025-04-09 at 4 08 59 PM" src="https://github.com/user-attachments/assets/37708650-8917-4ed1-930b-6bc99c37843d" /><br>

## 常见流媒体测试原理

为方便开发者和研究人员了解背后的技术工作原理，已将部分流媒体平台测试原理🛠️列出，但实际上会通过关键词扫描🔍的方式测试。

|测试项|测试链接|测试结果|
|-----|-------|-------|
|Google Search No CAPTCHA|搜索curl等任意关键词：<br>[https://www.google.com/search?q=curl](https://www.google.com/search?q=curl)|✅ 正常显示搜索结果<br>❌ 弹出CAPTCHA人机身份验证框|
|YouTube No Signin Required|观看4K等任意视频：<br>[https://www.youtube.com/watch?v=LXb3EKWsInQ](https://www.youtube.com/watch?v=LXb3EKWsInQ)|✅ 正常播放视频或广告<br>❌ 请登录，以便我们确认你不是聊天机器人|
|Google Scholar|[https://scholar.google.com](https://scholar.google.com)|✅ 正常显示Google学术搜索界面<br>❌ “We're sorry”或403错误界面|
|Netflix|[https://www.netflix.com/title/70143836](https://www.netflix.com/title/70143836)|✅ 正常显示电影信息<br>❌ 最上面有黄色“无法在你的国家/地区观赏”横幅|

## 常见问题FAQ

### 为什么用Python？

除了Linux系统和VPS虚拟服务器外，还可以用于以下类型的系统（包括手机）：
- iOS（在iSH APP中使用）
- 安卓（在Termux APP中使用）
- Windows
- macOS

Python也是我现在的其中一个技能。

### 为什么你只需要港区的节点？只有港区测试脚本？

作为一名香港的大学生🏫（和semi-local），只需要用到香港地区的节点，以使用/观看香港本地的服务和内容。

因为短时间内频繁切换地区可能会引发网站服务的账号登录安全警告(security alert)信息⚠️，甚至被封账号🚫。

另外，如长时间使用其它地区的出口IP节点，还会导致账号被标到/转到🔁其它地区。

### 为什么要增加红色/蓝色“地区错误 (Wrong Region)”的提示？

因为这个提示可以让自己更快判断☑️是否为港区节点/解锁。

### 为什么限制了脚本显示的宽度？

这样是为了方便自己在手机📲上使用、测试，但手机的屏幕比电脑🖥️的窄很多

### 为什么你还会在手机上使用？

这是为了方便我本人的研究和实验🔬，快速测试全香港不同地方WiFi热点🛜的IP质量和流媒体解锁情况。

### 为什么要进行这种测试？为什么用住宅IP？

作为一名香港的大学生，学习📝期间需要用到Google Scholar/Colab、WhatsApp等平台。

但内地无法直接使用🚧这些服务，需要用到专线，否则会影响学习。

但部分节点并不是ISP运营商、Business公司或Education教育网类型（一般为Hosting🗃️机房类型），或者很多人共用同一个IP地址🔂，就会无法解锁🚧Netflix等部分网站、流媒体服务（即IP地址被平台封禁）。

另外，如果一个IP地址下有很多滥用者abuser并被标为滥用⚠️，还有可能会伤账号🚫。

这就是为什么需要住宅IP节点（或者使用住宅IP的VPS服务器）。

> [!NOTE]
> 本项目只能测试IP质量和流媒体解锁，不提供❌任何VPS服务器、住宅IP、专线等其它产品/服务

## 我的研究

除了程序员🧑‍💻和开发者🛠️的身份以外，我还有**研究人员**🔬的身份，了解更多背后的技术原理。

前端空闲时间我已做过有关住宅IP以及香港本地宽带运营商(ISP)的研究和实验🧪。

### 常见香港本地宽带运营商

我已通过以下方式研究🔬、找到香港本地常见的宽带运营商(ISP)和它们的AS(自治系统)号码：
- 住宅IP🏡服务商
- 全香港不同地方的网络🛜（如移动数据、大学校园WiFi和不同商场的免费WiFi）

香港本地的免费WiFi热点一般会限制每天/每次的使用时间⏳（例如15-30分钟，但很小概率会有**不限时**的免费WiFi），但本测试只需**约3分钟**完成。

本表格仅为示例，可能还有表格内未列出的运营商<br>
- H = 家庭宽带 Home Broadband🏡
- B = 企业宽带 Business Broadband🏢
- M = 移动数据 Mobile Data📲

|名称|Hostname最后部分<sup>1</sup>|AS号码|类型|
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
|JUCC 大學聯合電腦中心 (仅供大学使用)<sup>3</sup><br>||AS3662|B|

备注：
1. 通过`nslookup`命令查看🔍IP地址对应的域名Hostname而得出
2. 被IPinfo错误❌标为**Hosting**（甚至**VPN**）类型；我已联系过IPinfo📩，但由于它之前已通过**全网端口扫描**🔍等方式确认为机房和VPN类型的IP，因此我的申诉未通过（邮件回复提供了端口扫描的证据）；但流媒体解锁**没有受到影响**，还是全解锁✅
3. 包括每所大学（下游）的AS自治系统编号

根据我自己的研究和实验结论，部分香港的大学使用的不是JUCC（即大学自己的AS编号），而是HGC或HKBN Enterprise的宽带。

常见香港住宅IP的VPS提供商使用了HGC（有时还有HKT）宽带提供商的线路。

### 住宅IP提供商的性格

根据实验结论，一些住宅IP提供商有以下其中一个性格：

- 屏蔽所有**银行**的网站和APP（包括香港本地和全球其它银行）
- 屏蔽所有**已备案**的网站和APP（即使在境外有服务器）

<img width="400" alt="Screenshot 2025-04-26 at 8 23 12 AM" src="https://github.com/user-attachments/assets/2b711d91-c64a-4ae4-bc13-a4b7f5321e31" /><br>

### IP地址被Google标为内地问题

由于部分内地用户使用Google时开启了定位服务📍（即GPS），即使部分节点的IP地址在**境外**，这些IP仍已被Google标为内地。

在运行测试脚本时，就会看到Google和YouTube的地区已显示为CN（内地）。

<img width="750" alt="Screenshot 2025-05-05 at 1 36 43 PM" src="https://github.com/user-attachments/assets/e0febc8b-d2a7-4b0d-bfe7-1866ef77a02c" /><br>

我在全香港范围内的网络（包括移动数据📲、大学校园"eduroam" WiFi🏫和免费WiFi热点🛜）进行测试和实验时，**并没有出现过**该情况（概率为0%）❌。

如要将节点IP地址拉回🔙到香港地区，只需持续1-30天⏳做这些事情即可（每天只需做几次）：
1. 在全香港范围内（**物理位置**）连接🔌到该节点
2. 在你的设备和浏览器中启用定位服务、允许定位权限
3. 在Google上搜索🔍任意内容，或打开Google地图🧭
4. 划到底部，并上报/更新自己的GPS位置📍

根据我的实验结果，其中两个被Google标为内地的节点IP地址**已成功**拉回✅到港区。

更多信息请参考：[https://www.tjsky.net/tutorial/546](https://www.tjsky.net/tutorial/546)（仅供参考，不是我写的文章）

### 香港本地宽带测试实验结论

在全香港不同地方的网络热点（即上方⬆️所列明的宽带运营商ISP）测试后，所有测试均已通过（包括被IPinfo错误标为Hosting的IP地址），例如：
- IP质量测试脚本中：
  - IP Usage Type（IP用户类型）的表格基本上为🟢**绿色的**"**ISP**"或🔵**蓝色的**"**Business**"或"**Education**"✅ *
  - IP Privacy（IP隐私）的表格基本上为🟢**绿色的**"**N**"✅ *
  - IP Risk（IP风险值）的表格所有都为🟢**绿色**特别低的数值
- 流媒体测试脚本中：
  - 所有测试均显示🟢**绿色的**"**Y**"✅

\* 被IPinfo错误标为Hosting的运营商除外，但**只有**IPinfo这一行被标错

这种现象又称“**流媒体全解锁**”✅，也是很多用户希望看到、青睐的结果。

## 我的特殊性格

作为一名专注、有技术能力的学生，我的性格**跟超过99%的其他同学都不一样**💘。我在个人项目和由我自主领导的团队项目中，都想一直**按自己独特的想法完成**。

我目前存在自闭症(ASD)、阿斯伯格综合症😡等症状，**无法**接受其他人的意见。

尽管如此，欢迎在Issues提出自己的想法📩，但要尽量避免反驳我独特的想法、思维。

更多信息请浏览我的个人网站🌎：([https://ken.kenstudyjourney.cn](https://ken.kenstudyjourney.cn))。

感谢你的理解和支持。
