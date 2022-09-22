# VERNON NG WEN FENG
# TP057910
import time


def display_message(message):
    print("\n" * 50)
    print(message)
    time.sleep(1)
    print("\n" * 50)


def grab_item_list(item_file):
    """
    get the item list from item file in the form of XXX;XXX;XXX;XXX
    """
    with open(item_file, "r") as grab_list:
        item_list = []
        for line in grab_list:
            item_list.append(line)

    return item_list


def check_item(selected_cat, itemid):
    """
    Check the if the item ID in the specific category is exist
    """
    item_list = grab_item_list(selected_cat + ".txt")
    item_exist = False
    for item in item_list:
        if itemid == item[:5]:
            item_exist = True
            break

    return item_exist


def search_groceries_detail():
    """
    allow admin to search for grocery detail using item id
    """
    file_list = ["Fresh Produce.txt", "Frozen.txt", "Beverages.txt", "Health Care.txt", "Beauty Personal Care.txt",
                 "Household.txt"]
    item_id = input("Enter item ID to search detail:").upper()
    item_found = False
    for file in file_list:
        with open(file, "r") as find_item:
            for line in find_item:
                if item_id == line[:5]:
                    item_info = line.strip().split(";")
                    file_cat = file[:-4]
                    item_found = True
                    break
    # if item found in file display information
    if item_found:
        print("\n" * 50)
        print("Category : %s"%file_cat)
        print("="*80)
        print("{:<20}{:<50}{:<1}".format("Item ID", "Item Name", "Item Price"))
        print("{:<20}{:<50}{:<1}".format(item_info[0], item_info[1], "RM" + item_info[2]))
        print("=" * 80)
    else:
        display_message("="*18 + "\nItem ID not Found.\n" + "="*18)
    input("\n\nPress [ENTER] to go back")
    print("\n"*50)


def view_personal_information(username):
    """
    Display user information to user
    """
    user_info = []
    # read and get user information from file
    with open("Accounts.txt", "r") as personal_info:
        for line in personal_info:
            user_info = line.strip().split(";")
            if username in user_info:
                break
    print("="*25)
    print("Username: " + user_info[0])
    print("address: " + user_info[2])
    print("Contact No.: " + user_info[3])
    print("=" * 25)
    input("\nPress [ENTER] to go back")
    print("\n"*50)



def view_order_history(username):
    """
    Display order history to the user and allow admin to serach for order history of specific user
    """
    with open("Order History.txt", "r") as order_history:
        count = 0
        user_order_history = []
        for line in order_history:
            if username in line:
                order_info = line.strip().split(";")
                user_order_history.append(order_info)
                count += 1

    if len(user_order_history) == 0:
        print("Username order record does not exist.")
    k = 0
    while k < count:
        print("="*23 + "\nOrder ID:" + user_order_history[k][0] + "\n" + "-"*23)
        print("Customer:" + user_order_history[k][1])
        print("Total Price: RM" + user_order_history[k][4])
        print("Address:" + user_order_history[k][2])
        print("Contact No.:" + user_order_history[k][3] + "\n" + "-"*110)
        print("{:<20}{:<50}{:<20}{:<1}".format("Item ID", "Item Name", "Item Price", "Quantity"))
        for item in user_order_history[k][5:][0:]:
            item_detail = item.strip().split("@")
            print("{:<20}{:<50}{:<20}{:<1}".format(item_detail[0], item_detail[1], item_detail[2], item_detail[3]))
        print("=" * 110 + "\n\n\n")
        k += 1
    input("Press [ENTER] to go back")
    print("\n"*50)


def record_order(total_price, item_in_cart, p_info):
    """
    record order information in to order history file.
    """
    with open("Order History.txt", "r") as read_order:
        order_id = []
        for line in read_order:
            order_id.append(line.strip().split(";"))
        # write order information into file
        # the information is record in the form of XXX;XXX;XXX;XXX;item1@item2@item3
        # XXX are the personal information
        with open("Order History.txt", "a") as write_order:
            write_order.write(
                (str(len(order_id) + 1).zfill(6)) + ";" + p_info[0] + ";" + p_info[2] + ";" + p_info[3] + ";" + str(
                    round(total_price, 2)))
            for item in item_in_cart[1:]:
                write_order.write(";" + item[0] + "@" + item[1] + "@" + item[2] + "@" + item[3])
            write_order.write("\n")
    with open("Cart.txt", "w") as empty_cart:
        empty_cart.write(p_info[0] + "\n")


