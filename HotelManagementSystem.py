import os
import sys
import mysql.connector
import pickle
rt = []
s_pr = 0
d_pr = 0
q_pr = 0
k_pr = 0
pr = []
mx = []
details = []
feedbacklist = []
rooms = []  # main list
total_rooms = 0
reservation_table = []


def restart():
    global mx
    global rooms
    global details
    global reservation_table
    db = mysql.connector.connect(
        host='localhost', user='root', password='tiger', database='hotel')
    cursor = db.cursor()
    cursor.execute('select * from rooms;')
    roomstable = cursor.fetchall()
    for rn in range(0, len(roomstable)):
        rooms.append({{"Room No.": roomstable[rn][0], "Room Type": roomstable[rn][1], "Price": roomstable[rn][2], "Status": roomstable[rn]
                     [3], "Max Occupants": mx[i-1], "Customer Name": roomstable[rn][4], "No of days": roomstable[rn][5], "No of people": 0}})
    cursor.execute('select * from details;')
    detailstable = cursor.fetchall()
    for rn in range(0, len(detailstable)):
        details.append({'Room No.': detailstable[rn][0], 'Phone': detailstable[rn][1],
                       'E-mail': detailstable[rn][2], 'Address': detailstable[rn][3], 'ID': '00000000000'})
    cursor.execute('select * from reservation;')
    reservations = cursor.fetchall()
    for rn in range(0, len(reservations)):
        reservation_table.append(
            {'Room no.': reservations[rn][0], 'Name': reservations[rn][1]})


def build_table():
    global rooms
    global details
    rooms = []
    details = []
    for i in range(1, total_rooms+1):
        rooms.append({"Room No.": i, "Room Type": rt[i-1], "Price": pr[i-1], "Status": 'Empty',
                     "Max Occupants": mx[i-1], "Customer Name": " - ", "No of days": 0, "No of people": 0})  # added new
    print('Saving in database')
    db = mysql.connector.connect(
        host='localhost', user='root', password='tiger', database='hotel')
    cursor = db.cursor()
    cursor.execute('create table  if not exists rooms(room_no int primary key,room_type varchar(10),price int(10),status varchar(10),customer_name varchar(25),No_of_Days int(10));')
    for k in range(0, total_rooms):  # added new
        roomno = rooms[k]['Room No.']
        roomtype = rooms[k]['Room Type']
        price = rooms[k]['Price']
        status = rooms[k]['Status']
        customername = rooms[k]['Customer Name']
        noofdays = rooms[k]['No of days']
        tup = (roomno, str(roomtype), price, str(
            status), str(customername), noofdays)
        query = 'insert into rooms values'+str(tup)
        cursor.execute(query)
        db.commit()
    for j in range(1, total_rooms+1):
        details.append({'Room No.': j, 'Phone': 00000000000,
                       'E-mail': '  --  ', 'Address': '     ', 'ID': '00000000000'})
    db = mysql.connector.connect(
        host='localhost', user='root', password='tiger', database='hotel')
    cursor = db.cursor()
    cursor.execute(
        'create table  if not exists details(room_no int primary key,phone int(17),Email varchar(20),address varchar(30))')
    for l in range(0, total_rooms):
        roomno = details[l]['Room No.']
        phoneno = details[l]['Phone']
        email = details[l]['E-mail']
        address = details[l]['Address']
        tup = (roomno, str(phoneno), str(email), str(address))
        query = 'insert into details values'+str(tup)
        cursor.execute(query)
        db.commit()


# build_table()


def main_table():
    print('\n***********MAIN TABLE********************')
    print('''
__________________________________________________________
13ROOM NO   |ROOM TYPE | PRICE    | STATUS   |CUSTOMER NAME|
----------------------------------------------------------''')
    for i in rooms:
        for j in ['Room No.', 'Room Type', 'Price', 'Status', 'Customer Name',]:
            length = (10-len(str(i[j])))
            print(' ', i[j], end='')
            print(' '*length, end='')
        print()


