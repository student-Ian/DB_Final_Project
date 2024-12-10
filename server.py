import socket
import threading
import json
from collections import Counter
from sqlfunction import *
import random
import hashlib
from datetime import datetime
from collections import defaultdict

# 伺服器設置
HOST = '127.0.0.1'
PORT = 9876

# 資料庫
restaurant_info = [
    {"RUsername": "234", "RPassword": "234", "RName": "美味餐廳234", "RPhone": "0911222345", "Address": "123 美食街", "OpenTime": "10:00", "CloseTime":"22:00"},
    {"RUsername": "345", "RPassword": "234", "RName": "和風餐廳345", "RPhone": "0914987362", "Address": "456 美食街", "OpenTime": "11:00","CloseTime":"21:00"}
]

coupons = [
    {"username": "234", "CDiscount": "0.9"},
    {"username": "345", "CDiscount": "0.85"}
]

usercoupons = [
    {"username": "111", "CCode" : "11233", "CDiscount": "0.9"},
    {"username": "222", "CCode" : "54412", "CDiscount": "0.85"}
]

dishes = [
    {"RUsername": "345", "DName": "壽司", "Price": "100", "Dstatus":"販售中"},
    {"RUsername": "345", "DName": "生魚片", "Price": "120", "Dstatus":"販售中"},
    {"RUsername": "234", "DName": "炒飯", "Price": "50", "Dstatus":"販售中"},
    {"RUsername": "234", "DName": "拉麵", "Price": "80", "Dstatus":"販售中"}
]

