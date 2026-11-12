# 影视仓 · 短剧 / AI短剧 / AI漫剧 源清单

> 实测日期：2026-11-12　｜　所有地址均为**真实请求验证**，非转载网上合集
> 交付目录：`outputs/`

---

## 一、结论先说

市面上能直接用的短剧源，**99% 只有「真人短剧」，没有「AI漫剧」和「AI剧」**。
我实测了 20+ 个仓库地址，找到 **AI漫剧/AI剧专属源只有两处**：

| 位置 | 内容 | 说明 |
|---|---|---|
| **TVbox.org 官方仓** | 5 个漫剧源 + 4 个短剧源 | `api` 走 jar 内置 `csp_XXXGuard` 爬虫，无需装插件 |
| **drpys 红果果[短].js** | 8 个分类，含**漫剧(tab=19)**、**AI剧(tab=11)** | 自包含 JS，内置字节全套签名，可完整跑通 |

---

## 二、直接可用的仓库地址（已实测 200 + JSON 合法）

### ⭐ 首选：AI漫剧/AI剧

```
https://raw.githubusercontent.com/TVboxorg/TVbox/main/dist/official.json
```
160 站点，其中 **5 个漫剧专用**：

| 站点 | key | 对应平台 |
|---|---|---|
| 🍉漫短┃小红 | `ManJuAiHongGuo` | 红果 |
| 🍉漫剧┃小龙 | `ManJuAiHuoLong` | 火龙漫剧 |
| 🍉漫剧┃小猫 | `ManJuAiQiMao` | 企鹅 |
| 🍉漫短┃小喜 | `ManJuAiXiFan` | 番茄 |
| 🍉漫短┃小马 | `ManJuAiHeMa` | 河马 |

另有 4 个短剧源（好看/小猫/星星/小薇）+ 4 个动漫源。

### ⭐ 短剧专仓

| 名称 | 地址 | 实测 |
|---|---|---|
| 乐哥短剧专仓（39站） | `https://gh-proxy.com/https://raw.githubusercontent.com/lege0001/TVbox/main/TV/dj.json` | 200 / 40KB ✅ |
| 优飞短剧专仓（34站） | `http://box.ufuzi.com/tv/qq/%E7%9F%AD%E5%89%A7%E9%A2%91%E9%81%93/api.json` | 200 / 27KB ✅ |
| 小马短剧（62站） | `https://szyyds.cn/tv/x.json` | 200 / 30KB ✅ |
| 东篱影视（93站） | `https://raw.githubusercontent.com/chitue/dongliTV/main/api.json` | 200 / 55KB ✅ |
| 小盒子短剧专线 | `http://aiduanju.vip/` | 配置在官方仓内 |

### ❌ 实测已失效（别浪费时间）

| 地址 | 状态 |
|---|---|
| `http://74.120.175.78/JK/XYQTVBox/dj.json` | 连接失败 |
| `https://cnb.cool/fish2018/duanju/...` | 仓库被冻结 |
| `http://pandown.pro/tvbox/tvbox.json` | 连接失败 |
| `http://xhztv.top/tvbox.txt` | 404 |
| `https://ghproxy.net/.../yyfxz/qqtv/main/qq.json` | 404 |
| `https://tv.youdu.fan:666` | 连接失败 |
| `https://chuanshuo.77blog.cn/dc.json` | 连接失败 |
| `http://itvbox.cc/可视仓库` | 连接失败 |
| `https://gh-proxy.com/.../keluo8824-cell/tvbox/.../mao.json` 等6个 | 全部 404（仓库改名） |
| `https://gitoscc/maintv/main/x.json` | 返回非 JSON |
| `https://www.imwzh.com/tv.json` | 返回非 JSON |

---

## 三、红果官网直出（本次挖到的硬通货）

红果官网 `hongguoduanju.com` 的 SSR 数据里有**四个独立分类**，其中两个是别处没有的：