def check_out(username):
    """
   check out order, clear cart and record the order information to order history file.
    """
    # read user personal information to get address and contact number
    while True:
        with open("Accounts.txt", "r") as read_Pinfo:
            for line in read_Pinfo:
                if username in line:
                    p_info = line.strip().split(";")
        item_in_cart = get_item_in_cart()
        total_price = 0
        # display the item in cart and total price and ask user whether to pay or go back previous page
        print("=" * 80)
        print("{:<50}{:<20}{:<1}".format("Item Name", "Item Price", "Quantity"))
        for item_info in item_in_cart[1:]:
            print("{:<50}{:<20}{:<1}".format(item_info[1], "RM" + item_info[2], item_info[3]))
            total_price = total_price + (float(item_info[2]) * float(item_info[3]))
        print("=" * 80)
        print("Total Price =RM" + str(round(total_price, 2)))
        print("=" * 25)
        print("Address :" + p_info[2] + "\nContact Number:" + p_info[3])
        print("="*25)

        instruction = input("\n\nDo you confirm to Pay.\n1.Pay\n2.BACK\nEnter instruction:")
        if instruction == "1":
            record_order(total_price, item_in_cart, p_info)
            display_message("="*31 + "\nThank you for shopping with us!\n" + "="*31)
            return True

        elif instruction == "2":
            print("\n" * 50)
            return False
        else:
            display_message("=" * 33 + "\nPlease Enter a Valid instruction.\n" + "=" * 33)


def get_item_in_cart():
    """
    get the item in cart and return item list
    return "empty" if nothing in cart
    """
    cart_list = grab_item_list("Cart.txt")
    if len(cart_list) < 2:
        return "Empty"
    item_in_cart = []
    for i in cart_list:
        item_in_cart.append(i.strip().split(";"))

    return item_in_cart


def modify_item_quantity(item_to_modify, item_in_cart, new_quantity):
    """
    get the new item information and overwrite the information in cart file
    """
    cart_list = grab_item_list("Cart.txt")
    count = 1
    for item in item_in_cart[1:]:
        if item_to_modify == item[0]:
            item[3] = str(new_quantity)
            if int(new_quantity) <= 0:
                cart_list.remove(cart_list[int(count)])
            else:
                item_new_quantity = str(item[0] + ";" + item[1] + ";" + item[2] + ";" + item[3] + "\n")
                cart_list[count] = item_new_quantity
        else:
            count += 1

    with open("Cart.txt", "w") as modify_quantity:
        for line in cart_list:
            modify_quantity.write(line)
        display_message("="*24 + "\nItem have been modified.\n" + "="*24)


def modify_cart():
    """
    Allow user to modify item in cart
    """
    while True:
        item_in_cart = get_item_in_cart()
        if item_in_cart == "Empty":
            break
        print("=" * 110)
        print("{:<20}{:<50}{:<20}{:<1}".format("Item ID", "Item Name", "Item Price", "Quantity"))
        itemid = []
        # display all the item in cart
        for item_info in item_in_cart[1:]:
            if int(item_info[3]) > 0:
                print("{:<20}{:<50}{:<20}{:<1}".format(item_info[0], item_info[1], "RM" + item_info[2], item_info[3]))
                itemid.append(item_info[0])
        print("=" * 110)
        # ask user to input item id to modify
        item_to_modify = input("Enter item id to modify or enter 'BACK' to go back:").upper()
        if item_to_modify == "BACK":
            print("\n"*50)
            break
        # ask user to enter new quantity
        elif item_to_modify in itemid:
            new_quantity = input("Enter new quantity:")
            modify_item_quantity(item_to_modify, item_in_cart, new_quantity)
        else:
            display_message("=" * 33 + "\nPlease Enter a Valid instruction.\n" + "=" * 33)



