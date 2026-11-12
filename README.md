# 影视仓 · 影视 / 短剧 / AI短剧 / AI漫剧 综合仓

> 实测日期：2026-11-12　｜　所有站点后端与 jar 类均**逐条验证**，非转载网上合集

---

## ⚡ 一键订阅地址

```
https://raw.githubusercontent.com/moa662/tvbox-duanju/master/tvbox-duanju.json
```

国内网络慢的话换这两个（均实测 200）：

```
https://cdn.jsdelivr.net/gh/moa662/tvbox-duanju@master/tvbox-duanju.json
https://gh-proxy.com/https://raw.githubusercontent.com/moa662/tvbox-duanju/master/tvbox-duanju.json
```

**影视仓 → 设置 → 配置地址 → 粘贴 → 刷新首页。**

---

## 一、v1 卡在「已搜索站点 稍等片刻」的根因（已修复）

这不是网络问题，是 **jar 和 api 对不上**。

影视仓加载站点时，会去 `jar` 里找 `api` 指定的类。找不到 → 站点永远转圈。

v1 犯的错：给所有短剧源写 `api: csp_XBPQ`，却挂了**官方 Guard jar**，
而那个 jar 里只有 `ManJuAi*Guard` / `DuanJuAi*Guard` 这类加密原生库的类，
**根本没有 XBPQ 爬虫类**。

实测两个 jar 的类分布（解析 `classes.dex` 得到）：

| jar | 大小 | 含什么 | 不含什么 |
|---|---|---|---|
| `xyq-spider.jar`（官方） | 1.0MB | `ManJuAi*Guard` `DuanJuAi*Guard` | **无 XBPQ** |
| `xyqxbpq.jar`（乐哥） | 636KB | `XBPQ` `Czsapp` `Duanju` | **无任何 Guard** |
| `yoursmile.jar`（小盒子） | 910KB | `Jianpian` `SixV` `Kkys` `Ddrk` `Auete` `Libvio` | — |

**v4 已逐站点校验：32 个站点中 31 个的 jar 确实包含其 api 类**（`csp_Drpy2` 除外，已标注为可选）。

另外修掉两个隐藏坑：

- **key 重名**：v1 用 `re.sub(r"[^A-Za-z0-9]","_", 站名)` 生成 key，中文被吃光，
  3 个站点都变成 `FILM_____` → TVBox 只保留一个，其余永远加载不出来。
  现在 key 全 ASCII 且唯一。
- **整仓 vs 按源**：直接引用别人的仓作为站点，`ext` 里的 api 与自己的 jar 对不上。
  现在按「源」拆开引用，每个源带自己的 api + 匹配的 jar。

---

## 二、分类归并方案（解决「分类太碎」）

原来 18 个短剧站各带 5–20 个自带分类（动作片/喜剧片/韩剧/美剧/纪录片/伦理片/竖屏剧…），
叠加后是上百个重复入口。

现在统一归并到 **6 个顶层分类**：

| 顶层分类 | 吸收的细分分类 |
|---|---|
| **电影** | 动作片 喜剧片 爱情片 科幻片 恐怖片 剧情片 战争片 纪录片 伦理片 体育 |
| **剧集** | 电视剧 美剧 韩剧 日剧 泰剧 国产剧 香港剧 韩国剧 欧美剧 台湾剧 日本剧 |
| **综艺** | 综艺 |
| **动漫** | 动漫 动画片 国漫 日漫 番剧 漫画 |
| **短剧** | 短剧 漫短 竖屏剧 |
| **AI漫剧** | 漫剧 AI剧 AI短剧 动态漫 |

短剧 / AI漫剧 / 动漫为**独立源独立分类**，不会和影视混排。

---

## 三、站点清单（32 个）

### 🎬 影视 15 个
| 站点 | 机制 | 备注 |
|---|---|---|
| 水晶影视 / 2水晶影视 | XBPQ 内联 | 分类页实测 99 条 |
| 泡沫 | XBPQ 内联 | |
| 速影影视 | XBPQ 内联 | |
| 云飞影视 | XBPQ 内联 | 30 条 |
| 韩片影视 | XBPQ 内联 | 102 条，**已验证列表→详情→播放页全通** |
| 看了么 | XBPQ 内联 | 42 条 |
| 55影院 | XBPQ 内联 | 112 条，**已验证全链路含 m3u8** |
| 厂长 | 原生爬虫 `csp_Czsapp` | czzy55.com |
| 荐片 | 原生爬虫 `csp_Jianpian` | api2.rinhome.com |
| 新6V | 原生爬虫 `csp_SixV` | xb6v.com |
| 酷看 | 原生爬虫 `csp_Kkys` | kkys.com |
| 低端 | 原生爬虫 `csp_Ddrk` | ddrk1.com |
| 奥特 | 原生爬虫 `csp_Auete` | auete.com |
| LibVio影视 | 原生爬虫 `csp_Libvio` | libvio.link |

