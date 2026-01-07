def get_or_create_user(db, user_id):
    user_ref = db.collection("users").document(user_id)
    user_doc = user_ref.get()

    if not user_doc.exists:
        user_ref.set({
            "resume_count": 0
        })

    return user_ref
