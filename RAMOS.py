import tkinter as tk
import tkinter.font as tkfont
from tkinter import ttk

SIZE = 10

# UI section

# surfaces
BG = "#ffffff"          # main background
CARD = "#ffffff"        # input-output surface
STRIPE = "#eef1f4"      # scrollbar trough
TABLE_BG = "#ffffff"    # used for whole table
BORDER = "#c8d0d8"      # control outlines
BORDER_STRONG = "#8a97a5"
SCROLL = "#b8c2cc"      # scrollbar thumb

# text
TEXT = "#1a1f24"        # body text
HEADING = "#1a1f24"     # title & section headings
NOTE = "#b36b00"        # notes
DATA = "#1a1f24"        # TEXT TABLE (empty cells), same as normal text

# buttons
BTN = "#4a9be8"         # buttons
BTN_TEXT = "#ffffff"
EXIT_BG = "#d9534f"     # Exit button

# brand & status
ACCENT = "#4a9be8"      # outline, radio dot
AZURE = "#007FFF"       # all four status boxes
SELECT = "#bcd9f5"      # text selection in the entry / output box
GREEN = "#1e8e4e"
RED = "#d93025"

# spacing
S1, S2, S3, S4, S5 = 4, 8, 12, 16, 24

TABLE_ROW_H = 28
TABLE_HEAD_PAD = (S3, S2)
TABLE_CARD_PAD = (S5, S2)
BOX_PAD_X = S4
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

    # shortcut: every set operation builds Set C from a list of items
    @staticmethod
    def make_c(items):
        c = MySet("C")
        for x in items:
            if c.add(x) == "full":
                raise OverflowError("too many elements")
        return c

    def union(self, other):
        return MySet.make_c(self.members() + other.members())

    def intersection(self, other):
        return MySet.make_c([x for x in self.members() if other.contains(x)])

    def difference(self, other):
        return MySet.make_c([x for x in self.members() if not other.contains(x)])


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
        self.stat_vars = {k: tk.StringVar() for k in ("current", "A", "B", "C")}

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

        # status boxes (bottom): all four are azure blue
        st.configure("Stat.TLabel", background=AZURE, foreground=BTN_TEXT,
                     font=self.section_font, padding=(S4, S2))

        # BUTTONS (normal = blue, Danger = red Exit button)
        st.layout("TButton", [("Button.border", {"sticky": "nswe", "children": [
            ("Button.padding", {"sticky": "nswe", "children": [
                ("Button.label", {"sticky": "nswe"})]})]})])
        for name, color in (("TButton", BTN), ("Danger.TButton", EXIT_BG)):
            st.configure(name, background=color, foreground=BTN_TEXT, padding=BTN_PAD,
                         relief="flat", width=-1, bordercolor=color,
                         lightcolor=color, darkcolor=color)
            # same color on hover/press so the buttons never change look
            st.map(name,
                   background=[("pressed", color), ("active", color)],
                   bordercolor=[("pressed", color), ("active", color)],
                   lightcolor=[("pressed", color), ("active", color)],
                   darkcolor=[("pressed", color), ("active", color)],
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

        #entry
        st.configure("TEntry", fieldbackground=CARD, foreground=TEXT, padding=(S2, S1),
                     bordercolor=BORDER, lightcolor=BORDER, darkcolor=BORDER,
                     insertcolor=TEXT, selectbackground=SELECT, selectforeground=TEXT)
        st.map("TEntry", bordercolor=[("focus", ACCENT)],
               lightcolor=[("focus", ACCENT)], darkcolor=[("focus", ACCENT)])
        st.configure("Bad.TEntry", bordercolor=RED, lightcolor=RED, darkcolor=RED)
        st.map("Bad.TEntry", bordercolor=[("focus", RED)], lightcolor=[("focus", RED)],
               darkcolor=[("focus", RED)])

        # scrollbar
        st.configure("Vertical.TScrollbar", background=SCROLL, troughcolor=STRIPE,
                     bordercolor=STRIPE, lightcolor=SCROLL, darkcolor=SCROLL,
                     arrowcolor=HEADING, gripcount=0, arrowsize=14)
        st.map("Vertical.TScrollbar", background=[("pressed", SCROLL),
                                                  ("active", SCROLL)])

        # table
        st.configure("Treeview", background=TABLE_BG, fieldbackground=TABLE_BG,
                     foreground=TEXT, rowheight=TABLE_ROW_H, borderwidth=0,
                     relief="flat", bordercolor=TABLE_BG, lightcolor=TABLE_BG,
                     darkcolor=TABLE_BG)
        st.configure("Treeview.Heading", background=TABLE_BG, foreground=HEADING,
                     font=self.section_font, relief="flat", padding=TABLE_HEAD_PAD,
                     bordercolor=TABLE_BG, lightcolor=TABLE_BG, darkcolor=TABLE_BG)
        st.map("Treeview.Heading", background=[("pressed", TABLE_BG), ("active", TABLE_BG)],
               relief=[("pressed", "flat"), ("active", "flat")])

    # LAYOUT DESIGN
    def section(self, parent, title, row, col):
        box = ttk.Frame(parent)
        box.grid(row=row, column=col, sticky="n", padx=S4, pady=(0, S2))
        ttk.Label(box, text=title, style="Section.TLabel").pack(pady=(0, S1))
        return box

    def makeButton(self, parent, text, command, danger=False):
        style = "Danger.TButton" if danger else "TButton"
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

        # number input
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
        for text, cmd in (("Add", self.do_add), ("Delete", self.do_delete),
                          ("Search", self.do_search), ("Display", self.show_sets)):
            self.makeButton(row, text, cmd).pack(side="left", padx=BTN_GAP)
        ttk.Label(box, text="Search tells if the element is a member of the set",
                  style="Note.TLabel").pack(pady=(S1, 0))

        # union, intersection, difference
        box = self.section(form, "Set Operations", 1, 1)
        row = ttk.Frame(box)
        row.pack()
        for text, symbol, op in (("Union", "A U B", MySet.union),
                                 ("Intersection", "A n B", MySet.intersection),
                                 ("Difference", "A - B", MySet.difference)):
            self.makeButton(row, text, lambda t=text, s=symbol, o=op:
                            self.run_set_op(t, s, o)).pack(side="left", padx=BTN_GAP)

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

        stats = ttk.Frame(footer)
        stats.pack()
        for key in ("current", "A", "B", "C"):
            ttk.Label(stats, textvariable=self.stat_vars[key], style="Stat.TLabel",
                      anchor="center", width=16).pack(side="left", padx=S1)
        btns = ttk.Frame(footer)
        btns.pack(pady=(S2, 0))
        self.makeButton(btns, "Clear Output", self.clear_log).pack(side="left", padx=BTN_GAP)
        self.makeButton(btns, "Exit", self.root.destroy, danger=True).pack(side="left", padx=BTN_GAP)

    def getCurrentSet(self):
        return self.setA if self.which.get() == "A" else self.setB

    def showNote(self, text, bad=False):
        self.noteVar.set(text)
        self.note.configure(style="Err.TLabel" if bad else "Note.TLabel")
        self.entry.configure(style="Bad.TEntry" if bad else "TEntry")

    def get_number(self):
        try:
            n = int(self.entryVar.get().strip())
        except ValueError:
            self.showNote("Please enter a whole number", bad=True)
            self.entry.focus_set()
            self.entry.select_range(0, "end")
            return None
        self.showNote(hint_msg)
        return n

    def log(self, text, tag=""):
        self.output.configure(state="normal")
        self.output.insert("end", text + "\n", tag)
        self.output.see("end")
        self.output.configure(state="disabled")

    def show_sets(self):
        for s in (self.setA, self.setB, self.set_c):
            self.log("SET " + s.name + ": {" + ", ".join(str(x) for x in s.members()) + "}")

    def redraw_table(self):
        sets = (self.setA, self.setB, self.set_c)
        self.tree.delete(*self.tree.get_children())
        for i in range(SIZE):
            cells = [i] + ["EMPTY" if s.table.slots[i] is None else s.table.slots[i]
                           for s in sets]
            empty = all(s.table.slots[i] is None for s in sets)
            self.tree.insert("", "end", values=cells, tags=("empty",) if empty else ())

    def update_status(self):
        self.stat_vars["current"].set(f"Current Set: {self.which.get()}")
        for s in (self.setA, self.setB, self.set_c):
            self.stat_vars[s.name].set(f"Set {s.name} Count: {s.size()}")

    def afterChange(self):
        self.redraw_table()
        self.update_status()
        self.entryVar.set("")
        self.entry.focus_set()

    # add / delete / search
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

    # union / intersection / difference
    def run_set_op(self, title, symbol, op):
        try:
            self.set_c = op(self.setA, self.setB)
        except OverflowError:
            self.log(f"{title} failed: result needs more than {SIZE} slots.", "bad")
            return
        self.log(f"{title} ({symbol}) done.", "good")
        self.show_sets()
        self.afterChange()

    # bottom buttons
    def clear_log(self):
        self.output.configure(state="normal")
        self.output.delete("1.0", "end")
        self.output.configure(state="disabled")


def main():
    root = tk.Tk()
    app = SetApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()