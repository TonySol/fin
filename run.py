from app import start_app
from config import Config, Development

app = start_app(Development)

if __name__ == "__main__":
    app.run()