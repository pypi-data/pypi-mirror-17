import re

from .group_names import GroupName
from .output_types import OutputTypes
from .align_types import ImageAlignType

from jupyweave.exceptions.processor_errors import ToManySettingOccurencesError, InvalidBoolValueError, \
    TimeoutValueError, ProcessingError


class Pattern:
    """Regular expressions container. Extracts selected data from strings"""

    def __init__(self, entry, default_settings, language, echo, output, context, snippet_id, timeout, error,
                 output_type, processor, echo_lines, image_name, font_size, image_width, image_height, image_align):
        """Compiles & initializes regexes"""
        self.__entry = re.compile(entry)
        self.__default_settings = re.compile(default_settings)
        self.__language = re.compile(language)
        self.__echo = re.compile(echo)
        self.__output = re.compile(output)
        self.__context = re.compile(context)
        self.__id = re.compile(snippet_id)
        self.__timeout = re.compile(timeout)
        self.__error = re.compile(error)
        self.__output_type = re.compile(output_type)
        self.__processor = re.compile(processor)
        self.__echo_lines = re.compile(echo_lines)
        self.__font_size = re.compile(font_size)
        self.__image_name = re.compile(image_name)
        self.__image_width = re.compile(image_width)
        self.__image_height = re.compile(image_height)
        self.__image_align = re.compile(image_align)

    def entry(self):
        """Returns regex for full entry (code snippet or output snippet)"""
        return self.__entry

    def default_settings(self):
        """Returns regex for default snippets settings entry"""
        return self.__default_settings

    def language(self, string):
        """Extracts language from setting string"""
        return Pattern.__extract_setting(string, self.__language, GroupName.LANGUAGE)

    def echo(self, string):
        """Extracts echo output information from setting string"""
        return Pattern.__convert_to_bool(Pattern.__extract_setting(string, self.__echo, GroupName.ECHO))

    def output(self, string):
        """Extracts result output information from setting string"""
        return Pattern.__convert_to_bool(Pattern.__extract_setting(string, self.__output, GroupName.OUTPUT))

    def context(self, string):
        """Extracts context from setting string"""
        return Pattern.__extract_setting(string, self.__context, GroupName.CONTEXT)

    def id(self, string):
        """Extracts snippet id from setting string"""
        return Pattern.__extract_setting(string, self.__id, GroupName.ID)

    def timeout(self, string):
        """Extracts execution timeout from settings string"""
        timeout = Pattern.__extract_setting(string, self.__timeout, GroupName.TIMEOUT)
        if timeout is None:
            return None

        try:
            return int(timeout) / 1000.0
        except ValueError:
            raise TimeoutValueError(timeout)

    def error(self, string):
        """Extracts error information from string"""
        return Pattern.__convert_to_bool(Pattern.__extract_setting(string, self.__error, GroupName.ALLOW_ERROR))

    def output_type(self, string):
        """Extracts output types"""
        return OutputTypes(Pattern.__extract_setting(string, self.__output_type, GroupName.OUTPUT_TYPE))

    def processor(self, string):
        """Extracts user defined processor name"""
        return Pattern.__extract_setting(string, self.__processor, GroupName.PROCESSOR)

    def echo_lines(self, string):
        """Extracts numbers of lines of source code to display. Returns tuple of inversion flag and list of lines"""
        lines = []
        invert = False

        lines_str = Pattern.__extract_setting(string, self.__echo_lines, GroupName.ECHO_LINES)
        if lines_str is None:
            return None

        lines_str = lines_str.strip()
        if lines_str.startswith('!'):
            lines_str = lines_str.lstrip('!')
            invert = True

        lines_ranges = lines_str.split(',')
        for r in lines_ranges:
            r = r.strip()
            rx = re.split(':|-', r)
            if len(rx) == 2:
                lines.extend(range(int(rx[0].strip()), int(rx[1].strip()) + 1))
            else:
                lines.append(int(r))

        return invert, lines

    def image_name(self, string):
        """Extracts image file name"""
        return Pattern.__extract_setting(string, self.__image_name, GroupName.IMAGE_NAME)

    def image_width(self, string):
        """Extracts image width"""
        value = Pattern.__extract_setting(string, self.__image_width, GroupName.IMAGE_WIDTH)
        return None if value is None else int(value)

    def image_height(self, string):
        """Extracts image height"""
        value = Pattern.__extract_setting(string, self.__image_height, GroupName.IMAGE_HEIGHT)
        return None if value is None else int(value)

    def image_align(self, string):
        """Extracts align"""
        align_str = Pattern.__extract_setting(string, self.__image_align, GroupName.IMAGE_ALIGN)

        if align_str is None:
            return ImageAlignType.Default

        align_str = align_str.strip().lower()

        if align_str == 'center':
            return ImageAlignType.Center

        if align_str == 'left':
            return ImageAlignType.Left

        if align_str == 'right':
            return ImageAlignType.Right

        raise ProcessingError("Invalid align value")

    @staticmethod
    def __extract_setting(string, regex, group_name):
        """Extracts setting with given regex and group name from string"""
        items = re.finditer(regex, string)
        items = [item for item in items]

        if len(items) == 0:
            return None

        if len(items) != 1:
            raise ToManySettingOccurencesError(group_name)

        return items[0].group(group_name).strip(',')

    @staticmethod
    def __convert_to_bool(value):
        """Converts value to bool, or raises exception"""
        if value is None:
            return None

        if value.lower().strip() in ['t', 'true', '1', 'y', 'yes']:
            return True

        if value.lower().strip() in ['f', 'false', '0', 'n', 'no']:
            return False

        raise InvalidBoolValueError(value)