Order = [
    {'OId': '20', 'OrderTime': '2024-06-11 05:45:00', 'CollectTime': '2024-06-12 14:32:00', 'ArriveTime': '2024-06-13 09:01:00', 'Destination': 'City D', 'OStatus': "運送中", 'Notes': 'Normal', 'OrderedBy': '111', 'DeliveredBy': 'User3'},
    {'OId': '19', 'OrderTime': '2024-09-01 22:15:00', 'CollectTime': '2024-09-02 16:00:00', 'ArriveTime': '2024-09-03 11:20:00', 'Destination': 'City C', 'OStatus': 'Pending', 'Notes': 'Urgent', 'OrderedBy': '111', 'DeliveredBy': 'User2'},
    {'OId': '18', 'OrderTime': '2024-12-05 08:25:00', 'CollectTime': '2024-12-06 13:10:00', 'ArriveTime': '2024-12-07 19:00:00', 'Destination': 'City B', 'OStatus': 'In Progress', 'Notes': '', 'OrderedBy': '111', 'DeliveredBy': 'User1'},
    {'OId': '17', 'OrderTime': '2024-01-20 19:45:00', 'CollectTime': '2024-01-21 18:30:00', 'ArriveTime': '2024-01-22 07:50:00', 'Destination': 'City A', 'OStatus': 'Cancelled', 'Notes': 'Delayed', 'OrderedBy': '111', 'DeliveredBy': 'User4'},
    {'OId': '16', 'OrderTime': '2024-05-15 11:05:00', 'CollectTime': '2024-05-16 14:45:00', 'ArriveTime': '2024-05-17 10:25:00', 'Destination': 'City D', 'OStatus': 'Completed', 'Notes': '', 'OrderedBy': '111', 'DeliveredBy': 'User3'},
    {'OId': '15', 'OrderTime': '2024-03-10 17:50:00', 'CollectTime': '2024-03-11 09:30:00', 'ArriveTime': '2024-03-12 13:10:00', 'Destination': 'City B', 'OStatus': 'Pending', 'Notes': 'Normal', 'OrderedBy': '111', 'DeliveredBy': 'User2'},
    {'OId': '14', 'OrderTime': '2024-11-15 07:20:00', 'CollectTime': '2024-11-16 14:50:00', 'ArriveTime': '2024-11-17 08:45:00', 'Destination': 'City C', 'OStatus': 'In Progress', 'Notes': 'Urgent', 'OrderedBy': '111', 'DeliveredBy': 'User4'},
    {'OId': '13', 'OrderTime': '2024-08-05 21:30:00', 'CollectTime': '2024-08-06 19:20:00', 'ArriveTime': '2024-08-07 09:10:00', 'Destination': 'City A', 'OStatus': 'Cancelled', 'Notes': 'Delayed', 'OrderedBy': '111', 'DeliveredBy': 'User1'},
    {'OId': '12', 'OrderTime': '2024-04-12 10:45:00', 'CollectTime': '2024-04-13 18:30:00', 'ArriveTime': '2024-04-14 14:25:00', 'Destination': 'City B', 'OStatus': 'Completed', 'Notes': 'Normal', 'OrderedBy': '111', 'DeliveredBy': 'User2'},
    {'OId': '11', 'OrderTime': '2024-02-14 06:15:00', 'CollectTime': '2024-02-15 08:25:00', 'ArriveTime': '2024-02-16 10:50:00', 'Destination': 'City D', 'OStatus': 'Pending', 'Notes': '', 'OrderedBy': '111', 'DeliveredBy': 'User4'},
    {'OId': '10', 'OrderTime': '2024-07-18 13:40:00', 'CollectTime': '2024-07-19 12:10:00', 'ArriveTime': '2024-07-20 08:00:00', 'Destination': 'City A', 'OStatus': 'In Progress', 'Notes': 'Urgent', 'OrderedBy': '111', 'DeliveredBy': 'User3'},
    {'OId': '9', 'OrderTime': '2024-10-23 09:55:00', 'CollectTime': '2024-10-24 18:40:00', 'ArriveTime': '2024-10-25 15:10:00', 'Destination': 'City C', 'OStatus': 'Cancelled', 'Notes': 'Delayed', 'OrderedBy': '111', 'DeliveredBy': 'User1'},
    {'OId': '8', 'OrderTime': '2024-06-06 22:25:00', 'CollectTime': '2024-06-07 20:00:00', 'ArriveTime': '2024-06-08 11:50:00', 'Destination': 'City D', 'OStatus': 'Completed', 'Notes': '', 'OrderedBy': '111', 'DeliveredBy': 'User4'},
    {'OId': '7', 'OrderTime': '2024-03-30 05:15:00', 'CollectTime': '2024-03-31 07:10:00', 'ArriveTime': '2024-04-01 12:20:00', 'Destination': 'City B', 'OStatus': 'Pending', 'Notes': 'Normal', 'OrderedBy': '111', 'DeliveredBy': 'User2'},
    {'OId': '6', 'OrderTime': '2024-09-12 17:35:00', 'CollectTime': '2024-09-13 22:50:00', 'ArriveTime': '2024-09-14 07:15:00', 'Destination': 'City A', 'OStatus': 'In Progress', 'Notes': 'Urgent', 'OrderedBy': '111', 'DeliveredBy': 'User3'},
    {'OId': '5', 'OrderTime': '2024-11-01 11:00:00', 'CollectTime': '2024-11-02 09:45:00', 'ArriveTime': '2024-11-03 10:40:00', 'Destination': 'City C', 'OStatus': 'Cancelled', 'Notes': '', 'OrderedBy': '111', 'DeliveredBy': 'User4'},
    {'OId': '4', 'OrderTime': '2024-01-22 07:50:00', 'CollectTime': '2024-01-23 14:30:00', 'ArriveTime': '2024-01-24 08:10:00', 'Destination': 'City D', 'OStatus': 'Completed', 'Notes': 'Normal', 'OrderedBy': '111', 'DeliveredBy': 'User1'},
    {'OId': '3', 'OrderTime': '2024-05-09 06:25:00', 'CollectTime': '2024-05-10 18:15:00', 'ArriveTime': '2024-05-11 13:35:00', 'Destination': 'City B', 'OStatus': 'Pending', 'Notes': '', 'OrderedBy': '111', 'DeliveredBy': 'User3'},
    {'OId': '2', 'OrderTime': '2024-08-25 10:20:00', 'CollectTime': '2024-08-26 19:55:00', 'ArriveTime': '2024-08-27 12:40:00', 'Destination': 'City A', 'OStatus': 'In Progress', 'Notes': 'Urgent', 'OrderedBy': '111', 'DeliveredBy': 'User2'},
    {'OId': '1', 'OrderTime': '2024-12-08 12:15:00', 'CollectTime': '2024-12-09 08:40:00', 'ArriveTime': '2024-12-10 14:10:00', 'Destination': 'City C', 'OStatus': 'Cancelled', 'Notes': 'Delayed', 'OrderedBy': '111', 'DeliveredBy': 'User4'}
]

