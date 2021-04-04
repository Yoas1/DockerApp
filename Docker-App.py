import docker
from ast import literal_eval
from sqlite3 import *
from tkinter import *
from tkinter import messagebox

client = docker.from_env()
app = Tk()
app.geometry("1200x400")
app.title("Docker App")
image_text = StringVar("")
name_text = StringVar("")
command_text = StringVar("")
port_text = StringVar("")
tag_text = StringVar("")
login_text = StringVar("")
user_text = StringVar("")
login_user_text = StringVar("")
login_pass_text = StringVar("")
table_start_row = 2


def create_sql_table(table):
    table.execute('''CREATE TABLE IF NOT EXISTS data(
    Container_ID TEXT,
    Image TEXT,
    Name TEXT,
    Status TEXT,
    Ports TEXT,
    Commands TEXT,
    PRIMARY KEY(Container_ID))''')


def update_sql_table(table, values):
    table.executemany("INSERT OR REPLACE INTO data VALUES(?, ?, ?, ?, ?, ?)", values)
    table.commit()


def run():
    try:
        container_table = connect('data.sqlite')
        create_sql_table(container_table)
        if image_text.get() == '':
            image_text.set('Pick image name')
            return None
        else:
            image = image_text.get()
            name = port = command = ''
            if name_text.get() != '':
                name = name_text.get()
            if command_text.get() != '':
                command = command_text.get()
            if port_text.get() != '':
                port = literal_eval('{' + port_text.get() + '}')
            container = client.containers.run(image=image, name=name, command=command, ports=port, detach=True)  # docker run
            container_list = [[container.short_id, "".join(container.image.tags), container.name, container.status,
                               " , ".join([f"{key}:{value}" for key, value in container.ports.items()]),
                               container.logs()]]  # insert data to database
            values = container_list
            update_sql_table(container_table, values)
            container_table.close()
            show_table()
    except docker.errors.APIError:
        messagebox.showerror('Docker Run', f'Name for container in use or Image not exists')
        return None


def show_table():
    container_table = connect('data.sqlite')
    create_sql_table(container_table)
    r_set = container_table.execute('''SELECT * from data LIMIT 0,10''')
    i = 3  # row value inside the loop
    for data in r_set:
        for j in range(len(data)):
            global table_start_row
            e = Entry(app, width=10, fg='blue')
            e.grid(row=i, column=3 + j, sticky=E)
            e.insert(END, data[j])
            table_start_row = i
        i = i + 1


def update_table():
    container_table = connect('data.sqlite')
    create_sql_table(container_table)
    name_list = [name[0] for name in container_table.execute("SELECT Name FROM data")]
    for name in range(len(name_list)):
        container = client.containers.get(name_list[name])
        container_list = [[container.short_id, "".join(container.image.tags), container.name, container.status,
                           " , ".join([f"{key}:{value}" for key, value in container.ports.items()]), container.logs()]]
        values = container_list
        update_sql_table(container_table, values)
    r_set = container_table.execute('''SELECT * from data LIMIT 0,10''')
    i = 3  # row value inside the loop
    for data in r_set:
        for j in range(len(data)):
            e = Entry(app, width=10, fg='blue')
            e.grid(row=i, column=3 + j, sticky=E)
            e.insert(END, data[j])
        i = i + 1
    container_table.close()


def remove():
    try:
        name = name_text.get()
        container_table = connect('data.sqlite')
        container_table.execute("DELETE FROM data WHERE Name = '%s';" % name_text.get())
        container_table.commit()
        container = client.containers.get(name_text.get())
        container.stop()
        container.remove()
        global table_start_row
        i = 3
        for test in range(table_start_row - 2):
            for j in range(6):
                e = Entry(app, text="", width=10, fg='blue')
                e.grid(row=i, column=3 + j, sticky=E)
            i = i + 1
        show_table()
    except docker.errors.NotFound:
        messagebox.showerror('Docker Run', f'No such container: {name} to remove')


def pull():
    try:
        image = image_text.get()
        client.images.pull('%s' % image_text.get())
    except docker.errors.ImageNotFound:
        messagebox.showerror('Docker Run', f'Image: {image} not found!')


def start():
    try:
        name = name_text.get()
        container = client.containers.get(name_text.get())
        container.start()
    except docker.errors.NotFound:
        messagebox.showerror('Docker Run', f'No such container: {name} to start')


def stop():
    try:
        name = name_text.get()
        container = client.containers.get(name_text.get())
        container.stop()
    except docker.errors.NotFound:
        messagebox.showerror('Docker Run', f'No such container: {name} to stop')


