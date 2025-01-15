# Dictionary to store file info
file_info = {}

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    """
    Let users upload files.
    """
    # Make an ID for the file
    file_id = str(uuid4())

    # Check if it is an image
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only image files are allowed.")

    # Save the file in the uploads folder
    file_path = upload_folder / f"{file_id}_{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Save info about the file
    file_info[file_id] = {"filename": file.filename, "status": "uploaded"}

    return {"file_id": file_id, "filename": file.filename}

@app.get("/status/{file_id}/")
def get_status(file_id: str):
    """
    Check if a file was uploaded.
    """
    if file_id not in file_info:
        raise HTTPException(status_code=404, detail="File not found.")

    return file_info[file_id]

@app.get("/files/{file_id}/")
def get_file(file_id: str):
    """
    Download a file by its ID.
    """
    if file_id not in file_info:
        raise HTTPException(status_code=404, detail="File not found.")

    file_path = upload_folder / f"{file_id}_{file_info[file_id]['filename']}"
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found on disk.")

    return FileResponse(file_path)

if name == "main":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
