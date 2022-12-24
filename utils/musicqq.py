import time
import asyncio
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import os
import traceback
from utils.log import *

class QQMusic():

    async def set_up(self):
        Log.log("QQMUSIC", "set up")
        try:
            d = DesiredCapabilities.CHROME
            d['loggingPrefs'] = {'browser': 'ALL'}
            self.browser = webdriver.Chrome(desired_capabilities=d)
            self.browser.get('https://y.qq.com/')
            self.browser.maximize_window()  # For maximizing window
        except Exception as inst:
            traceback.print_exc()
        await asyncio.sleep(2)

    async def getqrlogin(self):
        Log.log("QQMUSIC", "getqrlogin start")
        try:
            cli = self.browser.find_element("xpath", "/html/body/div[1]/div[1]/div[1]/div[1]/div[2]/span[1]/a[1]")
            cli.click()
            # qr timer only 2 min will need to refresh
            await asyncio.sleep(2)
            self.browser.switch_to.frame(0)
            self.browser.switch_to.frame("ptlogin_iframe")
            await asyncio.sleep(2)
            # 截图保存在本地
            self.browser.get_screenshot_as_file('123.png')
        except Exception as inst:
            traceback.print_exc()
        Log.log("QQMUSIC", "getqrlogin end")
        return '123.png'

    async def testlogin(self, name='思念是一种病'):
        try:
            self.browser.switch_to.default_content()
            serch = self.browser.find_element("xpath", '/html/body/div/div/div[1]/div/div[1]/div[1]/input')
            serch.click()
            serch.clear()
            serch.send_keys(name)
            self.browser.find_element("xpath", '//*[@id="app"]/div/div[1]/div/div[1]/div[1]/button/i').click()
            await asyncio.sleep(1)
            self.browser.find_element("xpath", '//*[@id="app"]/div/div[1]/div/div[1]/div[1]/button/i').click()
            await asyncio.sleep(1)
            button = self.browser.find_element("xpath", '/html/body/div/div/div[1]/div/h1/a')
            self.browser.execute_script("arguments[0].click();", button)
            return True
        except:
            traceback.print_exc()
            return False

    async def findsong(self, song_name):
        try:
            self.browser.refresh()
            self.browser.switch_to.default_content()
            # /html/body/div/div/div[1]/div/div[1]/div[1]/input
            serch = self.browser.find_element("xpath", '/html/body/div/div/div[1]/div/div[1]/div[1]/input')
            serch.click()
            serch.send_keys(song_name)
            self.browser.find_element("xpath", '//*[@id="app"]/div/div[1]/div/div[1]/div[1]/button/i').click()
            await asyncio.sleep(5)
            self.browser.switch_to.window(self.browser.window_handles[-1])
            pa = self.browser.find_element(By.CLASS_NAME, 'songlist__list')
            pa.find_element(By.CLASS_NAME, 'c_tx_highlight').click()
            # browser.find_element("xpath",'/html/body/div/div/div[3]/div/div/div[4]/ul[2]/li[1]/div/div[2]/span/a').click()
            await asyncio.sleep(2)
            self.browser.find_element("xpath", '/html/body/div/div/div[2]/div[1]/div/div[3]/a[1]/span').click()
            await asyncio.sleep(2)
            self.browser.switch_to.window(self.browser.window_handles[-1])
            self.browser.switch_to.default_content()
            url = self.browser.find_element("xpath", '/html/body/audio').get_attribute("src")
            print(url)
            # 播放器跳回主界面
            button = self.browser.find_element("xpath", '/html/body/div/h1/a')
            self.browser.execute_script("arguments[0].click();", button)
            self.browser.switch_to.window(self.browser.window_handles[0])
            self.browser.close()
            self.browser.switch_to.window(self.browser.window_handles[0])
            self.browser.close()
            self.browser.switch_to.window(self.browser.window_handles[0])
            return url
        except Exception as inst:
            traceback.print_exc()
            return None


    async def regetqr(self):
        try:
            button = self.browser.find_element("xpath", '/html/body/div[1]/div[4]/div[8]/div/span')
            self.browser.execute_script("arguments[0].click();", button)
            self.browser.get_screenshot_as_file('123.png')
        except Exception as inst:
            traceback.print_exc()
        return '123.png'

    def kill_chrom(self):
        self.browser.close()
