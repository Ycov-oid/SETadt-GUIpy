import tkinter as tk
import tkinter.font as tkfont
from tkinter import ttk

SIZE = 10  

#UI section 

#surfaces
BG = "#000810"          #main background
CARD = "#324659"        #input-output surface
STRIPE = "#2f4254"      #scrollbar trough
TABLE_BG = "#344a5f"    #used for whole table + status box
BORDER = "#4a6379"      #control outlines
BORDER_STRONG = "#8aa0b5"

# text
TEXT = "#eef3f8"        #body text
HEADING = "#c9d4df"     #title & section headings 
NOTE = "#f0a830"        #notes 
DATA = "#8da0b3"        #TEXT TABLE

# buttons
BTN = "#4a9be8"         #buttons
BTN_TEXT = "#ffffff"
DANGER_BG = "#d9534f"   #Exit button

# brand & status
ACCENT = "#4a9be8"      #utline, radio dot, accent button
SELECT = "#2f6fb0"      #text selection in the entry / output box
GREEN = "#5fd38d"
RED = "#ff7b72"

# spacing 
S1, S2, S3, S4, S5 = 4, 8, 12, 16, 24

TABLE_ROW_H = 28            
TABLE_HEAD_PAD = (S3, S2)   
TABLE_CARD_PAD = (S5, S2)   
BOX_PAD_X = S4              
STATUS_PAD = (S5, S1)       # status box
BTN_PAD = (20, 5)           # button label padding
BTN_GAP = S1                
RADIO_SIZE = 20             # diameter of the Set A / Set B circles 
RADIO_FONT_SIZE = 12        # label size for the Set A / Set B radio buttons

hint_msg = "Enter element here and click [add] button"


class HashTable:
    def __init__(self, size=SIZE):
        self.size = size
        self.slots = [None] * size
        self.used = 0

    def hashIt(self, value):
        return value % self.size

    def find(self, value):
        i = self.hashIt(value)
        tries = 0
        while tries < self.size:
            if self.slots[i] is None:
                return -1
            if self.slots[i] == value:
                return i
            i = (i + 1) % self.size
            tries += 1
        return -1

    def insert(self, value):
        if self.find(value) != -1:
            return "duplicate"
        if self.used == self.size:
            return "full"
        i = self.hashIt(value)
        while self.slots[i] != None:
            i = (i + 1) % self.size
        self.slots[i] = value
        self.used += 1
        return "ok"

    def delete_value(self, value):
        i = self.find(value)
        if i == -1:
            return False
        self.slots[i] = None
        self.used -= 1
        j = (i + 1) % self.size
        while self.slots[j] is not None:
            v = self.slots[j]
            self.slots[j] = None
            self.used -= 1
            self.insert(v)
            j = (j + 1) % self.size
        return True

    def getAll(self):
        out = []
        for v in self.slots:
            if v is not None:
                out.append(v)
        return out


class MySet:
    def __init__(self, name):
        self.name = name
        self.table = HashTable()

    def add(self, x):
        return self.table.insert(x)

    def delete(self, x):
        return self.table.delete_value(x)

    def contains(self, x):
        return self.table.find(x) != -1

    def members(self):
        return self.table.getAll()

    def size(self):
        return self.table.used

    def union(self, other):
        c = MySet("C")
        for x in self.members() + other.members():
            if c.add(x) == "full":
                raise OverflowError("too many elements")
        return c

    def intersection(self, other):
        c = MySet("C")
        for x in self.members():
            if other.contains(x):
                c.add(x)
        return c

    def difference(self, other):
        c = MySet("C")
        for x in self.members():
            if not other.contains(x):
                c.add(x)
        return c


class SetApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Set ADT")
        self.root.resizable(False, False)
        root.geometry("1280x820")
        

        self.setA = MySet("A")
        self.setB = MySet("B")
        self.set_c = MySet("C")

        self.which = tk.StringVar(value="A")
        self.entryVar = tk.StringVar()
        self.noteVar = tk.StringVar(value=hint_msg)
        self.status_var = tk.StringVar()

        self.setup_theme()
        self.build()
        self.redraw_table()
        self.update_status()
        self.which.trace_add("write", lambda *args: self.update_status())
        self.entry.focus_set()

    # THEME
    def setup_theme(self):
        self.root.configure(bg=BG)

        base = tkfont.nametofont("TkDefaultFont")
        base.configure(size=10)
        tkfont.nametofont("TkFixedFont").configure(size=10)
        fam = base.actual("family")
        self.titleFont = tkfont.Font(family=fam, size=16, weight="bold")
        self.section_font = tkfont.Font(family=fam, size=10, weight="bold")
        self.small_font = tkfont.Font(family=fam, size=9)
        self.radio_font = tkfont.Font(family=fam, size=RADIO_FONT_SIZE)

        st = ttk.Style(self.root)
        st.theme_use("clam")
        st.configure(".", background=BG, foreground=TEXT, bordercolor=BORDER,
                     focuscolor=ACCENT, troughcolor=STRIPE)

        # LABELS
        st.configure("Title.TLabel", font=self.titleFont, foreground=HEADING)
        st.configure("Section.TLabel", font=self.section_font, foreground=HEADING)
        st.configure("Note.TLabel", foreground=NOTE, font=self.small_font)
        st.configure("Err.TLabel", foreground=RED, font=self.small_font)
        st.configure("Status.TLabel", background=TABLE_BG, foreground=HEADING,
                     padding=STATUS_PAD)

        # BUTTONs
 
        st.layout("TButton", [("Button.border", {"sticky": "nswe", "children": [
            ("Button.padding", {"sticky": "nswe", "children": [
                ("Button.label", {"sticky": "nswe"})]})]})])
        st.configure("TButton", background=BTN, foreground=BTN_TEXT, padding=BTN_PAD,
                     relief="flat", width=-1, bordercolor=BTN, lightcolor=BTN,
                     darkcolor=BTN)
        st.map("TButton",
               background=[("pressed", BTN), ("active", BTN)],
               bordercolor=[("pressed", BTN), ("active", BTN)],
               lightcolor=[("pressed", BTN), ("active", BTN)],
               darkcolor=[("pressed", BTN), ("active", BTN)],
               relief=[("pressed", "flat"), ("active", "flat")])
        st.configure("Accent.TButton", background=ACCENT, foreground=BTN_TEXT,
                     bordercolor=ACCENT, lightcolor=ACCENT, darkcolor=ACCENT)
        st.map("Accent.TButton",
               background=[("pressed", ACCENT), ("active", ACCENT)],
               bordercolor=[("pressed", ACCENT), ("active", ACCENT)],
               lightcolor=[("pressed", ACCENT), ("active", ACCENT)],
               darkcolor=[("pressed", ACCENT), ("active", ACCENT)],
               relief=[("pressed", "flat"), ("active", "flat")])
        # Exit: red button so it reads as the "leave" action
        st.configure("Danger.TButton", background=DANGER_BG, foreground=BTN_TEXT,
                     padding=BTN_PAD, relief="flat", width=-1, bordercolor=DANGER_BG,
                     lightcolor=DANGER_BG, darkcolor=DANGER_BG)
        st.map("Danger.TButton",
               background=[("pressed", DANGER_BG), ("active", DANGER_BG)],
               bordercolor=[("pressed", DANGER_BG), ("active", DANGER_BG)],
               lightcolor=[("pressed", DANGER_BG), ("active", DANGER_BG)],
               darkcolor=[("pressed", DANGER_BG), ("active", DANGER_BG)],
               relief=[("pressed", "flat"), ("active", "flat")])

        # radio buttons
        st.layout("TRadiobutton", [("Radiobutton.padding", {"sticky": "nswe", "children": [
            ("Radiobutton.indicator", {"side": "left", "sticky": ""}),
            ("Radiobutton.label", {"side": "left", "sticky": "nswe"})]})])
        st.configure("TRadiobutton", background=BG, foreground=TEXT, font=self.radio_font,
                     indicatorsize=RADIO_SIZE, indicatormargin=(0, 0, S2, 0),
                     indicatorbackground=CARD, indicatorforeground=ACCENT,
                     upperbordercolor=BORDER_STRONG, lowerbordercolor=BORDER_STRONG)
        st.map("TRadiobutton", background=[("active", BG)],
               foreground=[("active", TEXT)],
               indicatorbackground=[("active", CARD), ("pressed", CARD)])

        # entry
        st.configure("TEntry", fieldbackground=CARD, foreground=TEXT, padding=(S2, S1),
                     bordercolor=BORDER, lightcolor=BORDER, darkcolor=BORDER,
                     insertcolor=TEXT, selectbackground=SELECT, selectforeground=TEXT)
        st.map("TEntry", bordercolor=[("focus", ACCENT)],
               lightcolor=[("focus", ACCENT)], darkcolor=[("focus", ACCENT)])
        st.configure("Bad.TEntry", bordercolor=RED, lightcolor=RED, darkcolor=RED)
        st.map("Bad.TEntry", bordercolor=[("focus", RED)], lightcolor=[("focus", RED)],
               darkcolor=[("focus", RED)])

        # scrollbar
        st.configure("Vertical.TScrollbar", background="#5a7084", troughcolor=STRIPE,
                     bordercolor=STRIPE, lightcolor="#5a7084", darkcolor="#5a7084",
                     arrowcolor=HEADING, gripcount=0, arrowsize=14)
        st.map("Vertical.TScrollbar", background=[("pressed", "#5a7084"),
                                                  ("active", "#5a7084")])

        # table
        st.configure("Treeview", background=TABLE_BG, fieldbackground=TABLE_BG,
                     foreground=TEXT, rowheight=TABLE_ROW_H, borderwidth=0,
                     relief="flat", bordercolor=TABLE_BG, lightcolor=TABLE_BG,
                     darkcolor=TABLE_BG)
        st.configure("Treeview.Heading", background=TABLE_BG, foreground=HEADING,
                     font=self.section_font, relief="flat", padding=TABLE_HEAD_PAD,
                     bordercolor=TABLE_BG, lightcolor=TABLE_BG, darkcolor=TABLE_BG)
        # headings are clickable too, so a click doesn't change them either
        st.map("Treeview.Heading", background=[("pressed", TABLE_BG), ("active", TABLE_BG)],
               relief=[("pressed", "flat"), ("active", "flat")])

    # LAYOUT DESIGN
    def section(self, parent, title, row, col):
        box = ttk.Frame(parent)
        box.grid(row=row, column=col, sticky="n", padx=S4, pady=(0, S2))
        ttk.Label(box, text=title, style="Section.TLabel").pack(pady=(0, S1))
        return box

    def makeButton(self, parent, text, command, accent=False, danger=False):
        if accent:
            style = "Accent.TButton"
        elif danger:
            style = "Danger.TButton"
        else:
            style = "TButton"
        return ttk.Button(parent, text=text, command=command, style=style,
                          cursor="hand2")

    def build(self):
        body = ttk.Frame(self.root, padding=(S5, S2))
        body.pack()

        ttk.Label(body, text="SET ADT OPERATIONS", style="Title.TLabel").pack(pady=(0, S2))

        form = ttk.Frame(body)
        form.pack(fill="x")
        form.columnconfigure(0, weight=1, uniform="cols")
        form.columnconfigure(1, weight=1, uniform="cols")

        # SET SELECTION
        box = self.section(form, "Select Set to Modify", 0, 0)
        row = ttk.Frame(box)
        row.pack()
        for name in ("A", "B"):
            ttk.Radiobutton(row, text="Set " + name, value=name, variable=self.which,
                            cursor="hand2").pack(side="left", padx=S2)

        #number input
        box = self.section(form, "Element", 0, 1)
        row = ttk.Frame(box)
        row.pack()
        ttk.Label(row, text="Enter integer:").pack(side="left", padx=(0, S2))
        self.entry = ttk.Entry(row, textvariable=self.entryVar, width=10)
        self.entry.pack(side="left")
        self.entry.bind("<Return>", lambda e: self.do_add())
        self.note = ttk.Label(box, textvariable=self.noteVar, style="Note.TLabel")
        self.note.pack(pady=(S1, 0))

        # add, delete, search, display 
        box = self.section(form, "Basic Set Operations", 1, 0)
        row = ttk.Frame(box)
        row.pack()
        self.makeButton(row, "Add", self.do_add, accent=False).pack(side="left", padx=BTN_GAP)
        self.makeButton(row, "Delete", self.do_delete).pack(side="left", padx=BTN_GAP)
        self.makeButton(row, "Search", self.do_search).pack(side="left", padx=BTN_GAP)
        self.makeButton(row, "Display", self.do_display).pack(side="left", padx=BTN_GAP)
        ttk.Label(box, text="Search tells if the element is a member of the set",
                  style="Note.TLabel").pack(pady=(S1, 0))

        # union 
        box = self.section(form, "Set Operations", 1, 1)
        row = ttk.Frame(box)
        row.pack()
        for text, cmd in (("Union", self.do_union),
                          ("Intersection", self.do_intersection),
                          ("Difference", self.do_difference)):
            self.makeButton(row, text, cmd).pack(side="left", padx=BTN_GAP)

        ttk.Label(body, text="Hash Table Visualization",
                  style="Section.TLabel").pack(pady=(0, S1))
        card = tk.Frame(body, bg=TABLE_BG, highlightthickness=1,
                        highlightbackground=BORDER, highlightcolor=BORDER)
        card.pack(fill="x")
        self.tree = ttk.Treeview(card, columns=("index", "A", "B", "C"),
                                 show="headings", height=SIZE, selectmode="none")
        for col, title, w in (("index", "Index", 80), ("A", "A", 170),
                              ("B", "B", 170), ("C", "C", 170)):
            self.tree.heading(col, text=title)
            self.tree.column(col, width=w, anchor="center")
        self.tree.tag_configure("empty", foreground=DATA)
        self.tree.pack(fill="x", padx=TABLE_CARD_PAD[0], pady=TABLE_CARD_PAD[1])

        # output
        ttk.Label(body, text="Set Contents / Operation Results",
                  style="Section.TLabel").pack(pady=(S2, S1))
        out = ttk.Frame(body)
        out.pack(fill="x")
        bar = ttk.Scrollbar(out)
        bar.pack(side="right", fill="y")
        self.output = tk.Text(out, height=5, width=10, wrap="word", state="disabled",
                              bg=CARD, fg=TEXT, relief="flat", padx=BOX_PAD_X, pady=S2,
                              font="TkFixedFont", highlightthickness=1,
                              highlightbackground=BORDER, highlightcolor=BORDER,
                              selectbackground=SELECT, selectforeground=TEXT,
                              inactiveselectbackground=SELECT, insertbackground=TEXT,
                              yscrollcommand=bar.set)
        self.output.pack(side="left", fill="both", expand=True)
        bar.configure(command=self.output.yview)
        self.output.tag_configure("good", foreground=GREEN)
        self.output.tag_configure("bad", foreground=RED)

        # bottom
        footer = ttk.Frame(body)
        footer.pack(fill="x", pady=(S2, 0))
        # the status line gets its own box, separate from the buttons
        status_box = tk.Frame(footer, bg=TABLE_BG, highlightthickness=1,
                              highlightbackground=BORDER, highlightcolor=BORDER)
        status_box.pack()
        ttk.Label(status_box, textvariable=self.status_var,
                  style="Status.TLabel").pack()
        btns = ttk.Frame(footer)
        btns.pack(pady=(S2, 0))
        self.makeButton(btns, "Clear Output", self.clear_log).pack(side="left", padx=BTN_GAP)
        self.makeButton(btns, "Exit", self.quit_app, danger=True).pack(side="left", padx=BTN_GAP)

    #helpers 
    def getCurrentSet(self):
        if self.which.get() == "A":
            return self.setA
        return self.setB

    def showNote(self, text, bad=False):
        self.noteVar.set(text)
        if bad:
            self.note.configure(style="Err.TLabel")
            self.entry.configure(style="Bad.TEntry")
        else:
            self.note.configure(style="Note.TLabel")
            self.entry.configure(style="TEntry")

    def get_number(self):
        raw = self.entryVar.get().strip()
        try:
            n = int(raw)
        except ValueError:
            self.showNote("Please enter a whole number", bad=True)
            self.entry.focus_set()
            self.entry.select_range(0, "end")
            return None
        self.showNote(hint_msg)
        return n

    def format_set(self, s):
        return "{" + ", ".join(str(x) for x in s.members()) + "}"

    def log(self, text, tag=""):
        self.output.configure(state="normal")
        if tag:
            self.output.insert("end", text + "\n", (tag,))
        else:
            self.output.insert("end", text + "\n")
        self.output.see("end")
        self.output.configure(state="disabled")

    def show_sets(self):
        for s in (self.setA, self.setB, self.set_c):
            self.log("SET " + s.name + ": " + self.format_set(s))

    def redraw_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for i in range(SIZE):
            cells = [i]
            filled = False
            for s in (self.setA, self.setB, self.set_c):
                v = s.table.slots[i]
                if v is None:
                    cells.append("EMPTY")
                else:
                    cells.append(v)
                    filled = True
            if filled:
                self.tree.insert("", "end", values=cells)
            else:
                self.tree.insert("", "end", values=cells, tags=("empty",))

    def update_status(self):
        self.status_var.set(
            f"Current Set: {self.which.get()}  |  "
            f"Set A Count: {self.setA.size()}  |  "
            f"Set B Count: {self.setB.size()}  |  "
            f"Set C Count: {self.set_c.size()}")

    def afterChange(self):
        self.redraw_table()
        self.update_status()
        self.entryVar.set("")
        self.entry.focus_set()

    # add \ delete \ search \ display 
    def do_add(self):
        n = self.get_number()
        if n is None:
            return
        target = self.getCurrentSet()
        result = target.add(n)
        if result == "ok":
            self.log(f"Added {n} to Set {target.name}.", "good")
        elif result == "duplicate":
            self.log(f"{n} is already in Set {target.name}.", "bad")
        else:
            self.log(f"Set {target.name} is full ({SIZE} slots), can't add {n}.", "bad")
        self.afterChange()

    def do_delete(self):
        n = self.get_number()
        if n is None:
            return
        target = self.getCurrentSet()
        if target.delete(n):
            self.log(f"Deleted {n} from Set {target.name}.", "good")
        else:
            self.log(f"{n} was not found in Set {target.name}.", "bad")
        self.afterChange()

    def do_search(self):
        n = self.get_number()
        if n is None:
            return
        target = self.getCurrentSet()
        if target.contains(n):
            self.log(f"{n} IS a member of Set {target.name}.", "good")
        else:
            self.log(f"{n} is NOT a member of Set {target.name}.")
        self.entry.focus_set()

    def do_display(self):
        self.show_sets()

    #union \ intersection / difference
    def run_set_op(self, title, symbol, op):
        try:
            self.set_c = op(self.setA, self.setB)
        except OverflowError:
            self.log(f"{title} failed: result needs more than {SIZE} slots.", "bad")
            return
        self.log(f"{title} ({symbol}) done.", "good")
        self.show_sets()
        self.afterChange()

    def do_union(self):
        self.run_set_op("Union", "A U B", MySet.union)

    def do_intersection(self):
        self.run_set_op("Intersection", "A n B", MySet.intersection)

    def do_difference(self):
        self.run_set_op("Difference", "A - B", MySet.difference)

    #bottom buttons 
    def clear_log(self):
        self.output.configure(state="normal")
        self.output.delete("1.0", "end")
        self.output.configure(state="disabled")

    def quit_app(self):
        self.root.destroy()


def main():
    root = tk.Tk()
    app = SetApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()