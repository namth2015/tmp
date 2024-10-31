from pyspark.sql import SparkSessionn


# Tạo một SparkSession
spark = SparkSession.builder \
    .appName("SparkMinIOExample") \
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
    .config("spark.hadoop.fs.s3a.access.key", "minio") \
    .config("spark.hadoop.fs.s3a.secret.key", "minio123") \
    .getOrCreate()   


# Đọc dữ liệu từ MinIO
df = spark.read.format("parquet") \
    .load("s3a://my-bucket/my-data")

# Chạy một số phép toán trên DataFrame
result = df.groupBy("column1").count()

# Cấu hình thông tin kết nối với SQL Server
jdbc_url = "jdbc:sqlserver://172.22.16.1:1433;databaseName=MinIO;encrypt=false"
jdbc_driver = "com.microsoft.sqlserver.jdbc.SQLServerDriver"
properties = {
    "user": "sa",
    "password": "123456"
}

# Ghi dữ liệu vào SQL Server
result.write \
    df.write.mode("append")  # Hoặc "overwrite" tùy theo yêu cầu
    .jdbc("jdbc:sqlserver://172.22.16.1:1433;databaseName=MinIO;encrypt=false", "customer_table", properties )