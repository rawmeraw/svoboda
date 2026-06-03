import json
from datetime import datetime, timezone, timedelta

import undetected_chromedriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains

ID_YA = 232553880063
url = f'https://yandex.ru/maps/org/{ID_YA}/reviews/'

CUTOFF_DATE = datetime.now(timezone.utc) - timedelta(days=365)

opts = undetected_chromedriver.ChromeOptions()
opts.add_argument('--no-sandbox')
opts.add_argument('--disable-dev-shm-usage')
opts.add_argument('--disable-gpu')
opts.add_argument('--remote-debugging-port=0')
opts.binary_location = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'

driver = undetected_chromedriver.Chrome(options=opts)
driver.get(url)

import time

time.sleep(5)

# Sort by newest
sort_btn = driver.find_element(By.CLASS_NAME, "rating-ranking-view")
actions = ActionChains(driver)
actions.move_to_element(sort_btn).click().perform()
time.sleep(1)

newest_btn = driver.find_element(By.XPATH, "//*[contains(text(), 'По новизне')]")
newest_btn.click()
time.sleep(2)
print("Sorted by newest", flush=True)

def parse_review(card):
    try:
        name = card.find_element(By.XPATH, ".//span[@itemprop='name']").text
    except NoSuchElementException:
        name = None
    try:
        icon_style = card.find_element(By.XPATH, ".//div[@class='user-icon-view__icon']").get_attribute('style')
        icon_href = icon_style.split('"')[1]
    except NoSuchElementException:
        icon_href = None
    try:
        date = card.find_element(By.XPATH, ".//meta[@itemprop='datePublished']").get_attribute('content')
    except NoSuchElementException:
        date = None
    try:
        more_btns = card.find_elements(By.XPATH, ".//*[contains(@class,'expand') or contains(@class,'more') or contains(@class,'show-more')]")
        if not more_btns:
            more_btns = card.find_elements(By.XPATH, ".//button[.='ещё' or .='Читать полностью' or .='Показать полностью']")
        for btn in more_btns:
            try:
                driver.execute_script("arguments[0].click(); arguments[0].remove();", btn)
                time.sleep(0.3)
            except:
                pass
        text = card.find_element(By.XPATH, ".//div[@class='business-review-view__body']").text
        if text:
            text = text.rstrip('…').rstrip(' \n\r\t')
    except NoSuchElementException:
        text = None
    try:
        stars_els = card.find_elements(By.CSS_SELECTOR, "[class*='rating-badge-view__stars'] > span")
        stars = sum(1 for s in stars_els if '_empty' not in s.get_attribute('class'))
    except NoSuchElementException:
        stars = 0
    try:
        answer_btn = card.find_element(By.CLASS_NAME, "business-review-view__comment-expand")
        driver.execute_script("arguments[0].click()", answer_btn)
        time.sleep(0.5)
        answer = card.find_element(By.CLASS_NAME, "business-review-comment-content__bubble").text
    except NoSuchElementException:
        answer = None
    return {
        "name": name,
        "icon_href": icon_href,
        "date": date,
        "text": text,
        "stars": stars,
        "answer": answer,
    }

def parse_date(review):
    d = review.get("date")
    if not d:
        return None
    try:
        return datetime.strptime(d, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=timezone.utc)
    except ValueError:
        return None

reviews = []
stale_rounds = 0
scroll_count = 0
reached_cutoff = False

while not reached_cutoff and stale_rounds < 3:
    time.sleep(3)
    cards = driver.find_elements(By.CLASS_NAME, "business-reviews-card-view__review")
    old_count = len(reviews)
    
    for card in cards[old_count:]:
        r = parse_review(card)
        dt = parse_date(r)
        if dt and dt < CUTOFF_DATE:
            reached_cutoff = True
            break
        reviews.append(r)
    
    if len(reviews) == old_count:
        stale_rounds += 1
    else:
        stale_rounds = 0
    
    scroll_count += 1
    print(f"Scroll {scroll_count}: {len(reviews)} reviews loaded", flush=True)
    
    if not reached_cutoff:
        driver.execute_script("arguments[0].scrollIntoView({behavior:'instant',block:'end'});", cards[-1])
        driver.execute_script("""
            var c = arguments[0].closest('.scroll__container') || 
                    document.querySelector('.scroll__container');
            if (c) c.scrollTop = c.scrollHeight;
        """, cards[-1])

company_name = None
try:
    company_name = driver.find_element(By.XPATH, ".//h1[@class='orgpage-header-view__header']").text
except NoSuchElementException:
    pass

driver.quit()

output = {
    "parsed_at": datetime.now().isoformat(),
    "company_id": ID_YA,
    "company_info": {"name": company_name} if company_name else {},
    "cutoff_date": CUTOFF_DATE.isoformat(),
    "total_scrolled": scroll_count,
    "reviews": reviews,
}

with open("reviews.json", "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

text_count = sum(1 for r in reviews if r.get("text"))
print(f"Сохранено {len(reviews)} отзывов за последний год (с {CUTOFF_DATE.date()})", flush=True)
print(f"Из них с текстом: {text_count}", flush=True)
