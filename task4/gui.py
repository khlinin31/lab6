import tkinter as tk
from client import Client


def main(username="Stranger"):
    client = Client()
    receive = client.start()

    window = tk.Tk()
    window.title('CHAT')

    message_form = tk.Frame(master=window)
    scrollbar = tk.Scrollbar(master=message_form)
    messages = tk.Listbox(
        master=message_form,
        yscrollcommand=scrollbar.set
    )
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y, expand=False)
    messages.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    client.messages = messages
    receive.messages = messages

    message_form.grid(row=0, column=0, columnspan=2, sticky="nsew")

    form_entry = tk.Frame(master=window)
    text_input = tk.Entry(master=form_entry)
    text_input.pack(fill=tk.BOTH, expand=True)
    text_input.bind("<Return>", lambda x: client.send(text_input))

    btn_send = tk.Button(
        master=window,
        text='Send',
        command=lambda: client.send(text_input)
    )

    form_entry.grid(row=1, column=0, padx=10, sticky="ew")
    btn_send.grid(row=1, column=1, pady=10, sticky="ew")

    window.rowconfigure(0, minsize=500, weight=1)
    window.rowconfigure(1, minsize=50, weight=0)
    window.columnconfigure(0, minsize=200, weight=1)
    window.columnconfigure(1, minsize=200, weight=0)

    window.protocol('WM_DELETE_WINDOW', lambda: close_application(window, client))

    window.mainloop()


def close_application(root, client):
    client.close()
    root.destroy()


if __name__ == '__main__':
    username = "Biba"
    main(username)
