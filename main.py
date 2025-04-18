from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import datetime
import cv2
import numpy as np
import pyautogui


class ScreenRecorder:
    def __init__(self):
        self.screen_size = pyautogui.size()
        self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.out = None

    def start_recording(self):
        filename = f"booking_record_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
        self.out = cv2.VideoWriter(filename, self.fourcc, 20.0,
                                   (self.screen_size.width, self.screen_size.height))
        print(f"开始录屏，文件将保存为: {filename}")

    def capture_frame(self):
        if self.out is None:
            return
        screenshot = pyautogui.screenshot()
        frame = np.array(screenshot)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        self.out.write(frame)

    def stop_recording(self):
        if self.out is not None:
            self.out.release()
            print("录屏已结束")

def get_day_selection():
    """从用户获取想要预约的星期几"""
    while True:
        print("\n请选择要预约的日期：")
        print("1. 周一")
        print("2. 周二")
        print("3. 周三")
        print("4. 周四")
        print("5. 周五")
        print("6. 周六")
        print("7. 周日")
        try:
            choice = int(input("请输入数字 (1-7): "))
            if 1 <= choice <= 7:
                days = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
                return days[choice - 1]
            print("请输入1-7之间的数字！")
        except ValueError:
            print("请输入有效的数字！")

def get_time_range_selection():
    """从用户获取想要预约的时间段范围"""
    while True:
        try:
            start_time = int(input("\n请输入起始时间段（从上往下第几个，例如：1）: "))
            end_time = int(input("请输入结束时间段（从上往下第几个，例如：5）: "))
            if start_time > 0 and end_time > 0 and start_time <= end_time:
                return start_time, end_time
            print("请输入有效的时间段范围！起始时间必须小于等于结束时间。")
        except ValueError:
            print("请输入有效的数字！")