def guest_details():
    global details
    print('\n*************GUEST DETAILS TABLE***************************** ')
    print('''
____________________________________________________________________________________
Room no.            |Phone no.           |Email               |Address             |
------------------------------------------------------------------------------------''')
    for i in details:
        for j in ['Room No.', 'Phone', 'E-mail', 'Address']:
            length = (20-len(str(i[j])))
            print(i[j], end='')
            print(length*' ', end=' ')
        print()


def reserve_table():
    print('\n ***************** RESERVATION TABLE************* ')
    print('_______________________')
    print('ROOM NO | NAME        |')
    for i in reservation_table:
        for j in ['Room no.', 'Name']:
            print('   ', i[j], end='  ')


def change_total_rooms():
    global total_rooms
    global rt
    global pr
    global mx
    global s_pr
    global d_pr
    global q_pr
    global k_pr
    global s_r
    global d_r
    global q_r
    global k_r
    global initialisation_status
    try:
        if total_rooms > 0:
            for r in range(0, total_rooms):
                if rooms[r]['Status'] == 'Full' or rooms[r]['Status'] == 'Reserved':
                    print(
                        'All rooms should be empty before changing the total number of rooms')
                    admin()
        total_rooms = int(input('>>Enter no of rooms='))
        check = 0
        rt = []
        pr = []
        mx = []
        s_r = int(input('\t>Enter no of single rooms: '))
        check += s_r
        s_pr = int(input('\t\t-Enter cost: '))
        d_r = int(input('\t>Enter no of double rooms '))
        check += d_r
        d_pr = int(input('\t\t-Enter cost: '))
        q_r = int(input('\t>Enter no of quad rooms: '))
        check += q_r
        q_pr = int(input('\t\t-Enter cost: '))
        k_r = int(input('\t>Enter no of king sized rooms: '))
        check += k_r
        k_pr = int(input('\t\t-Enter cost: '))
        if check != total_rooms:
            print(
                ' warning!total sum of the type of rooms dont match. Re-enter the no of type of rooms ')
            total_rooms = 0
            change_total_rooms()
    except:
        print('ERROR........ \n Invalid input,enter only integers in required places\n')
        change_total_rooms()

    for i in range(0, s_r):
        rt.append(1)
        pr.append(s_pr)
        mx.append(1)

    for i in range(0, d_r):
        rt.append(2)
        pr.append(d_pr)
        mx.append(2)

    for i in range(0, q_r):
        rt.append(3)
        pr.append(q_pr)
        mx.append(4)

    for i in range(0, k_r):
        rt.append(4)
        pr.append(k_pr)
        mx.append(2)

    initialisation_status = 1
    build_table()
    main_table()
    admin()


def change_cost():
    global s_pr
    global d_pr
    global q_pr
    global k_pr
    global pr
    try:
        t = int(input('''>Enter the room type of the room\'s cost to be changed
        1-single
        2-double
        3-quad
        4-king
        >> '''))
        if t == 1:
            s_pr = int(input('--Enter new cost for single room- '))
        elif t == 2:
            d_pr = int(input('--Enter new cost for duble room- '))
        elif t == 3:
            q_pr = int(input('--Enter new cost of quad room- '))
        elif t == 4:
            k_pr = int(input('--Enter new cost of king room- '))
        else:
            print('Invalid option')
            change_cost()
        pr = []
        for i in range(0, s_r):
            pr.append(s_pr)
        for i in range(0, d_r):
            pr.append(d_pr)
        for i in range(0, q_r):
            pr.append(q_pr)
        for i in range(0, k_r):
            pr.append(k_pr)
        for i in range(1, total_rooms+1):
            rooms[i-1]['Price'] = pr[i-1]
        print('****************************************************************')
        admin()
    except:
        print('ERROR............\n Wrong input.')
        change_cost()


