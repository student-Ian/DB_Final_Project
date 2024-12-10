import psycopg2

def db_conn():
    conn = psycopg2.connect(host="junction.proxy.rlwy.net",
                          port=45436,
                          database="railway",
                          user="postgres",
                          password="rHDdcNSyKZNyrctIWpNFnAYBfqRuxnIl")

    cur = conn.cursor()
    return conn, cur

def get_query_from_file(filename):
  sql_query = ""
  with open(filename, "r", encoding='utf-8') as f:
    for l in f.readlines():
      sql_query = sql_query + l
  f.close()
  return sql_query

def select_query(filename, format = 'list', has_param = False, params = list()):
  
    conn, cur = db_conn()

    query = get_query_from_file(filename)

    if not has_param:
        cur.execute(query)
    else:
        cur.execute(query, params)
    print(f"sql executed successfully")
    column_names = [desc[0] for desc in cur.description]

    results = cur.fetchall()

    conn.commit()

    cur.close()
    conn.close()

    if format == "list":
        return results
    if format == "dict":
       result_dict = [dict(zip(column_names, result)) for result in results]
       return result_dict
    
    # timber 4a01379a1c67ee2d
    # wildernesses bd9f2eb66804f8c2
    # backland c337a3b1f20e2eed

def no_output_query(filename, has_param = False, params = list()):

    conn, cur = db_conn()

    query = get_query_from_file(filename)

    if not has_param:
        cur.execute(query)
    else:
        cur.execute(query, params)
    print(f"sql executed successfully")

    conn.commit()
    print("sql committed")

    cur.close()
    conn.close()
    
def get_users():
   return select_query("get_customers.txt", "list")

def get_bosses():
   return select_query("get_bosses.txt", "list")

def get_restaurant_list():
    return select_query("get_restaurant_list.txt", "dict")

def get_menu():
    return select_query("get_menu.txt", "dict")

def get_current_order(param_list):
    return select_query("get_current_order.txt", "dict", True, param_list)

def send_order(param_list):
    return no_output_query("send_order.txt", True, param_list)

def send_order_detail(param_list):
    return no_output_query("send_order_detail.txt", True, param_list)

def get_vouchers():
    return select_query("get_vouchers.txt", "dict")

def get_coupons():
    return select_query("get_coupons.txt", "dict")

def get_menu_boss():
    return select_query("get_menu_boss.txt", "dict")

def add_dish_query(param_list):
    return no_output_query("add_dish.txt", True, param_list)

def update_dishes(param_list):
    return no_output_query("update_dishes.txt", True, param_list)

def get_order_history():
    return select_query("get_order_history.txt", "dict")

def get_boss_order_history():
    return select_query("get_boss_order_history.txt", "dict")

def get_order_detail_query(param_list):
    return no_output_query("get_orderdetail.txt", True, param_list)

def handle_view_and_modify_restaurant_info_query():
    return select_query("handle_view_and_modify_restaurant_info.txt", "dict")

def view_coupons_query():
    return select_query("view_coupons_query.txt", "dict")

def modify_coupon_query(param_list):
    return no_output_query("modify_coupon.txt", True, param_list)

def add_coupon_query(param_list):
    return no_output_query("add_coupon.txt", True, param_list)

def rate_restaurant_query(param_list):
    return select_query("rate_restaurant.txt", "dict", True, param_list)

def change_rating_query(param_list):
    return no_output_query("change_rating.txt", True, param_list)

def boss_rating_query(param_list):
    return select_query("boss_rating.txt", "dict", True, param_list)

def add_user(param_list):
    return no_output_query("add_user.txt", True, param_list)

def get_max_oid():
    return select_query("get_max_oid.txt", "list")[0][0]

def redeem_coupon_sql(param_list):
    return no_output_query("redeem_coupon.txt", True, param_list)
# user: timber 4a01379a1c67ee2d, wilderness bd9f2eb66804f8c2
# restaurant: backland c337a3b1f20e2eed