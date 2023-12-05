from app import init_app
import os

app = init_app()

if __name__ == "__main__":
    app.run(
        host=os.environ['HOST'],
        port=os.environ['PORT']
    )
