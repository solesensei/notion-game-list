import typing as tp


class BaseModel:

    @classmethod
    def load(cls, d: tp.Optional[dict]):
        if d is None:
            return None
        return cls(**d)
