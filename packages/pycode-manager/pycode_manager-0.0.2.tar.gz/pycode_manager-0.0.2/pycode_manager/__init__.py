import os

def add():
    if not os.path.exists('./programs'):
        os.makedirs('./programs')
    fn = input('Enter file name: ')
    f =open(f'./programs/{fn}', 'x')
    lines = []
    print('===== Write Code ======')
    while True:
        line = input()
        if line:
            lines.append(line + '\n')
        else:
            break
        code = '\n'.join(lines)
    f.writelines(lines)
    f.close()
    print(f'{fn} is Added !')


def run():
    lst = os.listdir('./programs')
    for i in range(len(lst)):
        print(i+1, '-', lst[i])
    which = int(input("Which code you want to run: "))
    print(f'===== {lst[which-1]} =====')
    exec(open(f'./programs/{lst[which-1]}').read())
    

def show():
    lst = os.listdir('./programs')
    for i in range(len(lst)):
        print(i+1, '-', lst[i])
    which = int(input("Which code you want to see: "))
    print(f'====== {lst[which-1]} =====')
    with open(f'./programs/{lst[which-1]}', 'r') as f:
        print(f.read())

def delete():
    lst = os.listdir('./programs')
    for i in range(len(lst)):
        print(i+1, '-', lst[i])
    which = int(input("Which code you want to delete: "))
    os.remove(f'./programs/{lst[which-1]}')
    print(f'{lst[which-1]} Deleted!')