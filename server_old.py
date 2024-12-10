import socket
import threading
import json
from collections import Counter
from sqlfunction import *

# 伺服器設置
HOST = '127.0.0.1'
PORT = 9999

# 資料庫
restaurant_info = [
    {"username": "234", "name": "美味餐廳234", "address": "123 美食街", "hours": "10:00-22:00"},
    {"username": "345", "name": "和風餐廳345", "address": "456 美食街", "hours": "11:00-21:00"}
]

coupons = [
    {"username": "234", "discount": "0.9"},
    {"username": "345", "discount": "0.85"}
]

usercoupons = [
    {"belongsto": "111", "belongsto" : "11233", "vdiscount": "0.9"},
    {"belongsto": "222", "belongsto" : "54412", "vdiscount": "0.85"}
]

dishes = [
    {"id": 0, "username": "345", "dish_name": "壽司", "price": "100"},
    {"id": 1, "username": "345", "dish_name": "生魚片", "price": "120"},
    {"id": 2, "username": "234", "dish_name": "炒飯", "price": "50"},
    {"id": 3, "username": "234", "dish_name": "拉麵", "price": "80"}
]

history_orders = [
    {"id": 1, "username": "234", "dish_name": "炒飯", "price": 50},
    {"id": 2, "username": "234", "dish_name": "拉麵", "price": 80},
    {"id": 3, "username": "345", "dish_name": "壽司", "price": 100},
    {"id": 4, "username": "345", "dish_name": "生魚片", "price": 120}
]

# 登錄帳戶
users = [("111", "aaa"), ("222", "bbb")]
boss = [("234", "rrr"), ("345", "ppp")]

orders = []

# 登錄處理 
# query ✅
def process_login_request(request): 
    """
    處理登入請求
    """
    try:
        users = get_users() # query
        boss = get_bosses() # query

        command, username, password = request.split("#")
        if command != "login":
            return "Invalid command"
        if (username, password) in users:
            return "userconfirm"
        elif (username, password) in boss:
            return "bossconfirm"
        else:
            return "deny"
    except ValueError:
        return "Malformed request"

# query ❌
def process_order_request(order_string):
    """
    處理訂單請求，統計餐點數量，並加入全域訂單列表。
    
    :param order_string: 訂單字串，格式為 "訂單內容: 餐點1, 餐點2, ..."
    :return: 統計結果 [(餐點, 數量), ...]
    """
    try:
        # 提取訂單內容
        prefix, items = order_string.split(": ", 1)
        if prefix != "訂單內容":
            return "Invalid order command"
        
        # 將餐點分割並統計
        item_list = [item.strip() for item in items.split(",")]
        item_counts = Counter(item_list)
        
        # 將統計結果轉為 [(餐點, 數量), ...] 格式
        order_summary = list(item_counts.items())
        
        # 將結果加入全域訂單列表
        orders.append(order_summary)
        print(orders)
        
        return order_summary
    except ValueError:
        return "Malformed order request"

# query - dishes ✅
def menu_request(message):
    parts = message.split("#")
    username = parts[1]

    dishes = get_menu() 
    user_dishes = [{"dname": dish["dname"], "price": dish["price"]} for dish in dishes if dish["rusername"] == username]
    return user_dishes  

# query ✅
def usercoupon_request(message):
    """
    查看或修改菜品：
    - 查看：dishes#username
    - 修改：updatedish#username#dish_name#new_name#new_price
    """
    parts = message.split("#")
    username = parts[1]

    usercoupons = get_vouchers() # query 
    usercoupon_list = [
        {"vcode": usercoupon["vcode"], "vdiscount": usercoupon["vdiscount"]}
        for usercoupon in usercoupons
        if usercoupon["belongsto"] == username
    ]
    return usercoupon_list
 

