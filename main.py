import g4f
import customtkinter as ctk
import threading as th

messages = []

temp = None
t10 = (10, 10)
t12 = (12, 0)
ew = "ew"
ctk.set_appearance_mode("dark")
app = ctk.CTk()
app.geometry("560x320")
app.resizable(False, True)
app.grid_columnconfigure(0, weight=3)
app.grid_columnconfigure(1, weight=0)


def change_text(text, is_human):
    if is_human:
        res = "Вы: " + str(text) + "\n"
    else:
        res = "ChatGPT: " + str(text) + "\n"
    textbox.configure(state="normal")
    textbox.insert("end", res)
    textbox.configure(state="disabled", require_redraw=True)


def wait_response():
    global temp
    try:
        response = g4f.ChatCompletion.create(
            model=g4f.models.gpt_4,
            messages=messages,
            provider=g4f.Provider.GeekGpt
        )
    except Exception as e:
        print(e)
        response = "Попробуйте написать снова."
    temp = response
    app.event_generate("<<TaskCompleted>>")


def handle_task(event):
    change_text(temp, False)
    messages.append({"role": "assistant", "content": temp})


def btn_callback():
    change_text(entry.get(), True)
    messages.append({"role": "user", "content": entry.get()})
    entry.delete(0, 'end')
    thread = th.Thread(target=wait_response)
    thread.start()


lbl = ctk.CTkLabel(app, text="Чат с нейросетью", height=30, font=("Helvetica", 24))
lbl.grid(row=0, column=0, columnspan=2, sticky=ew, pady=t10)
textbox = ctk.CTkTextbox(app, state="disabled")
textbox.grid(row=1, column=0, padx=t10, pady=t12, columnspan=2, sticky=ew)
entry = ctk.CTkEntry(app, height=34, placeholder_text="Введи сообщение")
entry.grid(row=2, column=0, pady=t12, padx=t10, sticky=ew)
btn = ctk.CTkButton(app, text="Отправить", height=34, command=btn_callback)
btn.grid(row=2, column=1, pady=t12, padx=t10, sticky=ew)
app.bind("<<TaskCompleted>>", handle_task)
app.mainloop()
