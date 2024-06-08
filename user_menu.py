from models import User


if __name__ == '__main__':
    menu = """
1 - Create a new user
2 - List of users
3 - Log in
4 - Change username
5 - Change password
6 - Delete user
7 - Load your messages
8 - Send message
9 - Log out
10 - Exit
"""

    logged_user = None

    print("Type a number to pick the following order:")
    while True:
        opcja = input(menu)
        if opcja == "1":
            username = input("Username: ")
            password = input("Password: ")
            while len(password) < 8:
                if len(password) >= 8:
                    continue
                else:
                    print("Password must be at least 8 characters")
                    password = input("Password: ")
            if User.load_user_by_username(username) is None:
                user = User(username, password)
                user.save()
                print("User created successfully")
            else:
                print("User already exists")

        elif opcja == "2":
            users_list = User.load_all_users()
            for user in users_list:
                print(user[1])

        elif opcja == "3":
            if logged_user is None:
                username = input("Username: ")
                password = input("Password: ")
                if User.load_user_by_username(username) is None:
                    print("That username does not exist")
                else:
                    if User.login_validate(username, password) is True:
                        print("Login successful")
                        user_id = User.load_user_id_by_username(username)
                        logged_user = User(username, password, user_id)
                    else:
                        print("Invalid password")
            else:
                print("You're alredy logged in")

        elif opcja == "4":
            if logged_user is not None:
                new_username = input("New Username: ")
                logged_user.change_username(new_username)
                logged_user.save()
                print("Username updated successfully")
            else:
                print("You have to login before you change your username")

        elif opcja == "5":
            if logged_user is not None:
                new_password = input("New Password: ")
                logged_user.change_password(new_password)
                logged_user.save()
                print("Password updated successfully")
            else:
                print("You have to login before you change your password")

        elif opcja == "6":
            if logged_user is not None:
                print("Are you sure you want to delete your account?")
                answer = input("y/n\n").lower()
                if answer == "y":
                    logged_user.delete()
                    print("User successfully deleted")
                else:
                    print("You didn't delete your account")
            else:
                print("You have to login before you delete your account")

        elif opcja == "7":
            if logged_user is not None:
                messages = logged_user.list_messages()
                for message in messages:
                    print(message)
            else:
                print("You have to login before you load your messages")

        elif opcja == "8":
            if logged_user is not None:
                receiver = input("Receiver: ")
                if User.load_user_by_username(receiver) is not None:
                    receiver_id = User.load_user_id_by_username(receiver)
                    message = input("Message: ")
                    if len(message) < 255:
                        logged_user.send_message(receiver_id, message)
                        print("Message sent successfully")
                    else:
                        print("Message too long")
                else:
                    print("Invalid receiver name")
            else:
                print("You have to login to be able to send messages")

        elif opcja == "9":
            if logged_user is not None:
                logged_user = None
                print("Logged out successfully")
            else:
                print("You are not logged in")

        elif opcja == "10":
            break

        else:
            print("Invalid choice")
