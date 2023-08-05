from PySide2 import QtCore


class Font:
    Regular = 25
    Medium = 75
    Bold = 99


COLORS = {
    # old colors
    # palette
    "white": "#ffffff",
    "light1": "#f7f7f7",
    "light2": "#ededed",
    "light3": "#dbdbdb",
    "light4": "#c7c7c7",
    "middle1": "#adadad",
    "middle2": "#919191",
    "middle3": "#787878",
    "middle4": "#5e5e5e",
    "dark1": "#3b3b3b",
    "dark2": "#303030",
    "dark3": "#242424",
    "dark4": "#181818",
    "black": "#000000",
    "green1": "#5ae4aa",
    "green2": "#1dcf8e",
    "green3": "#00ad74",
    "lime1": "#adf75e",
    "lime2": "#97de4b",
    "lime3": "#80c23a",
    "yellow1": "#f8df52",
    "yellow2": "#f5ca1b",
    "yellow3": "#dab00a",
    "red1": "#ff725c",
    "red2": "#ea5949",
    "red3": "#c9423b",
    "blue1": "#3ad4f2",
    "blue2": "#11b2df",
    "blue3": "#1083ad",
    # Athena2 colors
    "contrast": "#ffffff",  # We use it only if the shape lies on a colored or dark background.
    "base": "#dbdbdb",  # All main text on a dark background.
    "secondary": "#adadad",  # Secondary text: subtitle, signature.
    "nonessential": "#787878",  # Tertiary text if used in conjunction with base and secondary.
    "disabled": "#5e5e5e",  # Disabled element shapes: inactive button, non-editable setting.
    "inverted": "#000000",  # Figures on a light background.
    "interactive": "#5ae4aa",  # Clickable shapes.
    "attention": "#ff725c",  # For attracting attention, reporting a problem, warning you about unwanted consequences.
    "warning": "#ebab0a",  # To alert you to an event that could have negative consequences.
    "warningContrast": "#f8df52",  # To alert you to an event that could have negative consequences.
    "info": "#80c23a",  # To draw the user's attention to an event or process.
    "transparent": "#00000000",
}

BACKGROUNDS = {
    # Athena2 backgrounds
    "accent": "#F7F7F7",  # Для контрастных беков
    "highest": "#3B3B3B",  # Для карточек и основных элементов
    "high": "#303030",  # Для второстепенных беков
    "base": "#242424",  # Средний уровень
    "low": "#181818",  # Неактивные чипсы, подложка свитча и слайдера, чекбокса
    "lowest": "#000000",  # Для выбранных элементов и тулбаров
    "overlay": "#B3000000",  # + opacity 0.7!  Полупрозрачные затемнения под элементами, что находятся выше остальных
}

# === Athena 3 ===
FIGURE = {
    "base": "#dbdbdb",
    "secondary": "#adadad",
    "nonessential": "#787878",
    "disabled": "#5e5e5e",
    "inverted": "#000000",
    "contrast": "#ffffff",
    "interactive": "#5ae4af",
    "attention": "#ff725c",
    "positive": "#7fc337",
    "positiveContrast": "#adf75e",
    "warning": "#ebab0a",
    "warningContrast": "#f8df52",
    "transparent": "#00000000",
    "hazard": "#d080ff",
}
BG = {
    "highest": "#404040",
    "high": "#333333",
    "base": "#262626",
    "low": "#1c1c1c",
    "lowest": "#000000",
    "accent": "#ffffff",
    "overlay": "#b3000000",
}
SPECIAL = {
    "knob": "#333333",
    "hole": "#7a7a7a",
    "divider": "#000000",
    "white": "#ffffff",
    "black": "#000000",
    "selection": "#000000",
}
TEXT = {
    "title": {
        "XXLBold": {"size": 48, "height": 56, "weight": Font.Regular,},
        "XLBold": {"size": 32, "height": 40, "weight": Font.Medium,},
        "LBold": {"size": 28, "height": 40, "weight": Font.Medium,},
        "MBold": {"size": 24, "height": 32, "weight": Font.Medium,},
        "SBold": {"size": 20, "height": 28, "weight": Font.Medium,},
        "XSBold": {"size": 17, "height": 24, "weight": Font.Medium,},
        "XSRegular": {"size": 17, "height": 24, "weight": Font.Regular,},
    },
    "body": {
        "LBold": {"size": 16, "height": 24, "weight": Font.Medium,},
        "LRegular": {"size": 16, "height": 24, "weight": Font.Regular,},
        "MBold": {"size": 14, "height": 20, "weight": Font.Medium,},
        "MRegular": {"size": 14, "height": 20, "weight": Font.Regular,},
        "SBold": {"size": 12, "height": 16, "weight": Font.Medium,},
        "SRegular": {"size": 12, "height": 16, "weight": Font.Regular,},
        "XSRegular": {"size": 11, "height": 16, "weight": Font.Medium,},
    },
    "button": {
        "MBold": {"size": 17, "height": 24, "weight": Font.Bold,},
        "MRegular": {"size": 17, "height": 24, "weight": Font.Regular,},
        "SBold": {"size": 13, "height": 20, "weight": Font.Medium,},
    },
    "special": {
        "BadgeRegular": {"size": 13, "height": 20, "weight": Font.Regular,},
        "SectionCaps": {
            "size": 13,
            "height": 20,
            "weight": Font.Regular,
            "uppercase": True,
        },
    },
}
STATUS = {
    "DEFAULT": 0,
    "POSITIVE": 1,
    "WARNING": 2,
    "ATTENTION": 3,
    "HAZARD": 4,
    "NOT_IMPORTANT": 5,
}
# === Athena 3 ===

