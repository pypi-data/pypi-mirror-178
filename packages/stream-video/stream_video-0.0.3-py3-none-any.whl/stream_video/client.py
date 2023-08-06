import os
from typing import Any, Dict

import jwt
from google.protobuf.json_format import MessageToDict
from twirp.context import Context  # type: ignore

from .gen.video.coordinator.server_v1_rpc import server_rpc_pb2, server_rpc_twirp

try:
    from importlib import metadata  # type: ignore
except ImportError:  # for Python<3.8
    import importlib_metadata as metadata  # type: ignore

__version__ = metadata.version("stream_video")


def get_user_agent() -> str:
    return f"stream-python-client-{__version__}"


def get_default_header() -> Dict[str, str]:
    return {
        "Content-type": "application/json",
        "X-Stream-Client": get_user_agent(),
    }


class StreamVideo:
    def __init__(
        self, api_key: str, api_secret: str, timeout: float = 6.0, **options: Any
    ):
        self.base_url = "http://localhost:26991"
        if options.get("base_url"):
            self.base_url = options["base_url"]
        elif os.getenv("STREAM_VIDEO_URL"):
            self.base_url = os.environ["STREAM_VIDEO_URL"]

        self.timeout = timeout
        if os.getenv("STREAM_VIDEO_TIMEOUT"):
            self.timeout = float(os.environ["STREAM_VIDEO_TIMEOUT"])

        self.twirp = server_rpc_twirp.ServerRPCClient(
            address=self.base_url,
            timeout=self.timeout,
        )

        self.api_key = api_key
        self.api_secret = api_secret
        self.auth_token = jwt.encode(
            {"server": True}, self.api_secret, algorithm="HS256"
        )
        self.ctx = Context(
            headers={
                **get_default_header(),
                "api_key": self.api_key,
                "authorization": self.auth_token,
            }
        )

        self.options = options

    def get_app(self) -> Dict:
        return MessageToDict(
            self.twirp.GetApp(
                ctx=self.ctx,
                server_path_prefix="/rpc",
                request=server_rpc_pb2.GetAppRequest(),
            )
        )

    def query_session_timeline_events(self, session_id: str) -> Dict:
        return MessageToDict(
            self.twirp.QuerySessionTimelineEvents(
                ctx=self.ctx,
                server_path_prefix="/rpc",
                request=server_rpc_pb2.QuerySessionTimelineEventsRequest(
                    session_id=session_id
                ),
            )
        )

    def query_sessions(self) -> Dict:
        return MessageToDict(
            self.twirp.QuerySessions(
                ctx=self.ctx,
                server_path_prefix="/rpc",
                request=server_rpc_pb2.QuerySessionsRequest(),
            )
        )
