import json
from collections import Counter, defaultdict
from datetime import datetime, timedelta

with open("reviews.json", encoding="utf-8") as f:
    data = json.load(f)

reviews = data["reviews"]
company = "Свобода Концерт Холл"
total = len(reviews)
period_from = reviews[-1]["date"][:10]
period_to = reviews[0]["date"][:10]

star_dist = Counter(r["stars"] for r in reviews)
avg_rating = sum(r["stars"] for r in reviews) / total
pos_cnt = sum(1 for r in reviews if r["stars"] >= 4)
neg_cnt = sum(1 for r in reviews if r["stars"] <= 2)
neu_cnt = total - pos_cnt - neg_cnt

MONTHS_RU = ["ЯНВ","ФЕВ","МАР","АПР","МАЙ","ИЮН","ИЮЛ","АВГ","СЕН","ОКТ","НОЯ","ДЕК"]
AVAIL_YEARS = sorted(set(r["date"][:4] for r in reviews))
AVAIL_MONTHS = sorted(set(r["date"][5:7] for r in reviews))

SEASON_COLORS = {
    12:"#a0aec0",1:"#cbd5e0",2:"#e2e8f0",
    3:"#276749",4:"#38a169",5:"#48bb78",
    6:"#d69e2e",7:"#ecc94b",8:"#f6e05e",
    9:"#9c4221",10:"#dd6b20",11:"#ed8936",
}
SEASON_KEYS = {12:"w",1:"w",2:"w",3:"sp",4:"sp",5:"sp",6:"su",7:"su",8:"su",9:"a",10:"a",11:"a"}
SEASON_LABELS = {"w":"❄️ Зима","sp":"🌸 Весна","su":"☀️ Лето","a":"🍂 Осень"}
SEASON_ORDER = ["w","sp","su","a"]

ADVANTAGES = [
    ("звук отличн","Качество звука"),("отличный звук","Качество звука"),
    ("шикарный звук","Качество звука"),("хороший звук","Качество звука"),
    ("звук хорош","Качество звука"),("звук на уровне","Качество звука"),
    ("качество звука","Качество звука"),("звукорежиссёр","Качество звука"),
    ("свет","Световое шоу"),("освещение","Световое шоу"),("шоу","Световое шоу"),
    ("организация","Организация мероприятий"),("организовано","Организация мероприятий"),
    ("персонал","Персонал"),("сотрудник","Персонал"),("администратор","Персонал"),
    ("вежливый","Персонал"),("вежливо","Персонал"),("приветливый","Персонал"),
    ("доброжелательный","Персонал"),("отзывчивый","Персонал"),("внимательный","Персонал"),
    ("профессиональный","Персонал"),("профессионал","Персонал"),
    ("атмосфер","Атмосфера"),("уютно","Атмосфера"),("душевно","Атмосфера"),
    ("интерьер","Интерьер"),("красивый зал","Интерьер"),("стильный","Интерьер"),
    ("сцена","Сцена / обзор"),("обзор сцены","Сцена / обзор"),
    ("видно сцену","Сцена / обзор"),("видимость","Сцена / обзор"),
    ("транспортн","Расположение"),("расположение","Расположение"),
    ("расположен","Расположение"),("добраться","Расположение"),("ход","Расположение"),
    ("парковк","Парковка"),("припарк","Парковка"),("машину","Парковка"),
    ("бар","Бар / Еда"),("напитк","Бар / Еда"),("выбор","Бар / Еда"),
    ("еда","Бар / Еда"),("вкусно","Бар / Еда"),
    ("цена доступн","Цены / Доступность"),("недорого","Цены / Доступность"),
    ("дёшево","Цены / Доступность"),("приемлем","Цены / Доступность"),
    ("комфортн","Комфорт / Удобство"),("удобн","Комфорт / Удобство"),
    ("просторно","Комфорт / Удобство"),
    ("чисто","Чистота"),("чистый","Чистота"),("уборк","Чистота"),
    ("кондиционер","Вентиляция / Температура"),("свежий воздух","Вентиляция / Температура"),
    ("концерт","Концертная программа"),("мероприят","Концертная программа"),
    ("артист","Исполнители"),("музыкант","Исполнители"),("группа","Исполнители"),
    ("исполн","Исполнители"),("репертуар","Репертуар"),
]
PAINS = [
    ("охрана","Охрана / Секьюрити"),("охранник","Охрана / Секьюрити"),
    ("секьюрити","Охрана / Секьюрити"),("аркаша","Охрана / Секьюрити"),
    ("хам","Охрана / Секьюрити"),("нагрубил","Охрана / Секьюрити"),
    ("грубост","Охрана / Секьюрити"),("грубый","Охрана / Секьюрити"),
    ("полномочия","Охрана / Секьюрити"),
    ("душно","Духота / Температура"),("духота","Духота / Температура"),
    ("жарко","Духота / Температура"),("жара","Духота / Температура"),
    ("нечем дышать","Духота / Температура"),("спёртый воздух","Духота / Температура"),
    ("проветрива","Духота / Температура"),("холодно","Духота / Температура"),
    ("стул","Мебель / Комфорт"),("столик","Мебель / Комфорт"),
    ("сидень","Мебель / Комфорт"),("кресл","Мебель / Комфорт"),
    ("неудобные стул","Мебель / Комфорт"),("маленькие столик","Мебель / Комфорт"),
    ("грязные стул","Мебель / Комфорт"),("неудобн","Мебель / Комфорт"),
    ("тесно","Давка / Толпа"),("теснота","Давка / Толпа"),
    ("давк","Давка / Толпа"),("толп","Давка / Толпа"),
    ("акустик","Качество звука"),("слышно","Качество звука"),
    ("плохой звук","Качество звука"),("ужасный звук","Качество звука"),
    ("глухой звук","Качество звука"),("звук ужасн","Качество звука"),
    ("звук плох","Качество звука"),
    ("очеред","Очереди"),("ждать","Ожидание"),("ожидание","Ожидание"),
    ("прождали","Ожидание"),("долго","Обслуживание"),("обслуживание","Обслуживание"),
    ("гардероб","Гардероб"),("раздевалк","Гардероб"),("верхняя одежда","Гардероб"),
    ("цен","Цены"),("дорогой","Цены"),("дорого","Цены"),("завышен","Цены"),("дороговато","Цены"),
    ("парковк","Парковка (негатив)"),("припарк","Парковка (негатив)"),
    ("гряз","Чистота (негатив)"),("мусор","Чистота (негатив)"),
    ("санитар","Чистота (негатив)"),("туалет","Чистота (негатив)"),
    ("задержк","Организация"),("перенос","Организация"),("отменил","Организация"),("пускают","Организация"),
]

