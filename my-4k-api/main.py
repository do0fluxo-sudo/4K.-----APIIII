from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import FileResponse
import subprocess
import os
import uuid
import requests

app = FastAPI()

@app.get("/enhance")
async def enhance_image(image_url: str = Query(..., description="Image URL")):
    try:
        # Download image
        input_filename = f"{uuid.uuid4()}.jpg"
        output_dir = "results"
        os.makedirs(output_dir, exist_ok=True)
        output_filename = f"{output_dir}/{input_filename}"

        img_data = requests.get(image_url).content
        with open(input_filename, "wb") as f:
            f.write(img_data)

        # Run Real-ESRGAN (this assumes installed in your environment)
        result = subprocess.run(
            ["realesrgan-ncnn-vulkan", "-i", input_filename, "-o", output_filename],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

        if result.returncode != 0:
            raise Exception(f"Enhancement failed: {result.stderr.decode()}")

        return FileResponse(output_filename, media_type="image/jpeg")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
