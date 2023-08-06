# -*- coding: utf-8 -*-

from enum import Enum, auto
from typing import Any, Union
from collections import UserDict

#  Start-> INIT -> OFFLINE -> ONLINE
#                    |    <-     |

class ClientStatus(Enum):
    INIT = auto()      # init state
    OFFLINE = auto()   # set baseinfo and without login
    # after login, MAYBE cache outdate in SCU website, need get_status() to check
    ONLINE = auto()

class RespCode(Enum):
    OK = 0
    ERROR = 1
    WARNING = 2
    UNKNOWN = 3

class StudentType(Enum):
    UNDERGRADUATE = auto()
    GRADUATE = auto()

class RespType(UserDict):
    def __init__(self, status: RespCode, result: Any):
        '''
        @brief 标准API返回类型
        @param status(RespCode) 状态码
        @param result(Any) 返回的数据
        '''
        self.data = {
            'status': status,
            'result': result
        }
    
    def is_ok(self) -> bool:
        return self.data['status'] == RespCode.OK

    def __missing__(self, _key: str):
        if isinstance(_key, str):
            raise KeyError(_key)
        return self[_key]
    
    def __getattr__(self, _key: str) -> Union[RespCode, Any]:
        return self.data[_key]
