from website import create_app
from website.dm import start_twitter_listener

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
    start_twitter_listener()
