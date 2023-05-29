from minio import Minio
from minio.error import S3Error
#10.1.0.5 -> for api

def main():
    client = Minio("20.24.96.41:9000", access_key="rIWa7LGJRggjvhS3", secret_key="znTF7NZMQmpCglhgGmLgHUjJ9VKOeRhR", secure=False,)
    found = client.bucket_exists("dumy")
    if not found:
        client.make_bucket("dumy")
    else:
        print("Bucket 'dumy' already exists")

    client.fput_object("dumy", "898_starbucks.pdf", "C:/Users/spandey168/Desktop/work/rathyatraBackend/rathyatraBackend/static/image/facilities/foodDistribution/1.jpg",)
    print("'/Users/dghosh040/Downloads/898_starbucks.pdf' is successfully uploaded as " "object '898_starbucks.pdf' to bucket 'dumy'.")


if __name__ == "__main__":
    try:
        main()
    except S3Error as exc:
        print("error occurred.", exc)