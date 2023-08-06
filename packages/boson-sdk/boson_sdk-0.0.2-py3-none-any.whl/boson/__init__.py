import importlib.metadata

from boson.base import BaseProvider
from boson.boson_v1_pb2 import LandingPageRequest, LandingPageResponse, ConformanceRequest, ConformanceResponse, \
    CollectionsRequest, CollectionsResponse, CollectionRequest, CollectionResponse, CollectionItemsRequest, \
    CollectionItemsResponse, CollectionItemRequest, CollectionItemResponse, SearchRequest, SearchResponse, \
    WarpRequest, RasterResponse
from boson.features_pb2 import CollectionMsg, FeatureMsg, FeatureCollectionMsg, LinkMsg


__version__ = importlib.metadata.version("boson-sdk")
__all__ = [
    "BaseProvider",
    "LandingPageRequest",
    "LandingPageResponse",
    "ConformanceRequest",
    "ConformanceResponse",
    "CollectionsRequest",
    "CollectionsResponse",
    "CollectionRequest",
    "CollectionResponse",
    "CollectionItemsRequest",
    "CollectionItemsResponse",
    "CollectionItemRequest",
    "CollectionItemResponse",
    "SearchRequest",
    "SearchResponse",
    "WarpRequest",
    "RasterResponse",
    "CollectionMsg",
    "FeatureMsg",
    "FeatureCollectionMsg",
    "LinkMsg",
    "search_request_to_kwargs",
    "feature_collection_to_proto",
    "warp_request_to_kwargs",
    "numpy_to_raster_response"
]
