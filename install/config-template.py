import os

flask_secret_key='$FlaskSecretKey'
notasi_password='$NotasiPassword'
sqlalchemy_secret_key='$SQLAlchemySecretKey'
storage_location='$StorageLocation'
debug = False
saml_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'saml')
login_default = 'local'
