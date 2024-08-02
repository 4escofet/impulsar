from app import create_app, db, bcrypt
from app.models import User

app = create_app()

with app.app_context():
    admin = User.query.filter_by(email='sostenibilidad@lomanegra.com').first()
    if admin:
        print('Admin user already exists.')
    else:
        hashed_password = bcrypt.generate_password_hash('impulsar').decode('utf-8')
        admin = User(
            organization_name='ProgramaImpulsar',
            cuit=1,
            username='Admin',
            position='Administrator',
            email='sostenibilidad@lomanegra.com',
            phone=123456789,
            importance=True,
            password=hashed_password,
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()
        print('Admin user created.')