orderdetail = [
    {'OId':20, 'RUsername':"美味餐廳234", 'DName': "炒飯", 'Quantity':2}
]

# 登錄帳戶
login_user = []
login_boss = []

def process_login_request(request):
    """
    處理登入請求
    """
    try:

        command, mode, username, password = request.split("#")
        if mode == "1":
            users = get_users()  # query
            if (username, password) in users and username not in login_user:
                login_user.append(username)
                return "userconfirm"
            return "deny"
        elif mode == "2":
            boss = get_bosses()  # query
            if (username, password) in boss and username not in login_boss:
                login_boss.append(username)
                return "bossconfirm"
            return "deny"
        else:
            return "deny"
    except ValueError:
        return "Malformed request"
# query ✅
def user_current_order_request(message):
    username = message.split("#")[1]
    
    Order = get_current_order([username]) #query
    if not len(Order):
        return ["Empty Order"]    
    
    user_orders = [
        {
            "訂單編號": order["OId".lower()],
            "下單時間": str(order["OrderTime".lower()]),
            "騎手取餐時間": str(order["CollectTime".lower()]),
            "到達時間": str(order["ArriveTime".lower()]),
            "終點": order["Destination".lower()],
            "訂單狀態": order["OStatus".lower()],
            "騎手": order["DeliveredBy".lower()],
        }
        for order in Order
        if order["OrderedBy".lower()] == username
    ]
    # print([user_orders[0]])
    # return [user_orders[0]]

    print([user_orders[0]])
    return [user_orders[0]]

# TODO: TIME?
# query ✅
def order_request(message):
    #"order#username"
    username = message.split("#")[1]
    destination = message.split("#")[2]
    OId = str(int(get_max_oid()) + 1)
    print(OId)
    riders = ['VGQkyr', 'eGjwcL', 'UNDMQQ', 'YbyCWS', 'ppsvNg', 'dzGnUz', 'vmzEBF', 'KeKlgS']
    rider = random.choice(riders)
    send_order([OId, destination, username, rider]) # query
    # Order.insert(0,{'OId': OId, 'OrderTime': '2024-12-08 12:15:00', 'CollectTime': '2024-12-09 08:40:00', 'ArriveTime': '2024-12-10 14:10:00', 'Destination': f'{destination}', 'OStatus': '準備中', 'OrderedBy': f'{username}', 'DeliveredBy': rider})
    return OId

# query ✅
def orderdetail_request(order_string):
    parts = order_string.split("#")
    if len(parts) < 4:
        raise ValueError("訂單字串格式不正確")
    
    oid = parts[1]  # 訂單編號
    rusername = parts[2]  # 餐廳名稱
    items = parts[3].split(", ")  # 餐點列表
    
    aggregated_items = defaultdict(int)

    for item in items:
        DName, quantity = item.rsplit(" ", 1)
        quantity = int(quantity)
        aggregated_items[DName] += quantity

    # Process each unique DName and its total quantity
    for DName, total_quantity in aggregated_items.items():
        send_order_detail([oid, rusername, DName, total_quantity])  # Send query
        
    for item in items:
        DName, quantity = item.rsplit(" ", 1)  # 分離餐點名稱與數量
        orderdetail.insert(0, {
            "OId": oid,
            "RUsername": rusername,
            "DName": DName,
            "Quantity": int(quantity)
        })
    return [orderdetail[0]]

def show_restaurant_list():
    restaurant_info = get_restaurant_list()
    restaurants = [
        {
            "RUsername": restaurant["rusername"],
            "餐廳名稱": restaurant["rname"],
            "評分": str(restaurant["rating"])[:3],
            "OpenTime": str(restaurant["opentime"]),
            "CloseTime": str(restaurant["closetime"])
        }
        for restaurant in restaurant_info
    ]
    return restaurants