def change_username():
    global username
    ch = int(input('''1-Add username
2-remove username
\t\t>'''))
    if ch == 1:
        u = input('\t>Enter username to be added- ')
        username.append(u)
        admin()
    elif ch == 2:
        ru = input('\t>Enter username to be removed: ')
        username.remove(ru)
        print('Removed', ru)
    else:
        ('Invalid choice')
        change_username()
        print('****************************************************************')
    admin()


def change_password():
    global pw
    global adminpass
    pc = int(input("""Enter the password to be changed
    1-Staff
    2-Admin
    -- """))
    if pc == 1:
        pw = input('Enter new staff password: ')
    elif pc == 2:
        adminpass = input('Enter new admin password: ')
    else:
        print('Invalid option')
        change_password()
    print('****************************************************************')
    admin()


def admin():

    global total_room
    print('''
----------------------------------------------------
----------------ADMIN MENU--------------------------
Enter your action:
  1-Change number of rooms
  2-Change the cost of  one room
  3-Modify username list 
  4-Change password
  5-view tables
  6-login as staff
  7-logout
  8-Developer Mode
---------------------------------------------------''')
    try:
        choice = int(input('\t>Enter choice: '))
    except:
        print('ERROR................ \n Invalid input\n Returning to Admin menu')
        admin()
    if choice == 1:
        change_total_rooms()
    elif choice == 2:
        change_cost()
    elif choice == 3:
        change_username()
    elif choice == 4:
        change_password()
    elif choice == 5:
        main_table()
        guest_details()
        reserve_table()
        admin()
    elif choice == 6:
        staff()
    elif choice == 7:
        signin()
    elif choice == 8:
        print('''you can now call any function in the program
        Type - "admin()" to return ''')
    else:
        print('Invalid choice')
        admin()


def display_guest_menu():
    os.system('cls')
    print('''
---------------------------------------------
-------------GUEST MENU----------------------\n''')
    print("1. RESERVATION")
    print("2. CHECK IN: ")
    print("3. CHECK OUT: ")
    print("4. LOGOUT ")
    print('''
----------------------------------------------\n''')
    try:
        menu_no = int(input("\t>Enter menu no: "))
        return menu_no
    except:
        print('ERROR.............. \n Invalid input returning to guest menu\n\n')
        display_guest_menu()


def display_staff_menu():
    print('\n--------------------------------------------------------')
    print('---------------STAFF MENU---------------------------------\n')
    print("1. CHECK IN: ")
    print("2. CHECK OUT: ")
    print("3.SHOW CONTACT AND IDENTITY DETAILS")
    print("4.DISPLAY FEEDBACK LIST")
    print("5.LOGOUT")
    print('\n---------------------------------------------------------\n')
    try:
        menu_no = int(input("\t>Enter menu no: "))
        return menu_no
    except:
        print('ERROR..............\n Invalid input returning to staff menu\n')


