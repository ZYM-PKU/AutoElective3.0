#本文件定义识别验证码可能用到的常量

from enum import Enum

#定义验证码字符全集
CAPTCHA_LABELS = '2345678abcdefghklmnpqrstuvwxy'
CAPTCHA_SIZE = 52
MAX_EMAIL = 100 #最多邮件发送数

class SR(Enum):  # 声音提醒
    NONE = 0
    ANYTIME = 1
    APPROPRIATE = 2


class LM(Enum):  # 登录方式
    PORTAL = 0
    ELECTIVE = 1


class IM(Enum):  # ICR识别方式
    CNN = 0
    OCR = 1


class ERROR(Enum):  # 错误信息
    EMAIL_ERROR = 0
    DRIVER_ERROR = 1
    INTERNET_ERROR = 2
    REFRESH_ERROR = 3
    VALID_CODE_ERROR = 4
    PASSWORD_ERROR = 5
    EMPTY_ERROR = 6


class STATE(Enum):  # 运行状态
    LOADING = 0
    INITIALIZING = 1
    CONNECTING = 2
    LOGINING=3
    JUMPING=4
    EXAMINING = 5
    REFRESHING = 6
    SNATCHING = 7
    ERROR = 8
    RESTARTING = 9
    STOPPED = 10

class DRIVER(Enum): #驱动选择
    CHROME = 0
    EDGE = 1
    FIREFOX = 2
    IE = 3

