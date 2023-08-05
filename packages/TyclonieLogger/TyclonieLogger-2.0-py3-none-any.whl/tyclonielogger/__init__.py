import datetime
import inspect
from colorama import Fore, Back, Style, init

""" PLEASE NOTE THAT ALL COLOUR INFORMATION IS FROM COLORAMA """


class TyclonieLogger:
    def __init__(self, **options):
        self.__set_options(options)
        self.__load_colours()

    def __load_colours(self) -> None:
        self.fore_colours = {}
        self.back_colours = {}
        self.styles = {}
        all_fore_colours = inspect.getmembers(Fore)
        for fore_colour in all_fore_colours:
            if isinstance(fore_colour[0], str) and not fore_colour[0].endswith("__"):
                self.fore_colours[fore_colour[0]] = fore_colour[1]
        all_back_colours = inspect.getmembers(Back)
        for back_colour in all_back_colours:
            if isinstance(back_colour[0], str) and not back_colour[0].endswith("__"):
                self.back_colours[back_colour[0]] = back_colour[1]
        all_styles = inspect.getmembers(Style)
        for style in all_styles:
            if isinstance(style[0], str) and not style[0].endswith("__"):
                self.styles[style[0]] = style[1]

    def __set_options(self, options) -> None:
        self.__dict__.update({"datetime_format": '%Y/%m/%d @ %H:%M:%S',
                              "datetime_text_divider": ' | ',
                              "datetime_background": 'YELLOW',
                              "datetime_foreground": 'BLACK',
                              "datetime_style": 'NORMAL',
                              "log_identifier_foreground": 'GREEN',
                              "log_identifier_background": 'NORMAL',
                              "log_identifier_style": 'NORMAL',
                              "log_message_foreground": 'NORMAL',
                              "log_message_background": 'NORMAL',
                              "log_message_style": 'NORMAL',
                              "log_identifier_message_divider": ': ',
                              "log_dividers_foreground": 'NORMAL',
                              "log_dividers_background": 'NORMAL',
                              "log_dividers_style": 'NORMAL',
                              "warn_identifier_foreground": 'RED',
                              "warn_identifier_background": 'NORMAL',
                              "warn_identifier_style": 'BRIGHT',
                              "warn_message_foreground": 'NORMAL',
                              "warn_message_background": 'NORMAL',
                              "warn_message_style": 'NORMAL',
                              "warn_identifier_message_divider": ': ',
                              "warn_dividers_foreground": 'NORMAL',
                              "warn_dividers_background": 'NORMAL',
                              "warn_dividers_style": 'NORMAL',
                              "error_identifier_foreground": 'BLACK',
                              "error_identifier_background": 'RED',
                              "error_identifier_style": 'BRIGHT',
                              "error_message_foreground": 'RED',
                              "error_message_background": 'NORMAL',
                              "error_message_style": 'NORMAL',
                              "error_identifier_message_divider": ': ',
                              "error_dividers_foreground": 'NORMAL',
                              "error_dividers_background": 'NORMAL',
                              "error_dividers_style": 'NORMAL'})
        self.__dict__.update(options)

    def __get_style(self, option) -> str:
        return self.styles[self.__dict__.get(option)]

    def __get_foreground_colour(self, option) -> str:
        selected = self.__dict__.get(option)
        if selected == "NORMAL":
            return self.fore_colours["RESET"]
        return self.fore_colours[self.__dict__.get(option)]

    def __get_background_colour(self, option) -> str:
        selected = self.__dict__.get(option)
        if selected == "NORMAL":
            return self.back_colours.get("RESET")
        return self.back_colours[self.__dict__.get(option)]

    def __get_datetime_formatted(self) -> str:
        return f"{self.__get_foreground_colour('datetime_foreground')}{self.__get_background_colour('datetime_background')}{self.__get_style('datetime_style')}{datetime.datetime.now().strftime(self.__dict__.get('datetime_format'))}{Style.RESET_ALL}"

    def log(self, message) -> None:
        print(
            f"{self.__get_datetime_formatted()}{self.__get_style('log_dividers_style')}{self.__get_foreground_colour('log_dividers_foreground')}{self.__get_background_colour('log_dividers_background')}{self.__dict__.get('datetime_text_divider')}{self.__get_foreground_colour('log_identifier_foreground')}{self.__get_background_colour('log_identifier_background')}{self.__get_style('log_identifier_style')}Log{self.__get_style('log_dividers_style')}{self.__get_foreground_colour('log_dividers_foreground')}{self.__get_background_colour('log_dividers_background')}: {self.__get_style('log_message_style')}{self.__get_foreground_colour('log_message_foreground')}{self.__get_background_colour('log_message_background')}{message}{Style.RESET_ALL}")

    def warn(self, message) -> None:
        print(
            f"{self.__get_datetime_formatted()}{self.__get_style('warn_dividers_style')}{self.__get_foreground_colour('warn_dividers_foreground')}{self.__get_background_colour('warn_dividers_background')}{self.__dict__.get('datetime_text_divider')}{self.__get_foreground_colour('warn_identifier_foreground')}{self.__get_background_colour('warn_identifier_background')}{self.__get_style('warn_identifier_style')}Warning{self.__get_style('warn_dividers_style')}{self.__get_foreground_colour('warn_dividers_foreground')}{self.__get_background_colour('warn_dividers_background')}: {self.__get_style('warn_message_style')}{self.__get_foreground_colour('warn_message_foreground')}{self.__get_background_colour('warn_message_background')}{message}{Style.RESET_ALL}")

    def error(self, message) -> None:
        print(
            f"{self.__get_datetime_formatted()}{self.__get_style('error_dividers_style')}{self.__get_foreground_colour('error_dividers_foreground')}{self.__get_background_colour('error_dividers_background')}{self.__dict__.get('datetime_text_divider')}{self.__get_foreground_colour('error_identifier_foreground')}{self.__get_background_colour('error_identifier_background')}{self.__get_style('error_identifier_style')}Error{self.__get_style('error_dividers_style')}{self.__get_foreground_colour('error_dividers_foreground')}{self.__get_background_colour('error_dividers_background')}: {self.__get_style('error_message_style')}{self.__get_foreground_colour('error_message_foreground')}{self.__get_background_colour('error_message_background')}{message}{Style.RESET_ALL}")

    def show_styles(self):
        for style in self.styles:
            print(self.styles[style] + style)
        print(Style.RESET_ALL)

    def show_foreground_colours(self):
        for colour in self.fore_colours:
            print(self.fore_colours[colour] + colour)
        print(Style.RESET_ALL)

    def show_background_colours(self):
        for colour in self.back_colours:
            print(self.back_colours[colour] + colour)
        print(Style.RESET_ALL)


if __name__ != "__main__":
    init()