#boss query ❌ ?
def add_dish(message):
    parts = message.split('#')
    if len(parts) != 4:
        print("無效的消息格式")
        return "無效的消息格式"

    command, username, dish_name, dish_price = parts

    maxid = max(dishes, key=lambda x: x["id"])["id"]

    dishes.append({"id": maxid+1, "username": username, "dish_name": dish_name, "price": str(dish_price)})

    # 輸出成功消息
    print(f"已成功將菜品 '{dish_name}' 添加至用戶 {username} 的菜單，價格為 {dish_price} 元。")
    
    user_dishes = [{"dish_name": dish["dish_name"], "price": dish["price"]} for dish in dishes if dish["username"] == username]
    return user_dishes


# 處理菜品操作 query ✅
def view_dishes(message):
    """
    查看或修改菜品：
    - 查看：dishes#username
    - 修改：updatedish#username#dish_name#new_name#new_price
    """
    parts = message.split("#")
    username = parts[1]

    dishes = get_dishes() # query 
    user_dishes = [{"id":dish["id"], "dish_name": dish["dish_name"], "price": dish["price"]} for dish in dishes if dish["username"] == username]
    return user_dishes

# query ✅
def updated_dishes(message):
    parts = message.split("#")
    username = parts[1]
    try:
        id = parts[2] #???
        new_name = parts[3]
        new_price = int(parts[4])
        
        update_dishes([new_name, new_price, username, id]) #query
        for dish in dishes:
            if dish["id"] == id:
                dish["dish_name"] = new_name
                dish["price"] = str(new_price)
                
        return "success"
    except (IndexError, ValueError):
        return "failed"

# 處理歷史訂單 ✅
def boss_view_history_order(message):
    """
    查看歷史訂單：bosshistoryorder#username
    """
    username = message.split("#")[1]

    user_orders = get_order_history() #query
    user_orders = [order for order in history_orders if order["username"] == username]
    return user_orders

# 處理餐廳資訊
def handle_view_and_modify_restaurant_info(message):
    """
    查看或修改餐廳資訊：
    - 查看：restaurant_info#username
    - 修改：update_restaurant#username#key#new_value
    """
    parts = message.split("#")
    username = parts[1]

    if message.startswith("restaurant_info#"):
        info = next((info for info in restaurant_info if info["username"] == username), None)
        if info:
            return {"status": "success", "restaurant_info": info}
        return {"status": "error", "message": "未找到餐廳資訊。"}
    
    elif message.startswith("update_restaurant#"):
        key = parts[2]
        new_value = parts[3]
        for info in restaurant_info:
            if info["username"] == username:
                if key in info:
                    info[key] = new_value
                    return {"status": "success", "message": f"餐廳資訊 '{key}' 已更新為 {new_value}。"}
                return {"status": "error", "message": "無效的資訊鍵值。"}
    return {"status": "error", "message": "未知的餐廳資訊操作指令。"}

# 處理優惠券
def view_coupons(message):
    """
    查看或修改優惠券：
    - 查看：coupons#username
    - 修改：update_coupon#username#new_discount
    """
    parts = message.split("#")
    username = parts[1]

    couponlist = [coupon for coupon in coupons if coupon["username"] == username]
    return couponlist
    
    
    
def modify_coupons(message):
    parts = message.split("#")
    username = parts[1]
    new_discount = parts[2]
    for coupon in coupons:
        if coupon["username"] == username:
            coupon["discount"] = new_discount
            newcoupon = [coupon for coupon in coupons if coupon["username"] == username]
            return newcoupon
    return {"status": "error", "message": "未找到優惠券。"}

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
            elif message.startswith("訂單內容:"):
                order_summary = process_order_request(message)
                client_socket.sendall(json.dumps(order_summary).encode())
            elif message == "restaurant_list":
                response = [{"username":restaurant["username"], "name":restaurant["name"]} for restaurant in restaurant_info]
                client_socket.sendall(json.dumps(response).encode())
            elif message.startswith("menu"):
                response = menu_request(message)
                client_socket.sendall(json.dumps(response).encode())
            elif message.startswith("usercoupon"):
                response = usercoupon_request(message)
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