def view_cart():
    """
    open cart file and display item inside. and the total price
    if cart is empty display "Cart is Empty"
    """
    while True:
        item_in_cart = get_item_in_cart()
        if item_in_cart == "Empty":
            display_message("="*13 + "\nCart is Empty\n" + "="*13)
            break
        total_price = 0
        print("="*78)
        print("{:<50}{:<20}{:<1}".format("Item Name", "Item Price", "Quantity"))
        for item_info in item_in_cart[1:]:
            print("{:<50}{:<20}{:<1}".format(item_info[1], "RM" + item_info[2], item_info[3]))
            total_price = total_price + (float(item_info[2]) * float(item_info[3]))
        print("=" * 78)
        print("\n\t\t\t\t\t\tTotal Price =RM" + str(round(total_price, 2)))
        instruction = input("\n\nWhat you want to do\n1.Modify\n2.Check Out\n3.Back\nEnter Instruction:")
        if instruction == "3":
            print("\n"*50)
            break
        elif instruction == "1":
            print("\n" * 50)
            modify_cart()
        elif instruction == "2":
            print("\n" * 50)
            pay = check_out(item_in_cart[0][0][0:])
            if pay:
                break
        else:
            display_message("=" * 33 + "\nPlease Enter a Valid instruction.\n" + "=" * 33)



def add_to_cart(selected_cat, itemid, quantity):
    """
    read and get the item list from item file and write item to cart file.
    """
    # read and get item list from item file
    with open(selected_cat + ".txt", "r") as get_item:
        for line in get_item:
            if itemid in line:
                item_info = line.strip()
    cart = []
    cart_list = grab_item_list("Cart.txt")
    item_in_cart = False
    # get item in cart list
    for i in cart_list[1:]:
        cart.append(i.strip().split(";"))
    count = 1
    # check if item in cart list. if item in cart add the quantity to existing quantity
    # if item not in cart, write item to cart
    for item in cart:
        if itemid in item:
            item[3] = str(int(item[3]) + int(quantity))
            item_new_quantity = str(item[0] + ";" + item[1] + ";" + item[2] + ";" + item[3] + "\n")
            cart_list[count] = item_new_quantity
            with open("Cart.txt", "w") as overwrite_new_quantity:
                for line in cart_list:
                    overwrite_new_quantity.write(line)
                display_message("=" * 28 + "\nItem Have Been Added to cart\n" + "=" * 28)
            item_in_cart = True
            break
        else:
            count += 1

    if not item_in_cart:
        with open("Cart.txt", "a") as add_cart:
            add_cart.write(item_info + ";" + quantity + "\n")
            display_message("="*28 + "\nItem Have Been Added to cart\n" + "="*28)


def input_item_to_cart(selected_cat):
    """
    Ask user for item id and quantity to add to cart
    """
    while True:
        display_grocery(selected_cat)
        add_cart = input("Enter item ID to add to cart or 'BACK' to return:").upper()
        item_exist = check_item(selected_cat, add_cart)
        if add_cart == "BACK":
            print("\n" * 50)
            break
        if not item_exist:
            display_message("="*41 + "\nPlease enter an exist Item ID on the list\n" + "="*41)

            continue

        while True:
            try:
                quantity = int(input("Enter quantity you want:"))
                if quantity <= 0:
                    display_message("="*29 + "\nPlease enter a positive value\n" + "="*29)
                    continue
                break
            except:
                display_message("="*29 + "\nPlease enter an integer value\n" + "="*29)
                continue
        add_to_cart(selected_cat, add_cart, str(quantity))


def view_all_order_history():
    """
    Display all order history
    """
    with open("Order History.txt", "r") as order_history:
        count = 0
        user_order_history = []
        for line in order_history:
            order_info = line.strip().split(";")
            user_order_history.append(order_info)
            print("="*23 + "\nOrder ID:" + user_order_history[count][0] + "\n" + "-"*23)
            print("Customer:" + user_order_history[count][1])
            print("Total Price:" + user_order_history[count][4])
            print("Address:" + user_order_history[count][2])
            print("Contact No.:" + user_order_history[count][3] + "\n" + "-"*110)
            print("{:<20}{:<50}{:<20}{:<1}".format("Item ID", "Item Name", "Item Price", "Quantity"))
            for item in user_order_history[count][5:][0:]:
                item_detail = item.strip().split("@")
                print("{:<20}{:<50}{:<20}{:<1}".format(item_detail[0], item_detail[1], item_detail[2], item_detail[3]))
            print("="*110 + "\n\n\n")
            count += 1

    input("Press [ENTER] to go back")
    print("\n"*50)


