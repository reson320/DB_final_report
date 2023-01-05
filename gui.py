from operator import pos
import tkinter as tk
import subdir.app_func as app
import tabulate

win = tk.Tk() # create main window
# title
win.title("Champion Recommendation")

# window size
wd=700
ht=450
posX=500
posY=200
win.geometry(str(wd)+"x"+str(ht)+"+"+str(posX)+"+"+str(posY)) # width * height
win.minsize(width=wd, height=ht)

# window color
bgc="#D2E9FF"
win.config(bg=bgc) #background

# window 置頂 (if True)
win.attributes("-topmost", False)

# Functions
def main():
    txt.pack_forget()
    txt.delete("1.0", "end")
    btn_again.pack_forget()
    st.pack()
    btn_y.pack()
    btn_n.pack()
def record_pos(p):
    global ps
    ps=p
    choose_output()

def choose_pos():
    st.pack_forget()
    btn_y.pack_forget()
    btn_n.pack_forget()
    # labels
    lb.pack()
    # buttons
    btn_top.pack()
    btn_jg.pack()
    btn_mid.pack()
    btn_adc.pack()
    btn_sup.pack()

def choose_output():
    lb.pack_forget()
    btn_top.pack_forget()
    btn_jg.pack_forget()
    btn_mid.pack_forget()
    btn_adc.pack_forget()
    btn_sup.pack_forget()

    sl.pack()
    btn_fr.pack()
    btn_sec.pack()

def after_cho():
    sl.pack_forget()
    btn_fr.pack_forget()
    btn_sec.pack_forget()
    btn_again.pack()

ps=""

# labels definition
st = tk.Label(text="Do you want to update data to database?\nIt may take few minutes to finish")
st.config(bg=bgc, font=('Times', 20))
lb = tk.Label(text="Which positions you want?")
lb.config(bg=bgc, font=('Times', 20))
sl = tk.Label(text="Choose \"1\" for our first 5 champions\nChoose \"2\" for the whole table")
sl.config(bg=bgc, font=('Times', 20))

txt = tk.Text(win)

# buttons definition
btn_y = tk.Button(text="Yes", font=('Times', 20))
btn_y.config(command=app.update_DB)
btn_n = tk.Button(text="No", font=('Times', 20))
btn_n.config(command=choose_pos)

btn_top = tk.Button(text="top", font=('Times', 20))
#btn.config(fg="white", bg="black")
btn_top.config(command=lambda: record_pos("top"))
btn_jg = tk.Button(text="jungle", font=('Times', 20))
#btn.config(fg="white", bg="black")
btn_jg.config(command=lambda: record_pos("jungle"))
btn_mid = tk.Button(text="mid", font=('Times', 20))
#btn.config(fg="white", bg="black")
btn_mid.config(command=lambda: record_pos("mid"))
btn_adc = tk.Button(text="adc", font=('Times', 20))
#btn.config(fg="white", bg="black")
btn_adc.config(command=lambda: record_pos("adc"))
btn_sup = tk.Button(text="support", font=('Times', 20))
#btn.config(fg="white", bg="black")
btn_sup.config(command=lambda: record_pos("support"))

btn_fr = tk.Button(text="1", font=('Times', 20))
btn_fr.config(command=lambda: [after_cho(), app.recm(str(ps), "1", txt)])
btn_sec = tk.Button(text="2", font=('Times', 20))
btn_sec.config(command=lambda: [after_cho(), app.recm(str(ps), "2", txt)])

btn_again = tk.Button(text="Restart", font=('Times', 16))
btn_again.config(command=main)


main()
win.mainloop() #常駐win