from selenium import webdriver
import time
from info import password, mail
import cv2
import os
from webdriver_manager.chrome import ChromeDriverManager
import sys


class TinderBot():
    def __init__(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        # self.driver = webdriver.Chrome()

    def login(self):
        self.driver.get("https://tinder.com/")

        time.sleep(4)
        login = self.driver.find_element_by_xpath(
            '//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div/div/header/div/div[2]/div[2]/button')
        # login = self.driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/header/div[1]/div[2]/div/button')
        login.click()

        time.sleep(2)

        fb_button = self.driver.find_element_by_xpath(
            '//*[@id="modal-manager"]/div/div/div[1]/div/div[3]/span/div[2]/button')
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
        time.sleep(1)
        # ok_button = self.driver.find_element_by_xpath('//*[@id="platformDialogForm"]/div[3]/div/table/tbody/tr/td[2]/button[2]')
        # ok_button.click()
        self.driver.switch_to_window(base_window)

        time.sleep(6)
        first_pop_up = self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div/div/div[3]/button[1]')
        first_pop_up.click()
        time.sleep(2)
        second_pop_up = self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div/div/div[3]/button[1]')
        second_pop_up.click()
        accept_btn = self.driver.find_element_by_xpath('//*[@id="content"]/div/div[2]/div/div/div[1]/button')
        accept_btn.click()
        time.sleep(2)
        self.close_gold_pop_up()

    def like(self):
        like_btn = self.driver.find_element_by_xpath(
            '//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[2]/div[4]/button')
        like_btn.click()

    def dislike(self):
        dislike_btn = self.driver.find_element_by_xpath(
            '//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[2]/div[2]/button')
        dislike_btn.click()

    def close_popup(self):
        popup_3 = self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div[2]/button[2]')
        popup_3.click()

    def close_match(self):
        match_popup = self.driver.find_element_by_xpath('//*[@id="modal-manager-canvas"]/div/div/div[1]/div/div[3]/a')
        match_popup.click()

    def close_plat_pop_up(self):
        plat_pop_up = self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/button[2]')
        plat_pop_up.click()

    def close_gold_pop_up(self):
        gold_pop_up = self.driver.find_element_by_xpath('/html/body/div[2]/div/div/div/div[3]/button[2]')
        gold_pop_up.click()

    def send_message2matches(self):
        matches_tab = self.driver.find_element_by_xpath('//*[@id="match-tab"]')
        matches_tab.click()
        matches = self.driver.find_elements_by_class_name('matchListItem')[1:]
        matches[0].click()
        msg_box = self.driver.find_element_by_id('chat-text-area')
        msg_box.send_keys('how you doin??')
        send_btn = self.driver.find_element_by_xpath(
            '//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div/div[1]/div/div/div[3]/form/button')
        send_btn.click()

    def send_how_you_doin(self):
        matches_tab = self.driver.find_element_by_xpath('//*[@id="match-tab"]')
        matches_tab.click()
        matches = self.driver.find_elements_by_class_name('matchListItem')[1:]
        matches[0].click()
        gif_btn = self.driver.find_element_by_xpath(
            '//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div/div[1]/div/div/div[3]/div/div[1]/button')
        time.sleep(3)
        gif_btn.click()
        search_box = self.driver.find_element_by_id('chat-text-area')
        search_box.send_keys('how you doin')
        time.sleep(3)
        gif2send = self.driver.find_elements_by_class_name('gif__messages')
        gif2send[0].click()

    def send_message_to_match(self):
        message_box = self.driver.find_element_by_id('chat-text-area')
        message_box.send_keys("pick-up line")
        send_button = self.driver.find_element_by_xpath(
            '//*[@id="modal-manager-canvas"]/div/div/div[1]/div/div[3]/div[3]/form/button')
        send_button.click()

    def exit_program(self):
        end_of_likes_pop_up = self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div[3]/button')
        sys.exit()


def highlightFace(net, frame, conf_threshold=0.7):
    frameOpencvDnn = frame.copy()
    frameHeight = frameOpencvDnn.shape[0]
    frameWidth = frameOpencvDnn.shape[1]
    blob = cv2.dnn.blobFromImage(frameOpencvDnn, 1.0, (300, 300), [104, 117, 123], True, False)

    net.setInput(blob)
    detections = net.forward()
    faceBoxes = []
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > conf_threshold:
            x1 = int(detections[0, 0, i, 3] * frameWidth)
            y1 = int(detections[0, 0, i, 4] * frameHeight)
            x2 = int(detections[0, 0, i, 5] * frameWidth)
            y2 = int(detections[0, 0, i, 6] * frameHeight)
            faceBoxes.append([x1, y1, x2, y2])
            cv2.rectangle(frameOpencvDnn, (x1, y1), (x2, y2), (0, 255, 0), int(round(frameHeight / 150)), 8)
    return frameOpencvDnn, faceBoxes


def detect_gender(frame):
    faceProto = "opencv_face_detector.pbtxt"
    faceModel = "opencv_face_detector_uint8.pb"

    genderProto = "gender_deploy.prototxt"
    genderModel = "gender_net.caffemodel"

    MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
    global gender
    genderList = ['Male', 'Female']
    padding = 20
    faceNet = cv2.dnn.readNet(faceModel, faceProto)
    genderNet = cv2.dnn.readNet(genderModel, genderProto)
    resultImg, faceBoxes = highlightFace(faceNet, frame)
    for faceBox in faceBoxes:
        face = frame[max(0, faceBox[1] - padding):
                     min(faceBox[3] + padding, frame.shape[0] - 1), max(0, faceBox[0] - padding)
                                                                    :min(faceBox[2] + padding, frame.shape[1] - 1)]

        blob = cv2.dnn.blobFromImage(face, 1.0, (227, 227), MODEL_MEAN_VALUES, swapRB=False)
        genderNet.setInput(blob)
        genderPreds = genderNet.forward()
        gender = genderList[genderPreds[0].argmax()]
    return gender


def main():
    gender = None
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
        try:
            gender = detect_gender(img)
        except:
            gender = None
        print(gender)
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get(url)
        input_box = driver.find_element_by_xpath('//*[@id="upload"]')
        input_box.send_keys(os.getcwd() + "/img.png")
        time.sleep(10)
        obj = driver.switch_to.alert
        msg = obj.text
        rate = int(msg)
        obj.accept()
        driver.close()
        try:
            if rate >= 5 and gender == 'Female':
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
                bot.close_gold_pop_up()
            except:
                try:
                    bot.close_popup()
                    time.sleep(1)
                except Exception:
                    try:
                        bot.close_plat_pop_up()
                    except:
                        try:
                            bot.close_match()
                        except Exception:
                            bot.exit_program()


def boost():
    bot = TinderBot()
    bot.login()
    while True:
        try:
            bot.driver.save_screenshot('img.png')
            img = cv2.imread('img.png', 1)
            img = img[50:650, 420:830]
            gender = detect_gender(img)
            if gender == "Female":
                bot.like()
            else:
                bot.dislike()
        except Exception:
            try:
                bot.close_popup()
            except Exception:
                try:
                    bot.close_match()
                except Exception:
                    pass


main()
# boost()


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
