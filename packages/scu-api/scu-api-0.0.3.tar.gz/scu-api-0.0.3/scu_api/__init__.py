# -*- coding:utf-8 -*-

from .u_student import U_Student
from .constant import StudentType


def get_student(stutype: StudentType=StudentType.UNDERGRADUATE) -> U_Student:
    if stutype == StudentType.UNDERGRADUATE:
        return U_Student()
    else:
        return None