def search_del_groceries(item_to_del, item_list):
    """
    find the Item ID in item list and return item position in the list
    """
    count = 0
    print("\n" * 50)
    for item_id in item_list:
        if item_to_del in item_id:
            item_info = item_id.strip().split(";")
            # ask whether to confirm delete item
            while True:
                print("="*80)
                print("{:<20}{:<50}{:<1}".format("Item ID", "Item Name", "Item Price"))
                print("{:<20}{:<50}{:<1}".format(item_info[0], item_info[1], "RM" + item_info[2]))
                print("=" * 80)
                conf_del = input("\n\nDo you confirm to delete this item\n1. Confirm\n2.No\nEnter Instruction:")
                if conf_del == "1":
                    return count
                elif conf_del == "2":
                    print("\n" * 50)
                    return "NO"
                else:
                    display_message("="*19 + "\nInvalid Instruction\n" + "="*19)
        else:
            count += 1

    return "INVALID"


def inp_delete_groceries(selected_cat):
    """
   Ask admin the Item ID to delete item.
    """
    while True:
        display_grocery(selected_cat)
        item_to_del = input("Enter the Item ID to delete or enter 'BACK' to return to category menu.\nEnter Item ID:").upper()
        if item_to_del == "BACK":
            print("\n" * 50)
            break
        # get the item list and find the input item id in the list
        item_list = grab_item_list(selected_cat + ".txt")
        delete_item = search_del_groceries(str(item_to_del), item_list)
        if delete_item == "NO":
            continue
        elif delete_item == "INVALID":
            display_message("=" * 27 + "\nPlease Enter Valid Item ID.\n" + "=" * 27)
            continue
        else:
            # remove item from list
            item_list.remove(item_list[int(delete_item)])
        # write the new item list into file
        with open(selected_cat + ".txt", "w") as remove_item:
            for item in item_list:
                remove_item.write(item)
            display_message("="*23 + "\nItem Have been Deleted.\n" + "="*23)


def modify_item(item_list, item_to_modify, iname_or_iprice):
    """
    test whether admin select modify item name or price.
    and ask to input the selected information to modify
    """
    while True:
        if iname_or_iprice == "1":
            modify = input("Enter New Name for item:")
            if ";" in modify or "@" in modify:
                display_message("="*32 + "\nItem name contain invalid symbol\n" + "="*32)
                continue
            print("\n" * 50)
        else:
            try:
                # test the input value
                modify_price = float(input("Enter item price:RM"))
                if modify_price <= 0:
                    display_message("=" * 29 + "\nPlease enter a positive value\n" + "=" * 29)
                    continue
                modify = round(float(modify_price), 2)
                print("\n" * 50)
            except:
                display_message("="*28 + "\nPlease enter a proper value.\n" + "="*28)
                continue
        for item_info in item_list:
            if item_info[0] == item_to_modify:
                item_info[int(iname_or_iprice)] = str(modify)

        return item_list


def inp_modify_grocery(selected_cat):
    """
    Allow admin to modify item in selected category of grocery
    """
    while True:
        display_grocery(selected_cat)
        item_to_modify = input(
            "Enter the Item ID to Modify or enter 'BACK' to return to category menu.\nEnter Item ID:").upper()
        item_exist = check_item(selected_cat, item_to_modify)
        if item_to_modify == "BACK":
            print("\n" * 50)
            break
        if not item_exist:
            display_message("="*27 + "\nPlease Enter Valid Item ID.\n" + "="*27)

            continue
        # ask whether to modify item name of price
        while True:
            print("\n" * 50)
            iname_or_iprice = input(
                "Do you want to change the Item name or price.\n1.Item Name\n2.Item Price\nEnter instruction:")
            if iname_or_iprice == "1" or iname_or_iprice == "2":
                print("\n" * 50)
                break
            else:
                display_message("="*33 + "\nPlease Enter a Valid instruction.\n" + "="*33)
                continue
        # get the existing item list and modify the item
        item_list = grab_item_list(selected_cat + ".txt")
        item_list1 = []
        for items in item_list:
            item = items.strip().split(";")
            item_list1.append(item)
        new_list = modify_item(item_list1, item_to_modify, iname_or_iprice)
        # write new information into the system
        with open(selected_cat + ".txt", "w") as modify_item_info:
            for item in new_list:
                modify_item_info.write(item[0] + ";" + item[1] + ";" + item[2] + "\n")


