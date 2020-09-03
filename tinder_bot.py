from selenium import webdriver
import time
from info import password, mail
from random import random
import cv2
import numpy as np
from PIL import ImageGrab, Image
import os
from webdriver_manager.chrome import ChromeDriverManager
import matplotlib.pyplot as plt


class TinderBot():
    def __init__(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())

    def login(self):
        self.driver.get("https://tinder.com/")
    
        time.sleep(4)

        login = self.driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/header/div[1]/div[2]/div/button')
        login.click()

        time.sleep(2)

        fb_button = self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div[1]/div/div[3]/span/div[2]/button')
        fb_button.click()

        base_window = self.driver.window_handles[0]
        pop_up_window = self.driver.window_handles[1]

        self.driver.switch_to_window(pop_up_window)

        email_input = self.driver.find_element_by_xpath('//*[@id="email"]')
        email_input.send_keys(mail)

        pw_in = self.driver.find_element_by_xpath('//*[@id="pass"]')
        pw_in.send_keys(password)

        time.sleep(1)
        login_btn = self.driver.find_element_by_xpath('//*[@id="u_0_0"]')
        login_btn.click()

        self.driver.switch_to_window(base_window)

        time.sleep(6)
        first_pop_up = self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div/div/div[3]/button[1]')
        first_pop_up.click()
        time.sleep(2)
        second_pop_up = self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div/div/div[3]/button[1]')
        second_pop_up.click()
        accept_btn = self.driver.find_element_by_xpath('//*[@id="content"]/div/div[2]/div/div/div[1]/button')
        accept_btn.click()


    def screen_record(self):
        while True:
            self.printscreen = np.array(ImageGrab.grab(bbox=(0, 40, 700, 800)))
            #self.printscreen = self.grab_screen(region=(0,40,800,640))
            #print('loop took {} seconds'.format(time.time() - last_time))
            #last_time = time.time()
            self.face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
            self.gray = cv2.cvtColor(self.printscreen, cv2.COLOR_BGR2GRAY)
            self.faces = self.face_cascade.detectMultiScale(self.gray, 1.1, 4)
            for (x, y, w, h) in self.faces:
                cv2.rectangle(self.gray, (x, y), (x + w, y + h), (255, 0, 0), 2)

            cv2.imshow('window', self.gray)
            #time.sleep(3)
            try:
                if len(self.faces) > 0:
                    self.like()
                    time.sleep(2)
                else:
                    self.dislike()
                    time.sleep(2)

            except Exception:
                try:
                    self.close_popup()

                except Exception:
                    try:
                        self.close_match()
                    except Exception:
                        self.send_how_you_doin()


            if cv2.waitKey(25) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break
    def like(self):
        like_btn = self.driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[2]/div[4]/button')
        like_btn.click()

    def dislike(self):
        dislike_btn = self.driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[2]/div[2]/button')
        dislike_btn.click()

    def auto_swipe(self):
        while True:
            #time.sleep(2)
            #self.like()
            try:
                rand = random()
                print(rand)
                if rand < .73:
                    self.like()
                    time.sleep(2)
                else:
                    self.dislike()
                    time.sleep(2)
            except Exception:
                self.close_popup()
                try:
                    self.close_popup()
                except Exception:
                    #self.close_match()
                    pass

    def close_popup(self):
        popup_3 = self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div[2]/button[2]')
        popup_3.click()

    def close_match(self):
        match_popup = self.driver.find_element_by_xpath('//*[@id="modal-manager-canvas"]/div/div/div[1]/div/div[3]/a')
        match_popup.click()

    def send_message2matches(self):
        matches_tab = self.driver.find_element_by_xpath('//*[@id="match-tab"]')
        matches_tab.click()
        matches = self.driver.find_elements_by_class_name('matchListItem')[1:]
        matches[0].click()
        #msg_box = self.driver.find_elements_by_class_name('sendMessageForm__input')
        msg_box = self.driver.find_element_by_id('chat-text-area')
        msg_box.send_keys('how you doin??')
        send_btn = self.driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div/div[1]/div/div/div[3]/form/button')
        send_btn.click()


    def send_how_you_doin(self):
        matches_tab = self.driver.find_element_by_xpath('//*[@id="match-tab"]')
        matches_tab.click()
        matches = self.driver.find_elements_by_class_name('matchListItem')[1:]
        matches[0].click()
        gif_btn = self.driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div/div[1]/div/div/div[3]/div/div[1]/button')
        time.sleep(3)
        gif_btn.click()
        search_box = self.driver.find_element_by_id('chat-text-area')
        search_box.send_keys('how you doin')
        time.sleep(3)
        gif2send = self.driver.find_elements_by_class_name('gif__messages')
        gif2send[0].click()






url = 'http://localhost/rate_api/'
bot = TinderBot()
bot.login()
time.sleep(2)
like_counter = 0
dislike_counter = 0
while True:
    bot.driver.save_screenshot('img.png')
    img = cv2.imread('img.png', 1)
    img = img[50:650, 420:830]
    cv2.imwrite('img.png', img)
    driver = webdriver.Chrome()
    driver.get(url)
    input_box = driver.find_element_by_xpath('//*[@id="upload"]')
    input_box.send_keys(os.getcwd() + "/img.png")
    time.sleep(7)
    obj = driver.switch_to.alert
    msg = obj.text
    rate = int(msg)
    obj.accept()
    driver.close()
    try:
        if(rate >= 5):
            bot.like()
            like_counter += 1
            print('rate: ', rate, 'num of likes: ', like_counter)
            time.sleep(1)
        else:
            bot.dislike()
            dislike_counter += 1
            print('rate: ', rate, 'num of dislikes: ', dislike_counter)
            time.sleep(1)
    except Exception:
        try:
            bot.close_popup()
            time.sleep(1)
        except Exception:
            pass
            print('I think your likes are finished...')





































"""while True:
    screen = grab_screen(region=(0, 40, 800, 640))
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(screen, 1.1, 4)
    for (x, y, w, h) in faces:
        cv2.rectangle(screen, (x, y), (x + w, y + h), (255, 0, 0), 2)

    cv2.imshow('window', screen)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
    try:
        if(len(faces)>0):
            bot.like()
            time.sleep(1)
        else:
            bot.dislike()
            time.sleep(1)
    except Exception:
        try:
            bot.close_popup()
        except Exception:
            bot.close_match()

    finally:
        try:
            bot.send_how_you_doin()
        except Exception:
            pass
"""
