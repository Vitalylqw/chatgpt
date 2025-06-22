import base64
import os
from fastapi import FastAPI, UploadFile, File
import openai
from pdfminer.high_level import extract_text

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

app = FastAPI(title="Document Parser")

SYSTEM_PROMPT = (
    "You are an assistant that extracts structured data from financial documents. "
    "Return a JSON object with consistent keys. Use empty strings for missing values."
)

async def parse_with_text(text: str) -> str:
    response = openai.ChatCompletion.create(
        model="gpt-4-1106-preview",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text},
        ],
        max_tokens=1024,
    )
    return response.choices[0].message["content"].strip()

async def parse_with_image(content: bytes, content_type: str) -> str:
    b64 = base64.b64encode(content).decode("utf-8")
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Extract the data from this document."},
                {"type": "image_url", "image_url": f"data:{content_type};base64,{b64}"},
            ],
        },
    ]
    response = openai.ChatCompletion.create(
        model="gpt-4-vision-preview",
        messages=messages,
        max_tokens=1024,
    )
    return response.choices[0].message["content"].strip()

@app.post("/parse")
async def parse(file: UploadFile = File(...)):
    data = await file.read()
    if file.content_type == "application/pdf":
        from io import BytesIO
        text = extract_text(BytesIO(data))
        result = await parse_with_text(text)
    elif file.content_type and file.content_type.startswith("image/"):
        result = await parse_with_image(data, file.content_type)
    else:
        return {"error": "Unsupported file type"}
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
