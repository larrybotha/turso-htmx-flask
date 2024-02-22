from flask import render_template
from flask_assets import Bundle, Environment

from .config import config
from .route_handlers.seed import seed_factory

assets = Environment(config.app)
css = Bundle("./styles/main.css", output="dist/main.css")
js = Bundle("./scripts/*.js", output="dist/main.js")

assets.register("css", css)
assets.register("js", js)
css.build()
js.build()


app = config.app

app.route("/seed")(seed_factory(config.db_engine))


@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run()
