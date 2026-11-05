#!/usr/bin/env python3
"""把下载好的原文配图插回对应攻略的合适位置。

用法：python tools/insert_images.py
"""

import os
import re

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
GUIDES = os.path.join(ROOT, "docs", "guides")

A = "assets"


def img(name, caption):
    return "![%s](%s)\n\n*%s*" % (caption, "%s/%s" % (A, name), caption)


def gallery(names, captions, summary):
    """折叠的多图块"""
    out = ["<details>", "<summary>📸 %s</summary>" % summary, ""]
    for n, c in zip(names, captions):
        out.append("![%s](%s/%s)" % (c, A, n))
        out.append("")
        out.append("*%s*" % c)
        out.append("")
    out.append("</details>")
    return "\n".join(out)


# (guide file, anchor substring, images to insert after that line)
PLACEMENTS = [
    # ---------- 01 致富证券 ----------
    (
        "01-broker-chief.md",
        "- ⚠️ **这一步的银行卡用于身份认证，不是后续实际入金的卡**。填你本人的常用卡即可。",
        [img("01-broker-chief/01-broker-chief-01.jpg", "致富证券：内地银行卡认证页")],
    ),
    (
        "01-broker-chief.md",
        "- **税务编号（TIN）**：内地居民用**身份证号**",
        [
            img(
                "01-broker-chief/01-broker-chief-02.jpg",
                "致富证券：职业信息与税务资料填写",
            )
        ],
    ),
    # ---------- 02 盈立证券 ----------
    (
        "02-broker-phillip.md",
        "目前能开的还有盈立，内地身份证可以直接申请的券商之一了，后续还有其他不需要地址证明能开的券商也会更新给大家。",
        [
            img(
                "02-broker-phillip/02-broker-phillip-01.jpg",
                "盈立：内地身份证开户入口（原文截图）",
            )
        ],
    ),
    (
        "02-broker-phillip.md",
        "- **注意 App 来源**：只从官网或官方应用商店下载，不要装第三方改版包",
        [
            img(
                "02-broker-phillip/02-broker-phillip-02.jpg", "盈立：App 内「开户」入口"
            ),
            img(
                "02-broker-phillip/02-broker-phillip-03.jpg",
                "盈立：选择「内地身份证开户」",
            ),
            img("02-broker-phillip/02-broker-phillip-04.jpg", "盈立：开户方式选择"),
        ],
    ),
    (
        "02-broker-phillip.md",
        "- **受雇信息如实填写**",
        [
            img("02-broker-phillip/02-broker-phillip-05.jpg", "盈立：上传身份信息"),
            img("02-broker-phillip/02-broker-phillip-06.jpg", "盈立：受雇信息填写"),
        ],
    ),
    (
        "02-broker-phillip.md",
        "- 环境光线充足、不遮挡面部",
        [
            img(
                "02-broker-phillip/02-broker-phillip-07.jpg",
                "盈立：实名认证（人脸识别）",
            )
        ],
    ),
    (
        "02-broker-phillip.md",
        "- 提交后等待审核结果通知",
        [
            img("02-broker-phillip/02-broker-phillip-08.jpg", "盈立：签名提交"),
            img("02-broker-phillip/02-broker-phillip-09.jpg", "盈立：开户完成"),
        ],
    ),
    # ---------- 03 汇丰 ----------
    (
        "03-bank-hsbc.md",
        "- ⚠️ **需在入境当天操作**，确保记录时间与申请日期一致",
        [
            gallery(
                [
                    "03-bank-hsbc/03-bank-hsbc-01.jpg",
                    "03-bank-hsbc/03-bank-hsbc-02.jpg",
                    "03-bank-hsbc/03-bank-hsbc-03.jpg",
                ],
                [
                    "汇丰：移民局 12367 查询出入境记录",
                    "汇丰：下载带红章的 PDF",
                    "汇丰：出入境记录 PDF 示例",
                ],
                "原文截图：出入境记录 PDF 的获取（3 张）",
            )
        ],
    ),
    (
        "03-bank-hsbc.md",
        '| **收入申报** | **按实际情况填写** | ⚠️ 不建议照抄"填中间值"的做法 |',
        [
            gallery(
                ["03-bank-hsbc/03-bank-hsbc-%02d.jpg" % i for i in range(4, 15)],
                ["汇丰开户 %d/11" % i for i in range(4, 15)],
                "原文截图：开户申请全流程（11 张）",
            )
        ],
    ),
    # ---------- 04 中银香港 ----------
    (
        "04-bank-bochk.md",
        "- 收到**加密的 PDF**——这个文件就是银行认可的有效证明",
        [
            img("04-bank-bochk/04-bank-bochk-01.jpg", "中银香港：移民局 12367 查询"),
            img("04-bank-bochk/04-bank-bochk-02.jpg", "中银香港：发送至邮箱的加密 PDF"),
        ],
    ),
    (
        "04-bank-bochk.md",
        "- 打开后点击首页显著的「**开立账户**」按钮",
        [img("04-bank-bochk/04-bank-bochk-03.jpg", "中银香港：App 首页「开立账户」")],
    ),
    (
        "04-bank-bochk.md",
        "| 账户类型 | 建议「**自在理财**」 | 需维持 1 万港币综合理财总值，但**开户过程中无需立即存入** |",
        [img("04-bank-bochk/04-bank-bochk-04.jpg", "中银香港：账户类型选择")],
    ),
    (
        "04-bank-bochk.md",
        '- **位置权限**：App 请求时**必须选择"允许"**，用于验证身处香港',
        [
            gallery(
                [
                    "04-bank-bochk/04-bank-bochk-05.jpg",
                    "04-bank-bochk/04-bank-bochk-06.jpg",
                    "04-bank-bochk/04-bank-bochk-07.jpg",
                    "04-bank-bochk/04-bank-bochk-08.jpg",
                ],
                [
                    "中银香港：上传出入境记录",
                    "中银香港：上传身份证与通行证",
                    "中银香港：人脸识别",
                    "中银香港：填写个人资料",
                ],
                "原文截图：材料上传与验证（4 张）",
            )
        ],
    ),
    # ---------- 05 恒生 ----------
    (
        "05-bank-hang-seng.md",
        "- 约 **2–3 个工作日**后转账 / FPS / 投资功能全开",
        [
            img(
                "05-bank-hang-seng/05-bank-hang-seng-01.jpg",
                "恒生：网银注册完成与功能开通",
            )
        ],
    ),
    # ---------- 06 ZA Bank ----------
    (
        "06-bank-virtual-zabank.md",
        "- **输入内地手机号** → 接收短信验证码",
        [
            img(
                "06-bank-virtual-zabank/06-bank-virtual-zabank-01.jpg",
                "ZA Bank：立即开户 → 身份证 → 手机号验证",
            )
        ],
    ),
    (
        "06-bank-virtual-zabank.md",
        "| 职业与开户目的 | 「储蓄」或「个人财务」即可 |",
        [
            img(
                "06-bank-virtual-zabank/06-bank-virtual-zabank-02.jpg",
                "ZA Bank：个人资料与税务信息填写",
            )
        ],
    ),
    # ---------- 07 WeLab ----------
    (
        "07-bank-virtual-welab.md",
        "从手机文件中选择提前下载的 **PDF** 上传",
        [
            img(
                "07-bank-virtual-welab/07-bank-virtual-welab-01.jpg",
                "WeLab：上传出入境记录 PDF",
            )
        ],
    ),
    (
        "07-bank-virtual-welab.md",
        "- 完善职业信息与开户目的（原文建议选「**投资**」）",
        [
            gallery(
                [
                    "07-bank-virtual-welab/07-bank-virtual-welab-02.jpg",
                    "07-bank-virtual-welab/07-bank-virtual-welab-03.jpg",
                    "07-bank-virtual-welab/07-bank-virtual-welab-04.jpg",
                ],
                [
                    "WeLab：设置账户信息",
                    "WeLab：填写居住地址",
                    "WeLab：职业信息与开户目的",
                ],
                "原文截图：账户信息填写（3 张）",
            )
        ],
    ),
    (
        "07-bank-virtual-welab.md",
        "推荐码栏输入原文的 `FPNJ3F`（可自行决定是否使用）",
        [
            img(
                "07-bank-virtual-welab/07-bank-virtual-welab-05.jpg",
                "WeLab：推荐码填写",
            )
        ],
    ),
    (
        "07-bank-virtual-welab.md",
        "只需完成简单的风险评估问卷即可。",
        [
            gallery(
                [
                    "07-bank-virtual-welab/07-bank-virtual-welab-06.jpg",
                    "07-bank-virtual-welab/07-bank-virtual-welab-07.jpg",
                ],
                ["WeLab：开通投资账户入口", "WeLab：风险评估问卷"],
                "原文截图：开通投资账户（2 张）",
            )
        ],
    ),
    # ---------- 08 兴业电汇 ----------
    (
        "08-transfer-swift.md",
        "- ⚠️ **务必选「现汇」**——**现钞无法转账**",
        [
            gallery(
                [
                    "08-transfer-swift/08-transfer-swift-01.jpg",
                    "08-transfer-swift/08-transfer-swift-02.jpg",
                    "08-transfer-swift/08-transfer-swift-03.jpg",
                ],
                [
                    "兴业：进入「结售汇」",
                    "兴业：选择币种与金额",
                    "兴业：确认购汇与汇率优惠",
                ],
                "原文截图：购汇流程（3 张）",
            )
        ],
    ),
    (
        "08-transfer-swift.md",
        "| **代理行代码** | 同样填 `HSBCHKHHHKH` | 避免中转行扣费 |",
        [
            gallery(
                [
                    "08-transfer-swift/08-transfer-swift-04.jpg",
                    "08-transfer-swift/08-transfer-swift-05.jpg",
                    "08-transfer-swift/08-transfer-swift-06.jpg",
                ],
                ["兴业：跨境汇款信息填写", "兴业：手续费显示为 0", "兴业：电子回单"],
                "原文截图：跨境汇款填写（3 张）",
            )
        ],
    ),
    # ---------- 09 跨境支付通 ----------
    (
        "09-crossborder-payment.md",
        "- 搜索「**跨境支付通**」进入功能页",
        [
            img(
                "09-crossborder-payment/09-crossborder-payment-01.jpg",
                "跨境支付通：手机银行功能入口",
            )
        ],
    ),
    (
        "09-crossborder-payment.md",
        "- 用途按实际选择（南向为消费/旅游/生活费类）",
        [
            img(
                "09-crossborder-payment/09-crossborder-payment-02.jpg",
                "跨境支付通：金额、汇率与用途",
            )
        ],
    ),
    (
        "09-crossborder-payment.md",
        "- 确认后**资金秒到账**，可截图通知收款人",
        [
            img(
                "09-crossborder-payment/09-crossborder-payment-03.jpg",
                "跨境支付通：提交成功",
            )
        ],
    ),
    (
        "09-crossborder-payment.md",
        "> 💡 **北向操作差异**：通过香港银行 APP（中银香港、汇丰香港等）进入「跨境支付通至内地」界面，流程类似但**支持 24 小时汇款**。",
        [
            gallery(
                [
                    "09-crossborder-payment/09-crossborder-payment-04.jpg",
                    "09-crossborder-payment/09-crossborder-payment-05.jpg",
                ],
                ["跨境支付通：香港端「至内地」入口", "跨境支付通：北向转账界面"],
                "原文截图：北向（香港→内地）（2 张）",
            )
        ],
    ),
    # ---------- 10 蓝狮子 ----------
    (
        "10-card-blue-lion.md",
        "- **防丢操作**：申卡后立刻联系本地邮政所，报姓名 + 电话要求备注（原文称亲测有效）",
        [
            gallery(
                [
                    "10-card-blue-lion/10-card-blue-lion-01.jpg",
                    "10-card-blue-lion/10-card-blue-lion-02.jpg",
                    "10-card-blue-lion/10-card-blue-lion-03.jpg",
                    "10-card-blue-lion/10-card-blue-lion-04.jpg",
                ],
                [
                    "蓝狮子：申卡入口",
                    "蓝狮子：借记卡选择与填写",
                    "蓝狮子：地址与住宅地址设置",
                    "蓝狮子：实体卡寄送",
                ],
                "原文截图：申卡流程（4 张）",
            )
        ],
    ),
    # ---------- 11 港卡新规 ----------
    (
        "11-rules-2026.md",
        "> - 中银香港线上开户日限 1 万港币，**4 天后**升级至 20 万/天",
        [
            img(
                "11-rules-2026/11-rules-2026-01.jpg",
                "汇丰/中银香港开户要点（原文截图）",
            )
        ],
    ),
    (
        "11-rules-2026.md",
        "| **众安银行（ZA Bank）** | **5 分钟下户**：身份证 + 内地手机号，人在香港即可 App 操作；0 管理费；活期利率活动可冲 7% | [06](06-bank-virtual-zabank.md) |",
        [img("11-rules-2026/11-rules-2026-02.jpg", "虚拟银行对比（原文截图）")],
    ),
]

