from __future__ import annotations

import hashlib
import sys
import types
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
BACKEND = ROOT / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))


def _install_fastapi_stub() -> None:
    if "fastapi" in sys.modules:
        return
    fastapi = types.ModuleType("fastapi")

    class HTTPException(Exception):
        def __init__(self, status_code: int, detail: str | None = None):
            super().__init__(detail)
            self.status_code = status_code
            self.detail = detail

    class APIRouter:
        def __init__(self, *args: Any, **kwargs: Any):
            self.routes = []

        def include_router(self, router: Any) -> None:
            self.routes.append(router)

        def get(self, *args: Any, **kwargs: Any):
            return lambda fn: fn

        def post(self, *args: Any, **kwargs: Any):
            return lambda fn: fn

        def put(self, *args: Any, **kwargs: Any):
            return lambda fn: fn

        def patch(self, *args: Any, **kwargs: Any):
            return lambda fn: fn

        def delete(self, *args: Any, **kwargs: Any):
            return lambda fn: fn

    class FastAPI:
        def __init__(self, title: str | None = None, *args: Any, **kwargs: Any):
            self.title = title
            self.routers = []
            self.middleware = []
            self.startup_handlers = []

        def add_middleware(self, middleware: Any, **kwargs: Any) -> None:
            self.middleware.append((middleware, kwargs))

        def on_event(self, event: str):
            def decorator(fn):
                if event == "startup":
                    self.startup_handlers.append(fn)
                return fn

            return decorator

        def include_router(self, router: Any, prefix: str = "") -> None:
            self.routers.append((router, prefix))

    def Depends(dependency: Any = None) -> Any:
        return dependency

    status = types.SimpleNamespace(
        HTTP_201_CREATED=201,
        HTTP_204_NO_CONTENT=204,
        HTTP_400_BAD_REQUEST=400,
        HTTP_404_NOT_FOUND=404,
    )

    fastapi.APIRouter = APIRouter
    fastapi.Depends = Depends
    fastapi.FastAPI = FastAPI
    fastapi.HTTPException = HTTPException
    fastapi.status = status
    sys.modules["fastapi"] = fastapi

    middleware = types.ModuleType("fastapi.middleware")
    cors = types.ModuleType("fastapi.middleware.cors")

    class CORSMiddleware:
        pass

    cors.CORSMiddleware = CORSMiddleware
    sys.modules["fastapi.middleware"] = middleware
    sys.modules["fastapi.middleware.cors"] = cors


def _install_pydantic_stub() -> None:
    if "pydantic" in sys.modules:
        return
    pydantic = types.ModuleType("pydantic")

    class ConfigDict(dict):
        pass

    class BaseModel:
        model_config: dict[str, Any] = {}

        def __init__(self, **kwargs: Any):
            for key, value in kwargs.items():
                setattr(self, key, value)

        def model_dump(self) -> dict[str, Any]:
            return dict(self.__dict__)

    def Field(default: Any = ..., **kwargs: Any) -> Any:
        return None if default is ... else default

    pydantic.BaseModel = BaseModel
    pydantic.ConfigDict = ConfigDict
    pydantic.Field = Field
    sys.modules["pydantic"] = pydantic

    pydantic_settings = types.ModuleType("pydantic_settings")

    class BaseSettings(BaseModel):
        pass

    class SettingsConfigDict(dict):
        pass

    pydantic_settings.BaseSettings = BaseSettings
    pydantic_settings.SettingsConfigDict = SettingsConfigDict
    sys.modules["pydantic_settings"] = pydantic_settings


