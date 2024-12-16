from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
import time


def setup_driver():
    # 设置Chrome选项
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)

    # 先访问目标域名以便设置cookies
    driver.get("https://ehall.nbu.edu.cn")

    # 设置cookies
    cookies = {
        # 此处添加您的cookies
    }

    # 添加所有cookies
    for name, value in cookies.items():
        driver.add_cookie(
            {
                "name": name,
                "value": value,
                "domain": "ehall.nbu.edu.cn",  # 确保domain与实际域名匹配
            }
        )

    return driver


def main():
    driver = setup_driver()
    wait = WebDriverWait(driver, 20)

    try:
        # 重新加载页面以应用cookies
        driver.get(
            "https://ehall.nbu.edu.cn/portal/html/select_role.html?appId=5002777488276451"
        )
        driver.get(
            "https://ehall.nbu.edu.cn/tw/sys/nd54st/*default/index.do?t_s=1734320119872&amp_sec_version_=1&gid_=bnZnaWhPL0xQM0hsMi9SSS9ybUtpWXhHT3dFeWplNXlldHpOSUxXTi9WRGpKNkJsQWRSNitYcXhTZll1QXBtN3Z0b3ZrRDJwNzl1UzF5cG1TWFlDMlE9PQ&EMAP_LANG=zh&THEME=indigo#/myst"
        )

        # 给页面一些加载时间
        time.sleep(3)

        # 在导航到页面后，等待并点击成员按钮
        member_button = wait.until(
            EC.element_to_be_clickable(
                (
                    By.CSS_SELECTOR,
                    'button.bh-btn.bh-btn-primary.bh-btn-text[data-action="stusers"]',
                )
            )
        )
        # print("Member Button HTML:", member_button.get_attribute("outerHTML"))
        member_button.click()

        # 给页面一些加载时间
        time.sleep(2)

        while True:
            # 等待并点击第二个修改按钮
            buttons = wait.until(
                EC.presence_of_all_elements_located(
                    (
                        By.CSS_SELECTOR,
                        'button.bh-btn.bh-btn-primary.bh-btn-text[data-action="useredit2"]',
                    )
                )
            )
            if len(buttons) >= 2:
                # 输出第二个按钮的data-x-wid属性
                # print("Button data-x-wid:", buttons[1].get_attribute("data-x-wid"))
                buttons[1].click()
            else:
                print("未找到足够的修改按钮")
                return

            # 等待下拉框元素出现
            dropdown = wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, '[data-caption="当前状态"]')
                )
            )

            # 修改属性和值
            driver.execute_script(
                """
                arguments[0].setAttribute('aria-activedescendant', 'listitem2innerListBoxjqxWidget65896715');
                arguments[0].querySelector('input[type="hidden"]').value = '2';
                arguments[0].querySelector('.jqx-dropdownlist-content').textContent = '已退出';
            """,
                dropdown,
            )

            # 如果需要触发相关事件
            driver.execute_script(
                """
                var event = new Event('change', { bubbles: true });
                arguments[0].dispatchEvent(event);
            """,
                dropdown,
            )

            # 点击确定按钮
            confirm_button = wait.until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "button.bh-btn.bh-btn-primary.bh-pull-right")
                )
            )
            confirm_button.click()

            # 等待一会儿以确保操作完成
            time.sleep(1)
            print("社员 - 1")

    except Exception as e:
        print(f"发生错误: {str(e)}")

    finally:
        driver.quit()


if __name__ == "__main__":
    main()
