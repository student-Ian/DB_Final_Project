from Functions import clear_screen, progress_bar
from Customer import Customer
from Restaurant import Restaurant
from client import send_message
from datas import username

import os
import time


def login():
    while True:
        clear_screen()
        print("-----------------------")
        print('Welcome to DelishWay!!!')
        print("-----------------------")
        mode = input("客戶請選1，餐廳老闆請選2，註冊客戶請選3，註冊老闆請選4: ")
        username[0] = input("請輸入帳號: ")
        password = input("請輸入密碼: ")
        clear_screen()

        if mode == "1" or mode == "2":
            if mode == "1" and send_message(f"login#{mode}#{username[0]}#{password}") == "userconfirm":
                Customer()  # 實例化 Customer 類別
            elif mode == "2" and send_message(f"login#{mode}#{username[0]}#{password}") == "bossconfirm":
                Restaurant()  # 實例化 Restaurant 類別
            else:
                print("帳號或密碼錯誤，請重新登入")
                time.sleep(1)
                clear_screen()
    
if __name__ == "__main__":
    login()