def _install_sqlalchemy_stub() -> None:
    if "sqlalchemy" in sys.modules:
        return
    sqlalchemy = types.ModuleType("sqlalchemy")
    orm = types.ModuleType("sqlalchemy.orm")
    exc = types.ModuleType("sqlalchemy.exc")

    class IntegrityError(Exception):
        pass

    class FakeColumn:
        def __eq__(self, other: Any) -> tuple[str, Any]:  # noqa: D105
            return ("eq", other)

        def desc(self) -> tuple[str, str]:
            return ("order", "desc")

        def asc(self) -> tuple[str, str]:
            return ("order", "asc")

    class Integer:
        pass

    class Text:
        pass

    class ForeignKey:
        def __init__(self, *args: Any, **kwargs: Any):
            self.args = args
            self.kwargs = kwargs

    class UniqueConstraint:
        def __init__(self, *args: Any, **kwargs: Any):
            self.args = args
            self.kwargs = kwargs

    def create_engine(*args: Any, **kwargs: Any) -> object:
        return object()

    class DeclarativeBase:
        metadata = types.SimpleNamespace(create_all=lambda bind=None: None)

        def __init_subclass__(cls, **kwargs: Any):
            return super().__init_subclass__(**kwargs)

        def __init__(self, **kwargs: Any):
            for key, value in kwargs.items():
                setattr(self, key, value)

    class Mapped:
        def __class_getitem__(cls, item: Any) -> Any:
            return Any

    def mapped_column(*args: Any, **kwargs: Any) -> FakeColumn:
        return FakeColumn()

    def relationship(*args: Any, **kwargs: Any) -> None:
        return None

    class Session:
        pass

    def sessionmaker(*args: Any, **kwargs: Any):
        class SessionLocal:
            def close(self) -> None:
                pass

        return SessionLocal

    sqlalchemy.ForeignKey = ForeignKey
    sqlalchemy.Integer = Integer
    sqlalchemy.Text = Text
    sqlalchemy.UniqueConstraint = UniqueConstraint
    sqlalchemy.create_engine = create_engine
    sqlalchemy.orm = orm
    sqlalchemy.exc = exc
    orm.DeclarativeBase = DeclarativeBase
    orm.Mapped = Mapped
    orm.Session = Session
    orm.mapped_column = mapped_column
    orm.relationship = relationship
    orm.sessionmaker = sessionmaker
    exc.IntegrityError = IntegrityError
    sys.modules["sqlalchemy"] = sqlalchemy
    sys.modules["sqlalchemy.orm"] = orm
    sys.modules["sqlalchemy.exc"] = exc


def _install_argon2_stub() -> None:
    if "argon2" in sys.modules:
        return
    argon2 = types.ModuleType("argon2")
    exceptions = types.ModuleType("argon2.exceptions")
    low_level = types.ModuleType("argon2.low_level")

    class HashingError(Exception):
        pass

    class Type:
        ID = "ID"

    def hash_secret_raw(
        secret: bytes,
        salt: bytes,
        time_cost: int,
        memory_cost: int,
        parallelism: int,
        hash_len: int,
        type: str,
    ) -> bytes:
        if hash_len < 1:
            raise HashingError("invalid hash length")
        payload = secret + salt + str((time_cost, memory_cost, parallelism, type)).encode()
        return hashlib.blake2b(payload, digest_size=hash_len).digest()

    exceptions.HashingError = HashingError
    low_level.Type = Type
    low_level.hash_secret_raw = hash_secret_raw
    sys.modules["argon2"] = argon2
    sys.modules["argon2.exceptions"] = exceptions
    sys.modules["argon2.low_level"] = low_level


_install_fastapi_stub()
_install_pydantic_stub()
_install_sqlalchemy_stub()
_install_argon2_stub()


class FakeQuery:
    def __init__(self, data: list[Any]):
        self.data = data

    def filter(self, *args: Any, **kwargs: Any) -> "FakeQuery":
        return self

    def order_by(self, *args: Any, **kwargs: Any) -> "FakeQuery":
        return self

    def all(self) -> list[Any]:
        return list(self.data)

    def one_or_none(self) -> Any | None:
        return self.data[0] if self.data else None


class FakeDB:
    def __init__(self):
        self.data: dict[type, list[Any]] = {}
        self.added: list[Any] = []
        self.deleted: list[Any] = []
        self.commits = 0
        self.rollbacks = 0
        self.refreshed: list[Any] = []

    def seed(self, model: type, rows: list[Any]) -> None:
        self.data[model] = rows

    def query(self, model: type) -> FakeQuery:
        return FakeQuery(self.data.get(model, []))

    def get(self, model: type, item_id: int) -> Any | None:
        for row in self.data.get(model, []):
            if getattr(row, "id", None) == item_id:
                return row
        return None

    def add(self, item: Any) -> None:
        self.added.append(item)
        self.data.setdefault(type(item), []).append(item)
        if getattr(item, "id", None) is None or not isinstance(getattr(item, "id", None), int):
            item.id = len(self.data[type(item)])

    def delete(self, item: Any) -> None:
        self.deleted.append(item)

    def commit(self) -> None:
        self.commits += 1

    def rollback(self) -> None:
        self.rollbacks += 1

    def refresh(self, item: Any) -> None:
        self.refreshed.append(item)
