from db_functions import connect_db, get_query_from_file, connect_gen_coupon, copy_insert_with_file, select_query

if __name__ == "__main__":
    # connect_db(get_query_from_file("dishes.txt"))
    # a = select_query(get_query_from_file("db_query.txt"))
    # print(a[0][0])
    connect_db(get_query_from_file("db_query.txt"))
    # connect_gen_coupon()
    # copy_insert_with_file("order_detail", "OrderDetails.csv")
    # copy_insert_with_file("Order", "Orders.csv")

# 270762,backland,嫩煎雞腿堡,3
# 270762,backland,麥香雞,3
# 270762,backland,麥脆雞腿,1
# 270762,backland,麥香魚,2

# DETAIL:  Key (oid)=(270762-270777) is not present in table "Order".