def display_grocery(selected_cat):
    """
    read selected file and display the item inside
    """
    with open(selected_cat + ".txt", "r") as readfile:
        print("="*80)
        print("{:<20}{:<50}{:<1}".format("Item ID", "Item Name", "Item Price"))
        for line in readfile:
            item = line.strip().split(";")
            print("{:<20}{:<50}{:<1}".format(item[0], item[1], "RM" + item[2]))
        print("=" * 80)
        print("\n")


def view_category_list(instruction):
    """
    Display category list.
    """
    while True:
        selected_cat = select_category()
        if selected_cat == "BACK":
            print("\n" * 50)
            break
        elif selected_cat == "INVALID":
            continue

        if instruction == "View Only":
            print("\n" * 50)
            display_grocery(selected_cat)
            input("Press [Enter] to go back.")
            print("\n" * 50)
        elif instruction == "Place Order":
            print("\n" * 50)
            input_item_to_cart(selected_cat)
            print("\n" * 50)
        elif instruction == "Modify item":
            print("\n" * 50)
            inp_modify_grocery(selected_cat)
            print("\n" * 50)
        elif instruction == "Delete item":
            print("\n" * 50)
            inp_delete_groceries(selected_cat)
            print("\n" * 50)
        elif instruction == "Upload item":
            print("\n" * 50)
            upload_item(selected_cat + ".txt")
            print("\n" * 50)


def select_category():
    print(
        "Groceries Category List.\n1.Fresh Produce\n2.Frozen\n3.Beverages\n4.Health Care\n5.Beauty & Personal Care\n6.Household\n7.Back")
    instruction = input("Please enter instruction number to proceed.\nEnter instructions:")

    if instruction == "1":
        category = "Fresh Produce"
        return category
    elif instruction == "2":
        category = "Frozen"
        return category
    elif instruction == "3":
        category = "Beverages"
        return category
    elif instruction == "4":
        category = "Health Care"
        return category
    elif instruction == "5":
        category = "Beauty Personal Care"
        return category
    elif instruction == "6":
        category = "Household"
        return category
    elif instruction == "7":
        return "BACK"
    else:
        display_message("="*20 + "\nInvalid instruction\n" + "="*20)
        return "INVALID"


def item_codeindex(item_list, item_codename):
    """
    get new code index for new item
    """
    item_index = 1
    # read the index in file, and get new index
    for item_info in item_list:
        if item_index == int(item_info[0][2:]):
            item_index += 1
        else:
            break

    # return new index and the position it will be placed
    position = item_index - 1
    item_code = item_codename + str(item_index).zfill(3)
    return item_code, position


def item_codeID(cate_file):
    """
    get new item code for new item
    """
    if cate_file == "Fresh Produce.txt":
        item_code_name = "FP"
    elif cate_file == "Frozen.txt":
        item_code_name = "FR"
    elif cate_file == "Beverages.txt":
        item_code_name = "BV"
    elif cate_file == "Health Care.txt":
        item_code_name = "HC"
    elif cate_file == "Beauty Personal Care.txt":
        item_code_name = "BP"
    elif cate_file == "Household.txt":
        item_code_name = "HH"

    # read groceries file to get item list.
    with open(cate_file, "r") as file:
        item_list = []
        for line in file:
            item_info = line.strip().split(";")
            item_list.append(item_info)
        # get new code ID
        item_code_position = item_codeindex(item_list, item_code_name)

    return item_code_position


def check_name_exist(category_file, item_name):
    # check if name exist in system
    item_list = grab_item_list(category_file)
    for i in item_list:
        item = i.strip().split(";")
        if item_name == item[1]:
            return True


def input_groceries(category_file):
    while True:
        # ask for new item name
        item_name = input("Enter item name:")
        if ";" in item_name or "@" in item_name:
            display_message("="*33 + "\nitem name contain invalid symbol\n" + "="*33)
            continue
        # check if the new item name exist in the system
        name_exist = check_name_exist(category_file, item_name)
        if name_exist:
            display_message("="*16 + "\nItem Name Exist.\n" + "="*16)
            continue

        # ask for new item price and test the value
        try:
            input_item_price = float(input("Enter item price:RM"))
            item_price = round(float(input_item_price), 2)
        except:
            display_message("=" * 29 + "\nPlease enter a proper value.\n" + "=" * 29)
            continue

        # ask to confirm new item or rewrite item information
        while True:
            print("\n"*50)
            print("="*60)
            print("{:<50}{:<1}".format("Item Name", "Item Price"))
            print("{:<50}{:<1}".format(item_name, "RM" + str(item_price)))
            print("=" * 60)
            confirm_or_redo = input("\n\nDo you confirm this item.\n1.Confirm\n2.Redo\nEnter insturction:")
            if confirm_or_redo == "1":
                break
            elif confirm_or_redo == "2":
                break
            else:
                display_message("="*20 + "\nInvalid Instruction.\n" + "="*20)


        if confirm_or_redo == "1":
            print("\n" * 50)
            print("=" * 36 + "\nITEM CONFIRM ADDED TO %s" % category_file[:-3].upper())
            print("=" * 36)
            time.sleep(1)
            print("\n" * 50)

        elif confirm_or_redo == "2":
            display_message("=" * 19 + "\nReenter item info.\n" + "=" * 19)
            continue

        item_code_position = item_codeID(category_file)

        return [item_code_position[0], item_name, str("%.2f" % item_price), item_code_position[1]]