class VenueBooking:

    def __init__(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)
        self.target_url = "http://h5-tycg.dlut.edu.cn/#/?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhTWFzVHtbS2labUZEa1YiLCJhdWQiOiIiLCJpYXQiOjE3NDAzNjUyMDUsIm5iZiI6MTc0MDM2NTIwNSwiZXhwIjoxNzQxMjUxNjA1LCJkYXRhIjp7Im1lbWJlcl9pZCI6IjIyNDAzMTI1Iiwib3JnX2lkIjoiMDAwMzI2IiwibWVtYmVyX25hbWUiOiJcdTVmMjBcdTczY2YiLCJtZW1iZXJfc2V4IjoiXHU3NTM3IiwibWVtYmVyX3Bob25lIjoiMTU2Mzc3Mjc5MTAiLCJtZW1iZXJfdHlwZSI6Ilx1NjcyY1x1NjgyMVx1NWI2Nlx1NzUxZiIsIm1lbWJlcl9waG90byI6Ii9kbGxnaW1hZ2VzL2ZhY2UvMjI0MDMxMjUvMjI0MDMxMjVfc21hbGwuanBnIiwicHJvamVjdF9pZCI6MTAwNzJ9fQ.Y8jnqe_Zql0YxF-z2uRMcUzj9m1lfIyGUnDcTaLduxA"
        self.selected_day = None
        self.start_time = None   # 起始时间
        self.end_time = None     # 结束时间

    def open_page(self):
        """打开目标页面"""
        try:
            print("正在打开场馆预约页面...")
            self.driver.get(self.target_url)
            time.sleep(1)  # 等待页面加载
            print("页面加载成功")
        except Exception as e:
            print(f"打开页面失败: {str(e)}")
            raise

    def click_booking_button(self):
        """点击场地预定按钮"""
        try:
            # 使用文本内容定位按钮
            booking_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//div[@class='uni-tabbar__label' and contains(text(), '场地预定')]"))
            )

            try:
                booking_button.click()
                time.sleep(1)  # 等待页面加载
            except:
                # 如果直接点击失败，尝试使用JavaScript点击
                self.driver.execute_script("arguments[0].click();", booking_button)

            print("场地预定按钮点击成功")

        except Exception as e:
            raise

    def venue_button(self):
            try:
                print("等待去预约按钮出现...")

                """#选择什么球馆只需要把中文名替换即可"""
                venue_button_button  = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH,
                        "//uni-view[contains(@class, 'd-font-28')][contains(text(), '西山体育中心羽毛球场')]/../following-sibling::uni-view//uni-button//uni-view[text()='去预约']"
                    ))
                )

                try:
                    venue_button_button.click()
                    time.sleep(1)  # 等待页面加载
                except:
                    # 如果直接点击失败，尝试使用JavaScript点击
                    self.driver.execute_script("arguments[0].click();", venue_button_button)

                print("去预约点击成功")
                time.sleep(1)  # 等待页面响应

            except Exception as e:
                raise

    def time_button(self):
        """只需要把时间修改即可"""
        try:
            saturday_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH,
                    f"//uni-view[contains(@class, 'wk') and contains(text(), '{self.selected_day}')]"))
            )
            try:
                saturday_button .click()
                print("时间成功")
                time.sleep(5)  # 等待页面响应

            except:
                # 如果直接点击失败，尝试使用JavaScript点击
                self.driver.execute_script("arguments[0].click();", saturday_button )
        except Exception as e:
            raise

    def address_button(self):
        """遍历所有场地(1-15)和指定时间段寻找可预约的场地，尝试三次"""
        max_attempts = 3
        attempt = 1

        while attempt <= max_attempts:
            try:
                print(f"\n第 {attempt} 次尝试检查所有场地...")

                # 遍历所有场地(1-15)
                for court_num in range(1, 16):  # 1到15号场地
                    try:
                        # 等待并获取当前场地元素
                        court = self.wait.until(
                            EC.presence_of_element_located((By.XPATH,
                                                            f"//uni-view[contains(@class, 'wz')][.//uni-view[contains(@class, 'head') and contains(text(), '{court_num}')]]"
                                                            ))
                        )
                        print(f"\n正在检查 {court_num} 号场地")

                        # 获取该场地的所有时间段
                        time_slots = court.find_elements(By.XPATH, ".//uni-view[contains(@class, 'option')]")
                        search_range = range(self.start_time - 1, min(self.end_time, len(time_slots)))

                        # 遍历指定范围内的时间段
                        for index in search_range:
                            slot = time_slots[index]
                            # 检查时间段是否可预约
                            if 'none' not in slot.get_attribute('class'):
                                try:
                                    slot.click()
                                    print(f"找到可预约场地")
                                    return True
                                except:
                                    continue

                    except Exception as e:
                        print(f"检查 {court_num} 号场地时出错: {str(e)}")
                        continue

                print(f"\n第 {attempt} 次检查完毕，未找到可预约的时段")
                attempt += 1
                if attempt <= max_attempts:
                    print("等待2秒后进行下一次尝试...")
                    time.sleep(2)  # 在重试之前等待1秒

            except Exception as e:
                print(f"查找可用场地和时间段时发生错误: {str(e)}")
                raise

        print("\n三次尝试都未找到可预约时段")
        return False

    def true_button(self):
        """最后一步预定"""
        try:
            court_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH,
                                            "//uni-button[contains(@class, 'u-button--primary')]//uni-view[contains(@class, 'd-font-30') and text()='预定场地']"
                                            ))
            )
            try:
                court_button.click()
                print("场地选择成功")
            except:
                # 如果直接点击失败，尝试使用JavaScript点击
                self.driver.execute_script("arguments[0].click();", court_button)
        except Exception as e:
            raise



    def buy_button(self):
        """最后一步预定"""
        try:
            buy_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH,
                                            "//uni-button[contains(@class, 'u-button--primary')]//text()[contains(., '立即购买')]/ancestor::uni-button"
                                            ))
            )
            try:
                buy_button.click()
                print("倒数第三步")
            except:
                # 如果直接点击失败，尝试使用JavaScript点击
                self.driver.execute_script("arguments[0].click();", buy_button)
        except Exception as e:
            raise

    def know_button(self):
            """最后一步预定"""
            try:
                buy_button = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH,
                        "//uni-button[contains(@class, 'u-button--primary') and contains(@style, 'background: rgb(89, 160, 255)')][.='我知道了']"
                    ))
                )
                try:
                    buy_button.click()
                    print("我知道了")
                except:
                    # 如果直接点击失败，尝试使用JavaScript点击
                    self.driver.execute_script("arguments[0].click();", buy_button)
            except Exception as e:
                raise

    def finish1_button(self):
        """最后一步预定"""
        try:
            buy_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH,
                                            "//uni-button[contains(@class, 'u-button--primary') and .//text()='提交订单']"
                                            ))
            )
            try:
                buy_button.click()
                print("已经点击玉兰卡支付")
            except:
                # 如果直接点击失败，尝试使用JavaScript点击
                self.driver.execute_script("arguments[0].click();", buy_button)
        except Exception as e:
            raise

    def finish2_button(self):
        """最后一步预定"""
        try:
            buy_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH,
                                            "//uni-button[contains(@class, 'u-button--primary') and contains(@style, 'background: rgb(89, 160, 255)')][not(contains(@style, 'display: none'))]"
                                            ))
            )
            try:
                buy_button.click()
                print("玉兰卡支付成功")
            except:
                # 如果直接点击失败，尝试使用JavaScript点击
                self.driver.execute_script("arguments[0].click();", buy_button)
        except Exception as e:
            raise




