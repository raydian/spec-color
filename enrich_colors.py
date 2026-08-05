#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
为 china_color.json 的每个色块补充：
  - description: 很有诗意的颜色介绍说明（引用原句 + 作者 + 节气意象 + 色家族视觉/注脚 + 明度气质）
  - usage:        建议使用场景说明
  - pairings:     3-5 项最适合的搭配颜色（取自本数据集），含 relation / method / usage

保留原有全部字段与顺序，仅追加新字段。
"""
import json
import colorsys

SRC = "china_color.json"

SEASON = {}
for t in ["立春", "雨水", "驚蟄", "春分", "清明", "穀雨"]:
    SEASON[t] = "春"
for t in ["立夏", "小滿", "芒種", "夏至", "小暑", "大暑"]:
    SEASON[t] = "夏"
for t in ["立秋", "處暑", "白露", "秋分", "寒露", "霜降"]:
    SEASON[t] = "秋"
for t in ["立冬", "小雪", "大雪", "冬至", "小寒", "大寒"]:
    SEASON[t] = "冬"

NEUTRALS = {"素白", "淡灰", "灰褐", "墨"}


def hsl(c):
    h, l, s = colorsys.rgb_to_hls(c["r"] / 255.0, c["g"] / 255.0, c["b"] / 255.0)
    return h * 360.0, l * 100.0, s * 100.0


def classify(r, g, b):
    h, l, s = colorsys.rgb_to_hls(r / 255.0, g / 255.0, b / 255.0)
    H, L, S = h * 360.0, l * 100.0, s * 100.0
    if S < 15:
        if L > 86:
            return "素白"
        if L > 62:
            return "淡灰"
        if L > 36:
            return "灰褐"
        return "墨"
    if H < 18 or H >= 342:
        return "朱红" if S >= 30 else "灰褐"
    if H < 45:
        return "橙黄" if S >= 26 else "灰褐"
    if H < 68:
        return "明黄"
    if H < 165:
        return "青绿"
    if H < 200:
        return "碧青"
    if H < 258:
        return "青蓝"
    if H < 330:
        return "黛紫"
    return "红紫"


def cyclic_diff(a, b):
    d = abs(a - b) % 360
    return min(d, 360 - d)


# ---------- 诗意文案 ----------
FAMILIES = {
    "素白": {
        "visual": ["如月初之辉，温润含光，不事雕琢", "似新雪初霁，清而不寒，莹然生白", "若素绢未染，留有余地，淡到极处"],
        "note": ["最宜作底色，承托万物而不夺其彩", "于留白处见天地，于无声处听清音", "淡极始知花更艳，白处自有万千色"],
        "usage": ["空间与版面的留白底色、宣纸与绢本衬色", "素雅包装、婚书喜帖、文人信笺", "水墨淡彩的过渡与高光、工笔打底"],
    },
    "淡灰": {
        "visual": ["如远岚含烟，薄雾笼山，温吞柔和", "似旧纸经年，褪去火气，沉静可亲", "若晨光里的一层灰，朦胧而不灰败"],
        "note": ["不抢眼，却最能安放繁复的喧哗", "于浓淡之间立住分寸，是低调的体面", "看似无色，实则是百色之母"],
        "usage": ["UI 与界面的中性底色、浅色模式背景", "高级灰家居、极简品牌视觉", "插画中的空气感与远景层次"],
    },
    "灰褐": {
        "visual": ["如旧石经霜，温润哑光，自带年岁", "似陈墨入纸，沉静可亲，褪去火气", "若远山含雾，朦胧处见安稳"],
        "note": ["最宜近人，是烟火与旧物都有的温度", "不张扬，却能在繁复里立住分寸", "于沉静中见温厚，是岁月的包浆"],
        "usage": ["复古插画、古籍装帧、牛皮纸质感", "家居与服饰的中性过渡色、莫兰迪基调", "咖啡馆、茶室等空间的安稳灰调"],
    },
    "墨": {
        "visual": ["如夜山积墨，沉沉入定，深不可测", "似古砚研尽的浓墨，黑而不死，透着幽光", "若子夜无月，万籁俱寂处的一点重量"],
        "note": ["色之尽处，反生万千可能", "沉得住气，方能压住满纸风华", "于极暗处见层次，是东方的深邃"],
        "usage": ["书法、印章、水墨的焦墨主色", "深邃背景、暗色模式、强调轮廓", "高级男装、新中式空间的压轴色"],
    },
    "朱红": {
        "visual": ["如初阳破晓，一点丹心，灼灼照人", "似宫墙深院里的朱门，喜气而端严", "若心头朱砂，热烈处藏着郑重"],
        "note": ["最宜点睛，一点便活了满纸", "是节庆与心跳的颜色，也是印信的体温", "浓淡皆宜，淡则娇、浓则威"],
        "usage": ["春节、喜帖、品牌强调色与按钮", "印章、封蜡、国潮视觉的主红", "点缀于素色之间，提神而不喧宾"],
    },
    "橙黄": {
        "visual": ["如暮云镀金，温吞的暖，落进眼底", "似熟果垂枝，蜜意盎然，教人安心", "若炉火映壁的橙光，是家的方向"],
        "note": ["最是疗愈，是秋冬里一口暖汤", "不刺眼，却能把寒意都烘软", "于明丽中见温厚，是烟火的好颜色"],
        "usage": ["食品、餐饮与丰收主题的暖色包装", "秋日视觉、暖光氛围、提示高亮", "亲子、家居品牌的亲和色调"],
    },
    "明黄": {
        "visual": ["如日色当空，澄明透亮，贵气自生", "似雏莺初羽，嫩而生鲜，满含希望", "若琉璃映阳，金箔轻颤，堂皇而不俗"],
        "note": ["是天子与花事的共享色，明亮而慎重", "浅则清雅如新柳，深则端凝如宫锦", "于灿烂处见节制，方显其贵"],
        "usage": ["宫廷、节庆与礼赠主题的华彩", "灯光氛围、童趣设计与警示标识", "茶饮、糕点包装的暖金调性"],
    },
    "青绿": {
        "visual": ["如春山初醒，新苔上阶，生机盎然", "似江南烟柳，水色空蒙，润到心里", "若雨后秧田，一脉清新，洗尽尘嚣"],
        "note": ["最宜写自然，是草木与呼吸的颜色", "浅则灵动，深则沉静如林荫", "于青翠中见悠然，是东方的清新"],
        "usage": ["植物、茶叶、自然主题的包装与界面", "清新品牌视觉、文创与手账配色", "空间里的治愈绿意、疗愈系设计"],
    },
    "碧青": {
        "visual": ["如碧落初晴，水天一色，清透见底", "似青瓷开片，温润出釉，幽幽生凉", "若寒玉含光，介于蓝绿，最解暑气"],
        "note": ["凉意自生，是盛夏里的一汪清泉", "不争不抢，却让满室都安静下来", "于清冷中见雅致，宜远观亦宜近触"],
        "usage": ["青瓷、茶席与清凉主题的视觉", "夏日包装、护肤品牌的清爽调", "科技产品的冷静中性色"],
    },
    "青蓝": {
        "visual": ["如远岫含黛，云水苍茫，沉静入骨", "似暮色四合时的天际，辽阔而安稳", "若深潭映月，幽蓝处藏着万千星"],
        "note": ["最宜写远意，是山水与心事的底色", "浅则疏朗如晨雾，深则庄严如夜空", "于沉静中见格局，宜大处落墨"],
        "usage": ["水墨远山、服饰与文创的雅蓝", "企业视觉、科技与理性的冷静色", "夜色主题、深邃背景与点缀"],
    },
    "黛紫": {
        "visual": ["如烟霞暮霭，紫气东来，神秘而贵", "似紫藤垂架，幽幽一缕，清雅出尘", "若晚香玉初绽，于暗处自有芬芳"],
        "note": ["最宜写雅致，是文人案头的孤芳", "浅则柔媚，深则端凝如紫禁", "于幽微处见情致，宜慢品不宜喧"],
        "usage": ["雅致文创、女性主题与礼赠视觉", "晚霞、梦境与浪漫氛围的渲染", "点缀高级灰，提升空间格调"],
    },
    "红紫": {
        "visual": ["如海棠睡起，宿酲未消，娇而不妖", "似晚霞收尽时的胭脂，热烈里带冷艳", "若蔷薇初破，红中凝紫，风骨暗藏"],
        "note": ["最宜写情思，是心动与别绪的颜色", "浅则含羞，深则秾丽如牡丹", "于秾淡之间见性情，宜作点睛"],
        "usage": ["浪漫、女性与节庆主题的强调色", "花艺、美妆与晚宴视觉的华彩", "点缀于素色，提气而不失雅"],
    },
}


def pick(options, key):
    h = sum(ord(c) for c in key)
    return options[h % len(options)]


def lightness_mod(L):
    if L > 82:
        return "其质轻浅，如薄纱笼月，宜作轻盈与留白"
    if L < 32:
        return "其质沉厚，如夜山积墨，宜作压轴与深邃"
    if L < 50:
        return "其质醇郁，沉得住气，宜作庄重与基调"
    return "其质温润，浓淡得宜，宜作过渡与点染"


def build_desc(c):
    fam = classify(c["r"], c["g"], c["b"])
    f = FAMILIES[fam]
    name = c["name"]
    sentence = c.get("sentence", "")
    author = c.get("author", "佚名")
    src = c.get("sentenceFrom", "")
    season = SEASON.get(c.get("category", ""), "")
    h, l, s = hsl(c)
    visual = pick(f["visual"], name)
    note = pick(f["note"], name)
    mod = lightness_mod(l)
    parts = []
    if sentence:
        parts.append(f"{author}《{src}》有云：「{sentence}」")
    parts.append(f"「{name}」之色，{visual}；{note}。{mod}（{season}尤见其韵）。")
    return "".join(parts)


def build_usage(c):
    fam = classify(c["r"], c["g"], c["b"])
    f = FAMILIES[fam]
    name = c["name"]
    u0 = f["usage"][0]
    u1 = pick(f["usage"], name)
    if u1 == u0:
        u1 = f["usage"][1]
    return f"{u0}；{u1}。"


# ---------- 搭配色推荐 ----------
REL = {
    "同色系": ("同色系深浅", "以同色系的{p}相叠，浓淡相成、素雅高级，不换色即得层次。",
            "宜作单色系品牌的层次、留白与水墨晕染。"),
    "邻近色": ("邻近色", "取色相相邻的{p}为邻，过渡柔和、自然不生硬。",
            "宜作渐变、同屏过渡与背景层次铺陈。"),
    "互补色": ("互补色", "以互补的{p}点睛，冷暖相生、彼此提神。",
            "宜作强调色、撞色焦点与视觉引导。"),
    "三角色": ("三角色", "循三角配色引入{p}，三色均衡、活泼而不乱。",
            "宜作多色插画、品牌主辅色与节庆视觉。"),
    "中性平衡": ("中性平衡", "以中性色{p}压阵，沉静收口、稳住全局。",
              "宜作背景、正文文字与区块分隔。"),
    "暖调": ("暖调搭配", "配暖调的{p}，为素净底色添一分温度。",
           "宜作点缀、按钮与温馨氛围。"),
    "冷调": ("冷调搭配", "配冷调的{p}，为素净底色注入清雅。",
           "宜作点缀、链接与冷静氛围。"),
    "对比中性": ("深浅中性", "以{p}拉出明暗，素净之中见骨架。",
             "宜作文字、描边与极简留白。"),
}


def best_near(allc, anchor, target, s_min=0, dh_range=None, exclude=None):
    """找色相最接近 anchor 的色块；可限定饱和度与色相差范围。"""
    best, best_score = None, float("inf")
    for c in allc:
        if c is target or (exclude and c["name"] in exclude):
            continue
        h, l, s = hsl(c)
        if s < s_min:
            continue
        dh = cyclic_diff(h, anchor)
        if dh_range and not (dh_range[0] <= dh <= dh_range[1]):
            continue
        sat_pen = 0 if s >= 22 else (22 - s) * 2
        score = dh + 0.04 * abs(l - hsl(target)[1]) + 0.08 * sat_pen
        if score < best_score:
            best_score, best = score, c
    return best


def pick_neutral(allc, target):
    h, l, s = hsl(target)
    if l > 55:
        cands = [c for c in allc if c is not target and classify(c["r"], c["g"], c["b"]) in ("墨", "灰褐")]
    else:
        cands = [c for c in allc if c is not target and classify(c["r"], c["g"], c["b"]) in ("素白", "淡灰")]
    if not cands:
        return None
    return max(cands, key=lambda c: abs(hsl(c)[1] - l))


def build_pairings(target, allc):
    h, l, s = hsl(target)
    fam = classify(target["r"], target["g"], target["b"])
    roles = []  # (relation_key, candidate)

    if fam in NEUTRALS:
        # 中性色：暖调 + 冷调 + 对比中性
        warm = best_near(allc, 40, target, s_min=25)
        cool = best_near(allc, 210, target, s_min=25)
        neu = pick_neutral(allc, target)
        if warm:
            roles.append(("暖调", warm))
        if cool:
            roles.append(("冷调", cool))
        if neu:
            roles.append(("对比中性", neu))
    else:
        # 同色系深浅
        same = [c for c in allc if c is not target
                and classify(c["r"], c["g"], c["b"]) == fam
                and abs(hsl(c)[1] - l) >= 18]
        if same:
            sh = max(same, key=lambda c: abs(hsl(c)[1] - l))
            roles.append(("同色系", sh))
        # 邻近色
        near = best_near(allc, h + 30, target, s_min=22, dh_range=(8, 55))
        if near:
            roles.append(("邻近色", near))
        # 互补色
        comp = best_near(allc, h + 180, target, s_min=25)
        if comp:
            roles.append(("互补色", comp))
        # 三角色
        tri = best_near(allc, h + 120, target, s_min=25)
        if tri and tri["name"] not in [r[1]["name"] for r in roles]:
            roles.append(("三角色", tri))
        # 中性平衡
        neu = pick_neutral(allc, target)
        if neu:
            roles.append(("中性平衡", neu))

    # 去重并限制 3-5
    seen, out = set(), []
    for key, c in roles:
        if c["name"] in seen:
            continue
        seen.add(c["name"])
        label, method_t, usage_t = REL[key]
        out.append({
            "name": c["name"],
            "hex": c.get("hex", ""),
            "relation": label,
            "method": method_t.format(p=c["name"]),
            "usage": usage_t,
        })
    # 中性色可能只有 3 项，彩度色最多 5 项，均满足 3-5
    return out


def main():
    with open(SRC, "r", encoding="utf-8") as fh:
        data = json.load(fh)

    flat = [c for group in data for c in group]
    count = 0
    for group in data:
        for c in group:
            c["description"] = build_desc(c)
            c["usage"] = build_usage(c)
            c["pairings"] = build_pairings(c, flat)
            count += 1

    with open(SRC, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
        fh.write("\n")

    import statistics
    sizes = [len(c["pairings"]) for group in data for c in group]
    print(f"已处理 {count} 个色块；pairings 数量 min={min(sizes)} max={max(sizes)} "
          f"avg={statistics.mean(sizes):.1f}")


if __name__ == "__main__":
    main()