def check_in():
    global rooms
    global details
    global reservation_table
    name = input("\n\t\tEnter customer name: ")
    # try:
    for i in range(0, (total_rooms)):
        if rooms[i]['Status'] == 'Reserved' and rooms[i]['Name'] == name:
            for t in range(0, len(reservation_table)+1):
                if reservation_table[t] == {'Room no.': rooms[i]['Room No.'], 'Name': rooms[i]['Name']}:
                    temp = t
                    break
            print('You have a reserved room')
            print('room', rooms[i]['Room No.'],
                  'is reserved in the name ', rooms[i]['Name'])
            roomnumber = i+1
            X = input('press enter to continue')
            # enter=input('Enter 1-to continue to check into reserved room \n     2- To check into another room ')
            rooms[roomnumber-1]["Customer Name"] = name
            quantitypeople = input("Enter number of people: ")
            rooms[roomnumber-1]["No of people"] = quantitypeople
            noofdays = int(input("No of days: "))
            rooms[roomnumber-1]["No of days"] = noofdays
            phone_no = int(input("Enter your phone number:"))
            details[roomnumber-1]['Phone'] = phone_no
            email = input("enter your email address:")
            details[roomnumber-1]['E-mail'] = email
            residn_addrs = input("Enter your residental address:")
            # IDproof=eval(input("enter your passport number"))
            details[roomnumber-1]['Address'] = residn_addrs
            # details[roomnumber-1]['ID']=IDproof
            reservation_table.pop(temp)
            rooms[roomnumber-1]["Status"] = 'Full'
            # added
            db = mysql.connector.connect(
                host='localhost', user='root', password='tiger', database='hotel')
            cursor = db.cursor()
            db = mysql.connector.connect(
                host='localhost', user='root', password='tiger', database='hotel')
            cursor = db.cursor()
            query = "update rooms set status='Full',customer_name='"+name + \
                "',no_of_days="+str(noofdays)+" where room_no="+str(roomnumber)
            cursor.execute(query)
            query = "update details set phone="+str(phone_no)+",Email='"+str(
                email)+"',address='"+str(residn_addrs)+"' where room_no= "+str(roomnumber)
            cursor.execute(query)
            query = "delete from reservation where room_no="+str(roomnumber)
            cursor.execute(query)
            db.commit()
            print('you have check into room no.',
                  roomnumber, '.Enjoy your stay.')
            return
    print('\n\n---------------------------------------------------------')
    print("These are the following room types:")
    print(" 1. Single: A room assigned to one person. Price:", s_pr)
    print(" 2. Double: A room assigned to two people. Price:", d_pr)
    print(" 3. Quad: A room assigned to four people. Price:", q_pr)
    print(" 4. King: A room with a king-sized bed. Price:", k_pr)
    roomtype = int(input("Enter room type number: "))
    print("\nThese are the available room numbers: ")
    count = 0
    for room in rooms:
        if room["Room Type"] == roomtype and room["Status"] == 'Empty':
            print(room["Room No."])
            count += 1
    if count > 0:
        roomnumber = int(input("Enter chosen room number: "))
        rooms[roomnumber-1]["Customer Name"] = name
        quantitypeople = input("Enter number of people: ")
        rooms[roomnumber-1]["No of people"] = quantitypeople
        noofdays = int(input("No of days: "))
        rooms[roomnumber-1]["No of days"] = noofdays
        phone_no = int(input("Enter your phone number:"))
        details[roomnumber-1]['Phone'] = phone_no
        email = input("enter your email address:")
        details[roomnumber-1]['E-mail'] = email
        residn_addrs = input("Enter your residental address:")
        # IDproof=eval(input("enter your passport number"))
        details[roomnumber-1]['Address'] = residn_addrs
        # details[roomnumber-1]['ID']=IDproof
        rooms[roomnumber-1]["Status"] = 'Full'
        print('you have check into room no.', roomnumber, '.Enjoy your stay.')
        # print(rooms[roomnumber])
        db = mysql.connector.connect(
            host='localhost', user='root', password='tiger', database='hotel')
        cursor = db.cursor()
        query = "update rooms set status='Full',customer_name='"+name + \
            "',no_of_days="+str(noofdays)+" where room_no="+str(roomnumber)
        cursor.execute(query)
        query = "update details set phone="+str(phone_no)+",Email='"+str(
            email)+"',address='"+str(residn_addrs)+"' where room_no= "+str(roomnumber)
        cursor.execute(query)
        db.commit()
    else:
        print("No rooms avaliable")
    # print(rooms[roomnumber])
    x = input("Enter x to go back to menu")
    if x == "x":
        return
    '''except:
        print('ERROR.............\n Invalid input, enter valid information in required field')
        check_in()'''


def feedback():
    global feedbacklist
    print("We would love to hear your feedback on your stay with us")
    feedback = input("")
    feedbacklist.append(feedback)
    print("Thank you for your feedback")
    # print(feedbacklist)
    return


