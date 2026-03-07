from TestUrl.base import TestUrl


app = TestUrl()
app.URL = "https://api.restful-api.dev/objects"


if __name__ == "__main__":
    app.get_request_url(1)