def upload_item(selected_cat):
    """
    Ask admin to enter new item information
    """
    while True:
        # ask user to enter item info
        item_info = input_groceries(selected_cat)
        # grab item list from txt file
        item_list = grab_item_list(selected_cat)
        new_item = item_info[0] + ";" + item_info[1] + ";" + item_info[2] + "\n"
        item_list.insert(item_info[3], new_item)
        # write new item to list
        with open(selected_cat, "w") as upload_grocery:
            for item in item_list:
                upload_grocery.write(item)

        # Ask whether to add more
        while True:
            add_more = input(
                "Do you Want to add more item?\n1.Continue add item\n2.Back to category menu\nEnter instruction:")
            if add_more == "1" or add_more == "2":
                break
            else:
                display_message("=" * 20 + "\nInvalid instruction.\n" + "=" * 20)

        if add_more == "1":
            print("\n" * 50)
            continue
        elif add_more == "2":
            print("\n"*50)
            break


def admin_main_menu():
    while True:
        print(
            "What you want to do.\n1.View Groceries list\n2.Upload Groceries\n3.Modify Groceries "
            "information\n4.Delete Groceries information\n5.search Groceries detail\n6.View customers order\n7.Search "
            "customer order\n8.Logout")
        instruction = input("Please enter instruction number to proceed.\nEnter instructions:")

        if instruction == "1":
            print("\n" * 50)
            view_category_list("View Only")
        elif instruction == "2":
            print("\n" * 50)
            view_category_list("Upload item")
        elif instruction == "3":
            print("\n" * 50)
            view_category_list("Modify item")
        elif instruction == "4":
            print("\n"*50)
            view_category_list("Delete item")
        elif instruction == "5":
            print("\n" * 50)
            search_groceries_detail()
        elif instruction == "6":
            print("\n" * 50)
            view_all_order_history()
        elif instruction == "7":
            print("\n" * 50)
            customer_name = input("Enter customer name to search order:")
            print("\n" * 50)
            view_order_history(customer_name)
        elif instruction == "8":
            display_message("="*11 + "\nLogging out\n" + "="*11)
            break
        else:
            display_message("=" * 52 + "\nYou entered an INVALID instruction, please try again\n" + "=" * 52)


def customer_main_menu(username):
    while True:
        print(
            "What you want to do.\n1.Groceries Menu\n2.View Cart\n3.View Order History\n4.View Personal Infomation\n5.Log Out")
        instruction = input("Please enter instruction number to proceed.\nEnter instructions:")

        if instruction == "1":
            print("\n"*50)
            view_category_list("Place Order")
        elif instruction == "2":
            print("\n" * 50)
            view_cart()
        elif instruction == "3":
            print("\n" * 50)
            view_order_history(username)
        elif instruction == "4":
            print("\n" * 50)
            view_personal_information(username)
        elif instruction == "5":
            display_message("=" * 10 + "\nLoging out\n" + "=" * 10)
            break
        else:
            display_message("=" * 52 + "\nYou entered an INVALID instruction, please try again\n" + "=" * 52)


def user_PInfo(username, password):
    """
    get user information
    Contact Number, address
    """
    while True:
        address = input("Enter your address: ")
        contact_no = input("Enter your contact no: ")
        if ";" in address or ";" in contact_no:
            display_message("="*22 + "\nContain invalid symbol\n" + "="*22)
            continue
        elif "@" in address or "@" in contact_no:
            display_message("=" * 22 + "\nContain invalid symbol\n" + "=" * 22)
            continue

        with open("Accounts.txt", "a") as writeinfo:
            writeinfo.write(username + ";" + str(password) + ";" + address + ";" + contact_no + "\n")
        break


