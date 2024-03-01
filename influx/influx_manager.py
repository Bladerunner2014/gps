from influxdb import InfluxDBClient
import logging
from dotenv import dotenv_values


class influx:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.config = dotenv_values(".env")
        # self.key_prefix = key_prefix
        self.inf = None
        self.connect()

    def __call__(self, *args, **kwargs):
        return self.inf

    def connect(self):
        try:
            self.inf = InfluxDBClient(host=self.config['localhost'], port=self.config['INFLUXDB_PORT'],
                                      database=self.config['INFLUXDB_DATABASE'])
            self.inf.create_database(self.config['INFLUXDB_DATABASE'])


        except Exception as error:
            # self.logger.error(ErrorMessage.REDIS_CONNECTION)
            # self.logger.error(error)
            raise Exception
