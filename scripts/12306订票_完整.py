from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import openpyxl
import time


class TrainSpider(object):
    login_url = 'https://kyfw.12306.cn/otn/resources/login.html'
    user_url = 'https://kyfw.12306.cn/otn/view/index.html'
    left_ticket = 'https://kyfw.12306.cn/otn/leftTicket/init?linktypeid=dc'
    confirm_url = 'https://kyfw.12306.cn/otn/confirmPassenger/initDc'

    def __init__(self, from_station, to_station, train_date, train_select, passenger_list):
        self.from_station = from_station
        self.to_station = to_station
        self.train_date = train_date
        self.station_code = self.init_station_code()
        self.train_select = train_select
        self.passenger_list = passenger_list
        self.selected_no = None

        # 初始化浏览器
        options = Options()
        # 设置代理
        # options.add_argument('--proxy-server=http://代理IP:端口')
        # 或者使用认证代理
        # options.add_argument('--proxy-server=http://用户名:密码@代理IP:端口')

        #不显示浏览器界面
        # options.add_argument('--headless')
        # 这行代码的作用是让Chrome浏览器在Python脚本执行完毕后保持打开状态，而不是自动关闭
        options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(service=Service(executable_path=r'D:\chromedriver-win64\chromedriver.exe'), options=options)

    def init_station_code(self):
        wb = openpyxl.load_workbook('车站代码.xlsx')
        ws = wb.active
        return {row[0].value: row[1].value for row in ws.rows}
    def login(self):
        self.driver.get(self.login_url)
        print("请手动完成登录...")
        WebDriverWait(self.driver, 1000).until(
            ec.text_to_be_present_in_element((By.CSS_SELECTOR, '.welcome-name'), '付理想')
        )
        print('登录成功')
    def leave_ticket(self):
        self.driver.get(self.left_ticket)
        #设置cookies

        cookies = [
            {'name': 'JSESSIONID', 'value': 'A3ABF98B7D51C46698E503026AB24DF1'},
            {'name': 'tk', 'value': '-HjJw7grmBd9kmvGdXJoTeBHKy3_-iAHNITMLRiYRv0nxF1F0'},
            {'name': 'guidesStatus', 'value': 'off'},
            {'name': 'highContrastMode', 'value': 'defaltMode'},
            {'name': 'cursorStatus', 'value': 'off'},
            {'name': 'BIGipServerotn', 'value': '1943601418.24610.0000'},
            {'name': 'BIGipServerpassport', 'value': '837288202.50215.0000'},
            {'name': 'route', 'value': '6f50b51faa11b987e576cdb301e545c4'},
            {'name': '_jc_save_fromStation', 'value': '%u5317%u4EAC%2CBJP'},
            {'name': '_jc_save_toStation', 'value': '%u4E0A%u6D77%2CSHH'},
            {'name': '_jc_save_fromDate', 'value': '2025-04-18'},
            {'name': '_jc_save_toDate', 'value': '2025-04-10'},
            {'name': '_jc_save_wfdc_flag', 'value': 'dc'}
        ]

        for cookie in cookies:
            self.driver.add_cookie(cookie)
        self.driver.refresh()
        self.driver.implicitly_wait(10)

        # 设置出发站、到达站和日期
        from_station_code = self.station_code[self.from_station]
        to_station_code = self.station_code[self.to_station]
        #刷新页面
        self.driver.refresh()
        time.sleep(1)
        self.driver.execute_script(
            f"document.getElementById('fromStation').value='{from_station_code}';"
            f"document.getElementById('toStation').value='{to_station_code}';"
            f"document.getElementById('train_date').value='{self.train_date}';"
        )
        # 点击查询按钮
        WebDriverWait(self.driver, 10).until(
            ec.element_to_be_clickable((By.ID, 'query_ticket'))
        ).click()

        # 等待车次信息加载
        tt =WebDriverWait(self.driver, 30).until(
            ec.presence_of_all_elements_located((By.XPATH, '//*[@id="queryLeftTable"]/tr[not(@datatran)]'))
        )

        # 查找符合条件的车次
        trains = self.driver.find_elements(By.XPATH, '//*[@id="queryLeftTable"]/tr[not(@datatran)]')
        for train in trains:
            info = train.text.replace('\n', ' ').split(' ')
            train_num = info[0]

            if train_num in self.train_select:
                seat_types = self.train_select[train_num]
                for seat_type in seat_types:
                    seat_idx = 11 if seat_type == 'O' else 10
                    count = info[seat_idx]

                    if count.isdigit() or count == '有':
                        self.selected_no = train_num
                        try:
                            WebDriverWait(self.driver, 10).until(
                                ec.element_to_be_clickable((By.CLASS_NAME, 'btn72'))
                            ).click()
                            return True
                        except Exception as e:
                            print(f"点击预定按钮失败: {e}")
                            continue
        return False
    def confirm(self):
        # 等待订单确认页面加载
        time.sleep(1)
        WebDriverWait(self.driver, 1000).until(
            ec.text_to_be_present_in_element((By.CSS_SELECTOR, '#submitOrder_id'), '提交订单')
        )

        # 选择乘车人
        passengers = self.driver.find_elements(By.XPATH, '//*[@id="normal_passenger_id"]/li/label')
        for p in passengers:
            if p.text in self.passenger_list:
                p.click()

        # 选择席别
        seat_select = Select(self.driver.find_element(By.ID, 'seatType_1'))
        for seat_type in self.train_select[self.selected_no]:
            try:
                seat_select.select_by_value(seat_type)
                break
            except NoSuchElementException:
                continue

        # 提交订单
        self.driver.find_element(By.ID, 'submitOrder_id').click()
        time.sleep(5)
        # 确认订单
        # WebDriverWait(self.driver, 10).until(
        #     ec.presence_of_element_located((By.ID, 'qr_submit_id'))
        # ).click()
        time.sleep(10)

        print("订票成功")
    def run(self):
        try:
            # self.login()
            if self.leave_ticket():
                self.confirm()
            else:
                print("没有找到符合条件的车次")
        except Exception as e:
            print(f"订票失败: {e}")
        finally:
            self.driver.quit()


def start():
    spider = TrainSpider(
        from_station='北京',
        to_station='上海',
        train_date='2025-04-17',
        train_select={'G103': ['O', 'M']},
        passenger_list=['付理想']
    )
    spider.run()


if __name__ == '__main__':
    start()