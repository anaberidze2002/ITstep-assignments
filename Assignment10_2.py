def calculate_cart_total(discount_rate, *pricrs):
    total = 0
    for p in pricrs:
        discount_amount = (p * discount_rate) / 100
        discounted_price = p - discount_amount
        total += discounted_price
    return float(total)
print(calculate_cart_total(2,10))

def filter_and_sort_products(**products):
    products_list = []
    for product_name, product_price in products.items():
        products_list.append((product_price, product_name))
    filtered_products = filter(lambda product: product[0] >= 100, products_list)
    sorted_products = sorted(filtered_products)
    final_products = []
    for price, name in sorted_products:
        final_products.append((name,price))
    return final_products
result  =filter_and_sort_products(mous = 50, laptop = 2900, monitor = 350, phone = 1600)
print(result)