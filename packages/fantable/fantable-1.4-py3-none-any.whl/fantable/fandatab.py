import shutil, os, sys

if os.name == "nt":
    import msvcrt
    import ctypes

    class _CursorInfo(ctypes.Structure):
        _fields_ = [("size", ctypes.c_int), ("visible", ctypes.c_byte)]


def term_size():
    try:
        return shutil.get_terminal_size().columns
    except:
        exit("Terminal Tidak Didukung!")


class Table:
    def __init__(self, title=None, refresh=False):
        self.title = title
        self.__num = 0
        self.__tabl = {"coll": None, "trow": {}}
        self.__myTable = None
        self.__size = term_size()
        self.__refresh = refresh

    def column(self, *arg):
        self.__tabl.update({"coll": [data for data in arg]})

    def tab_row(self, *arg):
        self.__num += 1
        self.__tabl["trow"].update({f"row{self.__num}": [data for data in arg]})

    def commit(self):
        data_size = []
        terminal_size = term_size() if self.__refresh else self.__size
        for i in range(len(self.__tabl["coll"])):
            spliter = self.__tabl["coll"][i].splitlines()
            spliter = sorted(spliter, key=len)[-1]
            data_temp = [spliter]
            for z in range(len(self.__tabl["trow"])):
                spliter_ = self.__tabl["trow"][f"row{z+1}"][i].splitlines()
                spliter_ = sorted(spliter_, key=len)[-1]
                data_temp.append(spliter_)
            data_len = sorted(data_temp, key=len)
            data_size.append(len(data_len[-1]))
        ts = self.__size - ((4 * len(data_size)) - (len(data_size) - 1))
        hasil = self.size_max(data_size, ts)
        hasil_ = self.data_processing(self.__tabl, hasil)
        nump = self.size_identifier(hasil_)
        maker = self.table_maker(nump, hasil)
        self.__myTable = maker

    def size_max(self, data_size, ts) -> list:
        if sum(data_size) > ts:
            size = ts // len(data_size)
            siz = [a for a in data_size if a > size]
            num = sum(data_size) - sum(siz)
            num = ts - num
            num = num // len(siz)
            for i in range(len(data_size)):
                data_size[i] = num if data_size[i] > size else data_size[i]
            data_size[-1] = data_size[-1] + (ts - sum(data_size))
            return data_size
        else:
            return data_size

    def data_processing(self, data, hasil) -> dict:
        for x in range(len(data["coll"])):
            optext = data["coll"][x].splitlines()
            for datz in enumerate(optext):
                optext[datz[0]] = (
                    "\n".join(
                        items + " " * (hasil[x] - len(items))
                        for items in [
                            datz[1][num * hasil[x] : (num + 1) * hasil[x]]
                            for num in range((len(datz[1]) // hasil[x]) + 1)
                            if optext[num * hasil[x] : (num + 1) * hasil[x]] != ""
                        ]
                    )
                    if len(datz[1]) > hasil[x]
                    else "\n".join(
                        items + " " * (hasil[x] - len(items))
                        for items in [
                            datz[1][num * hasil[x] : (num + 1) * hasil[x]]
                            for num in range((len(datz[1]) // hasil[x]) + 1)
                            if optext[num * hasil[x] : (num + 1) * hasil[x]] != ""
                        ]
                    ).splitlines()[0]
                )
            data["coll"][x] = "\n".join(strs for strs in optext)
            for y in range(len(data["trow"])):
                optext_ = data["trow"][f"row{y+1}"][x].splitlines()
                for datz_ in enumerate(optext_):
                    optext_[datz_[0]] = (
                        "\n".join(
                            items_ + " " * (hasil[x] - len(items_))
                            for items_ in [
                                datz_[1][num_ * hasil[x] : (num_ + 1) * hasil[x]]
                                for num_ in range((len(datz_[1]) // hasil[x]) + 1)
                                if optext_[num_ * hasil[x] : (num_ + 1) * hasil[x]]
                                != ""
                            ]
                        )
                        if len(datz_[1]) > hasil[x]
                        else "\n".join(
                            items_ + " " * (hasil[x] - len(items_))
                            for items_ in [
                                datz_[1][num_ * hasil[x] : (num_ + 1) * hasil[x]]
                                for num_ in range((len(datz_[1]) // hasil[x]) + 1)
                                if optext_[num_ * hasil[x] : (num_ + 1) * hasil[x]]
                                != ""
                            ]
                        ).splitlines()[0]
                    )
                data["trow"][f"row{y+1}"][x] = "\n".join(strs_ for strs_ in optext_)
        return data

    def size_identifier(self, data) -> dict:
        data_size = [max([len(z.splitlines()) for z in data["coll"]])] + [
            max([len(z.splitlines()) for z in data["trow"][f"row{x+1}"]])
            for x in range(len(data["trow"]))
        ]
        for a in enumerate(data_size):
            if a[0] == 0:
                for q in range(len(data["coll"])):
                    if len(data["coll"][q].splitlines()) != a[1]:
                        blank = " " * len(data["coll"][q].splitlines()[0])
                        df = data["coll"][q]
                        for x in range(a[1] - len(df.splitlines())):
                            df = df + f"\n{blank}"
                        data["coll"][q] = df
            else:
                for q in range(len(data["trow"][f"row{a[0]}"])):
                    if len(data["trow"][f"row{a[0]}"][q].splitlines()) != a[1]:
                        blank = " " * len(data["trow"][f"row{a[0]}"][q].splitlines()[0])
                        df = data["trow"][f"row{a[0]}"][q]
                        for x in range(a[1] - len(df.splitlines())):
                            df = df + f"\n{blank}"
                        data["trow"][f"row{a[0]}"][q] = df
        return data

    def table_maker(self, data, size, spc=" ") -> str:
        head_line = "+" + "+".join("=" * (num + 2) for num in size) + "+"
        tab_line = "+" + "+".join("-" * (num + 2) for num in size) + "+"
        header = "\n".join(
            a
            for a in [
                "| "
                + " | ".join(
                    data["coll"][z].splitlines()[num] for z in range(len(data["coll"]))
                )
                + " |"
                for num in range(len(data["coll"][0].splitlines()))
            ]
        )
        header = f"{head_line}\n{header}\n{head_line}"
        for i in range(len(data["trow"])):
            header_ = "\n".join(
                a
                for a in [
                    "| "
                    + " | ".join(
                        data["trow"][f"row{i+1}"][z].splitlines()[num]
                        for z in range(len(data["trow"][f"row{i+1}"]))
                    )
                    + " |"
                    for num in range(len(data["trow"][f"row{i+1}"][0].splitlines()))
                ]
            )
            header = f"{header}\n{header_}\n{tab_line}"
        header = (
            header
            if self.title is None
            else f"{spc*((len(head_line)-len(self.title))//2)}{self.title}\n{header}"
        )
        return header

    def __repr__(self):
        return self.__myTable


class Live:
    def __init__(self, refresh=False):
        self.__size = None
        self.__sizer = term_size()
        self.__refr = refresh
        if os.name == "nt":
            ci = _CursorInfo()
            handle = ctypes.windll.kernel32.GetStdHandle(-11)
            ctypes.windll.kernel32.GetConsoleCursorInfo(handle, ctypes.byref(ci))
            ci.visible = False
            ctypes.windll.kernel32.SetConsoleCursorInfo(handle, ctypes.byref(ci))
        elif os.name == "posix":
            sys.stdout.write("\033[?25l")
            sys.stdout.flush()

    def text_processing(self, optext):
        optext = str(optext).splitlines()
        for datz in enumerate(optext):
            optext[datz[0]] = "\n".join(
                items + " " * (self.__size - len(items))
                for items in [
                    datz[1][num * self.__size : (num + 1) * self.__size]
                    for num in range((len(datz[1]) // self.__size) + 1)
                    if optext[num * self.__size : (num + 1) * self.__size] != ""
                ]
            )
        return "\n".join(strs for strs in optext)

    def render(self, description: str = None):
        self.__size = term_size() if self.__refr else self.__sizer
        dattext = self.text_processing(description)
        print(dattext)
        sys.stdout.write("\x1b[1A" * len(dattext.splitlines()))

    def print(self, text: str = None):
        dattext = self.text_processing(text)
        mytext = "\n".join(
            stc
            for stc in [
                items + " " * (self.__size - len(items))
                for items in dattext.splitlines()
            ]
        )
        print(mytext)
