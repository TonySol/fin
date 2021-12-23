from app import start_app
from config import Config, Development

application = start_app(Development)

if __name__ == "__main__":
    application.run()