def wait_until_time(target_hour=18, target_minute=0, target_second=0):
    """
    等待直到指定时间
    :param target_hour: 目标小时（24小时制）
    :param target_minute: 目标分钟
    :param target_second: 目标秒数
    """
    while True:
        now = datetime.datetime.now()
        # 设置目标时间
        target_time = now.replace(hour=target_hour, minute=target_minute, second=target_second, microsecond=0)

        # 如果当前时间已经过了今天的目标时间，就等待到明天
        if now >= target_time:
            target_time = target_time + datetime.timedelta(days=1)





        # 计算需要等待的时间
        wait_seconds = (target_time - now).total_seconds()

        if wait_seconds <= 20:  # 如果离目标时间小于60秒
            print(f"距离抢票时间还有{wait_seconds}秒...")
            if wait_seconds <= 1:
                break
            time.sleep(0.2)  # 最后一分钟每0.1秒检查一次


def get_target_time_from_user():
    """从用户获取目标抢票时间"""
    while True:
        try:
            print("\n请输入抢票时间（24小时制）")
            hour = int(input("小时 (0-23): "))
            minute = int(input("分钟 (0-59): "))
            second = int(input("秒数 (0-59): "))

            # 验证输入的有效性
            if 0 <= hour <= 23 and 0 <= minute <= 59 and 0 <= second <= 59:
                return hour, minute, second
            else:
                print("请输入有效的时间！")
        except ValueError:
            print("请输入有效的数字！")


def main():
    bot = VenueBooking()
    recorder = ScreenRecorder()
    try:
        print("\n=== 场地预约系统 ===")
        print("等待抢票时间...")
        hour, minute, second = get_target_time_from_user()

        # 获取用户选择的日期和时间范围
        bot.selected_day = get_day_selection()
        bot.start_time, bot.end_time = get_time_range_selection()
        print(f"\n系统将在 {hour:02d}:{minute:02d}:{second:02d} 开始抢票...")
        print(f"时间范围: 第{bot.start_time}-{bot.end_time}个时段")
        wait_until_time(hour, minute, second)
        print("开始抢票!")
        recorder.start_recording()

        def record():
            while True:
                try:
                    recorder.capture_frame()
                    time.sleep(0.05)  # 20 FPS
                except:
                    break

        import threading
        recording_thread = threading.Thread(target=record)
        recording_thread.daemon = True
        recording_thread.start()

        bot.open_page()
        bot.click_booking_button()
        bot.venue_button()
        bot.time_button()
        if bot.address_button():  # 如果找到可用场地和时段
            bot.true_button()
            bot.buy_button()
            bot.know_button()
            bot.finish1_button()
            bot.finish2_button()
            print("预约成功！")
        else:
            print("预约失败：没有找到可用场地和时段")
        recorder.stop_recording()


        # 调试用：保持窗口打开
        input("按回车键继续...")
    except Exception as e:
        time.sleep(15)  # 等待页面响应
        print(f"发生错误")
        recorder.stop_recording()



if __name__ == "__main__":
    main()