### 🤖 AI漫剧 5 个（官方 Guard 源）
漫短┃小红（红果）· 漫剧┃小龙（火龙）· 漫剧┃小猫（企鹅）· 漫短┃小喜（番茄）· 漫短┃小马（河马）

### 🎭 短剧 6 个
盒马短剧 · 聚合短剧 · 星芽短剧 · 乐哥短剧专仓(39站) · 优飞短剧专仓(34站) · 小马短剧(62站)

### 🎞 动漫 5 个
AGE动漫 · 方舟动漫 · 曼波动漫 · 咕咕动漫 · 巴士动漫

### ⚙️ 可选 1 个
红果果 JS 源 —— **唯一覆盖 AI剧(tab=11) 完整分类 + 4 个热播榜**，
但需客户端支持 drpy2 引擎（标准影视仓不支持，需影视仓v3/drpyS）。加载失败就用上面 5 个官方源。

---

## 四、仓内文件

| 文件 | 说明 |
|---|---|
| `tvbox-duanju.json` | **主仓配置**，32 站点 |
| `jar/xyq-spider.jar` | 官方 Guard jar（AI漫剧源用） |
| `jar/xyqxbpq.jar` | 乐哥 XBPQ jar（影视/短剧 XBPQ 源用） |
| `jar/yoursmile.jar` | 小盒子 jar（原生爬虫影视源用） |
| `jar/ufuzi-spider.jar` | 优飞短剧仓 jar |
| `jar/dongli-spider.jar` | 东篱仓 jar（盒马/聚合短剧/动漫源用） |
| `jar/xiaoma.jpg` | 小马仓 jar（md5 已校验 `4ce29ce2…`） |
| `src/hongguo-manju-ai.js` | 红果果 JS 源（drpy2 环境） |
| `hongguo-rank.json` | 红果官网四分类榜单 36 条 |
| `src/红果官网-分集解析器.py` | 命令行工具 |

---

## 五、红果官网直出（本次挖到的硬通货）

`hongguoduanju.com` 的 SSR 数据里有**四个独立分类**，其中两个别处没有：

```
tab_type = all    → 热播短剧
tab_type = human  → 热播真人剧
tab_type = comic  → 热播漫剧     ★
tab_type = ai     → 热播AI剧     ★
```

**免签名 MP4 直链**（最干净的播放源）：
```
GET https://hongguoduanju.com/player/{series_id}/{episode_id}
→ ld+json 的 contentUrl
→ https://hongguoduanju.com/video/public/{vid}/360p.mp4

实测: HTTP 200 / video/mp4 / Accept-Ranges: bytes
     免 x-gorgon 签名、免 CENC 解密
```

⚠️ **能力边界**：详情页 SSR **只渲染前 5 集**（某剧 202 集，HTML 里只有 5 个 episode），
第 2 集以后是客户端注入。全量分集依赖字节签名（x-gorgon/x-ladon/x-helios/x-medusa），
需 `红果果 JS 源` 才能完整跑通。

---

## 六、实测踩坑记录

1. **jar 与 api 必须严格对应**（见第一节）—— 这是「稍等片刻」的根因。
2. **Windows 下 `curl -o /dev/null` 会退出码 23**，导致 size 永远取 0，
   会把活着的站误判成死的。必须用真实临时文件路径。
3. **`git add repo/` 会把目录前缀带进索引**，导致仓库根目录空、raw 全部 404。
   解决：直接在内容目录 `git init` 推独立仓库。
4. **默认分支是 `master` 不是 `main`**，配置里写 `main` 直接 404。
5. **中文文件名 URL 需 percent-encode**，TVBox 端兼容性不稳 → 统一用 ASCII 别名。
6. **`\b` 不能用于 class 匹配**：`stui-vodlist__thumb` 里 thumb 前是下划线，
   `\b` 不成立，会导致整块匹配失败。
7. **HTML 内嵌 JSON 要做字符串感知的括号配对**（有转义引号），不能 `split(';')`。

---

## 七、版权说明

所有线路均为对公开接口的聚合，仅供个人学习观看。
短剧/漫剧版权分别归属字节跳动（红果/番茄）、腾讯（火龙）、百度（七猫/柚漫剧）、阿里（书旗）等平台。
请勿用于商业用途或二次分发。