```
tab_type = all    → 热播短剧
tab_type = human  → 热播真人剧
tab_type = comic  → 热播漫剧     ★
tab_type = ai     → 热播AI剧     ★
```

抓取方式（`outputs/红果官网-分集解析器.py --categories` 已跑通）：
```
GET https://hongguoduanju.com/
→ HTML 内嵌 window._ROUTER_DATA (Astro SSR)
→ loaderData.page.homeSections[]
```

**免签名 MP4 直链**（最干净的播放源）：
```
GET https://hongguoduanju.com/player/{series_id}/{episode_id}
→ ld+json 的 contentUrl
→ https://hongguoduanju.com/video/public/{vid}/360p.mp4

实测: HTTP 200 / Content-Type: video/mp4 / Accept-Ranges: bytes
     免 x-gorgon 签名、免 CENC 解密
```

### ⚠️ 能力边界（必须知道）

- 详情页 SSR **只渲染前 5 集**。某剧 202 集，HTML 里只有 5 个 `TVEpisode`
- 第 2 集及以后，`<video src>` 是客户端注入，服务端 HTML 里没有 mp4 地址
- 全量分集依赖字节签名接口（`x-gorgon` / `x-ladon` / `x-helios` / `x-medusa`）

→ **完整分集播放必须用 `红果果-漫剧AI剧-JS源.js`**，该源已把这套签名算法全部实现（含 SM3、手写 protobuf、自研 AES 变体）。

---

## 四、交付文件

| 文件 | 说明 |
|---|---|
| `影视仓-短剧AI漫剧专用仓.json` | **主交付**。22 个站点整合成一个仓，含官方漫剧源/红果果JS源/4个短剧专仓。导入影视仓即可用 |
| `红果果-漫剧AI剧-JS源.js` | 自包含 JS 源，8 分类含漫剧+AI剧+4 热播榜，带全套字节签名 |
| `红果官网-短剧漫剧AI剧-榜单明细.json` | 红果三大分类各 9 条，共 36 条，含 series_id / 详情页链接 |
| `红果官网-分集解析器.py` | 命令行工具：列分类 / 解析分集 / 探测 MP4 可播性 |

### 怎么用

**影视仓（TV/手机端）**
1. 设置 → 配置地址 → 粘贴 `影视仓-短剧AI漫剧专用仓.json` 的**托管地址**
   （本地文件需先传到可公网访问的地址，或用下方的 GitHub 直链）
2. 或直接添加上面第二节的仓库地址
3. 刷新首页 → 进入「短剧」/「漫剧」分类

**红果果 JS 源接入**
影视仓需支持 `csp_Drpy2` 且 Node ≥ 18（否则 SM3 签名会失败）。
源码头部 `@header` 已声明 `lang: 'ds'`。

---

## 五、实测踩坑记录

1. **`;md5;` 后缀会 404**：官方仓 spider 地址带 `;md5;xxx`，直接 curl 会 404，
   去掉后缀才能取到文件（TVBox 客户端自己会处理）。见 `oss4liview.moji.com` 那条。
2. **GitHub 国内必须走代理**：`gh-proxy.com` 可用；`keluo8824-cell` 等仓库已改名，
   网上合集里的地址大面积 404。
3. **中文文件名 URL 编码**：`红果果[短].js` 的 `[]` 和中文都要 percent-encode。
4. **HTML 里提取 JSON 要做括号配对**：`_ROUTER_DATA` 里有转义引号，
   不能用 `split(';')` 或正则贪婪匹配，得做字符串感知的括号计数。
5. **详情页 JSON-LD 只 SSR 前 5 集** —— 这是最容易误判「解析成功」的点。

---

## 六、版权说明

所有线路均为对公开接口的聚合，仅供个人学习观看。
短剧/漫剧版权分别归属字节跳动（红果/番茄）、腾讯（火龙）、百度（七猫/柚漫剧）、阿里（书旗）等平台。
请勿用于商业用途或二次分发。