ALL_KW = list(set(kw for kw, _ in ADVANTAGES + PAINS))
ALL_KW.sort(key=len, reverse=True)
ALL_KW_JSON = json.dumps(ALL_KW, ensure_ascii=False)
ADV_JSON = json.dumps(ADVANTAGES, ensure_ascii=False)
PAIN_JSON = json.dumps(PAINS, ensure_ascii=False)

rev_adv = []; rev_pain = []
for idx, r in enumerate(reviews):
    t = (r.get("text") or "").lower()
    a = set(); p = set()
    for kw, cat in ADVANTAGES:
        if kw in t: a.add(cat)
    for kw, cat in PAINS:
        if kw in t: p.add(cat)
    rev_adv.append(list(a)); rev_pain.append(list(p))

CLASSIFIED_JSON = json.dumps({"adv": rev_adv, "pain": rev_pain}, ensure_ascii=False)
MONTHS_RU_JSON = json.dumps(MONTHS_RU, ensure_ascii=False)
SEASON_COLORS_JSON = json.dumps(SEASON_COLORS, ensure_ascii=False)
SEASON_KEYS_JSON = json.dumps(SEASON_KEYS, ensure_ascii=False)
SEASON_LABELS_JSON = json.dumps(SEASON_LABELS, ensure_ascii=False)
SEASON_ORDER_JSON = json.dumps(SEASON_ORDER, ensure_ascii=False)

def esc(s):
    if s is None: return ""
    return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

def plural_ru(n):
    n = abs(n)
    if n % 10 == 1 and n % 100 != 11: return "отзыва"
    return "отзывов"

def plural_donut(n):
    n = abs(n)
    if n % 10 == 1 and n % 100 != 11: return "отзыв"
    if n % 10 in (2,3,4) and n % 100 not in (12,13,14): return "отзыва"
    return "отзывов"

def highlight(text):
    if not text: return ""
    lower = text.lower()
    matches = []
    for kw in ALL_KW:
        s = 0
        while True:
            pos = lower.find(kw, s)
            if pos == -1: break
            end = pos + len(kw)
            ws = pos
            while ws > 0 and lower[ws-1].isalpha(): ws -= 1
            while end < len(lower) and lower[end].isalpha(): end += 1
            overlaps = any(not (end <= ms or ws >= me) for ms, me in matches)
            if not overlaps: matches.append((ws, end))
            s = pos + 1
    if not matches: return esc(text)
    matches.sort()
    parts = []
    last = 0
    for pos, end in matches:
        if pos > last: parts.append(esc(text[last:pos]))
        parts.append(f'<strong>{esc(text[pos:end])}</strong>')
        last = end
    if last < len(text): parts.append(esc(text[last:]))
    return "".join(parts)

def bar(pct, color):
    return f'<div class="bar-track"><div class="bar-fill" style="width:{max(pct*100,2)}%;background:{color};"></div></div>'

star_colors = {1:"#f44336",2:"#FF9800",3:"#FFC107",4:"#8BC34A",5:"#4CAF50"}
stars_html = ""
for s in (5,4,3,2,1):
    cnt = star_dist.get(s, 0)
    stars_html += f'<div class="star-row"><span class="l">{s}★</span>{bar(cnt/total, star_colors[s])}<span class="r">{cnt}</span></div>'

# ── Donut chart (ALL months, no filter) ──
sorted_yms = sorted(set(r["date"][:7] for r in reviews))
month_data = []
for ym in sorted_yms:
    m = int(ym[5:7]); ms = [r["stars"] for r in reviews if r["date"][:7]==ym]
    month_data.append((ym, m, len(ms), sum(ms)/len(ms)))
total_donut = sum(m[2] for m in month_data)
grad_parts = []; cp = 0
for ym, m, cnt, _ in month_data:
    pct = cnt/total_donut*100 if total_donut else 0
    grad_parts.append(f"{SEASON_COLORS[m]} {cp:.2f}% {min(cp+pct,100):.2f}%")
    cp += pct
