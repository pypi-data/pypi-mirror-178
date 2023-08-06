class DetailGroup:
    def __init__(self) -> None:
        self.name = ""
        self.core = ""
        self.items = set()
        self.text_total = 0
        self.rodata_total = 0
        self.bss_total = 0
        self.data_total = 0
        self.calib_total = 0

    def __str__(self) -> str:
        lines = []
        lines.append("Name       : %s" % self.name)
        lines.append("Items      :")
        for item in self.items:
            lines.append("           : %s" % item)
        lines.append("Total BSS    : %d" % self.bss_total)
        lines.append("Total DATA   : %d" % self.data_total)
        lines.append("Total TEXT   : %d" % self.text_total)
        lines.append("Total RODATA : %d" % self.rodata_total)
        lines.append("Total CALIB  : %d" % self.calib_total)
        return "\n".join(lines)

    @property
    def files(self) -> str:
        return "\n".join(self.items)

    @property
    def total_ram(self)-> int:
        return self.bss_total + self.data_total

    @property
    def total_rom(self) -> int:
        return self.text_total + self.rodata_total

    @property
    def total(self) -> int:
        return self.total_ram + self.total_rom + self.calib_total