CONTROLS = {
    "plus": {
        "color": COLORS["interactive"],
        "imageSource": "qrc:/resources/images/Athena/common_icons/plus.svg",
    },
    "minus": {
        "color": COLORS["attention"],
        "imageSource": "qrc:/resources/images/Athena/common_icons/minus.svg",
    },
    "alarm": {
        "color": COLORS["warning"],
        "imageSource": "qrc:/resources/images/Athena/common_icons/alarm.svg",
    },
    "cross": {
        "color": BACKGROUNDS["base"],
        "imageSource": "qrc:/resources/images/Athena/common_icons/cross.svg",
    },
    "back": {
        "color": BACKGROUNDS["base"],
        "imageSource": "qrc:/resources/images/Athena/common_icons/Back-M.svg",
    },
}


class Athena3(QtCore.QObject):
    # Athena 3
    figure = QtCore.Property(
        QtCore.QJsonValue,
        lambda _: QtCore.QJsonValue.fromVariant(FIGURE),
        constant=True,
    )
    bg = QtCore.Property(
        QtCore.QJsonValue, lambda _: QtCore.QJsonValue.fromVariant(BG), constant=True
    )
    special = QtCore.Property(
        QtCore.QJsonValue,
        lambda _: QtCore.QJsonValue.fromVariant(SPECIAL),
        constant=True,
    )
    text = QtCore.Property(
        QtCore.QJsonValue, lambda _: QtCore.QJsonValue.fromVariant(TEXT), constant=True
    )
    status = QtCore.Property(
        QtCore.QJsonValue, lambda _: QtCore.QJsonValue.fromVariant(STATUS), constant=True
    )


class RegexProperty(QtCore.Property):
    def __init__(self, regex):
        super().__init__(
            type=QtCore.QRegExp, fget=lambda _: QtCore.QRegExp(regex), constant=True
        )


class Regexes(QtCore.QObject):
    _email_pattern = r"[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*"

    websiteUrl = RegexProperty(r"^https?:\/\/\w[\w-/]*(\.\w{1,})+$")
    ip = RegexProperty(
        r"^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4]["
        r"0-9]|25[0-5])$"
    )
    scenario_name = RegexProperty(r"^(?!.*  )(?=.*[\w-])[\w -]{1,24}$")
    time = RegexProperty(r"^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$")
    email = RegexProperty(f"^{_email_pattern}$")
    multi_emails = RegexProperty(fr"^({_email_pattern}\s+)*({_email_pattern})$")
    port = RegexProperty(
        r"^([0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])$"
    )
    qr_code = RegexProperty(
        r"^([0-9a-fA-F]{11})$|^([0-9a-fA-F]{9})$|^([0-9a-fA-F]{6})$"
    )
    user_passcode = RegexProperty(r"[0-9]{4,6}")
    object_number = RegexProperty(r"[0-9A-Fa-f]{0,16}")
    day_time = RegexProperty(r"^([0-1][0-9]|2[0-3]):([0-5][0-9])$")
    hours = RegexProperty(r"^([0-1][0-9]|2[0-3])$")
    hours_ampm = RegexProperty(r"^((1|0)?[0-9]) ([AaPp][Mm])$")
    minutes = RegexProperty(r"^([0-5][0-9])$")
    scenario_minutes = RegexProperty(r"^([0-5][0-9]|[0-9])$")
    scenario_seconds = RegexProperty(r"^([0-5][0-9]|[0-9])$")
    phone = RegexProperty(r"^[\+]?[0-9]{8,16}$")
    phoneNoCode = RegexProperty(r"^[0-9]{9,10}$")
    hub_qr = RegexProperty(r"[0-9A-Fa-f-]+")
    certification_master_key = RegexProperty(r"[0-9A-Fa-f]{0,8}")

class Customization(QtCore.QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._athena3 = Athena3()
        self._regexes = Regexes()

    ds3 = QtCore.Property(QtCore.QObject, lambda self: self._athena3, constant=True)

    def _get_colors(self):
        return QtCore.QJsonValue.fromVariant(COLORS)

    colors = QtCore.Property(QtCore.QJsonValue, _get_colors, constant=True)

    def _get_backgrounds(self):
        return QtCore.QJsonValue.fromVariant(BACKGROUNDS)

    backgrounds = QtCore.Property(QtCore.QJsonValue, _get_backgrounds, constant=True)

    def _get_specials(self):
        return QtCore.QJsonValue.fromVariant(SPECIAL)

    specials = QtCore.Property(QtCore.QJsonValue, _get_specials, constant=True)

    def _get_controls(self):
        return QtCore.QJsonValue.fromVariant(CONTROLS)

    controls = QtCore.Property(QtCore.QJsonValue, _get_controls, constant=True)

    def _get_required(self):
        return " <font color='#ff725c'>*</font>"

    required = QtCore.Property(str, _get_required, constant=True)

    def _get_checkbox_true(self):
        return "<font color='#60e3ab'>✔</font>  "

    checkbox_true = QtCore.Property(str, _get_checkbox_true, constant=True)

    def _get_checkbox_false(self):
        return "<font color='#ff0000'>✖</font>  "

    checkbox_false = QtCore.Property(str, _get_checkbox_false, constant=True)

    def _get_empty(self):
        return "-"

    empty = QtCore.Property(str, _get_empty, constant=True)

    regexes = QtCore.Property(QtCore.QObject, lambda self: self._regexes, constant=True)
