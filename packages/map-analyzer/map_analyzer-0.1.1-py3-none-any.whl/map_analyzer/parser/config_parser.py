from typing import Dict, List
from ..models import FileProperty

import toml
import re

class ConfigParser:
    def __init__(self) -> None:
        self.compiler = ""
        self.parameters = {}                    # type: Dict(str, str)
        self.file_properties = {}               # type: Dict(str, FileProperty)
        self.type_regexes = {}                  # type: Dict(str, str)
        self.group_regexes = {}                 # type: Dict(str, str)
        self.core_regexes = {}                  # type: Dict(str, str)
        self.group_core_mapping = {}            # type: Dict(str, str)
        self.group_formats = {}                 # type: Dict(str, str)
        self.section_types = {}                 # type: List(str, str)

        self.parameters['image']      = {}
        self.parameters['image']['start_addr'] = 0x00000000
        self.parameters['image']['end_addr']   = 0xFFFFFFFF

    def _parse_general(self, data):
        if ('compiler' in data['general']):
            self.compiler = data['general']['compiler']

    def _parse_calibration(self, data):
        param_keys = ['regex']
        for key in param_keys:
            if (key in data):
                self.parameters["calib_%s" % key] = data[key]

    def _parse_files(self, data):
        for key in data['files']:
            property = FileProperty()
            property.name = key
            property.group = data['files'][key]['group']

            self.file_properties[property.name] = property

    def _parse_type_regexes(self, data):
        for key in data['type_regexes']:
            self.type_regexes[key] = data['type_regexes'][key]

    def _parse_group_regexes(self, data):
        for key in data:
            self.group_regexes[key] = data[key]

    def _parse_group_format(self, data):
        for key in data:
            self.group_formats[key] = data[key]

    def _parse_core_regex(self, data):
        for key in data:
            self.core_regexes[key] = data[key]

    def _parse_group_core_mapping(self, data):
        for key in data:
            self.group_core_mapping[key] = data[key]

    #def _parse_number(self, data: str):
    #    m = re.match(r"0x([0-9a-f]+)", data, re.I)
    #    if (m):
    #        return int(m.group(1), base=16)
    #    return int(data)

    def _parse_image_size(self, data):
        if 'start_addr' in data:
            self.parameters['image']['start_addr'] = data['start_addr']
        if 'end_addr' in data:
            self.parameters['image']['end_addr'] = data['end_addr']

    def parse(self, name):
        data = toml.load(name)

        #print(data)
        
        if ('general' in data):
            self._parse_general(data)

        if ('calib' in data):
            self._parse_calibration(data['calib'])
        
        if ('files' in data):
            self._parse_files(data)

        if ('type_regexes' in data):
            self._parse_type_regexes(data)

        if ('group' in data):
            if ('regex' in data['group']):
                self._parse_group_regexes(data['group']['regex'])
            if ('format' in data['group']):
                self._parse_group_format(data['group']['format'])

        if ('core' in data):
            if ('regex' in data['core']):
                self._parse_core_regex(data['core']['regex'])
            if ('group' in data['core']):
                self._parse_group_core_mapping(data['core']['group'])

        if ('section' in data):
            if ('type' in data['section']):
                self.section_types = data['section']['type']

        if ('image' in data):
            self._parse_image_size(data['image'])
