from enum import Enum as PyEnum

# 성별 Enum
class Gender(str, PyEnum):
    male = "남"
    female = "여"

# 통신사 Enum
class Telecom(str, PyEnum):
    SKT = "SKT"
    KT = "KT"
    LGU = "LGU+"