from datetime import datetime
import serial
import pandas as pd
import structlog
from datetime import datetime

import typer

from src.models.config import ConfigModel
from src.models.data import HeartData

# Initialize Structlog
structlog.configure(logger_factory=structlog.PrintLoggerFactory())


class DataCollector:
    def __init__(self, config: ConfigModel):
        self.config = config
        self.logger = structlog.get_logger()
        self.data = pd.DataFrame(columns=["Timestamp", "Value"])
        self.start_time = None

    def collect_data(self) -> None:
        """
        Collect data from serial port and store it in a Pandas DataFrame.
        """
        self.logger.info(
            "Starting data collection",
            serial_port=self.config.serial_port,
            output_file=self.config.output_folder,
        )
        self.start_time = datetime.now()

        with serial.Serial(self.config.serial_port, self.config.baud_rate) as ser:
            while True:
                data = ser.readline().strip().decode().split(" ")
                data = HeartData(timestamp=data[0], value=data[1])
                self.data.append(data.model_dump())
                self.logger("info", data)

    def write_to_csv(self) -> None:
        """
        Write DataFrame to CSV file.
        """
        try:
            self.logger.info("Writing to csv file")
            self.data.to_csv(
                f"{self.config.output_folder}/{datetime.now().strftime('%Y%m%D_%H%M%S')}_data.csv",
                index=False,
            )
            self.logger.info("Wrote data to csv file")
        except Exception as e:
            self.logger.error("Error writing to CSV", error=str(e))
