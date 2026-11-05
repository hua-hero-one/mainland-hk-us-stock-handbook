#!/usr/bin/env python3
"""下载知乎原文配图到 docs/guides/assets/，并输出每张图在原文中的位置上下文。"""

import os
import re
import sys
import urllib.request

TMP = os.path.join(os.path.dirname(os.path.abspath(__file__)), "zhimg")
OUT = os.path.abspath(
    os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", "docs", "guides", "assets"
    )
)

FILES = [
    ("jina1.txt", "01-broker-chief", "致富证券"),
    ("j2.txt", "06-bank-virtual-zabank", "ZA Bank"),
    ("j4.txt", "02-broker-phillip", "盈立"),
    ("col_2099895936084398296.md", "05-bank-hang-seng", "恒生"),
    ("col_2030397653838713275.md", "07b-welab-bind", "WeLab 绑卡"),
    ("col_1913555428534650200.md", "08-transfer-swift", "兴业电汇"),
    ("col_1923146974200312971.md", "09-crossborder-payment", "跨境支付通"),
    ("col_2009603499395155739.md", "07-bank-virtual-welab", "WeLab 开户"),
    ("col_1930645691513939756.md", "11-rules-2026", "港卡新规"),
    ("col_1929602965393642802.md", "10-card-blue-lion", "蓝狮子"),
    ("col_1962113370862887516.md", "04-bank-bochk", "中银香港"),
    ("col_1962172303329727321.md", "03-bank-hsbc", "汇丰"),
]

UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
)
HDRS = {"User-Agent": UA, "Referer": "https://zhuanlan.zhihu.com/"}

os.makedirs(TMP, exist_ok=True)

manifest = []
for fname, slug, label in FILES:
    path = os.path.join(TMP, fname)
    if not os.path.exists(path):
        print("MISSING SOURCE", fname)
        continue
    text = open(path, encoding="utf-8").read()
    lines = text.split("\n")
    idx = 0
    for i, line in enumerate(lines):
        urls = re.findall(
            r"!\[[^\]]*\]\((https://pic[0-9]\.zhimg\.com/[^)\s]+)\)", line
        )
        for u in urls:
            ctx = ""
            for j in range(i - 1, -1, -1):
                s = lines[j].strip()
                if s and not s.startswith("!") and "Image" not in s[:8]:
                    ctx = re.sub(r"\[[^\]]*\]\([^)]*\)", "", s)
                    ctx = re.sub(r"\*\*|\*|`", "", ctx)[:90]
                    break
            idx += 1
            ext = ".png" if ".png" in u.split("?")[0] else ".jpg"
            name = "%s-%02d%s" % (slug, idx, ext)
            manifest.append((slug, label, name, u, ctx))

os.makedirs(OUT, exist_ok=True)
for slug, label, name, url, ctx in manifest:
    dest = os.path.join(OUT, slug, name)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    if os.path.exists(dest) and os.path.getsize(dest) > 1000:
        print("skip", name)
        continue
    try:
        req = urllib.request.Request(url, headers=HDRS)
        with urllib.request.urlopen(req, timeout=45) as r:
            data = r.read()
        open(dest, "wb").write(data)
        print("OK  %-34s %7d bytes  ctx=%s" % (name, len(data), ctx[:50]))
    except Exception as e:
        print("ERR %-34s %s" % (name, e))

with open(os.path.join(OUT, "manifest.tsv"), "w", encoding="utf-8") as f:
    for slug, label, name, url, ctx in manifest:
        f.write("%s\t%s\t%s\t%s\t%s\n" % (slug, label, name, url, ctx))
print("\nmanifest written:", os.path.join(OUT, "manifest.tsv"))
