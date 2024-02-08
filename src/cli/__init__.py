import typer
import yaml

from src.data.collector import DataCollector
from src.models.config import ConfigModel

app = typer.Typer()


def read_config(config_file: str) -> ConfigModel:
    """
    Read configuration from YAML file.

    Args:
        config_file: Path to the YAML configuration file.

    Returns:
        Dictionary containing the configuration.
    """
    with open(config_file, "r") as f:
        config = ConfigModel(**yaml.safe_load(f))
    return config


@app.command()
def start(
    config_file: str = typer.Argument(default="./src/config/config.yaml"),
) -> None:
    """
    Start collecting data from serial port.

    Args:
        config_file: Path to the YAML configuration file.
        serial_port: The serial port name (e.g., COM1 or /dev/ttyUSB0).
        output_file: The name of the CSV file to store the data (default is data.csv).
        baud_rate: The baud rate for serial communication (default is 9600).
    """
    config = read_config(config_file)
    collector = DataCollector(config)
    collector.collect_data()


if __name__ == "__main__":
    app()