# query ✅
def menu_request(message):
    parts = message.split("#")
    username = parts[1]

    dishes = get_menu() # query
    user_dishes = [
        {"DName": dish["Dname".lower()], 
         "Price": dish["Price".lower()]} 
         for dish in dishes 
         if dish["RUsername".lower()] == username 
         and dish["Dstatus".lower()] == "販售中"
        ]
    return user_dishes  

# query ✅
def Voucher_request(message):
    
    parts = message.split("#")
    username = parts[1]

    Vouchers = get_vouchers() #query
    Voucher_list = [{
        "VCode": voucher["VCode".lower()], 
        "VDiscount": str(voucher["VDiscount".lower()])}
        for voucher in Vouchers
        if voucher["BelongsTo".lower()] == username
    ]
    return Voucher_list

# query ✅
def Coupon_request(message):
    
    parts = message.split("#")
    username = parts[1]
    
    Coupons = get_coupons() #query
    Coupon_list = [{
        "CCode": coupon["CCode".lower()], 
        "CDiscount": str(coupon["CDiscount".lower()])
        }
        for coupon in Coupons
        if coupon["IssuedBy".lower()] == username
    ]
    return Coupon_list

def redeem_coupon(message):
    oid = message.split("#")[1]
    ccode = message.split("#")[2]
    redeem_coupon_sql([oid, ccode])

# query ✅
def user_view_history_order(message):
    """
    查看歷史訂單：bosshistoryorder#username
    """
    username = message.split("#")[1]
    
    Order = get_order_history() #query
    user_orders = [
    {
        "訂單編號": order["OId".lower()],
        "下單時間": str(order["OrderTime".lower()]),
        "騎手取餐時間": str(order["CollectTime".lower()]),
        "到達時間": str(order["ArriveTime".lower()]),
        "終點": order["Destination".lower()],
        "訂單狀態": order["OStatus".lower()],
        "騎手": order["DeliveredBy".lower()],
    }
    for order in Order
    if order["OrderedBy".lower()] == username
]
    return user_orders
 
#boss
# query ✅
def add_dish(message):
    parts = message.split('#')
    if len(parts) != 4:
        print("無效的消息格式")
        return "無效的消息格式"

    command, username, DName, dish_Price = parts
    add_dish_query([username, DName, str(dish_Price)]) #query
    # dishes.append({
    #     "RUsername": username, 
    #     "DName": DName, 
    #     "Price": str(dish_Price), 
    #     "Dstatus": "販售中"
    # })

    # 輸出成功消息
    print(f"已成功將菜品 '{DName}' 添加至用戶 {username} 的菜單，價格為 {dish_Price} 元。")
    
    dishes = get_menu_boss()
    user_dishes = [{
        "DName": dish["DName".lower()],
        "Price": dish["Price".lower()],
        "Dstatus": dish["Dstatus".lower()]}
        for dish in dishes 
        if dish["RUsername".lower()] == username
    ]
    return user_dishes

# 處理菜品操作
# query ✅
def view_dishes(message):
    """
    查看或修改菜品：
    - 查看：dishes#username
    - 修改：updatedish#username#DName#new_name#new_Price
    """
    parts = message.split("#")
    username = parts[1]

    dishes = get_menu_boss() # query 
    user_dishes = [{
        "DName": dish["DName".lower()],
        "Price": dish["Price".lower()],
        "Dstatus": dish["Dstatus".lower()]
        } for dish in dishes
          if dish["RUsername".lower()] == username
        ]
    print(user_dishes)
    return user_dishes

# query ✅
def updated_dishes(message):
    parts = message.split("#")
    username = parts[1]
    restaurant_info = get_restaurant_list()
    if username in [restaurant["rusername"] for restaurant in restaurant_info]:
        return "Opening hours"
    try:
        old_name = parts[2]
        new_name = parts[3]
        new_Price = parts[4]
        new_status = parts[5]

        update_dishes([new_name, new_Price, new_status,
                      username, old_name])  # query
        # for dish in dishes:
        #     if dish["RUsername"] == username and dish["DName"] == old_name:
        #         dish["DName"] = new_name
        #         dish["Price"] = str(new_Price)
        #         dish["Dstatus"] = new_status

        return "success"
    except (IndexError, ValueError):
        return "failed"
    
