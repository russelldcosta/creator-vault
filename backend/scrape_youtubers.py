import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Setup Chrome options
options = uc.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-blink-features=AutomationControlled")

# Specify path to correct ChromeDriver (v137)
driver = uc.Chrome(
    driver_executable_path=r"C:\Users\russe\OneDrive\Desktop\chromedriver-win64\chromedriver.exe",
    options=options
)

try:
    # 1. Open the itch.io horror tag page
    driver.get("https://itch.io/games/tag-horror")
    print("✅ Opened itch.io horror games page")

    # 2. Click the first game listed
    wait = WebDriverWait(driver, 15)
    first_game = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".game_cell a.thumb_link")))
    game_url = first_game.get_attribute("href")
    driver.get(game_url)
    print(f"🎮 Opened first game: {game_url}")

    # 3. Scroll down to the comments section
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)

    # 4. Wait for a YouTube link in the comments and click it
    try:
        yt_link = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//a[contains(@href,'youtube.com/watch')]")
        ))
        yt_url = yt_link.get_attribute("href")
        print(f"📺 Found YouTube link: {yt_url}")
        yt_link.click()
    except Exception as e:
        print("❌ Could not find a YouTube link in comments.")
        with open("debug_comments_page.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        raise e

    # At this point, YouTube has opened in a new tab or same tab
    time.sleep(3)

    # Optional: Grab channel link from video page
    channel_link = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//a[contains(@href, '/@')]")
    ))
    channel_url = channel_link.get_attribute("href")
    print(f"📡 Youtuber's channel: {channel_url}")

    # You can continue now to open /about, tick email checkbox, and fetch email
    # 🛑 This step will need more logic (captcha detection & solving, etc.)

except Exception as ex:
    print("⚠️ Error during scraping:", ex)
finally:
    driver.quit()