# 追加到 07 的 WeLab 绑卡附录
WELAB_BIND = """

---

## 六、附：把汇立借记卡绑到内地支付宝 / 微信

> 来源：知乎专栏 `c_1967646104905581431`《汇立银行卡（WeLab Bank）绑定支付宝/微信全攻略|图文版》

### 绑定前准备

1. **下载内地版**支付宝 / 微信（**不是** AlipayHK / WeChat Pay HK）
2. **获取卡片信息**：汇立 APP →「银行卡」→「卡资料」→ 记下**卡号、有效期、安全码**
3. **确保实名认证**：支付宝 / 微信需完成实名认证才能绑卡

### 支付宝绑定

```
支付宝 → 我的 → 银行卡 → 右上角「+」→ 输入卡号
      → 填写有效期与安全码 → 同意协议并添加 → 输入短信验证码
```

### 微信支付绑定

```
微信 → 我 → 服务 → 钱包 → 银行卡 → 添加银行卡
    → 输入支付密码验证身份 → 输入卡号
    → 填写卡片信息 → 下一步 → 输入短信验证码
"""

WELAB_BIND_IMAGES = [
    gallery(
        [
            "07b-welab-bind/07b-welab-bind-01.jpg",
            "07b-welab-bind/07b-welab-bind-02.jpg",
        ],
        ["WeLab：支付宝绑卡 - 添加银行卡", "WeLab：支付宝绑卡 - 填写卡片信息"],
        "原文截图：支付宝绑定（2 张）",
    ),
    gallery(
        [
            "07b-welab-bind/07b-welab-bind-03.jpg",
            "07b-welab-bind/07b-welab-bind-04.jpg",
            "07b-welab-bind/07b-welab-bind-05.jpg",
        ],
        [
            "WeLab：微信绑卡 - 银行卡入口",
            "WeLab：微信绑卡 - 输入卡号",
            "WeLab：微信绑卡 - 短信验证",
        ],
        "原文截图：微信绑定（3 张）",
    ),
]

