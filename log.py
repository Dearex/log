import datetime
import sys
import os

bold =                "\033[1m"
underlined =          "\033[2m"
italic =              "\033[3m"

black_text =          "\033[30m"
red_text =            "\033[31m"
green_text =          "\033[32m"
yellow_text =         "\033[33m"
blue_text =           "\033[34m"
rose_text =           "\033[35m"
cyan_text =           "\033[36m"
white_text =          "\033[37m"

black_background =    "\033[40m"
red_background =      "\033[41m"
green_background =    "\033[42m"
yellow_background =   "\033[43m"
blue_background =     "\033[44m"
rose_background =     "\033[45m"
cyan_background =     "\033[46m"
white_background =    "\033[47m"

qf_options = {
    "*": bold,
    "_": underlined,
    "/": italic,
    "+": green_text,
    "-": red_text,
    "=": yellow_text,
    "B": black_background,
    "r": red_background,
    "g": green_background,
    "y": yellow_background,
    "b": blue_background,
    "r": rose_background,
    "c": cyan_background,
    "W": white_background
}

end_format = "\033[m"

log_levels = {
    "debug": {
        "level":    0,
        "short":    "DBG",
        "format":   [black_text, green_background]
    },
    "info": {
        "level":    10,
        "short":    "INF",
        "format":   [blue_text]
    },  
    "warning": {    
        "level":    20,
        "short":    "WRN",
        "format":   [yellow_text]
    },  
    "error": {  
        "level":    30,
        "short":    "ERR",
        "format":   [red_text, bold]
    }
}

output_methonds = {
    "console":  {
        "method":   lambda self, string: _print(self, string),
        "level":    0,
        "extended_format":   True
    },
    "file":     {
        "method":   lambda self, string: _write(self, string),
        "level":    0,
        "extended_format":   False
    }     
}


class _log():
    '''
    Like print() but better!\n
    Many little features that allow for easy console or other logging of events without complicated setup.
    '''
    
    def __init__(self) -> None:
        self.log_level = 0
        self.output = {"console": None} # , "file": None
        self.log_file_path = (os.getcwd() + "/logs/").replace("\\", "/")
        self.log_file_format = "%Y-%m-%d.log"
        pass

    def debug(self, text:str, quick_format=""):
        _log_process(self, sys._getframe(0).f_code.co_name, text, quick_format)

    def info(self, text:str, quick_format=""):
        _log_process(self, sys._getframe(0).f_code.co_name, text, quick_format)

    def warning(self, text:str, quick_format=""):
        _log_process(self, sys._getframe(0).f_code.co_name, text, quick_format)

    def error(self, text:str, quick_format=""):
        _log_process(self, sys._getframe(0).f_code.co_name, text, quick_format)

    def _format_filename(self) -> str:
        return datetime.datetime.strftime(datetime.datetime.now(), self.log_file_format)

def _log_process(self, level, text, quick_format):
    for wanted_method in self.output.keys():
        general_method = output_methonds[wanted_method]
        if self.output[wanted_method] == None:
            if self.log_level <= log_levels[level]["level"]:
                general_method["method"](self, _log_format(level, text, quick_format, general_method["extended_format"]))
        else:
            if self.output[wanted_method] <= log_levels[level]["level"]:
                general_method["method"](self, _log_format(level, text, quick_format, general_method["extended_format"]))


def _log_format(level: str, text:str, quick_format:str, extended_format:bool) -> str:
    level = log_levels[level]
    output_string = ""
    if extended_format:
        for format in level["format"]:
            output_string += format
        output_string += f'{_formatted_time()} '
        output_string += f'[{level["short"]}]:{end_format} '
        output_string += f'{get_quick_formats(quick_format)}'
        output_string += f'{text}'
        output_string += f'{end_format}'
    else:
        output_string += f'{_formatted_time()} '
        output_string += f'[{level["short"]}]: '
        output_string += f'{text}'
    
    return output_string

def _print(self, output_string) -> None:
    print(output_string)

def _write(self, output_string) -> None:
    if not os.path.exists(self.log_file_path):
        os.mkdir(self.log_file_path)
    with open(self.log_file_path + f'{self._format_filename()}', "a") as file:
        file.write(output_string + "\n")


def get_quick_formats(quick_format: str) -> str:
    string = ""
    for char in quick_format:
        string += qf_options[char]
    return string

def _formatted_time(format="%Y-%m-%d %H:%M:%S") -> str:
    return datetime.datetime.strftime(datetime.datetime.now(), format)



log = _log()
