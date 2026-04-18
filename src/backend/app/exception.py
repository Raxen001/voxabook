class NotFoundError(Exception):
    entity: str

    def __init__(self, entity: str):
        self.entity = entity
        super().__init__(f"{entity} not found")


class AlreadyExistsError(Exception):
    entity: str

    def __init__(self, entity: str):
        self.entity = entity
        super().__init__(f"{entity} already exists")


class UpdateFailedError(Exception):
    entity: str

    def __init__(self, entity: str):
        self.entity = entity
        super().__init__(f"{entity} failed update")
