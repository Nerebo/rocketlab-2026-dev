from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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
    allow_origins=["http://localhost:5173"],  # Em produção, especifique os domínios permitidos
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

@app.get("/", tags=["Health"])
def health_check():
    return {"status": "ok", "message": "API rodando com sucesso!"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
