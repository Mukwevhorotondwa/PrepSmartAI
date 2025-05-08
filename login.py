from db_manager import *
def login():
    username = input("please enter your username")
    password = input("please enter your password")
    check = get_item_from_db(username)
    if check["description"]==password:
        return True
    return False
if __name__ == '__main__':
    login()