def check_out():

    global rooms
    global details
    count = 0
    for room in rooms:
        if room["Status"] == 'Full':
            # print(room["Room No."])
            count += 1
    if count > 0:
        try:
            roomnumber = int(input("Enter chosen room number: "))
        except:
            print('ERROR................\n\nInvalid entry')
            check_out()
        cost = (rooms[roomnumber-1]["Price"]) * \
            (rooms[roomnumber-1]["No of days"])
        print("Thank you", rooms[roomnumber-1]
              ["Customer Name"], "for staying with us.")
        print("You have stayed for ", rooms[roomnumber-1]["No of days"])
        print("The total cost is", cost)
        rooms[roomnumber-1]["Customer Name"] = " - "
        rooms[roomnumber-1]["No of days"] = 0
        rooms[roomnumber-1]["No of people"] = 0
        rooms[roomnumber-1]["Status"] = 'Empty'
        details[roomnumber-1]['Phone'] = 000000000000
        details[roomnumber-1]["E-mail"] = '-----'
        details[roomnumber-1]['Address'] = '          '
        # details[roomnumber-1]['ID']=000000000000
    # print(rooms[roomnumber])
        print('updating in database')
        db = mysql.connector.connect(
            host='localhost', user='root', password='tiger', database='hotel')
        cursor = db.cursor()
        query = "update rooms set status='Empty',customer_name='- ',no_of_days=0 where room_no=" + \
            str(roomnumber)
        cursor.execute(query)
        query = "update details set phone='000000',Email='-----',adress='    ' where room_no=" + \
            str(roomnumber)
        cursor.execute(query)
        db.commit()
    feedback()
    x = input("Enter x to go back to menu")
    if x == "x":
        return


def display_feedback():
    global feedbacklist
    print('')
    print('_____________________________________________________________________________')
    print('|FEEDBACK                                                                    |')
    print('|-----------------------------------------------------------------------------')
    for i in feedbacklist:
        print('|>', i)
        print('|--------------------------------------------------------------------------')
    print('_____________________________________________________________________________')
    n = input('Press enter')


def reservation():
    global rooms
    global reservation_table
    db = mysql.connector.connect(
        host='localhost', user='root', password='tiger', database='hotel')
    cursor = db.cursor()
    cursor.execute(
        'create table if not exists reservation(room_no int(11),name varchar(25))')
    db.commit()
    try:
        print('\n\n---------------------------------------------------------')
        print("These are the following room types:")
        print(" 1. Single: A room assigned to one person. Price:", s_pr)
        print(" 2. Double: A room assigned to two people. Price:", d_pr)
        print(" 3. Quad: A room assigned to four people. Price:", q_pr)
        print(" 4. King: A room with a king-sized bed. Price:", k_pr)
        roomtype = int(input("Enter room type number: "))
        print("\nThese are the available room numbers: ")
        count = 0
        temproom = []
        for room in rooms:
            if room["Room Type"] == roomtype and room["Status"] == 'Empty':
                print(room["Room No."])
                count += 1
                temproom.append(room['Room No.'])
        if count > 0:
            roomnumber = int(input("Enter chosen room number: "))
            if roomnumber in temproom:
                name = input("Enter customer name: ")
                rooms[roomnumber-1]['Status'] = 'Reserved'
                rooms[roomnumber-1]['Name'] = name
                reservation_table.append(
                    {'Room no.': roomnumber, 'Name': name})
                db = mysql.connector.connect(
                    host='localhost', user='root', password='tiger', database='hotel')
                cursor = db.cursor()
                tup = (roomnumber, str(name))
                query = "insert into reservation values"+str(tup)
                cursor.execute(query)
                db.commit()
            else:
                print('\n Please select from the displayed roomnumbers only.')
                reservation()
    except:
        print('ERROR............... \n Enter valid information if required fields.')


def staff():
    global rooms
    c = 1
    try:
        while c != 0:
            main_table()
            c = display_staff_menu()
            if c == 1:
                check_in()
            elif c == 2:
                check_out()
            elif c == 3:
                guest_details()
                enter = input('Press enter to continue')
            elif c == 4:
                display_feedback()
            elif c == 5:
                signin()
            else:
                print('Invalid choice')
                staff()
    except:
        print('ERROR................ \n Enter a valid choice ')
        staff()


