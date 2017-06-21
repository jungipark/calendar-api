# coding=utf-8
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app.extensions import db
from app import create_app

app = create_app(config_name='default')
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


@manager.command
def dev_run():
    """
    run app
    '앱을 실행시킴'
    """
    app.run(host='0.0.0.0', debug=True)


if __name__ == "__main__":
    manager.run()
