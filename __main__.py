from tkinter import *
from tkinter.filedialog import asksaveasfilename, askopenfilename
from multiprocessing import Process, freeze_support
import pyglet as pyg
import sys
import re, sys, io, builtins, webview

def watchVideo(link):
    webview.create_window("YouTube Video Player", link)
    webview.start()

def myApp():
    dark_blue_chars = {'def', 'class', 'lambda', 'True', 'False', 'not', 'and', 'or', 'None', 'nonlocal', 'global'}
    pink_chars = {'yield', 'async', 'import', 'as', 'from', 'if', 'elif', 'else', 'for', 'while', 'with', 'pass', 'break', 'return', 'await', 'except', 'in', 'raise', 'finally', 'try', 'assert', 'del', ''}
    cyan_chars = {'random'}

    writeText = [
        "\n\tHello! Welcome to your workshop. Would\n\tyou like a quick tutorial on how to use\n\tthe 'Python' programming language?",
        "\n\tLet's make a Random Password Generator!\n\tYou can watch the first step by clicking\n\tthe button down below.",
        "\n\tLet's continue.",
        '\n\tNow let`s do it yourself! Create a\n\tfunction that generates a random symbol\n\tout of this string of symbols:\n\t"~!#@$%^&*(_+-)',
        "\n\tHere is the corrected version:",
        "\n\tNow, we can put everything together\n\tand create our final result!",
        "\n\tYou've completed making a Random\n\tPassword Generator using Python!\n\tCongrats! Here are some additional\n\ttasks to go further into the project"
    ]

    # Assets
    pyg.font.add_file('monogram.ttf')

    # Init
    compiler = Tk()
    compiler.title('Python IDE')
    compiler.configure(background='black')

    compiler.state('zoomed')

    menu_bar = Menu(compiler)
    file_path = ''

    current_step = 0

    # Functions
    def on_enter(event):
        event.widget.config(background="#5E81AC", foreground="white")

    def on_leave(event):
        event.widget.config(background="#4C566A", foreground="white")

    def typewriter_effect(text_display, sentence, index=0):
        if index < len(sentence):
            text_display.config(state=NORMAL)
            text_display.insert(END, sentence[index])
            text_display.config(state=DISABLED)
            editor.after(40, typewriter_effect, text_display, sentence, index + 1)
        else:
            editor.after(1500, show_next_button)

    def display_next_sentence(text_display):
        nonlocal current_step
        if current_step < len(writeText):
            text_display.config(state=NORMAL)
            text_display.delete(1.0, END)
            text_display.config(state=DISABLED)

            typewriter_effect(text_display, writeText[current_step], 0)
            nextButton.place(relx=0, rely=1, anchor="sw", x=1000, y=-1000)
            watchButton.place(relx=0, rely=1, anchor="sw", x=1000, y=1000)
            
            current_step += 1

    def show_next_button():
        if current_step < len(writeText):
            nextButton.config(text='NEXT')
            nextButton.place(relx=0, rely=1, anchor="sw", x=10, y=-10)  # Show button again
        if current_step != 0:
            watchButton.place(relx=0, rely=1, anchor="sw", x=200, y=-250)
    
    def startView():
        with open('link.txt', 'r') as file:
            lines = file.readlines()
            
            if current_step <= len(lines):
                content = lines[current_step - 1].strip()
        p = Process(target=watchVideo, args=(content,))
        p.start()
        p.join()

    def set_file_path(path):
        global file_path
        file_path = path

    def run():
        code = editor.get("1.0", END).strip()
        if not code:
            console.insert(END, 'Error: No code to run.\n')
            return
        try:
            old_stdout = sys.stdout
            old_stderr = sys.stderr
            sys.stdout = io.StringIO()
            sys.stderr = io.StringIO()
            
            exec(code, {}, {})
            
            output = sys.stdout.getvalue()
            error = sys.stderr.getvalue()
            
            sys.stdout = old_stdout
            sys.stderr = old_stderr
            
            console.delete("1.0", END)
            if output:
                console.insert(END, output)
            if error:
                console.insert(END, error)
        
        except Exception as e:
            console.delete("1.0", END)
            console.insert(END, f"Error: {str(e)}\n")

    def save_as_file():
        save(asksaveasfilename(filetypes=[('Python Files', '*.py')], defaultextension='.py', initialfile='Python_Project'))

    def save_file():
        if not file_path:
            save_as_file()
        else:
            save(file_path)

    def save(file_path):
        with open(file_path, 'w') as file:
            code = editor.get('1.0', END)
            file.write(code)
            set_file_path(file_path)

    def open_file():
        path = askopenfilename(filetypes=[('Python Files', '*.py')], defaultextension='.py')
        with open(path, 'r') as file:
            new_code = file.read()
            editor.delete('1.0', END)
            editor.insert('1.0', new_code)
            set_file_path(path)
        
        num_lines = int(editor.index("end-1c").split('.')[0])
        for i in range(1,num_lines+1):
            line = f'{i}'+'.0'
            change_color(None, cursor_pos=line)

    def on_key_press(event):
        typed_char = event.char
        cursor_pos = editor.index(INSERT)

        if not typed_char.isalnum():
            if typed_char == '(':
                editor.insert(INSERT, '()')
                cursor_pos = editor.index(INSERT)
                editor.mark_set(INSERT, f"{cursor_pos} - 1c")
                return 'break'
            elif typed_char == '[':
                editor.insert(INSERT, '[]')
                cursor_pos = editor.index(INSERT)
                editor.mark_set(INSERT, f"{cursor_pos} - 1c")
                return 'break'
            elif typed_char == '{':
                editor.insert(INSERT, '{}')
                cursor_pos = editor.index(INSERT)
                editor.mark_set(INSERT, f"{cursor_pos} - 1c")
                return 'break'
            elif typed_char == "'" or typed_char == '"' or typed_char == '`':
                editor.insert(INSERT, f"{typed_char}{typed_char}")
                cursor_pos = editor.index(INSERT)
                editor.mark_set(INSERT, f"{cursor_pos} - 1c")
                return 'break'

    def on_enter_press(event):
        current_line = editor.get("insert linestart", "insert lineend")
        if current_line.strip().endswith(':'):
            indent = "\t"
        else:
            indent = current_line[:len(current_line) - len(current_line.lstrip())]
        editor.insert("insert", f"\n{indent}")
        return "break"

    def change_color(event, cursor_pos=None):
        cursor_position = (cursor_pos if cursor_pos else editor.index(INSERT))
        line, col = map(int, cursor_position.split('.'))
        
        start = f"{line}.0"
        end = f"{line}.end"
        editor.tag_remove("dark_green", start, end)
        editor.tag_remove("green", start, end)
        editor.tag_remove("yellow", start, end)
        editor.tag_remove("gold", start, end)
        editor.tag_remove("dark_blue", start, end)
        editor.tag_remove("pink", start, end)
        editor.tag_remove("orange", start, end)
        editor.tag_remove("light_blue", start, end)
        editor.tag_remove("cyan", start, end)

        line_content = editor.get(start, end)
        # Change Character Color
        for idx, char in enumerate(line_content):
            if char in "()[]{}":
                add_tag_to_character(line,idx,'gold')
            elif char in "0123456789":
                add_tag_to_character(line,idx,'green') 
            elif char in "'`" or char == '"':
                add_tag_to_character(line,idx,'orange')

        # Change Words in String Color
        for match in re.finditer(r'"(.*?)"', line_content):
            add_tag_to_word(line, match, "orange")
        for match in re.finditer(r'`(.*?)`', line_content):
            add_tag_to_word(line, match, "orange")
        for match in re.finditer(r"'(.*?)'", line_content):
            add_tag_to_word(line, match, "orange")
        
        # Change Keyword Color
        for word in pink_chars:
            for match in re.finditer(rf"\b{re.escape(word)}\b", line_content):
                add_tag_to_word(line, match, "pink")
        for word in dark_blue_chars:
            for match in re.finditer(rf"\b{re.escape(word)}\b", line_content):
                add_tag_to_word(line, match, "dark_blue")
        for word in cyan_chars:
            for match in re.finditer(rf"\b{re.escape(word)}\b", line_content):
                add_tag_to_word(line, match, "cyan")

        # Change Comment Color
        for match in re.finditer(r'#.*', line_content):
            add_tag_to_word(line, match, "dark_green")

        # Change Function Color
        for match in re.finditer(r'\b([a-zA-Z_][a-zA-Z0-9_]*)\b', line_content):
            word = match.group(1)
            if hasattr(builtins, word) and callable(getattr(builtins, word)):
                add_tag_to_word(line,match,"yellow")

    def add_tag_to_character(line,idx,tag):
        char_start = f"{line}.{idx}"
        char_end = f"{line}.{idx+1}"
        editor.tag_add(tag, char_start, char_end)

    def add_tag_to_word(line, match, tag):
        start_idx = f"{line}.{match.start()}"
        end_idx = f"{line}.{match.end()}"
        if ("orange" not in editor.tag_names(start_idx) or tag == 'orange') and ("dark_green" not in editor.tag_names(start_idx) or tag == 'dark_green'):
            editor.tag_add(tag, start_idx, end_idx)

    # File Button
    file_button = Menu(menu_bar, tearoff=0)
    file_button.add_command(label='Open', command=open_file)
    file_button.add_command(label='Save', command=save_file)
    file_button.add_command(label='Save As', command=save_as_file)
    file_button.add_command(label='Exit', command=sys.exit)
    menu_bar.add_cascade(label='File', menu=file_button)

    # Run Button
    menu_bar.add_cascade(label='Run', command=run)

    # Compile Menu Bar
    compiler.config(menu=menu_bar)

    # Editor
    editor = Text(height=24, width=100, font=('monogram', 20), fg='#FFFFFF', background='#303030', insertbackground='white', wrap='none', tabs=35)

    editor.tag_configure("gold", foreground='#eccb44')
    editor.tag_configure("orange", foreground='orange')
    editor.tag_configure("dark_blue", foreground='#677fec')
    editor.tag_configure("light_blue", foreground='#8d9dff')
    editor.tag_configure("dark_green", foreground='#007902')
    editor.tag_configure("green", foreground='#a4ffa6')
    editor.tag_configure("pink", foreground='#ec67b2')
    editor.tag_configure("yellow", foreground='yellow')
    editor.tag_configure("cyan", foreground="#21bf98")
    editor.pack(anchor=NW, side=LEFT, padx=1, pady=1)
    editor.bind("<Key>", on_key_press)
    editor.bind("<Return>", on_enter_press)
    editor.bind("<KeyRelease>", change_color)

    # Interactive Section
    interactive = Text(height=24, width=100, font=('monogram', 20), fg='#000000', background='#FFFFFF', state=DISABLED)
    interactive.pack(anchor=NE, padx=1, pady=1)

    # Buttons
    nextButton = Button(interactive, text="START", font=('helvetica', 30, "bold"), borderwidth=0, relief=FLAT, background='#4C566A', foreground='white', command=lambda: display_next_sentence(interactive))
    watchButton = Button(interactive, text="WATCH", font=('helvetica', 30, "bold"), borderwidth=0, relief=FLAT, background='#4C566A', foreground='white', command=startView)

    buttonList = [nextButton, watchButton]
    for button in buttonList:
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)

    nextButton.place(relx=0, rely=1, anchor="sw", x=200, y=-250)

    # Console
    console = Text(height=13, width=153, font=('monogram', 20), fg='#FFFFFF', background='#242424', wrap='none', padx=1, pady=1)
    console.place(x=1, y=510)

    compiler.mainloop()

if __name__ == "__main__":
    freeze_support()
    myApp()

