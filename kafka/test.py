from confluent_kafka import KafkaAdminClient
import boto3

# Cấu hình Kafka
bootstrap_servers = 'localhost:9092'
config = {'bootstrap.servers': bootstrap_servers}

# Tạo admin client để quản lý Kafka
admin = KafkaAdminClient(config)

# Tạo các topic cần thiết
topics = ['your_topic']
admin.create_topics([{'topic': topic} for topic in topics])

# Cấu hình connector JDBC Source
#jdbc_source_config = {
#    'name': 'jdbc-source',
#    'connector.class': 'io.confluent.connect.jdbc.JdbcSourceConnector',
    # ... các cấu hình khác cho JDBC Source
#}
# JDBC Source connector
{
  "name": "sql-server-source",
  "connector.class": "io.confluent.connect.jdbc.JdbcSourceConnector",
  "tasks.max": "1",
  "connection.url": "jdbc:sqlserver://172.22.16.1:1433;;databaseName=AB;encrypt=false",
  "connection.user": "sa",
  "connection.password": "123456",
  "table.whitelist": "Customer",
  "mode": "bulk",
  "topic.prefix": "db.Customer",
  "key.converter": "org.apache.kafka.connect.json.JsonConverter",
  "value.converter": "org.apache.kafka.connect.json.JsonConverter"
}

# Cấu hình connector S3 Sink
# s3_sink_config = {
#     'name': 's3-sink',
#     'connector.class': 'io.confluent.connect.s3.S3SinkConnector',
#     # ... các cấu hình khác cho S3 Sink
# }

{
  "name": "s3-sink",
  "connector.class": "io.confluent.connect.s3.S3SinkConnector",
  "tasks.max": "1",
  "bucket.name": "kafka",
  "path.format": "data/${topic}/${2024}/${10}/${28}/${08}/${00}/${00}/",
  "format.class": "io.confluent.connect.s3.format.json.JsonFormatter"
}

# Khởi động các connector
def start_connector(config):
    admin.create_configs([config])

start_connector(jdbc_source_config)
start_connector(s3_sink_config)