# 處理歷史訂單
# query ✅
def boss_view_history_order(message):
    """
    查看歷史訂單：bosshistoryorder#username
    """
    username = message.split("#")[1]
    Order = get_boss_order_history() #query
    user_orders = [{
            key: str(value)
            for key, value in order.items()
        }
        for order in Order
        if order["rusername"] == username
    ]
    print(user_orders)
    return user_orders

# 處理餐廳資訊
# query ✅
def handle_view_and_modify_restaurant_info(message):
    """
    查看或修改餐廳資訊：
    - 查看：restaurant_info#username
    - 修改：update_restaurant#username#key#new_value
    """
    parts = message.split("#")
    Rusername = parts[1]

    if message.startswith("restaurant_info#"):
    # 假設 restaurant_info 是一個包含字典的列表
        restaurant_info = handle_view_and_modify_restaurant_info_query() #query
        info = [
            {
                "餐廳名稱": restaurant["RName".lower()],
                "餐廳電話號碼": restaurant["RPhone".lower()],
                "餐廳地址": restaurant["Address".lower()],
                "開始營業時間": restaurant["OpenTime".lower()],
                "結束營業時間": restaurant["CloseTime".lower()]
            }
            for restaurant in restaurant_info if restaurant["RUsername".lower()] == Rusername
        ]
        return info

    # ??? TODO
    elif message.startswith("update_restaurant#"):
        key = parts[2]
        new_value = parts[3]
        for info in restaurant_info:
            if info["RUsername".lower()] == Rusername:
                if key in info:
                    info[key] = new_value
                    return info     

# 處理優惠券
# query ✅
def view_coupons(message):
    """
    查看或修改優惠券：
    - 查看：coupons#username
    - 修改：update_coupon#username#new_CDiscount
    """
    parts = message.split("#")
    username = parts[1]
    couponlist = view_coupons_query() #query
    # couponlist = [coupon for coupon in coupons if coupon["username"] == username]
    return couponlist
    
# query ✅
def modify_coupons(message):
    try:
        parts = message.split("#")
        username = parts[1]
        new_CDiscount = parts[2]
        cEndsAt = parts[3]
        modify_coupon_query([username, new_CDiscount, cEndsAt]) #query
        newcoupon = view_coupons_query()
        return newcoupon
    except:
    # for coupon in coupons:
    #     if coupon["username"] == username:
    #         coupon["CDiscount"] = new_CDiscount
            # newcoupon = [coupon for coupon in coupons if coupon["username"] == username]
            # return newcoupon
        return {"status": "error", "message": "未找到優惠券。"}

#add coupon
def add_coupons(message):
    parts = message.split("#")
    username = parts[1]
    new_CDiscount = parts[2]
    new_CCode = hashlib.md5(str(random.random()).encode()).hexdigest()[:6]
    cBeginsAt = parts[3]
    cEndsAt = parts[4]
    add_coupons([new_CCode, new_CDiscount, cBeginsAt, cEndsAt, username])
    Coupons = get_coupons()
    # Coupons.insert(0, {"IssuedBy": username, "CCode" : new_CCode, "CDiscount": new_CDiscount})
    newcoupon = [coupon for coupon in Coupons if coupon["IssuedBy".lower()] == username]
    return newcoupon

def get_order_detail(message):
    parts = message.split("#")
    oId = parts[1]
    order_details = get_order_detail_query([oId])
    return order_details

def rate_restaurant(message):
    parts = message.split("#")
    cusername = parts[1]
    restaurant_with_rating = rate_restaurant_query([cusername])
    return restaurant_with_rating

def change_rating(message):
    try:
        parts = message.split("#")
        cusername = parts[1]
        rusername = parts[2]
        new_rate = parts[3]
        change_rating_query([cusername, rusername, new_rate])
        return "success"
    except Exception as E:
        return "SQL Query Failed"

def boss_rating(message):
    parts = message.split("#")
    rusername = parts[1]
    boss_ratings = boss_rating_query([rusername])
    return boss_ratings
    
