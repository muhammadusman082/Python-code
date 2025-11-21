inventory = {
    "P001": {"name": "Laptop", "category": "Electronics", "price": 899.99, "quantity": 15, "supplier": "TechCorp"},
    "P002": {"name": "Wireless Mouse", "category": "Electronics", "price": 25.50, "quantity": 45, "supplier": "TechCorp"},
    "P003": {"name": "Office Chair", "category": "Furniture", "price": 149.99, "quantity": 8, "supplier": "ComfortZone"},
    "P004": {"name": "Notebook", "category": "Stationery", "price": 4.99, "quantity": 100, "supplier": "PaperWorks"}
}
categories = {"Electronics", "Furniture", "Stationery", "Books", "Clothing"}
suppliers = {"TechCorp", "ComfortZone", "PaperWorks", "ReadMore", "FashionHub"}
transactions = []
def format_price(price):
    return f"${price:.2f}"

def display_header(title):
    print(f"\n{title.upper()}\n")

def get_valid_input(prompt, input_type=str, validation_func=None):
    while True:
        try:
            raw = input(prompt)
            value = raw.strip() if input_type == str else input_type(raw)
            if validation_func and not validation_func(value):
                print("Invalid input! Please try again.")
                continue
            return value
        except ValueError:
            print("Invalid input! Please enter a valid value.")
def validate_positive_number(value):
    return value > 0
def small_table(rows, headers):
    col_widths = [max(len(str(item)) for item in col) for col in zip(*([headers] + rows))]
    fmt = "  ".join("{:<" + str(w) + "}" for w in col_widths)
    print(fmt.format(*headers))
    print("-" * (sum(col_widths) + 2*(len(col_widths)-1)))
    for row in rows:
        print(fmt.format(*[str(x) for x in row]))
def generate_product_id(category):
    code = category[:3].upper()
    existing = [pid for pid in inventory.keys() if pid.startswith(code)]
    num = len(existing) + 1
    return f"{code}{num:03d}"
def add_product():
    display_header("Add New Product")
    print("Available categories:", ", ".join(sorted(categories)))
    category = get_valid_input("Enter product category: ", str, lambda x: x in categories)

    pid = generate_product_id(category)
    print(f"Auto-generated Product ID: {pid}")

    name = get_valid_input("Enter product name: ", str)
    price = get_valid_input("Enter product price: $", float, validate_positive_number)
    quantity = get_valid_input("Enter initial quantity: ", int, validate_positive_number)

    print("Available suppliers:", ", ".join(sorted(suppliers)))
    supplier = get_valid_input("Enter supplier: ", str)
    if supplier not in suppliers:
        suppliers.add(supplier)

    inventory[pid] = {"name": name, "category": category, "price": price, "quantity": quantity, "supplier": supplier}
    transactions.append(f"ADDED: {pid} - {name} (Qty: {quantity})")
    print(f"Product '{name}' added successfully with ID: {pid}")
def view_all_products():
    display_header("All Products in Inventory")
    if not inventory:
        print("Inventory is empty!")
        return
    rows = []
    for pid, d in inventory.items():
        rows.append((pid, d['name'], d['category'], format_price(d['price']), d['quantity'], d['supplier']))
    small_table(rows, ("ID", "Name", "Category", "Price", "Qty", "Supplier"))
def display_product_details(product_id):
    product = inventory[product_id]
    display_header(f"Product Details - {product_id}")
    print(f"Product ID: {product_id}")
    print(f"Name: {product['name']}")
    print(f"Category: {product['category']}")
    print(f"Price: {format_price(product['price'])}")
    print(f"Quantity: {product['quantity']}")
    print(f"Supplier: {product['supplier']}")
    qty = product['quantity']
    stock_status = "In Stock" if qty > 10 else "Low Stock" if qty > 0 else "Out of Stock"
    print(f"Stock Status: {stock_status}")
def display_search_results(products, criteria):
    if not products:
        print(f"No products found for {criteria}")
        return
    print(f"\nSearch Results for {criteria}:")
    rows = [(pid, d['name'], format_price(d['price']), d['quantity']) for pid, d in products]
    small_table(rows, ("ID", "Name", "Price", "Qty"))
def search_product():
    display_header("Search Products")
    print("1. Search by Product ID\n2. Search by Product Name\n3. Search by Category\n4. Search by Supplier")
    choice = get_valid_input("Choose search option (1-4): ", int, lambda x: 1 <= x <= 4)
    if choice == 1:
        pid = get_valid_input("Enter Product ID: ", str)
        if pid in inventory:
            display_product_details(pid)
        else:
            print("Product not found!")
    elif choice == 2:
        term = get_valid_input("Enter product name: ", str).lower()
        found = [(pid, d) for pid, d in inventory.items() if term in d['name'].lower()]
        display_search_results(found, f"Name containing '{term}'")
    elif choice == 3:
        print("Available categories:", ", ".join(sorted(categories)))
        cat = get_valid_input("Enter category: ", str)
        found = [(pid, d) for pid, d in inventory.items() if d['category'] == cat]
        display_search_results(found, f"Category: {cat}")
    else:
        print("Available suppliers:", ", ".join(sorted(suppliers)))
        sup = get_valid_input("Enter supplier: ", str)
        found = [(pid, d) for pid, d in inventory.items() if d['supplier'] == sup]
        display_search_results(found, f"Supplier: {sup}")