gradient_str = "conic-gradient("+", ".join(grad_parts)+")"
legend = "".join(
    f'<span style="display:inline-flex;align-items:center;gap:4px;margin:0 8px 4px 0;font-size:12px"><span style="width:8px;height:8px;border-radius:2px;background:{SEASON_COLORS[m]};flex-shrink:0"></span>{MONTHS_RU[m-1]}<span style="color:#718096">{cnt}</span></span>'
    for ym, m, cnt, _ in month_data
)
donut_html = f'<div style="display:flex;gap:24px;align-items:center;flex-wrap:wrap"><div style="position:relative;width:180px;height:180px;flex-shrink:0"><div style="width:180px;height:180px;border-radius:50%;background:{gradient_str};"></div><div style="position:absolute;inset:50%;transform:translate(-50%,-50%);width:90px;height:90px;border-radius:50%;background:white;display:flex;flex-direction:column;align-items:center;justify-content:center;line-height:1.2;box-shadow:inset 0 0 0 1px #e2e8f0"><span style="font-size:24px;font-weight:700">{total_donut}</span><span style="font-size:10px;color:#718096">{plural_donut(total_donut)}</span></div></div><div style="flex:1;min-width:200px">{legend}</div></div>'

# ── Monthly stats chart (last 6 months) ──
monthly_timeline = []
for ym in sorted_yms[-13:]:
    m = int(ym[5:7])
    ms = [r for r in reviews if r["date"][:7]==ym]
    pos_m = sum(1 for r in ms if r["stars"]>=4)
    neg_m = sum(1 for r in ms if r["stars"]<=2)
    neu_m = len(ms)-pos_m-neg_m
    avg_m = sum(r["stars"] for r in ms)/len(ms)
    monthly_timeline.append((ym, m, len(ms), avg_m, pos_m, neu_m, neg_m))

max_bar = max((m[4]+m[5]+m[6] for m in monthly_timeline), default=1)
timeline_html = ""
for ym, m, cnt, avg_m, pos_m, neu_m, neg_m in monthly_timeline:
    timeline_html += f"""
    <div class="tm-row">
        <span class="tm-l">{MONTHS_RU[m-1]}</span>
        <div class="tm-bar"><div class="tm-fill tm-pos" style="width:{pos_m/max_bar*100:.1f}%"></div><div class="tm-fill tm-neu" style="width:{neu_m/max_bar*100:.1f}%"></div><div class="tm-fill tm-neg" style="width:{neg_m/max_bar*100:.1f}%"></div></div>
        <span class="tm-cnt">{cnt}</span>
        <span class="tm-avg">★{avg_m:.2f}</span>
    </div>"""

# ── Static classifications ──
sorted_all = sorted(reviews, key=lambda r: -r["stars"])
all_review_rows = ""
for r in sorted_all:
    date = (r.get("date") or "")[:10]
    ym = date[:7]
    all_review_rows += f'<tr class="rv" data-date="{date}" data-ym="{ym}"><td>{esc(r.get("name","?"))}</td><td class="stars-{r["stars"]}">{r["stars"]}</td><td style="white-space:nowrap">{date}</td><td>{highlight(r.get("text",""))}</td></tr>\n'

def classify_static(rlist):
    adv_map = {}; pain_map = {}
    for idx, r in enumerate(rlist):
        t = (r.get("text") or "").lower()
        for kw, cat in ADVANTAGES:
            if kw in t: adv_map.setdefault(cat, []).append(idx)
        for kw, cat in PAINS:
            if kw in t: pain_map.setdefault(cat, []).append(idx)
    adv_rank = sorted([(c, len(v)) for c, v in adv_map.items()], key=lambda x: -x[1])
    pain_rank = sorted([(c, len(v)) for c, v in pain_map.items()], key=lambda x: -x[1])
    mixed = [i for i,r in enumerate(rlist) if any(kw in (r.get("text")or"").lower() for kw,_ in ADVANTAGES) and any(kw in (r.get("text")or"").lower() for kw,_ in PAINS)]
    return adv_map, adv_rank, pain_map, pain_rank, mixed

def pick_quotes(cat_arr, rlist, min_stars, limit=2):
    cand = [rlist[i] for i in cat_arr if len((rlist[i].get("text")or"").strip())>30]
    cand.sort(key=lambda r: -r["stars"] if min_stars>=4 else r["stars"])
    seen=set(); res=[]
    for c in cand:
        k=c["name"]+(c.get("text")or"")[:50]
        if k not in seen: seen.add(k); res.append(c)
        if len(res)>=limit: break
    return res

adv_map, adv_rank, pain_map, pain_rank, mixed = classify_static(reviews)

max_adv = max((cnt for _, cnt in adv_rank), default=1)
adv_bars_html = ""
for cat, cnt in adv_rank:
    adv_bars_html += f'<div class="bar-row"><span class="label">{esc(cat)}</span><div class="track">{bar(cnt/max_adv,"#4CAF50")}</div><span class="count">{cnt}</span></div>\n'
for cat, _ in adv_rank[:5]:
    qs = pick_quotes(adv_map[cat], reviews, 4, 2)
    if qs:
        adv_bars_html += f"<h3>{esc(cat)}</h3>\n"
        for q in qs: adv_bars_html += f'<div class="quote quote-adv"><span class="name">{esc(q["name"])} ★{q["stars"]}</span> <span class="text">«{highlight(q.get("text",""))}»</span></div>\n'

