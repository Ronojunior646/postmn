from flask import Flask
import sentry_sdk


sentry_sdk.init(
    dsn="https://04fce712893c9870e96943104c7869aa@o4507805055057920.ingest.us.sentry.io/4507805084090368",
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for tracing.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
)

app = Flask(__name__)

@app.route("/")
def hello_world():
    1/0  # raises an error
    return "<p>Hello, World!</p>"
        