class Comparable:
    def __init__(self, id_value, class_type):
        self.__id = id_value
        self.__type = class_type
        assert issubclass(class_type, Comparable)

    def __eq__(self, other):
        return isinstance(other, self.__type) and other.__id == self.__id

    def __hash__(self) -> int:
        return hash(self.__id)
