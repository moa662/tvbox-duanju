"""
红果官网 (hongguoduanju.com) 分集解析器 — 能力边界说明 + 实测可用部分

═══════════════════════════════════════════════════════════════════
实测结论（2026-11-12 真实请求，非推测）
═══════════════════════════════════════════════════════════════════

【可用部分】本脚本已端到端验证通过：

  1) 三大分类直出
     GET https://hongguoduanju.com/
     -> HTML 内嵌 window._ROUTER_DATA (Astro SSR)
     -> loaderData.page.homeSections[] 数组，每项含:
          tab_type: 'all' (热播短剧) / 'human' (热播真人剧)
                   'comic' (热播漫剧) / 'ai' (热播AI剧)
          tab_name: 中文分类名
          video_list[]: series_id / series_title / series_cover / episode_cnt
     ★ 这是普通影视仓短剧源普遍缺失的「漫剧」和「AI剧」两类

  2) 详情页首屏分集
     GET https://hongguoduanju.com/detail?series_id={id}
     -> HTML 内嵌 JSON-LD，含 episode[] 数组
     -> 每个分集: episodeNumber / name / url
     分集 URL 规则: https://hongguoduanju.com/player/{series_id}/{episode_id}

  3) 免签名 MP4 直链
     GET 分集URL -> HTML 内 ld+json 的 contentUrl
     格式: https://hongguoduanju.com/video/public/{vid}/360p.mp4
     实测响应: HTTP 200 / Content-Type: video/mp4 / Content-Length: 648281
               / Accept-Ranges: bytes  (支持拖动与断点续传)
     ★ 无需 x-gorgon 签名、无需 CENC 解密，是最干净的播放源

【能力边界】必须说明白，避免误用：

  · 详情页 SSR 只渲染前 5 集。某剧 202 集，HTML 里只出现 5 个 TVEpisode，
    其余分集由客户端调字节签名接口（bookapi / multi_video_detail，
    需 x-gorgon / x-ladon / x-helios / x-medusa 全套签名）懒加载。
  · 第 2 集及以后，播放页的 <video src> 为客户端注入，服务端 HTML 内
    不含 mp4 地址，同样依赖签名接口。
  => 因此：本脚本只保证「首屏 5 集 + 第1集免签名 MP4 直链」。
     完整分集播放请用《红果果-漫剧AI剧-JS源.js》，该源已内置字节全套
     签名算法（含 SM3 / 手写 protobuf / 自研 AES 变体），可完整跑通。

【用法】
    python 红果官网-分集解析器.py --categories           # 列四大分类榜单
    python 红果官网-分集解析器.py <series_id>            # 解析首屏分集
    python 红果官网-分集解析器.py <series_id> --probe    # 顺带探测MP4可播性
"""
import json
import re
import subprocess
import sys

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")
BS = chr(92)
HOME = "https://hongguoduanju.com/"


def get(url):
    try:
        r = subprocess.run(["curl", "-sL", "--max-time", "30", "-A", UA, url],
                           capture_output=True, timeout=45)
        return r.stdout.decode("utf-8", errors="ignore")
    except Exception:
        return ""


def _balanced_json(s):
    """从 '{' 开始做括号配对提取（正确处理字符串内的转义引号）"""
    depth, end, instr, esc = 0, -1, False, False
    for idx, ch in enumerate(s):
        if instr:
            if esc:
                esc = False
            elif ch == BS:
                esc = True
            elif ch == '"':
                instr = False
            continue
        if ch == '"':
            instr = True
            continue
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                end = idx
                break
    if end < 0:
        return None
    try:
        return json.loads(s[:end + 1])
    except Exception:
        return None


def categories():
    """返回红果官网四大分类（短剧/真人剧/漫剧/AI剧）"""
    html = get(HOME)
    i = html.find("_ROUTER_DATA = ")
    if i < 0:
        return []
    d = _balanced_json(html[i + len("_ROUTER_DATA = "):])
    if not d:
        return []
    out = []
    for sec in d.get("loaderData", {}).get("page", {}).get("homeSections", []):
        out.append({
            "tab_type": sec.get("tab_type"),
            "tab_name": sec.get("tab_name"),
            "video_list": [{
                "series_id": v.get("series_id"),
                "series_title": v.get("series_title"),
                "episode_cnt": v.get("episode_cnt"),
                "series_cover": v.get("series_cover"),
            } for v in sec.get("video_list", [])],
        })
    return out


def episodes(series_id):
    """返回首屏已渲染的分集 [{ep_no, name, player_url}]"""
    html = get("https://hongguoduanju.com/detail?series_id=%s" % series_id)
    i = html.find('"episode":[')
    if i < 0:
        return []
    seg = html[i:]
    out = []
    for m in re.finditer(r'\{"@type":"TVEpisode".*?\}', seg, re.S):
        blob = m.group(0)
        num = re.search(r'"episodeNumber":(\d+)', blob)
        nm = re.search(r'"name":"(.*?)"', blob)
        url = re.search(r'"url":"(https://hongguoduanju\.com/player/[^"]+)"', blob)
        if num and url:
            out.append({
                "ep_no": int(num.group(1)),
                "name": nm.group(1) if nm else "第%s集" % num.group(1),
                "player_url": url.group(1).replace("\\/", "/"),
            })
    return out


def mp4_of(player_url):
    """从播放页解析免签名 MP4 直链"""
    html = get(player_url)
    m = re.search(r'"contentUrl":"(https://[^"]+\.mp4)"', html)
    if m:
        return m.group(1).replace("\\/", "/")
    m = re.search(r'/video/public/\d+/\d+p\.mp4', html)
    if m:
        return "https://hongguoduanju.com" + m.group(0)
    return None


def probe(url):
    try:
        r = subprocess.run(["curl", "-sIL", "--max-time", "25", "-A", UA, url],
                           capture_output=True, timeout=40)
        return [l.strip() for l in r.stdout.decode("utf-8", "ignore").splitlines()
                if re.match(r"(?i)(HTTP/|content-type|content-length|accept-ranges)", l)]
    except Exception:
        return []


if __name__ == "__main__":
    args = sys.argv[1:]

    if not args:
        print(__doc__)
        raise SystemExit(0)

    if args[0] == "--categories":
        cats = categories()
        print("红果官网四大分类（%s）\n" % HOME)
        for c in cats:
            print("【%s】tab_type=%s  条目=%d" % (c["tab_name"], c["tab_type"], len(c["video_list"])))
            for v in c["video_list"]:
                print("    %-32s %4s集   series_id=%s" %
                      (v["series_title"], v["episode_cnt"], v["series_id"]))
            print()
        raise SystemExit(0)

    sid = args[0]
    eps = episodes(sid)
    print("剧集ID:", sid, "| 首屏分集数:", len(eps), "(注: 完整分集需用 JS 源)")
    for e in eps:
        print("  第%-4d集  %s" % (e["ep_no"], e["name"]))
    if eps:
        mp4 = mp4_of(eps[0]["player_url"])
        print("\n第1集 MP4 直链:", mp4)
        if "--probe" in args and mp4:
            for line in probe(mp4):
                print("   ", line)