def update_product():
    display_header("Update Product")
    view_all_products()
    pid = get_valid_input("Enter Product ID to update: ", str)
    if pid not in inventory:
        print("Product not found!")
        return
    display_product_details(pid)
    print("\n1. Price\n2. Quantity\n3. Name\n4. Supplier")
    choice = get_valid_input("Choose field to update (1-4): ", int, lambda x: 1 <= x <= 4)
    if choice == 1:
        new = get_valid_input("Enter new price: $", float, validate_positive_number)
        old = inventory[pid]['price']
        inventory[pid]['price'] = new
        transactions.append(f"UPDATED: {pid} - Price changed from {format_price(old)} to {format_price(new)}")
        print("Price updated successfully!")
    elif choice == 2:
        new = get_valid_input("Enter new quantity: ", int, validate_positive_number)
        old = inventory[pid]['quantity']
        inventory[pid]['quantity'] = new
        transactions.append(f"UPDATED: {pid} - Quantity changed from {old} to {new}")
        print("Quantity updated successfully!")
    elif choice == 3:
        new = get_valid_input("Enter new name: ", str)
        old = inventory[pid]['name']
        inventory[pid]['name'] = new
        transactions.append(f"UPDATED: {pid} - Name changed from '{old}' to '{new}'")
        print("Name updated successfully!")
    else:
        new = get_valid_input("Enter new supplier: ", str)
        old = inventory[pid]['supplier']
        inventory[pid]['supplier'] = new
        if new not in suppliers:
            suppliers.add(new)
        transactions.append(f"UPDATED: {pid} - Supplier changed from '{old}' to '{new}'")
        print("Supplier updated successfully!")
def delete_product():
    display_header("Delete Product")
    view_all_products()
    pid = get_valid_input("Enter Product ID to delete: ", str)
    if pid not in inventory:
        print("Product not found!")
        return
    name = inventory[pid]['name']
    confirm = input(f"Are you sure you want to delete '{name}'? (yes/no): ").lower()
    if confirm == "yes":
        del inventory[pid]
        transactions.append(f"DELETED: {pid} - {name}")
        print("Product deleted successfully!")
    else:
        print("Deletion cancelled.")
def transaction_history():
    display_header("Transaction History")
    if not transactions:
        print("No transactions recorded!")
        return
    print("Recent Transactions (Newest First):")
    for t in transactions[::-1][:10]:
        print(f"• {t}")
def generate_reports():
    transaction_history()
def display_sorted_results(sorted_products, title):
    print(f"\n{title}:")
    rows = [(pid, d['name'], d['category'], format_price(d['price']), d['quantity']) for pid, d in sorted_products]
    small_table(rows, ("ID", "Name", "Category", "Price", "Qty"))
def sort_products():
    display_header("Sort Products")
    print("1. Sort by Name (A-Z)\n2. Sort by Price (Low to High)\n3. Sort by Quantity (High to Low)\n4. Sort by Category")
    ch = get_valid_input("Choose sorting option (1-4): ", int, lambda x: 1 <= x <= 4)
    products_list = list(inventory.items())
    if ch == 1:
        sorted_products = sorted(products_list, key=lambda x: x[1]['name'])
        title = "Products Sorted by Name (A-Z)"
    elif ch == 2:
        sorted_products = sorted(products_list, key=lambda x: x[1]['price'])
        title = "Products Sorted by Price (Low to High)"
    elif ch == 3:
        sorted_products = sorted(products_list, key=lambda x: x[1]['quantity'], reverse=True)
        title = "Products Sorted by Quantity"
    else:
        sorted_products = sorted(products_list, key=lambda x: (x[1]['category'], x[1]['name']))
        title = "Products Sorted by Category"
    display_sorted_results(sorted_products, title)
def display_menu():
    display_header("Inventory Management System")
    print("1. View All Products")
    print("2. Add New Product")
    print("3. Search Products")
    print("4. Update Product")
    print("5. Delete Product")
    print("6. Generate Reports")
    print("7. Sort Products")
    print("8. Exit")
def main():
    print("Welcome to Inventory Management System!")
    print("Manage your products efficiently and effectively")
    while True:
        display_menu()
        choice = get_valid_input("Enter your choice (1-8): ", int, lambda x: 1 <= x <= 8)
        if choice == 1:
            view_all_products()
        elif choice == 2:
            add_product()
        elif choice == 3:
            search_product()
        elif choice == 4:
            update_product()
        elif choice == 5:
            delete_product()
        elif choice == 6:
            generate_reports()
        elif choice == 7:
            sort_products()
        elif choice == 8:
            print("Thank you for using Inventory Management System!")
            break
        input("\nPress Enter to continue...")

main()
