import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def setup_driver():
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)

    driver.get("https://ehall.nbu.edu.cn")

    cookies = {
        # add cookies here
    }

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
        driver.get(
            "https://ehall.nbu.edu.cn/portal/html/select_role.html?appId=5002777488276451"
        )
        driver.get(
            "https://ehall.nbu.edu.cn/tw/sys/nd54st/*default/index.do?t_s=1734320119872&amp_sec_version_=1&gid_=bnZnaWhPL0xQM0hsMi9SSS9ybUtpWXhHT3dFeWplNXlldHpOSUxXTi9WRGpKNkJsQWRSNitYcXhTZll1QXBtN3Z0b3ZrRDJwNzl1UzF5cG1TWFlDMlE9PQ&EMAP_LANG=zh&THEME=indigo#/myst"
        )

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
            buttons = wait.until(
                EC.presence_of_all_elements_located(
                    (
                        By.CSS_SELECTOR,
                        'button.bh-btn.bh-btn-primary.bh-btn-text[data-action="useredit2"]',
                    )
                )
            )
            if len(buttons) >= 2:
                # print("Button data-x-wid:", buttons[1].get_attribute("data-x-wid"))
                buttons[1].click()
            else:
                print("未找到足够的修改按钮")
                return

            dropdown = wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, '[data-caption="当前状态"]')
                )
            )

            driver.execute_script(
                """
                arguments[0].setAttribute('aria-activedescendant', 'listitem2innerListBoxjqxWidget65896715');
                arguments[0].querySelector('input[type="hidden"]').value = '2';
                arguments[0].querySelector('.jqx-dropdownlist-content').textContent = '已退出';
            """,
                dropdown,
            )

            # event dispatch
            driver.execute_script(
                """
                var event = new Event('change', { bubbles: true });
                arguments[0].dispatchEvent(event);
            """,
                dropdown,
            )

            confirm_button = wait.until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "button.bh-btn.bh-btn-primary.bh-pull-right")
                )
            )
            confirm_button.click()

            time.sleep(1)
            print("社员 - 1")

    except Exception as e:
        print(f"发生错误: {str(e)}")

    finally:
        driver.quit()


if __name__ == "__main__":
    main()
