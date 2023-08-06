from enum import Enum

class GeneralEnum(Enum):
    
    __aliases__ = {
    }

    @classmethod
    def on_parse_exception(cls, expr:str):
        options = cls.get_members()
        raise RuntimeError(f"invalid option \"{expr}\" for the enum class \"{cls.__name__}\" "
                           f"(allowed options: {', '.join(options)})")
    
    @classmethod
    def parse(cls, expr:str):
        if isinstance(expr, cls):
            return expr
        elif isinstance(expr, int):
            return cls(expr)
        _expr = expr.strip().upper()
        if _expr in cls.__members__:
            return cls[_expr]
        elif _expr in cls.__aliases__:
            return cls(cls.__aliases__[_expr])
        else:
            cls.on_parse_exception(expr)
            
    @classmethod
    def get_members(cls):
        return [i.lower() for i in cls.__members__]
    
class DescriptiveEnum(GeneralEnum):
    
    def __new__(cls, value:int, description:str=""):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.description = description
        return obj

    @classmethod
    def on_parse_exception(cls, expr:str):
        enum_descriptions = "".join([f"    {key.lower()} - {val.description}\n" \
                                     for key, val in cls.__members__.items()])
        raise RuntimeError(f"invalid option \"{expr}\" for the enum class \"{cls.__name__}\"\n"
                           f"  Allowed options:\n{enum_descriptions}")