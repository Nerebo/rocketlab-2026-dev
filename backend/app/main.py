from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
import httpx

from app.routers.vendedor_router import route as vendedor_route
from app.routers.produto_router import route as produto_route
from app.routers.pedido_routers import route as pedido_route
from app.routers.item_pedido_router import router as item_pedido_route
from app.routers.consumidor_router import route as consumidor_route
from app.routers.avaliacao_pedido_router import route as avaliacao_pedido_route

app = FastAPI(
    title="Sistema de Compras Online",
    description="API para gerenciamento de pedidos, produtos, consumidores e vendedores.",
    version="1.0.0",
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especifique os domínios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(vendedor_route)
app.include_router(produto_route)
app.include_router(pedido_route)
app.include_router(item_pedido_route)
app.include_router(consumidor_route)
app.include_router(avaliacao_pedido_route)


# Proxy de imagens para contornar CORS
@app.get("/images/proxy")
async def proxy_image(url: str = Query(..., description="URL da imagem para fazer proxy")):
    """
    Proxy de imagens para contornar restrições CORS.
    Permite que o frontend carregue imagens de terceiros diretamente via este endpoint.
    """
    try:
        # Validar URL básica
        if not url.startswith(('http://', 'https://')):
            return JSONResponse(
                status_code=400,
                content={"error": "URL inválida"}
            )

        async with httpx.AsyncClient(timeout=10.0, follow_redirects=True) as client:
            response = await client.get(url)
            response.raise_for_status()
            
            return StreamingResponse(
                iter([response.content]),
                media_type=response.headers.get("content-type", "image/jpeg"),
                headers={
                    "Cache-Control": "public, max-age=86400",
                    "Access-Control-Allow-Origin": "*"
                }
            )
    except httpx.TimeoutException:
        return JSONResponse(
            status_code=504,
            content={"error": "Timeout ao buscar imagem"}
        )
    except httpx.HTTPError as e:
        return JSONResponse(
            status_code=502,
            content={"error": f"Erro ao buscar imagem: {str(e)}"}
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Erro interno: {str(e)}"}
        )

@app.get("/", tags=["Health"])
def health_check():
    return {"status": "ok", "message": "API rodando com sucesso!"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
