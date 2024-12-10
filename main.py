from sqlfunction import *

if __name__ == "__main__":
    print("get_users()")
    users = get_users()
    print(users)

    print("get_bosses()")
    bosses = get_bosses()
    print(bosses)

    print("get_menu()")
    menu = get_menu()
    print(menu)

    print("get_current_order(crapes_8YE)")
    current_order = get_current_order(param_list=["crapes_8YE"])  # Replace with actual parameters
    print(current_order)

    print("get_vouchers()")
    vouchers = get_vouchers()
    print(vouchers)

    print("get_coupons()")
    coupons = get_coupons()
    print(coupons)

    print("get_menu_boss()")
    menu_boss = get_menu_boss()
    print(menu_boss)

    print("get_order_history()")
    order_history = get_order_history()
    print(order_history)

    print("handle_view_and_modify_restaurant_info_query()")
    restaurant_info = handle_view_and_modify_restaurant_info_query()
    print(restaurant_info)

    print("view_coupons_query()")
    viewed_coupons = view_coupons_query()
    print(viewed_coupons)

    # Functions that modify data or send queries (no return values)
    # print("send_order(param_list)")
    # send_order(param_list=["order_id", "customer_id"])  # Replace with actual parameters

    # print("send_order_detail(param_list)")
    # send_order_detail(param_list=["order_detail_param1", "order_detail_param2"])  # Replace with actual parameters

    # print("add_dish_query(param_list)")
    # add_dish_query(param_list=["dish_name", "price"])  # Replace with actual parameters

    # print("update_dishes(param_list)")
    # update_dishes(param_list=["dish_id", "new_price"])  # Replace with actual parameters

    # print("modify_coupon_query(param_list)")
    # modify_coupon_query(param_list=["coupon_id", "new_value"])  # Replace with actual parameters