WELAB_BIND_NOTES = """

### 绑定后的优势

| 优势 | 说明 |
| --- | --- |
| **人民币直接扣款** | 避免港币结算的汇率损失 |
| **0 外币兑换手续费** | 汇立提供人民币 $0 外币兑换及交易手续费 |
| **最低汇率保证** | 汇立提供有竞争力的低汇率 |
| **消费现金回赠** | 绑定后消费另有回赠 |

### ⚠️ 注意事项

| 项 | 说明 |
| --- | --- |
| **支付限额** | 境外卡单笔限额 6,000 元，月累计 5 万，年累计 6 万 |
| **手续费** | 单笔 ≤ 200 元免手续费，> 200 元收 3% 手续费 |
| **优先付款** | 绑卡后记得在支付设置中设为优先付款方式 |

### 💡 小贴士

1. **汇率锁定**：提前在汇立 APP 兑换人民币，锁好汇率再消费
2. **双钱包策略**：保留港版钱包用于本地消费，内地钱包专门用于跨境支付
3. **定期检查**：每月检查绑定状态与交易记录

> ⚠️ **用途边界**：绑卡做**个人消费**没问题；🚫 但**不要用他人卡替别人过账、换汇**，那实质上是个人换汇/地下钱仓，见 [08 外汇管理红线](../08-tax-compliance.md#5-外汇管理红线)。
"""