max_pain = max((cnt for _, cnt in pain_rank), default=1)
pain_bars_html = ""
for cat, cnt in pain_rank:
    pain_bars_html += f'<div class="bar-row"><span class="label">{esc(cat)}</span><div class="track">{bar(cnt/max_pain,"#f44336")}</div><span class="count">{cnt}</span></div>\n'
for cat, _ in pain_rank:
    qs = pick_quotes(pain_map[cat], reviews, 1, 2)
    if qs: pain_bars_html += f"<h3>{esc(cat)}</h3>\n"
    for q in qs: pain_bars_html += f'<div class="quote quote-pain"><span class="name">{esc(q["name"])} ★{q["stars"]}</span> <span class="text">«{highlight(q.get("text",""))}»</span></div>\n'

mix_count = len(mixed)
mix_html = ""
for i in sorted(mixed, key=lambda i: reviews[i]["stars"])[:6]:
    t = (reviews[i].get("text") or "").strip()
    if len(t)>20: mix_html += f'<div class="quote quote-mixed"><span class="name">{esc(reviews[i]["name"])} ★{reviews[i]["stars"]}</span> <span class="text">«{highlight(t)}»</span></div>\n'

neg_all = sorted([r for r in reviews if r["stars"]<=2], key=lambda r: r["stars"])
neg_count = len(neg_all)
neg_table = ""
for r in neg_all[:15]: neg_table += f'<tr><td>{esc(r["name"])}</td><td class="stars-{r["stars"]}">{r["stars"]}</td><td>{highlight(r.get("text",""))}</td></tr>\n'

# ── Keyword summary bars ──
max_adv_kw = max((cnt for _, cnt in adv_rank), default=1)
kw_adv_html = ""
for cat, cnt in adv_rank:
    kw_adv_html += f'<div class="bar-row"><span class="label">{esc(cat)}</span><div class="track">{bar(cnt/max_adv_kw,"#4CAF50")}</div><span class="count">{cnt}</span></div>\n'
max_pain_kw = max((cnt for _, cnt in pain_rank), default=1)
kw_pain_html = ""
for cat, cnt in pain_rank:
    kw_pain_html += f'<div class="bar-row"><span class="label">{esc(cat)}</span><div class="track">{bar(cnt/max_pain_kw,"#f44336")}</div><span class="count">{cnt}</span></div>\n'

REVIEWS_JSON = json.dumps(reviews, ensure_ascii=False)

month_options = '<option value="">Все</option>' + "".join(f'<option value="{m:02d}">{MONTHS_RU[m-1]}</option>' for m in range(1,13))
year_options = '<option value="">Все</option>' + "".join(f'<option value="{y}">{y}</option>' for y in AVAIL_YEARS)

