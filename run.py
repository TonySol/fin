"""Simple app starter outside of the web app package.

Use it to change config for development/production or start web server.
"""

from app import start_app
from config import Config, Development

app = start_app(Development)

if __name__ == "__main__":
    app.run()