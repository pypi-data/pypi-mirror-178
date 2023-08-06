from typing import Optional, Any
from types import FunctionType
from fastapi import FastAPI, APIRouter, Request, Response, HTTPException
from boson import BaseProvider, LandingPageRequest, ConformanceRequest, CollectionsRequest, CollectionRequest, \
    WarpRequest, SearchRequest

__all__ = ["serve"]


class BosonProvider(BaseProvider):
    def __init__(
                 self,
                 title: str = 'remote',
                 description: str = 'a remote Boson provider',
                 license: str = '(unknown)',
                 extent: Optional[dict] = None,
                 search_func: Optional[FunctionType] = None,
                 warp_func: Optional[FunctionType] = None) -> None:

        super().__init__(title, description, license, extent, search_func, warp_func)

        self.router = APIRouter()
        self.router.add_api_route("/", self.landing_page, methods=['POST'])
        self.router.add_api_route("/conformance", self.conformance, methods=['POST'])
        self.router.add_api_route("/collections", self.collections, methods=['POST'])
        self.router.add_api_route("/collection", self.collection, methods=['POST'])
        self.router.add_api_route("/collection_items", self.collection_items, methods=['POST'])
        self.router.add_api_route("/collection_item", self.collection_item, methods=['POST'])
        self.router.add_api_route("/search", self.search, methods=['POST'])
        self.router.add_api_route("/warp", self.warp, methods=['POST'])

    async def landing_page(self, request: Request):
        body = await request.body()

        req = LandingPageRequest()
        req.ParseFromString(body)

        resp = super().landing_page(req)
        return self.proto_response(resp)

    async def conformance(self, request: Request):
        body = await request.body()

        req = ConformanceRequest()
        req.ParseFromString(body)

        resp = super().conformance(req)
        return self.proto_response(resp)

    async def collections(self, request: Request):
        body = await request.body()

        req = CollectionsRequest()
        req.ParseFromString(body)

        resp = super().collections(req)
        return self.proto_response(resp)

    async def collection(self, request: Request):
        body = await request.body()

        req = CollectionRequest()
        req.ParseFromString(body)

        resp = super().collection(req)
        return self.proto_response(resp)

    async def collection_items(self, request: Request):
        raise HTTPException(status_code=501, detail='not implemented')

    async def collection_item(self, request: Request):
        raise HTTPException(status_code=501, detail='not implemented')

    async def warp(self, request: Request):
        body = await request.body()

        req = WarpRequest()
        req.ParseFromString(body)

        try:
            resp = super().warp(req)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f'unable to run warp function: {str(e)}')
        return self.proto_response(resp)

    async def search(self, request: Request):
        body = await request.body()

        req = SearchRequest()
        req.ParseFromString(body)

        try:
            resp = super().search(req)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f'unable to run search function: {str(e)}')

        return self.proto_response(resp)

    def proto_response(self, resp: Any) -> Response:
        return Response(
            content=resp.SerializeToString(),
            media_type="application/x-protobuf"
        )


def serve(search_func: Optional[FunctionType] = None, warp_func: Optional[FunctionType] = None, **kwargs):
    app = FastAPI()
    server = BosonProvider(warp_func=warp_func, search_func=search_func, **kwargs)
    app.include_router(server.router)
    return app