def guest():
    global rooms
    c = 1
    # try:
    while c != 0:
        c = display_guest_menu()
        if c == 2:
            check_in()
        elif c == 3:
            check_out()
        elif c == 1:
            reservation()
        elif c == 4:
            signin()
        else:
            print('Invalid choice')
            guest()
    '''except:
        print('Error........... \n Enter a valid choice')
        guest()'''


username = []
pw = ''
admins = []
adminpass = ''
x = 1
initialisation_status = 0


def signin():
    global x
    global initialisation_status
    try:
        b = open('saves.dat', 'rb+')
        vardict = pickle.load(b)
        initialisation_status = vardict['initialisationstatus']
        b.close()
    except:
        initialisation_status = 0
    while x == 1:
        # try:
        print('***************************************************')
        print('**********************WELCOME**********************\n\n')
        if initialisation_status == 0:
            print('>>Please enter as ADMIN for setup.')
        sign_in = int(input('''Do you want to continue as guest / staff /admin:
        1-Guest
        2-Staff
        3-Admin
        4-Exit
        >'''))
        if sign_in == 1:
            if initialisation_status == 0:
                print(
                    'The setup has not been completed.Please login as admin finish setup.')
                signin()
            os.system('cls')
            print('\n\nYou are logged in as a guest\n\n')
            guest()
        elif sign_in == 2:
            if initialisation_status == 0:
                print(
                    'The setup has not been completed.Please login as admin finish setup.')
                signin()
            user = input('\t\tEnter Username: ')
            password = input('\t\tEnter password: ')
            if user in username and password == pw:
                os.system('cls')
                print('You are logged in as: ', user)
                staff()
            else:
                print('Invalid credentials\n\n\n')
                signin()
        elif sign_in == 3:
            if initialisation_status == 0:
                setup()
            if initialisation_status == 1:
                use = input('\t\tEnter username: ')
                pas = input('\t\tEnter password: ')
                if use in admins and pas == adminpass:

                    print(
                        '********************************************************************')
                    print('You are logged in as ', use)
                    admin()
                else:
                    print('Invalid credentials\n\n\n')
                    signin()
        elif sign_in == 4:
            # backup
            b = open('saves.dat', 'wb+')
            vardict = {'initialisationstatus': initialisation_status, 'username': username, 'admins': admins, 'pw': pw, 'adminpass': adminspass,
                       'total_rooms': total_rooms, 'rt': rt, 's_pr': s_pr, 'd_pr': d_pr, 'q_pr': q_pr, 'k_pr': k_pr, 'pr': pr, 'mx': mx, 'feedbacklist': feedbacklist}
            pickle.dump(vardict, b)
            b.close()
            print('bye ')
            sys.exit()
        else:
            print('Please choose from the above options only')
            signin()
        '''except:
            print('ERROR.............. \nInvalid input returning to Login Page\n\n\n')
            signin()'''


def setup():
    global username
    global admins
    global pw
    global adminpass
    global rt
    global s_pr
    global d_pr
    global q_pr
    global k_pr
    global pr
    global mx
    global details
    global feedbacklist
    global rooms
    global total_rooms
    global reservation_table
    global initialisation_status
    print('-----------------------------------------------')
    print('---------------SET UP--------------------------')
    print('\n\n')
    print('Welcome to the setup:-')
    username = []
    admins = []
    pw = ''
    adminpass = ''
    add_admin = input('>Enter administrator username: ')
    admins.append(add_admin)
    adminpass = input('\t>Enter admin password: ')
    while True:
        try:
            staff_no = int(input('\n--Enter no of staff members: '))
            break
        except:
            print('No of staff members has to be a number')
    for i in range(staff_no):
        staff_user = input('>Enter username: ')
        print('\tStaff member', staff_user, 'has been added\n')
        username.append(staff_user)
    pw = input('\t>Enter Staff password: ')
    x = input('\nPress Enter to continue to Rooms Setup....\n')
    change_total_rooms()


'''if initialisation_status !=1:
setup()
exit()'''

signin()
