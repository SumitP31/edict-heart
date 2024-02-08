from pydantic import BaseModel


class ConfigModel(BaseModel):
    serial_port: str
    output_folder: str
    baud_rate: int
