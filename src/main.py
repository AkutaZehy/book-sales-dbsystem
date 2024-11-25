from views import Views

def main():
    views = Views()

    # 示例：获取所有图书
    books = views.get_books()
    print("Books:")
    for book in books:
        print(book.__dict__)

    # 示例：获取特定客户的订单
    customer_id = '12345'
    customer_orders = views.get_customer_orders(customer_id)
    print(f"Customer Orders for {customer_id}:")
    for order in customer_orders:
        print(order)

    # 示例：获取仓库管理订单
    warehouse_orders = views.get_warehouse_manager_orders()
    print("Warehouse Manager Orders:")
    for order in warehouse_orders:
        print(order)

if __name__ == "__main__":
    main()