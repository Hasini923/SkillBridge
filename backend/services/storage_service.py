def upload_resume(bucket, user_id, file):
    blob = bucket.blob(f"resumes/{user_id}/{file.filename}")
    blob.upload_from_file(file)
    return blob.name
