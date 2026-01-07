from firebase_admin import credentials, firestore, initialize_app, _apps
import os

def init_firebase():
    if not _apps:
        cred = credentials.Certificate(
            os.getenv("FIREBASE_SERVICE_ACCOUNT")
        )
        initialize_app(cred)

    return firestore.client()
