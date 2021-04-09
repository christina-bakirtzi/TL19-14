from app import create_app
from app.models import db

app = create_app()

with app.app_context():
    db.create_all()
    db.session.commit()

if __name__ == "__main__":
    app.run(host='127.0.0.1', debug=True, port=8765, ssl_context='adhoc')