import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

def qqurlget(username,password,song_name):
    d = DesiredCapabilities.CHROME
    d['loggingPrefs'] = { 'browser':'ALL' }
    browser=webdriver.Chrome(desired_capabilities=d)
    browser.get('https://y.qq.com/')
    browser.maximize_window() # For maximizing window
    time.sleep(3)
    cli=browser.find_element("xpath","/html/body/div[1]/div[1]/div[1]/div[1]/div[2]/span[1]/a[1]")
    cli.click()
    #print('1')
    time.sleep(2)
    browser.switch_to.frame(0)
    browser.switch_to.frame("ptlogin_iframe")
    clic=browser.find_element("id","switcher_plogin")
    clic.click()
    #print('2')进入输入登录
    usern=browser.find_element("id","u")
    usern.click()
    usern.clear()
    usern.send_keys(username)
    passw=browser.find_element("id","p")
    passw.click()
    passw.clear()
    passw.send_keys(password)
    submi=browser.find_element("xpath","//*[@id='login_button']")
    submi.click()
    #print('5')登陆完成
    time.sleep(60)
    #nwb='https://y.qq.com/n/ryqq/search?w='+song_name
    browser.switch_to.default_content()
    serch=browser.find_element("xpath",'/html/body/div/div/div[1]/div/div[1]/div[1]/input')
    serch.clear()
    serch.send_keys(song_name)
    browser.find_element("xpath",'//*[@id="app"]/div/div[1]/div/div[1]/div[1]/button/i').click()
    #print('6')播放歌曲
    time.sleep(3)
    browser.switch_to.window(browser.window_handles[-1])
    pa=browser.find_element(By.CLASS_NAME,'songlist__list')
    pa.find_element(By.CLASS_NAME,'c_tx_highlight').click()
    #browser.find_element("xpath",'/html/body/div/div/div[3]/div/div/div[4]/ul[2]/li[1]/div/div[2]/span/a').click()
    time.sleep(5)
    browser.find_element("xpath",'/html/body/div/div/div[2]/div[1]/div/div[3]/a[1]/span').click()
    time.sleep(5)
    #print('7')按键播放跳player地址
    browser.switch_to.window(browser.window_handles[-1])
    browser.switch_to.default_content()
    url=browser.find_element("xpath",'/html/body/audio').get_attribute("src")
    #print('8')下载url
    return url

