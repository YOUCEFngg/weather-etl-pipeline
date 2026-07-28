import json
import os
from datetime import datetime
from io import BytesIO
from minio import Minio


def save_to_bronze(records):
    """Save raw weather data to MinIO Bronze layer."""
    
    client = Minio(
        os.getenv("MINIO_ENDPOINT", "minio:9000"),
        access_key=os.getenv("MINIO_ACCESS_KEY", "minioadmin"),
        secret_key=os.getenv("MINIO_SECRET_KEY", "minioadmin"),
        secure=False
    )
    
    bucket = "bronze"
    
    # Create bucket if it doesn't exist
    if not client.bucket_exists(bucket):
        client.make_bucket(bucket)
        print(f"Created bucket: {bucket}")
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    object_name = f"weather/raw_{timestamp}.json"
    
    # Convert records to JSON bytes
    json_data = json.dumps(records, indent=2).encode("utf-8")
    data_stream = BytesIO(json_data)
    
    # Upload to MinIO
    client.put_object(
        bucket,
        object_name,
        data_stream,
        length=len(json_data),
        content_type="application/json"
    )
    
    print(f"Bronze: Saved raw data to minio://{bucket}/{object_name}")
    print(f"         Size: {len(json_data)} bytes")
