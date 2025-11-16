"""
Masterpost.io Backend API - Qwen Only
Serverless para Vercel
"""

from fastapi import FastAPI, File, UploadFile, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
import os
import httpx
import base64
from typing import Optional, List
from io import BytesIO
import uuid

# ============================================================
# CONFIGURACIÓN
# ============================================================

app = FastAPI(title="Masterpost API", version="3.0")

# CORS - permitir frontend de Netlify
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://masterpost.io",
        "https://www.masterpost.io",
        "https://masterpost-io.netlify.app",
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
# FUNCIONES AUXILIARES
# ============================================================

async def call_qwen_api(image_bytes: bytes, pipeline: str = "amazon") -> bytes:
    """
    Procesar imagen con Qwen VL API

    Returns: bytes de la imagen procesada
    """

    # Prompts optimizados por marketplace
    prompts = {
        "amazon": """Remove the background completely from this product image and replace it with pure white (RGB 255, 255, 255).
Keep ONLY the main product, remove everything else.
Preserve all product details with maximum precision.
Ensure the product covers exactly 85% of the image area.
Remove ALL shadows, reflections, and background elements.""",

        "ebay": """Remove the background completely and replace with pure white (RGB 255, 255, 255).
Preserve MAXIMUM detail quality for zoom inspection.
Keep all fine details: textures, engravings, small text.
Remove all background shadows and elements.""",

        "instagram": """Remove the background completely and replace with pure white (RGB 255, 255, 255).
Create a visually appealing, social-media ready image.
Enhance colors while maintaining natural look.
Remove all background elements."""
    }

    prompt = prompts.get(pipeline, prompts["amazon"])

    # Encode imagen a base64
    image_b64 = base64.b64encode(image_bytes).decode('utf-8')

    # Configuración Qwen API
    api_key = os.getenv("DASHSCOPE_API_KEY")

    if not api_key:
        raise HTTPException(500, "Qwen API key not configured")

    url = "https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "qwen-vl-max",
        "input": {
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"image": f"data:image/jpeg;base64,{image_b64}"},
                        {"text": prompt}
                    ]
                }
            ]
        },
        "parameters": {
            "result_format": "message"
        }
    }

    print(f"🔄 Calling Qwen API for pipeline: {pipeline}")

    # Llamar a Qwen API
    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            response = await client.post(url, json=payload, headers=headers)

            if response.status_code != 200:
                print(f"❌ Qwen API error: {response.text}")
                raise HTTPException(500, f"Qwen API error: {response.text}")

            data = response.json()

            # Extraer URL de imagen procesada
            try:
                image_url = data['output']['choices'][0]['message']['content'][0]['image']
                print(f"✅ Qwen returned image URL: {image_url[:50]}...")
            except (KeyError, IndexError) as e:
                print(f"❌ Invalid Qwen response structure: {data}")
                raise HTTPException(500, f"Invalid Qwen API response")

            # Descargar imagen procesada
            print(f"📥 Downloading processed image...")
            img_response = await client.get(image_url)

            if img_response.status_code != 200:
                raise HTTPException(500, "Failed to download processed image")

            print(f"✅ Image downloaded successfully ({len(img_response.content)} bytes)")
            return img_response.content

        except httpx.TimeoutException:
            raise HTTPException(504, "Qwen API timeout")
        except Exception as e:
            print(f"❌ Exception calling Qwen: {str(e)}")
            raise HTTPException(500, f"Processing error: {str(e)}")


# ============================================================
# ENDPOINTS
# ============================================================

@app.get("/")
async def root():
    """Health check raíz"""
    return {
        "status": "ok",
        "service": "Masterpost API - Qwen Only",
        "version": "3.0"
    }


@app.get("/api/health")
async def health():
    """Health check detallado"""
    return {
        "status": "healthy",
        "qwen_configured": bool(os.getenv("DASHSCOPE_API_KEY")),
        "environment": os.getenv("VERCEL_ENV", "development")
    }


@app.post("/api/v1/upload")
async def upload_endpoint(
    files: List[UploadFile] = File(...),
    authorization: Optional[str] = Header(None)
):
    """
    Endpoint de upload (compatibilidad con frontend)

    En realidad no guardamos nada, solo retornamos job_id dummy
    El procesamiento real es síncrono en /api/v1/process
    """

    print(f"📤 Upload endpoint called with {len(files)} file(s)")

    # Generar job_id dummy para compatibilidad
    job_id = str(uuid.uuid4())

    return JSONResponse({
        "success": True,
        "job_id": job_id,
        "message": f"Uploaded {len(files)} files",
        "files_uploaded": len(files),
        "images_found": len(files)
    })


@app.post("/api/v1/process")
async def process_endpoint(
    file: UploadFile = File(...),
    pipeline: str = "amazon",
    authorization: Optional[str] = Header(None)
):
    """
    ENDPOINT PRINCIPAL - Procesar imagen con Qwen

    Este es el endpoint REAL que procesa con Qwen API
    Retorna la imagen procesada directamente
    """

    print(f"🎯 Process endpoint called")
    print(f"   Pipeline: {pipeline}")
    print(f"   File: {file.filename} ({file.content_type})")

    try:
        # Leer imagen
        image_bytes = await file.read()
        print(f"   File size: {len(image_bytes)} bytes")

        # Procesar con Qwen
        processed_bytes = await call_qwen_api(image_bytes, pipeline)

        # Devolver imagen procesada
        return StreamingResponse(
            BytesIO(processed_bytes),
            media_type="image/png",
            headers={
                "Content-Disposition": f"attachment; filename=processed_{file.filename}",
                "X-Credits-Used": "3",
                "X-Processing-Method": "qwen-api",
                "Access-Control-Expose-Headers": "Content-Disposition, X-Credits-Used, X-Processing-Method"
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Processing error: {str(e)}")
        raise HTTPException(500, f"Processing error: {str(e)}")


@app.get("/api/v1/status/{job_id}")
async def status_endpoint(job_id: str):
    """
    Endpoint de status (compatibilidad)

    Como el procesamiento es síncrono, siempre retorna completed
    """

    return JSONResponse({
        "status": "completed",
        "job_id": job_id,
        "progress": 100,
        "images_processed": 1
    })


# ============================================================
# VERCEL HANDLER
# ============================================================

# Esto es necesario para Vercel
handler = app


# Para testing local
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
