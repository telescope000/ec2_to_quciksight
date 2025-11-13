CREATE EXTERNAL TABLE starshop.orders (
  datetime string,
  product string,
  region string,
  qty int,
  price double
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
  "skip.header.line.count" = "1"
)
LOCATION 's3://starshop-orders5/';
