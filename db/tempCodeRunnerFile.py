from db_functions import connect_db, get_query_from_file, connect_gen_coupon, copy_insert_with_file, select_query

if __name__ == "__main__":
    # connect_db(get_query_from_file("dishes.txt"))
    # select_query(get_query_from_file("db_query.txt"))
    connect_db(get_query_from_file("db_query.txt"))
    # connect_gen_coupon()
    # copy_insert_with_file("dish", "Dishes.csv")