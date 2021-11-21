import json
import os
import getpass
import socket

def cls():
    os.system('clear')

def is_str_int(inp: str):
    is_int = True
    numbers = ['1','2','3','4','5','6','7','8','9','0']
    for i in inp:
        if not i in numbers:
            is_int = False
    return is_int

with open('meta.json') as file:
    meta_data = json.load(file)

with open('todo.json') as file:
    app_data = json.load(file)

def view(id: int):
    inmenu = True
    while inmenu:
        cls()
        if app_data[id]['done']: done = 'Is Done'
        else: done = 'Isn\'t Done'
        due_list = []
        for k,v in app_data[id]['due'].items():
            due_list.append(str(v))
        if 'None' in due_list: due_disp = 'N/A'
        else: due_disp = '.'.join(due_list)
        print('Name: {}'.format(app_data[id]['name']))
        print('Description: {}'.format(app_data[id]['desc']))
        print(f'Due: {due_disp}')
        print(done)
        print('M. Mark As Done/Undone')
        print('B. Back')
        inp = input('Select: ').lower()
        if inp == 'b':
            inmenu = False
        elif 'm' == inp:
            mark(id)

def mark(id: int):
    app_data[id]['done'] = not app_data[id]['done']
    with open('todo.json', 'w') as f:
        json.dump(app_data, f, indent=4)

def read():
    if bool(len(app_data)):
        inmenu = True
        maxval = 0
        while inmenu:
            cls()
            for count, i in enumerate(app_data, start=1):
                if i['done']: done = 'Done'
                else: done = 'Not Done'
                due_list = []
                for k,v in i['due'].items():
                    due_list.append(str(v))
                if 'None' in due_list: due_disp = 'N/A'
                else: due_disp = '.'.join(due_list)
                print('{count}. {name} | {due} | {done}'.format(count=count,name=i['name'], done=done, due='Due: '+due_disp))
                maxval = count

            print('B. Back')
            inp = input('Select: ').lower()
            if inp == 'b':
                inmenu = False
            elif inp == '': pass
            elif is_str_int(inp):
                if int(inp) <= maxval and int(inp) > 0:
                    view(int(inp)-1)

def remove():
    if bool(len(app_data)):
        inmenu = True
        maxval = 0
        while inmenu:
            cls()
            for count, i in enumerate(app_data, start=1):
                if i['done']: done = 'Done'
                else: done = 'Not Done'
                due_list = []
                for k,v in i['due'].items():
                    due_list.append(str(v))
                if 'None' in due_list: due_disp = 'N/A'
                else: due_disp = '.'.join(due_list)
                print('{count}. {name} | {due} | {done}'.format(count=count,name=i['name'], done=done, due='Due: '+due_disp))
                maxval = count

            print('B. Back')
            inp = input('Select: ').lower()
            if inp == 'b':
                inmenu = False
            elif inp == '': pass
            elif is_str_int(inp):
                if int(inp) <= maxval and int(inp) > 0:
                    inp = int(inp)-1
                    del app_data[inp]
                    with open('todo.json', 'w') as f:
                        json.dump(app_data, f, indent=4)

def add():
    days_of_month = [31,28,31,30,31,30,31,31,30,31,30,31]
    due = {'day':None, 'month':None, 'year':None}
    cls()
    name = input('Enter Title: ')
    cls()
    desc = input('Enter Description: \n')
    inmenu = True
    while inmenu:
        cls()
        inp = input('1. Enter Due-Date\n2. Don\'t enter Due-Date\nSelect: ').lower()
        if inp == '2':
            inmenu = False
        elif inp == '1':
            ok = True
            cls()
            year = int(input('Due-Year: '))
            leap_year = not bool(year % 4)
            cls()
            month = int(input('Due-Month (as number): '))
            cls()
            day = int(input('Due-Day (day of month): '))
            cls()
            if year < 0:
                ok = False
            elif month < 1 or month > 12:
                ok = False
            elif leap_year and month == 2 and (day > 29 or day < 1):
                ok = False
            elif (not leap_year) and (day > days_of_month[month-1] or day < 1):
                ok = False
            elif (leap_year and month != 2) and (day > days_of_month[month-1] or day < 1):
                ok = False
            if ok:
                inmenu = False
                due = {'day':day, 'month':month, 'year':year}
                
    app_data.append({'name':name, 'desc':desc, 'due':due, 'done':False})
    with open('todo.json', 'w') as f:
        json.dump(app_data, f, indent=4)

def main():
    running = True 
    if os.name == 'nt':
        running = False
        duty = True
        while duty:
            print()
            print('This program is not designed to run on windows!')
            inp = input('Please press enter\n{}>exit'.format(os.getcwd()))
            if inp != '':
                print('Invalid command: exit'+inp)
            else:
                duty = False

    title='##### Welcome to {n} {v} #####'.format(n=meta_data['appName'], v=meta_data['ver'])
    while running:
        cls()
        print(title)
        print('-'*len(title))
        print('R. Read/Mark Task')
        print('C. Create')
        print('D. Delete')
        print('Q. Quit')
        inp = input('Select: ').lower()
        if inp == 'q':
            running = False
            duty = True
            cls()
            while duty:
                print('\nGoodbye!')
                inp = input('Press enter to continue\n{}@{}:{}$ exit'.format(getpass.getuser(), socket.gethostname(),os.getcwd()))
                if inp != '':
                    print('Invalid command: exit'+inp)
                else:
                    duty = False
        elif inp=='r':
            read()
        elif inp=='d':
            remove()
        elif inp=='c':
            add()

if __name__ == '__main__':
    main()
