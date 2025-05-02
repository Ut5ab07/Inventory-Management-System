import os
from datetime import datetime

INVENTORY_FILE = 'inventory.txt'
SALES_DIR = 'sales'
RESTOCK_DIR = 'restocks'

# Ensuring if directories exists or  not
os.makedirs(SALES_DIR, exist_ok=True)
os.makedirs(RESTOCK_DIR, exist_ok=True)

def read_inventory():
    inventory = []
    with open("inventory.txt", "r") as file:
        for line in file:
            parts = line.strip().split(", ")
            if len(parts) == 5:
                name, brand, quantity, cost, country = parts
                inventory.append({
                    "name": name,
                    "brand": brand,
                    "quantity": int(quantity),
                    "cost": float(cost),
                    "country": country
                })
    return inventory

def write_inventory(inventory):
    with open(INVENTORY_FILE, 'w') as file:
        for item in inventory:
            line = f"{item['name']}, {item['brand']}, {item['quantity']}, {item['cost']}, {item['country']}\n"
            file.write(line)

def display_products():
    inventory = read_inventory()
    if not inventory:
        print("No products to display.")
        return
    print("\nAvailable Products:\n")
    for item in inventory:
        selling_price = item["cost"] * 2
        print(f"Product: {item['name']} | Brand: {item['brand']} | Stock: {item['quantity']} | Price: Rs. {selling_price:.2f} | Country: {item['country']}")


def generate_filename(prefix):
    return f"{prefix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

def sell_products(customer_name, purchases):
    inventory = read_inventory()
    total_amount = 0
    sold_items = []

    for purchase in purchases:
        product_name = purchase['name'].strip().lower()  # Make sure the name is stripped and lowercased
        quantity_requested = purchase['quantity']
        product_found = False  

        for item in inventory:
           
            if item['name'].strip().lower() == product_name:
                print(f"Found product: {item['name']} | Available stock: {item['quantity']}")  
                quantity_with_free = quantity_requested + (quantity_requested // 3)
                if item['quantity'] >= quantity_with_free:
                    item['quantity'] -= quantity_with_free  
                    amount = quantity_requested * item['cost'] * 2  
                    total_amount += amount
                    sold_items.append((item['name'], item['brand'], quantity_requested, quantity_with_free))
                    product_found = True
                    print(f"Stock updated for {item['name']}: {item['quantity']} left") 
                else:
                    print(f"Not enough stock for {item['name']}. Requested: {quantity_with_free}, Available: {item['quantity']}")
                    break

        if not product_found:
            print(f"Product '{purchase['name']}' not found in inventory.")
    
    write_inventory(inventory)  # Saves updated inventory

    invoice_name = os.path.join(SALES_DIR, generate_filename('sale'))
    with open(invoice_name, 'w') as f:
        f.write(f"Customer: {customer_name}\nDate: {datetime.now()}\n\n")
        for name, brand, qty, total_qty in sold_items:
            f.write(f"Product: {name} | Brand: {brand} | Bought: {qty} | Total with Free: {total_qty}\n")
        f.write(f"\nTotal Amount: Rs. {total_amount:.2f}\n")
    print(f"Invoice generated: {invoice_name}")


def restock_products(supplier_name, restocks):
    inventory = read_inventory()
    total_cost = 0
    restocked_items = []

    for restock in restocks:
        product_name = restock['name']
        found = False
        for item in inventory:
            if item['name'].lower() == product_name.lower():
                item['quantity'] += restock['quantity']
                item['cost'] = restock['cost']  # Updates cost if changed
                found = True
                restocked_items.append((item['name'], item['brand'], restock['quantity'], restock['cost']))
                total_cost += restock['quantity'] * restock['cost']
        if not found:
            # Adds new product to inventory
            inventory.append({
                'name': product_name,
                'brand': restock['brand'],
                'quantity': restock['quantity'],
                'cost': restock['cost'],
                'country': restock['country']
            })
            restocked_items.append((product_name, restock['brand'], restock['quantity'], restock['cost']))
            total_cost += restock['quantity'] * restock['cost']

    write_inventory(inventory)

    invoice_name = os.path.join(RESTOCK_DIR, generate_filename('restock'))
    with open(invoice_name, 'w') as f:
        f.write(f"Supplier: {supplier_name}\nDate: {datetime.now()}\n\n")
        for name, brand, qty, cost in restocked_items:
            f.write(f"Product: {name} | Brand: {brand} | Quantity: {qty} | Cost per item: Rs. {cost:.2f}\n")
        f.write(f"\nTotal Restock Cost: Rs. {total_cost:.2f}\n")
    print(f"Restock invoice generated: {invoice_name}")

def main():
    while True:
        print("\n==== WeCare Store Management ====")
        print("1. Display Products")
        print("2. Sell Products")
        print("3. Restock Products")
        print("4. Exit")

        choice = input("Enter your choice (1-4): ")

        if choice == '1':
            display_products()

        elif choice == '2':
            customer = input("Enter customer name: ")
            purchases = []
            while True:
                name = input("Enter product name to buy (or 'done' to finish): ")
                if name.lower() == 'done':
                    break
                quantity = int(input("Enter quantity to buy: "))
                purchases.append({'name': name, 'quantity': quantity})
            sell_products(customer, purchases)

        elif choice == '3':
            supplier = input("Enter supplier name: ")
            restocks = []
            while True:
                name = input("Enter product name to restock (or 'done' to finish): ")
                if name.lower() == 'done':
                    break
                brand = input("Enter brand: ")
                quantity = int(input("Enter quantity to add: "))
                cost = float(input("Enter cost per item: "))
                country = input("Enter country of origin: ")
                restocks.append({'name': name, 'brand': brand, 'quantity': quantity, 'cost': cost, 'country': country})
            restock_products(supplier, restocks)

        elif choice == '4':
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()
