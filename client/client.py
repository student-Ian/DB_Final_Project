import json
import socket

# 全域變數：共享的 socket
_client_socket = None

def connect_to_server(host='127.0.0.1', port=9999):
    global _client_socket
    if _client_socket is None:
        _client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        _client_socket.connect((host, port))
        print(f"Connected to server {host}:{port}")

def send_message(message):
    """
    傳送訊息到伺服器，並接收伺服器的回應。
    :param message: 傳送的訊息 (str)
    :return: 伺服器的回應 (list 或 str)
    """
    global _client_socket
    if _client_socket is None:
        raise RuntimeError("Client is not connected to the server. Call connect_to_server first.")
    
    try:
        # 傳送訊息
        _client_socket.sendall(message.encode())
        data = _client_socket.recv(2147483648)
        
        if not data:
            raise ConnectionError("Server closed the connection.")
        
        
        # 嘗試解析 JSON
        decoded_data = data.decode()
        try:
            return json.loads(decoded_data)  # 解碼並返回 JSON
        except json.JSONDecodeError:
            return decoded_data  # 如果不是 JSON，回傳純字串
    except Exception as e:
        print(f"Error in send_message: {e}")
        return None

def close_connection():
    global _client_socket
    if _client_socket:
        _client_socket.close()
        _client_socket = None
        print("Connection closed.")