def register():
    while True:
        username = input("Registration Page\n\nEnter your Username: ")
        password = input("Enter your Password: ")
        confirm_password = input("Reenter your Password: ")
        with open("Accounts.txt", "r") as accfile:
            # get existing username
            username_list = []
            for line in accfile:
                userid = line.strip().split(";")
                username_list.append(userid[0])

            # validation check
            if username == "admin":
                display_message("=" * 20 + "\nInvalid username.\n" + "=" * 20)
                continue
            elif len(username) < 1:
                display_message("="*26 + "\nPlease provide a username.\n" + "="*26)
                continue
            elif ";" in username or ";" in password:
                display_message("="*44 + "\nUSERNAME or PASSWORD contain invalid symbol.\n" + "="*44)
                continue
            elif "@" in username or "@" in password:
                display_message("="*44 + "\nUSERNAME or PASSWORD contain invalid symbol.\n" + "="*44)
                continue
            elif confirm_password != password:
                display_message("="*48 + "\nPlease make sure your password match. Try again.\n" + "="*48)
                continue
            elif len(password) < 6:
                display_message("="*44 + "\nPassword must contain at least 6 characters.\n" + "="*44)
                continue
            elif username in username_list:
                display_message("="*14 + "\nUsername exist\n" + "="*14)
                continue
            else:
                # register account
                # get user personal info
                user_PInfo(username, password)
                display_message("=" * 25 + "\nRegistration complete!\nPlease login to proceed.\n" + "=" * 25)
                break


def test_account(username, password):
    # test validation of username and password
    with open("Accounts.txt", "r") as accfile:
        validation = False
        for line in accfile:
            user_acc = line.strip().split(";")
            if username == user_acc[0]:
                if password == user_acc[1]:
                    validation = True
                    break
    if validation:
        return True
    else:
        return False


def login_attempts(log_attemps):
    """
    Allow user to attempt login only 3 times
    """
    if log_attemps < 3:
        print("\n" * 50)
        print("Login Failed. Attempts %d of 3.\nIncorrect username or password. Try again." % log_attemps)
        time.sleep(1)
        print("\n" * 50)
    else:
        print("\n" * 50)
        exit("Attemps 3 of 3.\nYou have used up your login attempts. System shutting down.")


def login():
    """
    User login page
    Admin account is set and cannot be created
    Admin - username: admin password: admin
    """
    log_attempts_count = 0
    while True:
        username = input("Login Page\n\nEnter Username: ")
        password = input("Enter Password: ")
        if not len(username and password) < 1:
            # check if the user is admin
            if username == 'admin' and password == 'admin':
                print("\n" * 50)
                print("=" * 18 + "\nLogin Success!\nWelcome, Admin\n" + "=" * 18 + "\n")
                admin_main_menu()
                break

            test_login = test_account(username, password)
            if test_login:
                print("\n" * 50)
                print("=" * 18 + "\nLogin Success!\nWelcome, " + username + "\n" + "=" * 18 + "\n")
                # Clear previous user cart and write current username to cart
                with open("Cart.txt", "w") as cart:
                    cart.write(username + "\n")
                customer_main_menu(username)
                break
            else:
                # Check login attempts
                log_attempts_count += 1
                login_attempts(log_attempts_count)
        else:
            display_message("=" * 18 + "\nPlease enter data\n" + "=" * 18)



def main_menu():
    print("Welcome to FRESHCO online groceries.")

    while True:
        print("What you want to do.")
        print("1.Login\n2.Register\n3.View Groceries List\n4.Exit")
        instruction = input("Please enter instruction number to proceed.\nEnter instructions:")

        if instruction == "1":
            print("\n" * 50)
            login()
        elif instruction == "2":
            print("\n" * 50)
            register()
        elif instruction == "3":
            print("\n" * 50)
            view_category_list("View Only")
        elif instruction == "4":
            print("\n" * 50)
            print("=" * 30 + "\nThank you for using FRESHCO.\n" + "=" * 30 + "\n\n\n")
            time.sleep(1)
            exit()
        else:
            display_message("=" * 52 + "\nYou entered an INVALID instruction, please try again\n" + "=" * 52)



main_menu()
