import requests


def main():
    res = requests.get("http://localhost:9000/api/v1/refresh/")

    if res.status_code == 200:
        print("Success")


if __name__ == "__main__":
    main()
