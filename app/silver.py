import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_unixtime, lit, current_timestamp, when
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, IntegerType, LongType


def get_spark_session(app_name="WeatherSilver"):
    """Create Spark session with Delta Lake enabled."""
    spark = (
        SparkSession.builder
        .appName(app_name)
        .master("local[*]")
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config(
            "spark.sql.catalog.spark_catalog",
            "org.apache.spark.sql.delta.catalog.DeltaCatalog",
        )
        .config("spark.sql.adaptive.enabled", "true")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("WARN")
    return spark


def bronze_to_silver(records):
    """
    Transform raw Bronze records into clean Silver Delta Lake table.
    
    What we clean:
    - Proper data types (timestamp, double, int)
    - Add derived columns (temp_category, humidity_level)
    - Add metadata (processed_at, layer)
    - Handle nulls gracefully
    """
    print("=" * 50)
    print(" SILVER LAYER: Spark + Delta Lake Processing")
    print("=" * 50)
    
    spark = get_spark_session()
    
    # Create DataFrame from raw Bronze records
    df = spark.createDataFrame(records)
    print(f"   Input records: {df.count()}")
    
    # Show raw schema
    print("\n Raw Bronze schema:")
    df.printSchema()
    
    # ===== TRANSFORMATIONS =====
    
    # 1. Convert timestamp from Unix seconds to proper timestamp
    df = df.withColumn("timestamp", from_unixtime(col("timestamp")).cast("timestamp"))
    
    # 2. Cast numeric columns to proper types
    df = df.withColumn("temperature", col("temperature").cast("double"))
    df = df.withColumn("humidity", col("humidity").cast("integer"))
    
    # 3. Add derived column: temperature category
    df = df.withColumn(
        "temp_category",
        when(col("temperature") < 10, "cold")
        .when(col("temperature") < 25, "mild")
        .otherwise("hot")
    )
    
    # 4. Add derived column: humidity level
    df = df.withColumn(
        "humidity_level",
        when(col("humidity") < 30, "dry")
        .when(col("humidity") < 60, "comfortable")
        .otherwise("humid")
    )
    
    # 5. Add metadata columns
    df = df.withColumn("processed_at", current_timestamp())
    df = df.withColumn("layer", lit("silver"))
    
    # 6. Standardize text columns (lowercase, trim)
    df = df.withColumn("city", col("city").cast("string"))
    df = df.withColumn("weather_description", col("weather_description").cast("string"))
    
    # Show cleaned sample
    print("\nCleaned Silver sample:")
    df.select("city", "temperature", "temp_category", "humidity", "humidity_level", "timestamp").show(truncate=False)
    
    # ===== WRITE DELTA LAKE (SILVER) =====
    silver_path = "/app/data/silver/weather"
    
    print(f"\n Writing Silver Delta table to: {silver_path}")
    
    df.write.format("delta").mode("overwrite").option("overwriteSchema", "true").save(silver_path)
    
    print(f"    Silver table created: {df.count()} records")
    
    # ===== DELTA LAKE FEATURES DEMO =====
    print("\n⏰ Delta Lake History:")
    history = spark.sql(f"DESCRIBE HISTORY delta.`{silver_path}`")
    history.select("version", "timestamp", "operation").show(truncate=False)
    
    print("\n Silver Table Schema:")
    spark.read.format("delta").load(silver_path).printSchema()
    
    print("\n" + "=" * 50)
    print("Silver layer complete!")
    print("=" * 50)
    
    spark.stop()
    return silver_path