# 處理客戶端連線
def handle_client(client_socket, address):
    print(f"New connection from {address}")
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                break
            print(f"Received: {message}")

            #user
            if message.startswith("login#"):
                response = process_login_request(message)
                client_socket.sendall(response.encode())
            elif message.startswith("usercurrentorder"):
                response = user_current_order_request(message)
                client_socket.sendall(json.dumps(response).encode())
            elif message.startswith("order#"):
                response = order_request(message)
                client_socket.sendall(response.encode())
            elif message.startswith("orderdetail#"):
                response = orderdetail_request(message)
                client_socket.sendall(json.dumps(response).encode())
            elif message == "restaurant_list":
                response = show_restaurant_list()
                client_socket.sendall(json.dumps(response).encode())
            elif message.startswith("menu"):
                response = menu_request(message)
                client_socket.sendall(json.dumps(response).encode())
            elif message.startswith("usercoupon"):
                response = Coupon_request(message)
                client_socket.sendall(json.dumps(response).encode())
            elif message.startswith("redeemcoupon"):
                response = redeem_coupon(message)
                client_socket.sendall(json.dumps(response).encode())
            elif message.startswith("uservoucher"):
                response = Voucher_request(message)                
                client_socket.sendall(json.dumps(response).encode())
            elif message.startswith("userhistoryorder#"):
                response = user_view_history_order(message)
                client_socket.sendall(json.dumps(response).encode())
            elif message.startswith("customerorderdetail#"): #OID TODO
                response = get_order_detail(message)
                client_socket.sendall(json.dumps(response).encode())
                
            #restaurant
            elif message.startswith("adddish#"):
                response = add_dish(message)
                client_socket.sendall(json.dumps(response).encode())
            elif message.startswith("dishes#"):
                response = view_dishes(message)
                client_socket.sendall(json.dumps(response).encode())
            elif message.startswith("updatedish#"):
                response = updated_dishes(message)
                client_socket.sendall(response.encode())
            elif message.startswith("bosshistoryorder#"):
                response = boss_view_history_order(message)
                client_socket.sendall(json.dumps(response).encode())
            elif message.startswith("restaurant_info#"):
                response = handle_view_and_modify_restaurant_info(message)
                client_socket.sendall(json.dumps(response).encode())
            elif message.startswith("update_restaurant#"):
                response = handle_view_and_modify_restaurant_info(message)
                client_socket.sendall(json.dumps(response).encode())
            elif message.startswith("coupons#"):
                response = view_coupons(message)
                client_socket.sendall(json.dumps(response).encode())
            elif message.startswith("update_coupon#"):
                response = modify_coupons(message)
                client_socket.sendall(json.dumps(response).encode())
            elif message.startswith("add_coupon#"):
                response = add_coupons(message)
                client_socket.sendall(json.dumps(response).encode())
            elif message.startswith("bossorderdetail#"): # OID TODO
                response = get_order_detail(message)
                client_socket.sendall(json.dumps(response).encode())   
                                
            #rating
            elif message.startswith("rating#"):
                response = rate_restaurant(message)
                client_socket.sendall(json.dumps(response).encode())
            elif message.startswith("changerating#"):
                response = change_rating(message)
                client_socket.sendall(json.dumps(response).encode())                
            elif message.startswith("bossrating#"):
                response = boss_rating(message)
                client_socket.sendall(json.dumps(response).encode())                         
           
            # new_user
            elif message.startswith("registercustomer#"):
                parts = message.split("#")
                username = parts[1]
                password = parts[2]
                name = parts[3]
                phone = parts[4]
                add_user([username, password, name, phone])
                response = "註冊成功"
                client_socket.sendall(response.encode())
            elif message.startswith("registerboss#"):
                parts = message.split("#")
                username = parts[1]
                password = parts[2]
                name = parts[3]
                phone = parts[4]
                addr = parts[5]
                opentime = parts[6]
                closetime = parts[7]
                add_user([username, password, name, phone,
                         addr, opentime, closetime])
                response = "註冊成功"
                client_socket.sendall(response.encode())
            else:
                response = "未知的指令。"
                client_socket.sendall(response.encode())

            
        except Exception as e:
            print(f"Error: {e}")
            break
    client_socket.close()

# 啟動伺服器
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print("Server is listening...")

    while True:
        client_socket, address = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, address))
        client_thread.start()

if __name__ == "__main__":
    start_server()