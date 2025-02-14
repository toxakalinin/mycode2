import argparse
from database import Session, AuthorizedUser, Base
from sqlalchemy import create_engine

def init_db():
    engine = create_engine(os.getenv("DATABASE_URL"))
    Base.metadata.create_all(engine)
    print("Database initialized")

def add_user():
    parser = argparse.ArgumentParser(description='Add authorized user')
    parser.add_argument('telegram_id', type=int, help='Telegram user ID')
    parser.add_argument('username', type=str, help='Username for login')
    args = parser.parse_args()

    try:
        with Session() as db:
            if db.query(AuthorizedUser).filter_by(telegram_id=args.telegram_id).first():
                print("Error: User already exists")
                return

            user = AuthorizedUser(
                telegram_id=args.telegram_id,
                username=args.username
            )
            db.add(user)
            db.commit()
            print(f"User {args.username} added successfully")

    except Exception as e:
        print(f"Error adding user: {e}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Database management')
    subparsers = parser.add_subparsers()

    init_parser = subparsers.add_parser('init_db')
    init_parser.set_defaults(func=init_db)

    add_parser = subparsers.add_parser('add_user')
    add_parser.set_defaults(func=add_user)

    args = parser.parse_args()
    args.func()
