from enum import Enum

# 성별 Enum
class Gender(str, Enum):
    male = "남"
    female = "여"

# 통신사 Enum
class Telecom(str, Enum):
    SKT = "SKT"
    KT = "KT"
    LGU = "LGU+"

