from uuid import UUID
class JobCreate:
    pipeline: str
    input: dict


class JobResponse:
    id:UUID
    status:str
    output:dict|None