from Functions import clear_screen, progress_bar
from AnOrder import AnOrder
import time
from client import send_message
from datas import username


class Customer:
    def __init__(self):
        self.cart = []  # 在 Customer 中添加購物車屬性
        self.customer_menu()

    def customer_menu(self):
        while True:
            print("1. 開始點餐")
            print("2. 查看當前送餐進度")
            print("3. 查看歷史訂單")
            print("4. 進行餐廳評分")
            print("q. 登出")
            choice = input("請選擇操作: ")

            if choice == '1':
                clear_screen()
                currentorder = send_message(f"usercurrentorder#{username[0]}")
                # print(currentorder)
                if currentorder[0] == "Empty Order" or currentorder[0]['訂單狀態'] == "已完成" or currentorder[0]['訂單狀態'] == "已取消":
                    an_order = AnOrder()  # 創建 AnOrder 實例
                    self.cart = an_order.cart  # 從 AnOrder 獲取購物車
                    
                else:
                    print("請等待現在訂單完成後再訂餐")
                    time.sleep(2)
                    clear_screen()
                    
            elif choice == '2':
                clear_screen()
                self.view_current_order()
            elif choice == '3':
                clear_screen()
                self.view_history_order()
            elif choice == '4':
                clear_screen()
                self.rating()
            elif choice == 'q':
                clear_screen()
                print("已成功登出，將自動跳轉登入頁面")
                time.sleep(1)
                clear_screen()
                break
            else:
                print("無效選擇，請重新輸入。")

    def view_current_order(self):
        usercurrentorder = send_message(f"usercurrentorder#{username[0]}")
        status = usercurrentorder[0]['訂單狀態']
        if status == "已送出" or status == "準備中":
            print("餐點準備中", end='', flush=True)

            symbols = ['\\', '|', '/', '-']

            for i in range(10):
                time.sleep(0.2)
                print("\r餐點準備中 " + symbols[i % 4], end='', flush=True)
            clear_screen()

        elif status == "配送中":
            print('餐點配送中...')
            print(f'負責的騎手是{usercurrentorder[0]["DRName".lower()]}，可以撥打{usercurrentorder[0]["DRPhone".lower()]}來聯絡他哦')
            progress_bar()
            clear_screen()
        elif status == "已完成":
            print('餐點已送達！')
            self.cart.clear()
            time.sleep(2)
            clear_screen()
        elif status == "已取消":
            print('訂單已取消！')
            self.cart.clear()
            time.sleep(2)
            clear_screen()
        for order in usercurrentorder:
            for key, value in order.items():
                print(f"{key}: {value}")
        print()
        

        

    def view_history_order(self):
        # 模擬從伺服器獲取的資料
        userhistoryorder = send_message(f"userhistoryorder#{username[0]}")
        page_size = 10  # 每頁顯示的筆數
        current_page = 0
        total_pages = (len(userhistoryorder) + page_size - 1) // page_size  # 總頁數

        def display_page(page):
            """顯示當前頁面的資料"""
            clear_screen()
            start_index = page * page_size
            end_index = min(start_index + page_size, len(userhistoryorder))
            print(f"=== 歷史訂單 (第 {page + 1}/{total_pages} 頁) ===")  # 顯示頁數
            print()
            index = start_index + 1  # 設定初始索引
            for order in userhistoryorder[start_index:end_index]:
                for key, value in order.items():
                   print(f"{key}: {value}", end=" | ")
                index += 1  # 每次迭代後索引加 1
                print()
                 

        while True:
            display_page(current_page)

            # 等待使用者輸入
            order = input("輸入頁碼或輸入d進入查看訂單細節，輸入f刷新，輸入q回到上一頁: ").strip().lower()

            if order == "q":
                clear_screen()
                print("已退出歷史訂單檢視")
                break
            elif order == "f":
                # 刷新訂單資料
                userhistoryorder = send_message(f"userhistoryorder#{username[0]}")
                current_page = 0  # 回到第一頁
            elif order.isdigit():
                # 跳轉到指定頁碼
                page = int(order) - 1
                if 0 <= page < total_pages:
                    current_page = page
                else:
                    clear_screen()
                    print("頁碼超出範圍，請重新輸入")
                    time.sleep(1)
            elif order == "d":
                selectdetail = input("輸入想要查看的訂單編號，或輸入q回到上一頁: ").strip().lower()
                if selectdetail == "q":
                    clear_screen()
                elif selectdetail.isdigit():
                    clear_screen()
                    orderdetails = send_message(f"customerorderdetail#{selectdetail}")
                    sum = 0
                    for details in orderdetails:
                        print (f"{details['OId']} {details['RName'.lower()]} {details['DName'.lower()]} {details['Price'.lower()]}元 {details['Quantity'.lower()]}份")
                        sum += int(details['Price'.lower()])*int(details['Quantity'.lower()])*int(details['VDiscount'.lower()])*int(details['CDiscount'.lower()])
                    print (f"共{sum}元")
                    quit = input("輸入任意鍵離開")
                    clear_screen()
                    
                else:
                    clear_screen()
                    print("無效輸入，即將退出模式")
                    time.sleep(1)
            else:
                clear_screen()
                print("無效輸入，請重新輸入")
                time.sleep(1)

    def rating(self):
        while True:
            ratinglist = send_message(f"rating#{username[0]}")
            n = 1
            for rates in ratinglist:
                print(f"{n}. {rates['RNname'.lower()]} {rates['Rating'.lower()]}")
            order = input("輸入想要變更的評分或q離開：")
            if order == "q":
                clear_screen()
                break
            elif order.isdigit() and int(order) <= len(ratinglist):
                new_rate = input("輸入評分：")
                if send_message(f"changerating#{username[0]}#{ratinglist[order - 1]['RUsername'.lower()]}#{new_rate}") == "success":
                    print("分數更新成功")
                else:
                    print("分數更新失敗")
                time.sleep(1)
                clear_screen()
            else:
                print("錯誤輸入")
                time.sleep(1)
                clear_screen()
# crapes_8YE
# 8e8dd1824091492f
# backland
# c337a3b1f20e2eed