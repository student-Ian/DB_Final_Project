from Functions import clear_screen
from client import send_message
from datas import username
import time
from datetime import datetime

class AnOrder:
    def __init__(self):
        self.cart = []  # 將購物車作為類別屬性
        self.restaurant = None  # 儲存使用者選擇的店家
        self.vdiscount = 1.0
        self.cdiscount = 1.0
        self.sum = 0
        self.destination = ""
        self.vcode = "0"
        self.ccode = "0"
        self.select_restaurant()

    def select_restaurant(self):
        """
        處理選擇店家的邏輯。
        """
        restaurants = send_message("restaurant_list")
        restaurants = [restaurant for restaurant in restaurants if datetime.strptime(restaurant['OpenTime'], "%H:%M:%S").time() 
                       < datetime.now().time() < datetime.strptime(restaurant['CloseTime'], "%H:%M:%S").time()]
        if not restaurants or not isinstance(restaurants, list):
            print("無法獲取店家列表或店家格式錯誤")
            return

        while True:
            print('請選擇店家:')
            self.print_numbered_restaurants(restaurants)
            choice = input("輸入店家號碼選擇，或輸入'q'取消: ")

            if choice == 'q':
                print("取消操作...")
                time.sleep(1)
                return
            try:
                rest_choice = int(choice)
                if 1 <= rest_choice <= len(restaurants):
                    self.restaurant = restaurants[rest_choice - 1]
                    clear_screen()
                    print(f"已選擇店家: {self.restaurant['餐廳名稱']}")
                    self.order_menu()  # 進入點餐流程
                    break
                else:
                    print("輸入範圍錯誤，請重新輸入")
            except ValueError:
                print("錯誤輸入，請輸入數字")

    def order_menu(self):
        """
        處理點餐邏輯，與伺服器互動以獲取菜單。
        """
        if not self.restaurant:
            print("未選擇店家，無法獲取菜單")
            return

        menu = send_message(f"menu#{self.restaurant['RUsername']}")
        if not menu or not isinstance(menu, list):
            print("無法獲取菜單或菜單格式錯誤")
            return

        while True:
            print('輸入餐點號碼點餐，輸入"v"查看購物車，輸入"s"送出訂單，輸入"q"取消點餐')
            self.print_numbered_menu(menu)
            choice = input("請選擇餐點: ")

            if choice == 'v':
                clear_screen()
                self.view_cart()  # 查看購物車
            elif choice == 'q':
                clear_screen()
                print('取消點餐...')
                time.sleep(1)
                break
            elif choice == 's':
                clear_screen()
                self.vdiscount = self.select_voucher(username)
                self.cdiscount = self.select_coupon(username)
                self.view_cart() 
                self.destination = input('請輸入地址:')
                ifsend = input('請問是否送出訂單? (y/n): ')
                if ifsend == 'y':
                    clear_screen()
                    print('訂單已送出')
                    oid = send_message(f"order#{username[0]}#{self.destination}#{self.vcode}#{self.ccode}")
                    result = ", ".join([f"{item['DName']} {item['Price']}" for item in self.cart])
                    detail = send_message(f"orderdetail#{oid}#{self.restaurant['RUsername']}#{result}")  # 發送訂單到伺服器
                    send_message(f"redeemcoupon#{oid}#{self.ccode}")  # 發送訂單到伺服器
                    time.sleep(2)
                    clear_screen()
                    break
                else:
                    clear_screen()
                    print('繼續點餐...')
                    time.sleep(1)
            else:
                try:
                    dishchoice = int(choice)
                    if 1 <= dishchoice <= len(menu):
                        clear_screen()
                        # print(menu)
                        print(f'成功添加餐點: {menu[dishchoice - 1]["DName"]} ${menu[dishchoice - 1]["Price"]}')
                        print()
                        self.cart.append(menu[dishchoice - 1])
                        time.sleep(1)
                    else:
                        print("錯誤輸入，請重新輸入")
                except ValueError:
                    print("錯誤輸入，請輸入數字")

    @staticmethod
    def print_numbered_restaurants(restaurants):
        """
        打印店家清單，並對每個店家進行編號。
        """
        print("Restaurants:")
        for index, restaurant in enumerate(restaurants, start=1):
            if restaurant['評分'] == "Non":
                print(f"{index}. {restaurant['餐廳名稱']}  - ")
            else:
                print(f"{index}. {restaurant['餐廳名稱']} {restaurant['評分']}")

    @staticmethod
    def print_numbered_menu(menu):
        """
        打印展平的菜單，並對每個項目進行編號。
        """
        print("Menu:")
        for index, item in enumerate(menu, start=1):
            print(f"{index}. {item['DName']} ${item['Price']}")

    def view_cart(self):
        """
        顯示購物車內容。
        """
        print('購物車中餐點如下：')
        if self.cart:
            self.sum = 0
            for index, item in enumerate(self.cart, start=1):
                print(f"{index}. {item['DName']} ${item['Price']}")
                self.sum += int(item['Price'])
            print(f"總金額為：${int(self.sum*self.vdiscount*self.cdiscount)}")

        else:
            print("購物車為空")
        print()

    def select_voucher(self, username):
        """
        從伺服器獲取折價券清單，讓使用者選擇是否使用折價券。
        
        :param username: 使用者名稱，用於請求折價券清單
        :return: 選擇的折扣值 (int)，若無折價券或不使用折價券則返回 0
        """
        voucher_list = send_message(f"uservoucher#{username[0]}")  # 從伺服器獲取折價券清單

        if not voucher_list:  # 檢查折價券清單是否為空
            print("目前沒有可用的折價券")
            time.sleep(1)
            clear_screen()
            return 1.0  # 折扣值為 0

        # 列出折價券
        print("以下是您的可用折價券：")
        for index, coupon in enumerate(voucher_list, start=1):
            print(f"{index}. {coupon['VCode']} - 折扣值: {coupon['VDiscount']}")

        # 詢問是否使用折價券
        use_coupon = input("是否使用折價券? (y/n): ").strip()
        if use_coupon == "y":
            while True:
                try:
                    choice = input("請選擇要使用的折價券編號: ").strip()  # 去除空格
                    print(f"用戶輸入: {choice}")  # 顯示用戶的輸入
                    choice = int(choice)  # 嘗試將選擇轉換為整數
                    
                    if 1 <= choice <= len(voucher_list):  # 檢查編號是否有效
                        selected_coupon = voucher_list[choice - 1]
                        discount = float(selected_coupon["VDiscount"])  # 使用 float 來處理折扣
                        print(f"已選擇折價券：{selected_coupon['VCode']}，折扣為 {discount}")
                        self.vcode = selected_coupon['VCode']
                        return discount  # 返回選擇的折價券折扣值
                    else:
                        print("輸入的編號無效，請重新輸入")
                except ValueError:
                    print("請輸入有效的數字編號")
        else:
            print("您選擇不使用折價券")
            time.sleep(1)
            clear_screen()
            return 1.0  # 不使用折價券，折扣值為 0


    def select_coupon(self, username):
        """
        從伺服器獲取折價券清單，讓使用者選擇是否使用折價券。
        
        :param username: 使用者名稱，用於請求折價券清單
        :return: 選擇的折扣值 (int)，若無折價券或不使用折價券則返回 0
        """
        coupon_list = send_message(f"usercoupon#{self.restaurant['RUsername']}")  # 從伺服器獲取折價券清單

        if not coupon_list:  # 檢查折價券清單是否為空
            print("目前沒有可用的折價券")
            time.sleep(1)
            clear_screen()
            return 1.0  # 折扣值為 0

        # 列出折價券
        print("以下是餐廳的可用折價券：")
        for index, coupon in enumerate(coupon_list, start=1):
            print(f"{index}. {coupon['CCode']} - 折扣值: {coupon['CDiscount']}")

        # 詢問是否使用折價券
        use_coupon = input("是否使用折價券? (y/n): ").strip()
        if use_coupon == "y":
            while True:
                try:
                    choice = input("請選擇要使用的折價券編號: ").strip()  # 去除空格
                    print(f"用戶輸入: {choice}")  # 顯示用戶的輸入
                    choice = int(choice)  # 嘗試將選擇轉換為整數
                    
                    if 1 <= choice <= len(coupon_list):  # 檢查編號是否有效
                        selected_coupon = coupon_list[choice - 1]
                        discount = float(selected_coupon["CDiscount"])  # 使用 float 來處理折扣
                        print(f"已選擇折價券：{selected_coupon['CCode']}，折扣為 {discount}")
                        self.ccode = selected_coupon['CCode']
                        return discount  # 返回選擇的折價券折扣值
                    else:
                        print("輸入的編號無效，請重新輸入")
                except ValueError:
                    print("請輸入有效的數字編號")
        else:
            print("您選擇不使用折價券")
            time.sleep(1)
            clear_screen()
            return 1.0  # 不使用折價券，折扣值為 0
