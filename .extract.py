import re
import sys

FILES = [
    ("jina1.txt", "p/2037859250710521065", "内地致富证券开户教程2026"),
    ("j2.txt", "p/1943285844677984517", "众安银行（ZA Bank）开户流程极速版"),
    ("j4.txt", "p/1992233805193425359", "2026年1月盈立HK开户攻略及开户奖励"),
    (
        "col_2099895936084398296.md",
        "p/2099895936084398296",
        "内地居民手机开恒生香港账户",
    ),
    (
        "col_2030397653838713275.md",
        "p/2030397653838713275",
        "汇立银行卡绑定支付宝/微信全攻略",
    ),
    (
        "col_1913555428534650200.md",
        "p/1913555428534650200",
        "兴业寰宇卡无损转账香港汇丰全攻略",
    ),
    ("col_1923146974200312971.md", "p/1923146974200312971", "一文读懂跨境支付通"),
    (
        "col_2009603499395155739.md",
        "p/2009603499395155739",
        "汇立银行（WeLab Bank）开户流程全图文",
    ),
    ("col_1930645691513939756.md", "p/1930645691513939756", "2025港卡办理新规"),
    ("col_1929602965393642802.md", "p/1929602965393642802", "香港汇丰「蓝狮子」实测"),
    ("col_1962113370862887516.md", "p/1962113370862887516", "内地居民开通中银香港账户"),
    (
        "col_1962172303329727321.md",
        "p/1962172303329727321",
        "香港汇丰银行支持内地线上开户",
    ),
]

STOP = [
    "关于作者",
    "喜欢",
    "分享",
    "申请转载",
    "知乎",
    "登录",
    "扫码",
    "验证码",
    "评论",
    "赞同",
    "未登录用户",
    "大家在搜",
    "推荐阅读",
    "编辑于",
    "发布于",
    "相关搜索",
    "下载知乎App",
    "手机号",
    "区号",
    "极简发布",
]


def extract(fname):
    t = open(fname, encoding="utf-8").read()
    i = t.find("Markdown Content:")
    b = t[i + 17 :] if i >= 0 else t
    b = re.sub(r"\[!\[[^\]]*\]\([^)]*\)\]\([^)]*\)", "", b)
    b = re.sub(r"\[Image \d+\]\([^)]*\)", "", b)
    b = re.sub(r"!\[[^\]]*\]\([^)]*\)", "\n[图]\n", b)
    b = re.sub(r"\[([^]]*)\]\(javascript:[^)]*\)", r"\1", b)
    b = re.sub(r"\[([^]]*)\]\(https://zhida\.zhihu\.com/[^)]*\)", r"\1", b)
    b = re.sub(r"\[([^]]*)\]\((https?://[^)]*)\)", r"\1(\2)", b)
    lines = b.split("\n")
    out = []
    for ln in lines:
        s = ln.strip()
        if s.startswith("#"):
            out.append(ln)
            continue
        if any(s.startswith(k) or s == k for k in STOP):
            continue
        if re.match(r"^[\d]+\s*条评论", s):
            continue
        out.append(ln)
    b = "\n".join(out)
    b = re.sub(r"\n{3,}", "\n\n", b)
    return b


for fname, pid, title in FILES:
    if len(sys.argv) > 1 and sys.argv[1] not in fname:
        continue
    print("=" * 70)
    print("### %s  (%s)" % (title, pid))
    print("=" * 70)
    print(extract(fname))
    print()
