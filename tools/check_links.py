#!/usr/bin/env python3
"""校验仓库内 Markdown 内部链接与锚点。

用法：
    python tools/check_links.py

退出码：0 = 全部通过，1 = 存在失效链接。
"""

import os
import re
import sys
import urllib.parse

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# 显式 HTML 锚点
EXPLICIT = re.compile(r'<a id="([^"]+)"></a>')
# 标题派生的兜底 slug（近似 GitHub 规则）
HEADING = re.compile(r"^#{1,6}\s+(.*)$", re.M)


def slug(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[`*_]", "", text)
    text = re.sub(r"[^\w\u4e00-\u9fff\- ]", "", text)
    return text.replace(" ", "-")


def ids_of(path: str, cache: dict) -> set:
    if path not in cache:
        text = open(path, encoding="utf-8").read()
        found = set(EXPLICIT.findall(text))
        found |= {slug(m) for m in HEADING.findall(text)}
        cache[path] = found
    return cache[path]


def main() -> int:
    cache: dict = {}
    problems: list = []
    checked = 0

    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d != ".git"]
        for name in filenames:
            if not name.endswith(".md"):
                continue
            path = os.path.join(dirpath, name)
            text = open(path, encoding="utf-8").read()
            for m in re.finditer(r"\[[^\]]*\]\(([^)\s]+)\)", text):
                link = m.group(1)
                if link.startswith(("http://", "https://", "mailto:")):
                    continue
                checked += 1
                target, _, fragment = link.partition("#")
                if target:
                    resolved = os.path.normpath(
                        os.path.join(dirpath, urllib.parse.unquote(target))
                    )
                    if not os.path.exists(resolved):
                        problems.append(
                            (os.path.relpath(path, ROOT), link, "文件不存在")
                        )
                        continue
                else:
                    resolved = path
                if fragment:
                    if urllib.parse.unquote(fragment) not in ids_of(resolved, cache):
                        problems.append(
                            (os.path.relpath(path, ROOT), link, "锚点不存在")
                        )

    print("内部链接检查：%d 条" % checked)
    if problems:
        print("失效链接：%d 条" % len(problems))
        for where, link, reason in problems:
            print("  %s | %s | %s" % (where, link, reason))
        return 1
    print("全部通过 ✅")
    return 0


if __name__ == "__main__":
    sys.exit(main())
