class Section:
    def __init__(self) -> None:
        self.name = ""
        self.base_addr = 0
        self.size = 0
        self.offset = 0
        self.type = "N/A"

    def __str__(self) -> str:
        lines = []
        lines.append("Name       : %s" % self.name)
        lines.append("Base Addr  : %x" % self.base_addr)
        lines.append("Offset     : %d" % self.offset)
        lines.append("Size       : %d" % self.size)
        lines.append("Type       : %s" % self.type)
        
        return "\n".join(lines)