def main():
    for fname, anchor, blocks in PLACEMENTS:
        path = os.path.join(GUIDES, fname)
        text = open(path, encoding="utf-8").read()
        if anchor not in text:
            print("!! ANCHOR NOT FOUND  %s  <<%s>>" % (fname, anchor[:40]))
            continue
        insert = "\n\n" + "\n\n".join(blocks) + "\n"
        # 只替换第一次出现
        text = text.replace(anchor, anchor + insert, 1)
        open(path, "w", encoding="utf-8").write(text)
        print("OK  %-34s +%d block(s)" % (fname, len(blocks)))

    # WeLab 绑卡附录
    path = os.path.join(GUIDES, "07-bank-virtual-welab.md")
    text = open(path, encoding="utf-8").read()
    marker = "## 六、风险与合规提示"
    if marker in text:
        text = text.replace(marker, "## 六、风险与合规提示", 1)
    extra = WELAB_BIND.replace("## 六、附：", "## 七、附：")
    extra = extra.replace("WELAB_BIND_IMAGES", "")
    imgs = "\n\n".join(WELAB_BIND_IMAGES)
    extra = extra.replace("### 微信支付绑定", imgs + "\n\n### 微信支付绑定")
    extra = extra.replace(
        "### 绑定后的优势", WELAB_BIND_NOTES.strip() + "\n\n### 绑定后的优势"
    )
    # 插到「六、风险与合规提示」之前，并把原六改名为七
    text = text.replace(marker, extra.strip() + "\n\n---\n\n## 七、风险与合规提示", 1)
    open(path, "w", encoding="utf-8").write(text)
    print("OK  07-bank-virtual-welab.md + 绑卡附录")


if __name__ == "__main__":
    main()
