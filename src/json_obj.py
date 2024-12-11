class obj[A]:
    def __init__(self, **kwargs: A):
        self.__dict__.update(kwargs)
        self.items_dict: dict[str, A] = {}
        self._iter_keys = None  # Initialize for iteration
        self.__refresh__()

    def __refresh__(self):
        if len(self.items_dict) == len(self.__dict__) - 2:
            self.items_dict = self.__dict__.copy()
            del self.items_dict["items_dict"]
            del self.items_dict["_iter_keys"]

    def __repr__(self):
        self.__refresh__()
        return str(self.items_dict)

    def __iter__(self):
        self.__refresh__()
        self._iter_keys = iter(self.items_dict.items())
        return self

    def __next__(self):
        if self._iter_keys is None:
            raise StopIteration
        try:
            return next(self._iter_keys)
        except StopIteration:
            self._iter_keys = None
            raise

    def update(self, other_obj: "obj"):
        self.__refresh__()
        self.items_dict.update(other_obj.items_dict)