def login():
    try:
        name = login_user_text.get()
        log = client.login(username=login_user_text.get(), password=login_pass_text.get())
        status = ''.join(log["Status"])
        messagebox.showerror('Docker Run', f'{name} {status}')
    except KeyError:
        messagebox.showerror('Docker Run', f'Allready login!')
    except docker.errors.APIError:
        messagebox.showerror('Docker Run', f'User Name or Password incorrect')


def push():
    try:
        container = client.containers.get(name_text.get())
        container.start()
        image = container.commit(repository=image_text.get(), tag=tag_text.get())
        print(image.id)
        for line in client.images.push(image_text.get(), tag=tag_text.get(), stream=True, decode=True):
            print(line)
    except docker.errors.NullResource:
        messagebox.showerror('Docker Run', f'Resource ID was not provided')
    except docker.errors.NotFound:
        messagebox.showerror('Docker Run', f'Image to push not found')


# app interface
app.grid_rowconfigure(8, minsize=20)
title_app = Label(app, text="Docker APP", fg='blue', font="calibri 20 bold").grid(row=0, column=0)
image_label = Label(app, text="Image For Container:", fg='black', font="calibri 12 bold").grid(row=3, column=0)
image_entry = Entry(app, textvariable=image_text, fg='red', width=17, borderwidth=4).grid(row=3, column=1)
name_label = Label(app, text="Name For Container:", fg='black', font="calibri 12 bold").grid(row=4, column=0)
name_entry = Entry(app, textvariable=name_text, fg='red', width=17, borderwidth=4).grid(row=4, column=1)
port_label = Label(app, text="Port:", fg='black', font="calibri 12 bold").grid(row=5, column=0)
port_entry = Entry(app, textvariable=port_text, fg='red', width=17, borderwidth=4).grid(row=5, column=1)
command_label = Label(app, text="Command:", fg='black', font="calibri 12 bold").grid(row=6, column=0)
command_entry = Entry(app, textvariable=command_text, fg='red', width=17, borderwidth=4).grid(row=6, column=1)

# push
tag_label = Label(app, text="tag", fg='black', font="calibri 12 bold").grid(row=8, column=2, sticky=W)
tag_entry = Entry(app, textvariable=tag_text, fg='red', width=7, borderwidth=4).grid(row=8, column=2, sticky=E)

# login
login_user_entry = Entry(app, textvariable=login_user_text, fg='red', width=7, borderwidth=4).grid(row=9, column=0, sticky=W)
login_pass_entry = Entry(app, textvariable=login_pass_text, fg='red', width=7, borderwidth=4).grid(row=9, column=0, sticky=E)
user_label = Label(app, text='USER', fg='black', font="calibri 10 bold").grid(row=8, column=0, sticky=W)
pass_label = Label(app, text='PASS', fg='black', font="calibri 10 bold").grid(row=8, column=0, sticky=E)
login_user_label = Label(app, textvariable=user_text, fg='black', font="calibri 12 bold").grid(row=10, column=0)
login_status_label = Label(app, textvariable=login_text, fg='black', font="calibri 12 bold").grid(row=11, column=0)

# Buttons
docker_run_bt = Button(app, text="Docker Run!", command=run, bd=4, bg='green', font="calibri 12 bold").grid(row=1, column=2)
pull_bt = Button(app, text="Pull", command=pull, bd=4).grid(row=3, column=2)
stop_bt = Button(app, text="Stop", command=stop, bd=4).grid(row=4, column=2)
start_bt = Button(app, text="Start", command=start, bd=4).grid(row=5, column=2)
remove_bt = Button(app, text="Remove", command=remove, bd=4).grid(row=6, column=2)
update_tb = Button(app, text="Update list", command=update_table, bd=4).grid(row=0, column=3)
login_bt = Button(app, text="Login", command=login, bd=4).grid(row=9, column=1)
push_bt = Button(app, text="Push", command=push, bd=4).grid(row=9, column=2)


# table labels
table_label = Label(app, text="Containers:", fg='blue', font="calibri 12 bold").grid(row=1, column=3)
id_t = Label(app, text="ID", fg='black', font="calibri 10 bold").grid(row=2, column=3)
image_t = Label(app, text="IMAGE", fg='black', font="calibri 10 bold").grid(row=2, column=4)
name_t = Label(app, text="NAME", fg='black', font="calibri 10 bold").grid(row=2, column=5)
status_t = Label(app, text="STATUS", fg='black', font="calibri 10 bold").grid(row=2, column=6)
port_t = Label(app, text="PORT", fg='black', font="calibri 10 bold").grid(row=2, column=7)
command_t = Label(app, text="COMMAND", fg='black', font="calibri 10 bold").grid(row=2, column=8)



show_table()
app.mainloop()
