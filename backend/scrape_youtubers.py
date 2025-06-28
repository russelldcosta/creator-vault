from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
import time
import random
from main import save_youtuber

DRIVER_PATH = r"C:\Users\russe\OneDrive\Desktop\chromedriver-win64\chromedriver.exe"
TAG_PAGE = "https://itch.io/games/tag-horror"
EMAIL_QUOTA = 1


def human_sleep(min_s=1.0, max_s=2.5):
    time.sleep(random.uniform(min_s, max_s))


def human_move(driver, element):
    try:
        size = element.size
        actions = ActionChains(driver)
        for _ in range(random.randint(2, 4)):
            x_offset = random.randint(1, size['width'] - 1)
            y_offset = random.randint(1, size['height'] - 1)
            actions.move_by_offset(x_offset, y_offset).pause(random.uniform(0.2, 0.5))
        actions.move_to_element(element).perform()
    except:
        pass


def browser():
    opts = webdriver.ChromeOptions()
    opts.add_experimental_option("excludeSwitches", ["enable-automation"])
    opts.add_experimental_option("useAutomationExtension", False)
    return webdriver.Chrome(service=Service(DRIVER_PATH), options=opts)


def extract_channel_info(driver, iframe, seen):
    try:
        vid = iframe.get_attribute("src").split("/embed/")[-1].split("?")[0]
        driver.get(f"https://www.youtube.com/watch?v={vid}")
        WebDriverWait(driver, 5).until(EC.presence_of_element_located(
            (By.TAG_NAME, "ytd-video-primary-info-renderer")
        ))
        human_sleep(1.5, 2.5)

        # Get channel element
        channel_el = driver.find_element(By.XPATH, "//ytd-video-owner-renderer//a")
        channel_url = channel_el.get_attribute("href")
        if channel_url in seen:
            return None
        seen.add(channel_url)

        channel_name = channel_el.text.strip()

        # ✅ FIRST: go to /about to get email (this fixes the issue)
        driver.get(channel_url.rstrip("/") + "/about")
        WebDriverWait(driver, 5).until(EC.presence_of_element_located(
            (By.ID, "additional-info-container")
        ))
        human_sleep(1.5, 2.5)

        more_info = driver.find_element(By.ID, "additional-info-container")
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth'});", more_info)
        human_sleep(1.5, 2.5)

        view_btn = WebDriverWait(driver, 5).until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "#view-email-button-container button")
        ))
        human_move(driver, view_btn)
        view_btn.click()
        human_sleep(2.5, 3.5)

        anchor_iframe = WebDriverWait(driver, 5).until(EC.presence_of_element_located(
            (By.XPATH, "//iframe[contains(@src,'api2/anchor')]")
        ))
        driver.switch_to.frame(anchor_iframe)

        tick = WebDriverWait(driver, 5).until(EC.element_to_be_clickable(
            (By.ID, "recaptcha-anchor")
        ))
        human_move(driver, tick)
        tick.click()
        human_sleep(4.5, 6.0)

        driver.switch_to.default_content()

        submit_btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
            (By.ID, "submit-btn")
        ))
        human_move(driver, submit_btn)
        human_sleep(1.5, 3.0)
        submit_btn.click()
        human_sleep(2.5, 4.0)

        email_el = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.ID, "email")
        ))
        email = email_el.text.strip()

        # ✅ THEN: go to homepage to get subscriber count (safer this way)
        driver.get(channel_url)
        sub_el = WebDriverWait(driver, 5).until(EC.presence_of_element_located(
            (By.ID, "subscriber-count")
        ))
        subscribers = sub_el.text.strip().replace(" subscribers", "").replace(",", "")
        try:
            if "K" in subscribers:
                subscribers = int(float(subscribers.replace("K", "")) * 1_000)
            elif "M" in subscribers:
                subscribers = int(float(subscribers.replace("M", "")) * 1_000_000)
            else:
                subscribers = int(subscribers)
        except:
            subscribers = None

        return {
            "username": channel_name,
            "link": channel_url,
            "email": email,
            "subscribers": subscribers,
            "genre": "horror"
        }

    except Exception as e:
        print("❌ Failed to extract info:", e)
        return None


def main():
    driver = browser()
    wait = WebDriverWait(driver, 10)
    seen = set()
    emails = []

    try:
        driver.get("https://www.youtube.com/")
        input("🔐 Sign in to YouTube in the opened window, then type 'continue' & press Enter → ")

        driver.get(TAG_PAGE)
        games = [a.get_attribute("href") for a in wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".game_cell a.thumb_link"))
        )][:10]

        for game_url in games:
            if len(emails) >= EMAIL_QUOTA:
                break
            driver.get(game_url)
            time.sleep(2)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            human_sleep(1.2, 2.2)

            iframes = driver.find_elements(By.XPATH, "//iframe[contains(@src,'youtube.com/embed')]")
            for frame in iframes:
                if len(emails) >= EMAIL_QUOTA:
                    break
                data = extract_channel_info(driver, frame, seen)
                if data:
                    print("✅ Collected:", data)
                    emails.append(data["email"])
                    save_youtuber(**data)
                else:
                    print("– No email, skipping…")

                human_sleep(1.0, 2.0)

        print(f"\n🎉 Done: Collected {len(emails)} emails →", emails)

    finally:
        driver.quit()


if __name__ == "__main__":
    main()
