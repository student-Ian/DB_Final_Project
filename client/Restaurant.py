from Functions import clear_screen
from client import send_message
from datas import username
import time
import datetime

class Restaurant:
  def __init__(self):
      self.manage_menu()
      

  def manage_menu(self):
      while True:
          clear_screen()
          print("1. 添加菜品")
          print("2. 查看/變更提供菜品")
          print("3. 查看/變更當前訂單狀態")
          print("4. 查看歷史訂單")
          print("5. 查看/修改餐廳資訊")
          print("6. 查看/設定優惠券")
          print("7. 查看評分")
          print("q. 登出")
          choice = input("請選擇操作: ")

          if choice == '1':
              clear_screen()
              self.add_dish()
              print()
          elif choice == '2':
              clear_screen()
              self.view_and_modify_dishes()
              print()
          elif choice == '3':
              clear_screen()
              self.view_and_modify_orders()
              print()
          elif choice == '4':
              clear_screen()
              self.view_history_order()
              print()
          elif choice == '5':
              clear_screen()
              self.view_and_modify_restaurant_info()
              print()
          elif choice == '6':
              clear_screen()
              self.view_and_modify_coupons()
              print()
          elif choice == '7':
              clear_screen()
              self.view_rating()
              print() 
          elif choice == 'q':
              clear_screen()
              print("已成功登出，將自動跳轉登入頁面")
              time.sleep(1)
              clear_screen()
              break
          else:
              clear_screen()
              print("無效選擇，請重新輸入。")
              time.sleep(1)
              print()

  def add_dish(self):
    DName = input("請輸入菜品名稱或q返回: ")
    if DName == "q":
        return
    Price = input("請輸入菜品價格: ")
    
    # 發送菜品添加請求到伺服器
    message = f"adddish#{username[0]}#{DName}#{Price}"
    response = send_message(message)
    
    if response == "無效的消息格式":
        print("無效的消息格式，請檢查菜品名稱和價格")
        return

    # 顯示用戶的所有菜品清單
    print("更新後菜單:")
    for dish in response:
        print(f"{dish['DName'.lower()]} - {dish['Price'.lower()]} 元")
    
    print(f"菜品 {DName} 已添加，價格為 {Price} 元。")
    time.sleep(2)

  def view_and_modify_dishes(self):
    while True:
        # 假設 send_message 是用於從伺服器獲取菜單資訊
        dishes = send_message(f"dishes#{username[0]}")
        for index, item in enumerate(dishes, start=1):
            print(f"{index}. {item['DName'.lower()]} {item['Price'.lower()]}元 {item['Dstatus'.lower()]}")
        
        # 提示使用者輸入操作
        change = input("請輸入想要變更的菜編號，或是輸入返回 (q): ").strip()

        if change.lower() == 'q':  # 如果輸入是 'q'，則返回上一層
            clear_screen()
            break

        if change.isdigit():  # 確保輸入是數字
            dish_index = int(change) - 1  # 將輸入轉換為對應的索引值
            if 0 <= dish_index < len(dishes):
                new_name = input(
                    f"請輸入菜品 '{dishes[dish_index]['DName']}' 的新名稱或r維持不變: ").strip()
                if new_name == "r":
                    new_name = dishes[dish_index]['DName']
                new_price = input(
                    f"請輸入菜品 '{dishes[dish_index]['DName']}' 的新價格或r維持不變: ").strip()
                if new_price == "r":
                    new_price = dishes[dish_index]['Price']
                new_status = input(
                    f"請選擇菜品 '{dishes[dish_index]['DName']}' 的狀態：1.販售中 2.售完 3.下架: ").strip()
                if new_status == "1":
                    new_status = "販售中"
                elif new_status == "2":
                    new_status = "售完"
                elif new_status == "3":
                    new_status = "下架"
                if new_name:
                    # 更新菜單名稱（這裡假設 send_message 用於發送更新請求）
                    response = send_message(
                        f"updatedish#{username[0]}#{dishes[dish_index]['DName']}#{new_name}#{new_price}#{new_status}")
                    if response == "success":
                        print("菜品已成功更新！")
                        time.sleep(1)
                        clear_screen()
                    elif response == "Opening hours":
                        print("餐廳正在營業，請稍後再試。")
                    else:
                        print("更新失敗，請稍後再試。")
    
  def view_and_modify_orders(self):
    while True:
        # 獲取歷史訂單
        orders = send_message(f"bosshistoryorder#{username[0]}")  # 向伺服器請求歷史訂單
        page_size = 10  # 每頁顯示的筆數
        current_page = 0
        total_pages = (len(orders) + page_size - 1) // page_size  # 總頁數

        def display_page(page):
            """顯示當前頁面的資料"""
            clear_screen()
            start_index = page * page_size
            end_index = min(start_index + page_size, len(orders))
            print(f"=== 歷史訂單 (第 {page + 1}/{total_pages} 頁) ===")  # 顯示頁數
            print()
            index = start_index + 1  # 設定初始索引
            for order in bosshistoryorder[start_index:end_index]:
                for key, value in order.items():
                   print(f"{key}: {value}", end=" | ")
                index += 1  # 每次迭代後索引加 1
                print()
                 

        while True:
            display_page(current_page)

            # 等待使用者輸入
            order = input("輸入頁碼或輸入f刷新，輸入c進入修改模式，輸入d進入查看訂單細節，輸入q回到上一頁: ").strip().lower()

            if order == "q":
                clear_screen()
                print("已退出歷史訂單檢視")
                break
            elif order == "f":
                # 刷新訂單資料
                bosshistoryorder = send_message(f"bosshistoryorder#{username[0]}")
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
                    orderdetails = send_message(f"bossorderdetail#{selectdetail}")
                    sum = 0
                    for details in orderdetails:
                        print (f"{details['OId'.lower()]} {details['RName'.lower()]} {details['DName'.lower()]} {details['Price'.lower()]}元 {details['Quantity'.lower()]}份")
                        sum += int(details['Price'.lower()])*int(details['Quantity'.lower()])*int(details['VDiscount'.lower()])*int(details['CDiscount'.lower()])
                    print (f"共{sum}元")
                    quit = input("輸入任意鍵離開")
                    clear_screen()
                    
                else:
                    clear_screen()
                    print("無效輸入，即將退出模式")
                    time.sleep(1)
            elif order == "c":
                change = input("請輸入想要變更的訂單編號，或是輸入q返回: ").strip()

                if change.lower() == 'q':  # 如果輸入是 'q'，則返回上一層
                    break

                if change.isdigit():  # 確保輸入是數字
                    order_id = int(change) # 將輸入轉換為對應的索引值
                    if 0 <= order_id <= int(len(orders)):
                        new_content = input(f"請選擇訂單 '{orders[-order_id]['OId'.lower()]}{orders[-order_id]['Status'.lower()]}' 的新狀態(d是運送f是完成)或q離開: ").strip()
                        if new_content == "q":
                            clear_screen()
                        elif new_content == "f":
                            # 發送更新請求到伺服器（假設 send_message 可發送更新請求）
                            response = send_message(f"orderfinish#{order_id}")
                            if response == "success":
                                print("訂單已成功更新！")
                            else:
                                print("更新失敗，請稍後再試。")
                        elif new_content == "d":
                            # 發送更新請求到伺服器（假設 send_message 可發送更新請求）
                            response = send_message(f"orderdelivered#{order_id}")
                            if response == "success":
                                print("訂單已成功更新！")
                            else:
                                print("更新失敗，請稍後再試。")
                        
                        else:
                            print("新內容不能為空！")
                    else:
                        print("無效的訂單編號，請重新輸入。")
                else:
                    print("請輸入有效的編號或 'q' 返回。")


            else:
                clear_screen()
                print("無效輸入，請重新輸入")
                time.sleep(1)
        
        
  
  def view_history_order(self):
        # 模擬從伺服器獲取的資料
        bosshistoryorder = send_message(f"bosshistoryorder#{username[0]}")
        page_size = 10  # 每頁顯示的筆數
        current_page = 0
        total_pages = (len(bosshistoryorder) + page_size - 1) // page_size  # 總頁數

        def display_page(page):
            """顯示當前頁面的資料"""
            clear_screen()
            start_index = page * page_size
            end_index = min(start_index + page_size, len(bosshistoryorder))
            print(f"=== 歷史訂單 (第 {page + 1}/{total_pages} 頁) ===")  # 顯示頁數
            print()
            index = start_index + 1  # 設定初始索引
            for order in bosshistoryorder[start_index:end_index]:
                for key, value in order.items():
                   print(f"{key}: {value}", end=" | ")
                index += 1  # 每次迭代後索引加 1
                print()
                 

        while True:
            display_page(current_page)

            # 等待使用者輸入
            order = input("輸入頁碼或輸入f刷新，輸入q回到上一頁: ").strip().lower()

            if order == "q":
                clear_screen()
                print("已退出歷史訂單檢視")
                break
            elif order == "f":
                # 刷新訂單資料
                bosshistoryorder = send_message(f"bosshistoryorder#{username[0]}")
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
            else:
                clear_screen()
                print("無效輸入，請重新輸入")
                time.sleep(1)

  def view_and_modify_restaurant_info(self):
    while True:
        # 假設 send_message 用於從伺服器獲取餐廳資訊
        restaurant_info = send_message(f"restaurant_info#{username[0]}")
        print("目前餐廳資訊：")
        for key, value in restaurant_info[0].items():
            print(f"{key}: {value}")

        action = input("請輸入要修改的資訊項目名稱，或輸入返回 (q): ").strip()
        
        
            
        if action.lower() == 'q':  # 返回上一層
            clear_screen()
            break

        if action in restaurant_info[0]:
            new_value = input(f"請輸入 '{action}' 的新值: ").strip()
            if new_value:
                if action == "餐廳名稱":
                    action = "RName"
                elif action == "餐廳電話號碼":
                    action = "RPhone"
                elif action == "餐廳地址":
                    action = "Address"
                elif action == "開始營業時間": 
                    action = "OpenTime"
                elif action == "結束營業時間":
                    action = "CloseTime"
                    
                response = send_message(f"update_restaurant#{username[0]}#{action}#{new_value}")
                if response:
                    for key, value in restaurant_info[0].items():
                        print(f"{key}: {value}")
                else:
                    print("更新失敗，請稍後再試。")
            else:
                print("新值不能為空！")
        else:
            print("無效的項目名稱，請重新輸入。")


  def view_and_modify_coupons(self):
    while True:
        # 假設 send_message 用於從伺服器獲取優惠券列表
        coupons = send_message(f"coupons#{username[0]}")
        print("目前可用的優惠券：")
        for index, coupon in enumerate(coupons, start=1):
            print(f"{index}. {coupon['CCode'.lower()]}: {coupon['CDiscount'.lower()]}")

        action = input("請輸入c修改優惠券或輸入a新增，輸入q返回: ").strip()

        if action.lower() == 'q':  # 返回上一層
            break

        elif action.lower() == 'c':  # 確保輸入是數字
            
            new_value = input("請輸入優惠券的新折扣(0.00~0.99)或q返回: ").strip()
            if new_value == "q":
                print("已取消")
                time.sleep(1)
                clear_screen()
            elif new_value.startswith("0.") and 3 <= len(new_value) <= 4 and new_value[2].isdigit() and new_value[3].isdigit():
                while True:
                    new_endtime = input("請輸入優惠券的新結束時間(如2020 01 01)或r維持不變: ")
                    if new_endtime == "r":
                        new_endtime = coupons[0]["CEndsAt".lower()]
                        break
                    else:
                        try:
                            new_endtime = [int(i) for i in new_endtime.split()]
                            new_endtime = datetime.datetime(*new_starttime)
                            
                            if new_endtime > new_starttime:
                                break
                        except:
                            print("錯誤！請重新輸入")

                responses = send_message(f"update_coupon#{username[0]}#{new_value}#{new_endtime}")
                if responses:
                    print("優惠券已成功更新！")
                    time.sleep(1)
                    clear_screen()
                        
                else:
                    print("更新失敗")
                    time.sleep(1)
                    clear_screen()
            else:
                print("輸入格式錯誤！")
                time.sleep(1)
                clear_screen()
            
        elif action.lower() == 'a':
            if coupon == []:
                new_value = input("請輸入新優惠券的折扣: ").strip()
                while True:
                    new_starttime = [int(i) for i in input("請輸入新優惠券的開始時間(如2020 01 01): ").split()]
                    try:
                        new_starttime = datetime.datetime(*new_starttime)
                        break
                    except:
                        print("錯誤！請重新輸入")

                while True:
                    new_endtime = [int(i) for i in input("請輸入新優惠券的結束時間(如2020 01 01): ").split()]
                    try:
                        new_endtime = datetime.datetime(*new_starttime)

                        if new_endtime > new_starttime:
                            break
                    except:
                        print("錯誤！請重新輸入")

                if new_value:
                    responses = send_message(f"add_coupon#{username[0]}#{new_value}#{new_starttime}#{new_endtime}")
                    if responses:
                        print("優惠券已成功更新！")
                        time.sleep(1)
                        clear_screen()
                            
                    else:
                        print("更新失敗")
                        time.sleep(1)
                        clear_screen()
                else:
                    print("新內容不能為空！")
                    time.sleep(1)
                    clear_screen()
            else:
                print("當前已有有效優惠券，請選擇修改")
                time.sleep(1)
                clear_screen()

        else:
            print("請輸入有效的編號或 'q' 返回。")
            time.sleep(1)
            clear_screen()

  def view_rating(self):
    response = send_message(f"bossrating#{username[0]}")
    avg = 0
    for r in response:
        avg += float(list(r.values())[0])
    avg = round(avg / len(response), 1)
    print(f"用戶平均評分：{avg}")
    quit = input("輸入任意鍵離開")
    clear_screen()
    
