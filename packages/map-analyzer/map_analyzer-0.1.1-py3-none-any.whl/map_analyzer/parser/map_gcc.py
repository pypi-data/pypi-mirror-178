from .map import MapParser
from ..models import DetailItem
from typing import Dict

import re

class GccMapParser(MapParser):
    def __init__(self) -> None:
        super().__init__()

    def _parse_item(self, line) -> None:
        m = re.match(r'\s+([\w\.]+)\s+0x([\w\d]+)\s+0x([\w\d]+)\s+([\w\d\/]+)\.o', line)
        if (m):
            item = DetailItem()
            item.long_name  = m.group(4)
            item.start_addr = int(m.group(2), base=16)
            item.size       = int(m.group(3), base=16)
            item.type       = m.group(1)
            item.section    = m.group(1)
            
            if (item.size > 0):
                self.items.append(item)

    def _parse_calibration_item(self, line, regex):
        m = re.match(regex, line)
        if (m):
            item = DetailItem()
            item.long_name  = m.group(4)
            item.start_addr = int(m.group(1), base=16)
            item.size       = int(m.group(2), base=16)
            item.type       = "calibration"
            item.section    = m.group(3)

            self.items.append(item)
    
    def parse(self, file_name, params: Dict[str, str]) -> None:
        print("Start to parse %s..." % file_name)

        with open(file_name) as f_in:
             for line in f_in:
                m = re.match(r'\s+([\w\.]+)\s+0x([\w\d]+)\s+0x([\w\d]+)\s+([\w\d\/]+)\.o', line, re.IGNORECASE)
                if (m):
                    if (m.group(1) == ".debug_frame" or m.group(1) == ".comment" or m.group(1) == ".debug_line" 
                        or m.group(1) == ".debug_info" or m.group(1) == ".debug_loc" or m.group(1) == ".group" 
                        or m.group(1) == ".debug_macro" or m.group(1) == ".debug_str" or m.group(1) == ".debug_abbrev"
                        or m.group(1) == ".debug_ranges"):
                        continue
                    self.lines.append(m.group(0))
                    self._parse_item(line)
                
                if ('calib_regex' in params):
                    m = re.match(params['calib_regex'], line)
                    if (m):
                        self.lines.append(m.group(0))
                        self._parse_calibration_item(line, params['calib_regex'])
                        
