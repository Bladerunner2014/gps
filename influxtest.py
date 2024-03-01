import influxdb_client, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
#
# token = os.environ.get("INFLUXDB_TOKEN")
org = "linkargroup"
url = "http://localhost:8086"

write_client = influxdb_client.InfluxDBClient(url=url, token="p1iXF54Gw_h7_GQBwas1i2FzSncgVC_8l_UOr9o492EjJziMJuu1kxEDiBt1Iuqahh2npTrNsMELxObqRYcgyg==", org=org)

bucket = "lin"

# write_api = write_client.write_api(write_options=SYNCHRONOUS)
#
# for value in range(5):
#     point = (
#         Point("measurement1")
#         .tag("tagname1", "tagvalue1")
#         .field("field1", value)
#     )
#     write_api.write(bucket=bucket, org="linkargroup", record=point)
#     time.sleep(1)  # separate points by 1 second
query_api = write_client.query_api()

query = """from(bucket: "lin")
 |> range(start: -10m)
 |> filter(fn: (r) => r._measurement == "measurement1")"""
tables = query_api.query(query, org="linkargroup")

for table in tables:
  for record in table.records:
    print(record)