html = f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Анализ отзывов — {company}</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:#f5f7fa;color:#1a1a2e;line-height:1.6}}
.container{{max-width:1100px;margin:0 auto;padding:20px}}
@keyframes pulse{{0%{{opacity:0.6;transform:scale(0.95)}}50%{{opacity:1;transform:scale(1.05)}}100%{{opacity:1;transform:scale(1)}}}}
.animating{{animation:pulse 0.4s ease}}
.filter-bar{{background:white;border-radius:12px;padding:16px 24px;margin-bottom:20px;box-shadow:0 1px 3px rgba(0,0,0,0.08);display:flex;align-items:center;gap:12px;flex-wrap:wrap}}
.filter-bar label{{font-size:13px;color:#4a5568;user-select:none}}
.filter-bar select{{padding:6px 10px;border:1px solid #e2e8f0;border-radius:6px;font-size:14px;background:white;cursor:pointer;-webkit-appearance:none;appearance:none;background-image:url("data:image/svg+xml,%3Csvg width='10' height='6' viewBox='0 0 10 6' fill='none' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M1 1L5 5L9 1' stroke='%234a5568' stroke-width='1.5' stroke-linecap='round'/%3E%3C/svg%3E");background-repeat:no-repeat;background-position:right 8px center;padding-right:28px}}
.filter-bar select:focus{{outline:none;border-color:#1a1a2e;box-shadow:0 0 0 2px rgba(26,26,46,0.15)}}
.filter-bar .sep{{color:#cbd5e0;font-size:16px;margin:0 2px}}
.filter-bar .btn{{padding:6px 16px;background:#1a1a2e;color:white;border:none;border-radius:6px;cursor:pointer;font-size:14px;font-weight:500}}
.filter-bar .btn:hover{{background:#16213e}}
.section{{background:white;border-radius:12px;padding:24px;margin-bottom:20px;box-shadow:0 1px 3px rgba(0,0,0,0.08)}}
.section h2{{font-size:20px;margin-bottom:12px;padding-bottom:8px;border-bottom:2px solid #e2e8f0}}
.section h3{{font-size:14px;margin:12px 0 6px;color:#4a5568}}
.bar-track{{height:24px;background:#edf2f7;border-radius:12px;overflow:hidden}}
.bar-fill{{height:100%;border-radius:12px;min-width:2px;transition:width 0.4s ease}}
.bar-row{{display:flex;align-items:center;margin-bottom:6px}}
.bar-row .label{{width:180px;font-size:13px;text-align:right;margin-right:12px;flex-shrink:0}}
.bar-row .track{{flex:1}}
.bar-row .count{{width:40px;font-size:13px;margin-left:8px;font-family:'SF Mono',monospace}}
.star-row{{display:flex;align-items:center;margin-bottom:4px}}
.star-row .l{{width:36px;text-align:right;margin-right:8px;font-size:11px}}
.star-row .r{{margin-left:8px;font-size:12px;color:#718096}}
.tm-row{{display:flex;align-items:center;margin-bottom:10px;gap:10px}}
.tm-l{{width:32px;font-size:11px;font-weight:600;text-align:right;flex-shrink:0}}
.tm-bar{{flex:1;height:28px;border-radius:6px;overflow:hidden;display:flex;background:#edf2f7}}
.tm-fill{{height:100%;min-width:2px;transition:width 0.4s ease}}
.tm-pos{{background:#4CAF50}} .tm-neu{{background:#FFC107}} .tm-neg{{background:#f44336}}
.tm-cnt{{width:30px;font-size:12px;font-family:'SF Mono',monospace;text-align:right;color:#718096}}
.tm-avg{{width:48px;font-size:12px;font-weight:600;text-align:right;color:#1a1a2e}}
.quote{{background:#f7fafc;border-left:4px solid;padding:10px 14px;margin:6px 0;border-radius:4px;font-size:13px;word-break:break-word}}
.quote-adv{{border-color:#4CAF50}} .quote-pain{{border-color:#f44336}} .quote-mixed{{border-color:#FF9800}}
.quote .name{{font-weight:600;font-size:12px;color:#2d3748;display:block;margin-bottom:2px}}
.quote .text{{color:#4a5568}}
.grid-2{{display:grid;grid-template-columns:1fr 1fr;gap:20px}}
.grid-3{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:20px}}
@media(max-width:700px){{.grid-2,.grid-3{{grid-template-columns:1fr}}}}
table{{width:100%;border-collapse:collapse;font-size:13px}}
th,td{{padding:6px 10px;text-align:left;border-bottom:1px solid #e2e8f0}}
th{{background:#f7fafc;font-weight:600;color:#4a5568;position:sticky;top:0}}
.tbl-wrap{{max-height:600px;overflow-y:auto;border:1px solid #e2e8f0;border-radius:8px}}
.stars-5{{color:#4CAF50;font-weight:700}} .stars-4{{color:#8BC34A}} .stars-3{{color:#FFC107}}
.stars-2{{color:#FF9800}} .stars-1{{color:#f44336;font-weight:700}}
.hidden{{display:none!important}}
.text-sm{{font-size:13px}} .text-xs{{font-size:11px}}
.text-gray{{color:#718096}} .mt-2{{margin-top:8px}}
.badges{{display:flex;gap:8px;flex-wrap:wrap}}
.badge{{display:inline-block;padding:4px 12px;border-radius:999px;font-size:12px;font-weight:600}}
.bg-green{{background:#C6F6D5;color:#22543D}} .bg-yellow{{background:#FEFCBF;color:#744210}} .bg-red{{background:#FED7D7;color:#742A2A}}
.header{{background:linear-gradient(135deg,#1a1a2e 0%,#16213e 100%);color:white;padding:40px;border-radius:16px;margin-bottom:24px}}
.header h1{{font-size:28px;margin-bottom:8px}} .header .sub{{color:#a0aec0;font-size:14px}}
.header .big-number{{font-size:64px;font-weight:800;line-height:1;transition:all 0.4s ease}} .header .big-number-label{{font-size:16px;color:#a0aec0}}
.empty-state{{text-align:center;padding:40px 20px;color:#718096}}
.empty-state p{{font-size:16px;margin-bottom:8px}}
td strong, .quote .text strong{{background:#fef3c7;color:#92400e;padding:0 2px;border-radius:2px;font-weight:500}}
.tm-legend{{display:flex;gap:16px;flex-wrap:wrap;margin-bottom:12px;font-size:12px;color:#4a5568}}
.tm-legend span{{display:inline-flex;align-items:center;gap:4px}}
.tm-legend .dot{{width:10px;height:10px;border-radius:2px;flex-shrink:0}}
</style>
</head>
<body>
<div class="container">

<div class="filter-bar">
  <label>С:</label>
  <select id="monthFrom" onchange="applyFilter()">{month_options}</select>
  <select id="yearFrom" onchange="applyFilter()">{year_options}</select>
  <span class="sep">—</span>
  <label>По:</label>
  <select id="monthTo" onchange="applyFilter()">{month_options}</select>
  <select id="yearTo" onchange="applyFilter()">{year_options}</select>
  <button class="btn" onclick="resetFilter()">Сброс</button>
</div>

<div class="header">
  <h1>{company}</h1>
  <div class="sub" id="headerSubtitle">Анализ {total} {plural_ru(total)}</div>
  <div style="margin-top:20px;display:flex;gap:40px;align-items:flex-end;flex-wrap:wrap;">
    <div><div class="big-number" id="avgRating">{avg_rating:.2f}</div><div class="big-number-label">средняя оценка</div></div>
    <div class="badges" id="badges">
      <span class="badge bg-green">{pos_cnt}&nbsp;({pos_cnt*100//total}%) положительных</span>
      <span class="badge bg-yellow">{neu_cnt}&nbsp;({neu_cnt*100//total}%) нейтральных</span>
      <span class="badge bg-red">{neg_cnt}&nbsp;({neg_cnt*100//total}%) отрицательных</span>
    </div>
  </div>
</div>

<!-- Always-visible: donut + timeline -->
<div class="grid-2">
  <div class="section"><h2>Распределение оценок</h2><div id="secStars">{stars_html}</div></div>
  <div class="section"><h2>Динамика по месяцам</h2>{donut_html}</div>
</div>

<div class="section">
  <h2>Средняя оценка по месяцам</h2>
  <div class="tm-legend">
    <span><span class="dot" style="background:#4CAF50"></span>положительные</span>
    <span><span class="dot" style="background:#FFC107"></span>нейтральные</span>
    <span><span class="dot" style="background:#f44336"></span>отрицательные</span>
    <span style="margin-left:auto">★ — средняя оценка</span>
  </div>
  <div id="secTimeline">{timeline_html}</div>
</div>

<!-- Filter-dependent content -->
<div id="reportContent">
<div class="section"><h2>Преимущества</h2><div id="secAdv">{adv_bars_html}</div></div>
<div class="section"><h2>Боли и проблемы</h2><div id="secPains">{pain_bars_html}</div></div>
<div class="section"><h2>Смешанные отзывы <span class="text-sm text-gray" id="mixCount">({mix_count})</span></h2><div id="secMixed">{mix_html}</div></div>
<div class="section"><h2>Отрицательные отзывы <span class="text-sm text-gray" id="negCount">({neg_count})</span></h2>
<div class="tbl-wrap"><table><thead><tr><th>Имя</th><th>★</th><th>Отзыв</th></tr></thead><tbody id="secNeg">{neg_table}</tbody></table></div></div>
<div class="section"><h2>Все отзывы <span class="text-sm text-gray" id="allCount">({total})</span></h2>
<div class="tbl-wrap" style="max-height:600px">
<table id="reviewsTable"><thead><tr><th>Имя</th><th>★</th><th>Дата</th><th>Отзыв</th></tr></thead>
<tbody>{all_review_rows}</tbody></table></div></div>
<div class="section"><h2>Упоминания ключевых слов</h2>
<div class="grid-2">
<div><h3>Положительные</h3><div id="secKwAdv">{kw_adv_html}</div><p class="text-gray text-sm" id="secKwAdvEmpty" style="display:none">Нет данных</p></div>
<div><h3>Отрицательные</h3><div id="secKwPain">{kw_pain_html}</div><p class="text-gray text-sm" id="secKwPainEmpty" style="display:none">Нет данных</p></div>
</div></div>
</div>

<div id="emptyState" class="empty-state hidden">
  <p>На выбранный диапазон не опубликовано ни одного отзыва</p>
</div>

<div style="text-align:center;padding:20px;font-size:12px;color:#a0aec0">
Сгенерировано {datetime.now().strftime('%d.%m.%Y %H:%M')} · {company}
</div>

</div>

<script>
const ALL_REVIEWS = {REVIEWS_JSON};
const CLASSIFIED = {CLASSIFIED_JSON};
const ADVANTAGES = {ADV_JSON};
const PAINS = {PAIN_JSON};
const ALL_KW = {ALL_KW_JSON};
const MONTHS_RU = {MONTHS_RU_JSON};
const SEASON_COLORS = {SEASON_COLORS_JSON};
const SEASON_KEYS = {SEASON_KEYS_JSON};
const SEASON_LABELS = {SEASON_LABELS_JSON};
const SEASON_ORDER = {SEASON_ORDER_JSON};

function plural(n) {{
    n = Math.abs(n);
    if (n % 10 === 1 && n % 100 !== 11) return 'отзыва';
    return 'отзывов';
}}

function pluralDonut(n) {{
    n = Math.abs(n);
    if (n % 10 === 1 && n % 100 !== 11) return 'отзыв';
    if (n % 10 >= 2 && n % 10 <= 4 && (n % 100 < 10 || n % 100 >= 20)) return 'отзыва';
    return 'отзывов';
}}

function esc(s) {{
    if (s == null) return '';
    return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}}

function highlight(text) {{
    if (!text) return '';
    const lower = text.toLowerCase();
    const matches = [];
    ALL_KW.forEach(kw => {{
        let s = 0;
        while (true) {{
            let pos = lower.indexOf(kw, s);
            if (pos === -1) break;
            let end = pos + kw.length;
            let ws = pos;
            while (ws > 0 && /[a-zа-яё]/.test(lower[ws-1])) ws--;
            while (end < lower.length && /[a-zа-яё]/.test(lower[end])) end++;
            const overlaps = matches.some(([ms, me]) => !(end <= ms || ws >= me));
            if (!overlaps) matches.push([ws, end]);
            s = pos + 1;
        }}
    }});
    matches.sort((a,b) => a[0] - b[0]);
    if (!matches.length) return esc(text);
    const parts = [];
    let last = 0;
    matches.forEach(([pos, end]) => {{
        if (pos > last) parts.push(esc(text.slice(last, pos)));
        parts.push('<strong>'+esc(text.slice(pos, end))+'</strong>');
        last = end;
    }});
    if (last < text.length) parts.push(esc(text.slice(last)));
    return parts.join('');
}}

function bar(pct, color) {{
    return '<div class="bar-track"><div class="bar-fill" style="width:'+Math.max(pct*100,2)+'%;background:'+color+';"></div></div>';
}}

function classify(indices) {{
    const adv = {{}}; const pain = {{}}; const mixed = [];
    const texts = indices.map(i => (ALL_REVIEWS[i].text||'').toLowerCase());
    indices.forEach((ri, idx) => {{
        const t = texts[idx];
        const ha = {{}}; const hp = {{}};
        ADVANTAGES.forEach(([kw, cat]) => {{ if (t.includes(kw)) ha[cat] = true; }});
        PAINS.forEach(([kw, cat]) => {{ if (t.includes(kw)) hp[cat] = true; }});
        Object.keys(ha).forEach(c => {{ if(!adv[c]) adv[c]=[]; adv[c].push(ri); }});
        Object.keys(hp).forEach(c => {{ if(!pain[c]) pain[c]=[]; pain[c].push(ri); }});
        if (Object.keys(ha).length && Object.keys(hp).length) mixed.push(ri);
    }});
    return {{adv, pain, advRank:Object.entries(adv).map(([k,v])=>[k,v.length]).sort((a,b)=>b[1]-a[1]), painRank:Object.entries(pain).map(([k,v])=>[k,v.length]).sort((a,b)=>b[1]-a[1]), mixed}};
}}

function pickQuotes(catArr, minStars, limit) {{
    const cand = catArr.map(i => ALL_REVIEWS[i]).filter(r => (r.text||'').trim().length>30);
    cand.sort((a,b) => minStars===1 ? a.stars-b.stars : b.stars-a.stars);
    const seen = new Set();
    return cand.filter(c => {{ const k=c.name+(c.text||'').slice(0,50); if(seen.has(k)) return false; seen.add(k); return true; }}).slice(0,limit||2);
}}

function emptyBlock() {{
    document.getElementById('avgRating').textContent = '—';
    document.getElementById('badges').innerHTML = '';
    document.getElementById('secAdv').innerHTML = '';
    document.getElementById('secPains').innerHTML = '';
    document.getElementById('secKwAdv').innerHTML = '';
    document.getElementById('secKwPain').innerHTML = '';
    document.getElementById('mixCount').textContent = '(0)';
    document.getElementById('secMixed').innerHTML = '';
    document.getElementById('negCount').textContent = '(0)';
    document.getElementById('secNeg').innerHTML = '';
    document.getElementById('allCount').textContent = '(0)';
    document.querySelectorAll('#reviewsTable tbody tr.rv').forEach(r => r.classList.add('hidden'));
    document.getElementById('reportContent').classList.add('hidden');
    document.getElementById('emptyState').classList.remove('hidden');
    document.getElementById('headerSubtitle').textContent = 'Ни одного отзыва';
}}

function applyFilter(animate) {{
    const mFrom = document.getElementById('monthFrom').value;
    const yFrom = document.getElementById('yearFrom').value;
    const mTo = document.getElementById('monthTo').value;
    const yTo = document.getElementById('yearTo').value;

    let fromStr = '', toStr = '';
    if (yFrom && mFrom) fromStr = yFrom+'-'+mFrom+'-01';
    else if (yFrom) fromStr = yFrom+'-01-01';
    if (yTo && mTo) {{
        const ld = new Date(parseInt(yTo), parseInt(mTo), 0).getDate();
        toStr = yTo+'-'+mTo+'-'+(ld<10?'0':'')+ld;
    }} else if (yTo) toStr = yTo+'-12-31';

    const indices = [];
    ALL_REVIEWS.forEach((r, i) => {{
        const d = (r.date||'').slice(0,10);
        if (fromStr && d < fromStr) return;
        if (toStr && d > toStr) return;
        indices.push(i);
    }});

    if (!indices.length) {{ emptyBlock(); return; }}

    const filtered = indices.map(i => ALL_REVIEWS[i]);
    const total = filtered.length;

    const avgEl = document.getElementById('avgRating');
    if (animate) avgEl.classList.add('animating');
    setTimeout(() => avgEl.classList.remove('animating'), 500);

    const sumStars = filtered.reduce((s,r) => s + r.stars, 0);
    const avg = (sumStars / total).toFixed(2);
    document.getElementById('avgRating').textContent = avg;
    const pos = filtered.filter(r => r.stars >= 4).length;
    const neg = filtered.filter(r => r.stars <= 2).length;
    const neu = total - pos - neg;
    document.getElementById('badges').innerHTML = '<span class="badge bg-green">'+pos+'&nbsp;('+Math.round(pos/total*100)+'%) положительных</span><span class="badge bg-yellow">'+neu+'&nbsp;('+Math.round(neu/total*100)+'%) нейтральных</span><span class="badge bg-red">'+neg+'&nbsp;('+Math.round(neg/total*100)+'%) отрицательных</span>';
    document.getElementById('headerSubtitle').textContent = 'Анализ '+total+' '+plural(total);

    // Stars
    const starDist = {{}};
    filtered.forEach(r => starDist[r.stars] = (starDist[r.stars]||0) + 1);
    const colors = {{1:'#f44336',2:'#FF9800',3:'#FFC107',4:'#8BC34A',5:'#4CAF50'}};
    let sh = '';
    [5,4,3,2,1].forEach(s => {{ const cnt = starDist[s]||0; sh += '<div class="star-row"><span class="l">'+s+'★</span>'+bar(cnt/total,colors[s])+'<span class="r">'+cnt+'</span></div>'; }});
    document.getElementById('secStars').innerHTML = sh;

    const {{ adv, advRank, pain, painRank, mixed }} = classify(indices);

    // Advantages
    let ah = '';
    const maxAdv = advRank.length ? Math.max(...advRank.map(([,c])=>c)) : 1;
    advRank.forEach(([cat, cnt]) => {{ ah += '<div class="bar-row"><span class="label">'+esc(cat)+'</span><div class="track">'+bar(cnt/maxAdv,'#4CAF50')+'</div><span class="count">'+cnt+'</span></div>'; }});
    advRank.slice(0,5).forEach(([cat]) => {{
        const qs = pickQuotes(adv[cat], 4, 2);
        if (qs.length) {{ ah += '<h3>'+esc(cat)+'</h3>'; qs.forEach(q => {{ ah += '<div class="quote quote-adv"><span class="name">'+esc(q.name)+' ★'+q.stars+'</span> <span class="text">«'+highlight(q.text)+'»</span></div>'; }}); }}
    }});
    document.getElementById('secAdv').innerHTML = ah;

    // Pains
    let ph = '';
    const maxPain = painRank.length ? Math.max(...painRank.map(([,c])=>c)) : 1;
    painRank.forEach(([cat, cnt]) => {{ ph += '<div class="bar-row"><span class="label">'+esc(cat)+'</span><div class="track">'+bar(cnt/maxPain,'#f44336')+'</div><span class="count">'+cnt+'</span></div>'; }});
    painRank.forEach(([cat]) => {{
        const qs = pickQuotes(pain[cat], 1, 2);
        if (qs.length) {{ ph += '<h3>'+esc(cat)+'</h3>'; qs.forEach(q => {{ ph += '<div class="quote quote-pain"><span class="name">'+esc(q.name)+' ★'+q.stars+'</span> <span class="text">«'+highlight(q.text)+'»</span></div>'; }}); }}
    }});
    document.getElementById('secPains').innerHTML = ph;

    // Keyword summary
    let kwa = '';
    const mxa = advRank.length ? Math.max(...advRank.map(([,c])=>c)) : 1;
    advRank.forEach(([cat, cnt]) => {{ kwa += '<div class="bar-row"><span class="label">'+esc(cat)+'</span><div class="track">'+bar(cnt/mxa,'#4CAF50')+'</div><span class="count">'+cnt+'</span></div>'; }});
    document.getElementById('secKwAdv').innerHTML = kwa;
    let kwp = '';
    const mxp = painRank.length ? Math.max(...painRank.map(([,c])=>c)) : 1;
    painRank.forEach(([cat, cnt]) => {{ kwp += '<div class="bar-row"><span class="label">'+esc(cat)+'</span><div class="track">'+bar(cnt/mxp,'#f44336')+'</div><span class="count">'+cnt+'</span></div>'; }});
    document.getElementById('secKwPain').innerHTML = kwp;

    // Mixed
    let mh = '';
    mixed.sort((a,b) => ALL_REVIEWS[a].stars - ALL_REVIEWS[b].stars).slice(0,6).forEach(i => {{
        const r = ALL_REVIEWS[i]; const t = (r.text||'').trim();
        if (t.length > 20) mh += '<div class="quote quote-mixed"><span class="name">'+esc(r.name)+' ★'+r.stars+'</span> <span class="text">«'+highlight(t)+'»</span></div>';
    }});
    document.getElementById('mixCount').textContent = '('+mixed.length+')';
    document.getElementById('secMixed').innerHTML = mh;

    // Negatives
    const negArr = filtered.filter(r => r.stars <= 2).sort((a,b) => a.stars - b.stars);
    document.getElementById('negCount').textContent = '('+negArr.length+')';
    let nh = '';
    negArr.slice(0,15).forEach(r => {{ nh += '<tr><td>'+esc(r.name)+'</td><td class="stars-'+r.stars+'">'+r.stars+'</td><td>'+highlight(r.text)+'</td></tr>'; }});
    document.getElementById('secNeg').innerHTML = nh;

    const rows = document.querySelectorAll('#reviewsTable tbody tr.rv');
    let vis = 0;
    rows.forEach(row => {{
        const d = row.getAttribute('data-date');
        let show = true; if (fromStr && d < fromStr) show = false; if (toStr && d > toStr) show = false;
        row.classList.toggle('hidden', !show); if (show) vis++;
    }});
    document.getElementById('allCount').textContent = '('+vis+')';

    document.getElementById('reportContent').classList.remove('hidden');
    document.getElementById('emptyState').classList.add('hidden');
}}

function resetFilter() {{
    const dates = ALL_REVIEWS.map(r => (r.date||'').slice(0,10)).filter(Boolean).sort();
    if (dates.length) {{
        const to = dates[dates.length-1];
        const d = new Date(to); d.setDate(d.getDate() - 180);
        const fromStr = d.toISOString().slice(0,10);
        const from = fromStr < dates[0] ? dates[0] : fromStr;
        document.getElementById('monthFrom').value = from.slice(5,7);
        document.getElementById('yearFrom').value = from.slice(0,4);
        document.getElementById('monthTo').value = to.slice(5,7);
        document.getElementById('yearTo').value = to.slice(0,4);
    }}
    applyFilter(true);
}}

document.addEventListener('DOMContentLoaded', function() {{ resetFilter(); }});
</script>
</body>
</html>"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print(f"Отчёт сохранён: index.html ({len(html)} байт, {total} отзывов)", flush=True)
