import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from authorization import cookies


def setup_driver():
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)

    driver.get("https://ehall.nbu.edu.cn")

    for name, value in cookies.items():
        driver.add_cookie(
            {
                "name": name,
                "value": value,
                "domain": "ehall.nbu.edu.cn",
            }
        )

    return driver


def main():
    driver = setup_driver()
    wait = WebDriverWait(driver, 20)

    try:
        driver.get("https://ehall.nbu.edu.cn/tw/sys/nd54st/*default/index.do#/myst")
        time.sleep(3)

        member_button = wait.until(
            EC.element_to_be_clickable(
                (
                    By.CSS_SELECTOR,
                    'button.bh-btn.bh-btn-primary.bh-btn-text[data-action="stusers"]',
                )
            )
        )
        member_button.click()
        time.sleep(2)

        while True:
            retired_member_button = wait.until(
                EC.element_to_be_clickable(
                    (
                        By.CSS_SELECTOR,
                        '.bh-btn.bh-btn-text[data-action="historyUser"]',
                    )
                )
            )
            retired_member_button.click()
            time.sleep(0.3)

            buttons = wait.until(
                EC.presence_of_all_elements_located(
                    (
                        By.CSS_SELECTOR,
                        'button.bh-btn.bh-btn-primary.bh-btn-text[data-action="deluser"]',
                    )
                )
            )
            if len(buttons):
                buttons[0].click()
            else:
                print("unable to find any [deluser] button")
                return

            confirm_button = wait.until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, ".bh-dialog-center a.bh-btn.bh-btn-primary")
                )
            )
            confirm_button.click()
            time.sleep(0.3)

            exit_button = wait.until(
                EC.element_to_be_clickable(
                    (
                        By.CSS_SELECTOR,
                        "div#buttons button.bh-btn.bh-btn-default.bh-pull-right",
                    )
                )
            )
            exit_button.click()

            print("member removed")

    except Exception as e:
        print(f"error: {str(e)}")

    finally:
        driver.quit()


if __name__ == "__main__":
    main()
