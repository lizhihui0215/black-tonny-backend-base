from pathlib import Path
from typing import Literal, cast

from sqlalchemy.sql.schema import MetaData as MetaDataType

from .db.database import CaptureBase, ServingBase

AlembicTarget = Literal["capture", "serving"]


def resolve_alembic_target(explicit_target: str | None, config_filename: str | None) -> AlembicTarget:
    if explicit_target is not None:
        normalized_target = explicit_target.lower()
        if normalized_target in {"capture", "serving"}:
            return cast(AlembicTarget, normalized_target)
        raise ValueError("ALEMBIC_DB_TARGET must be either 'capture' or 'serving'.")

    if config_filename is not None:
        stem = Path(config_filename).stem.lower()
        if "capture" in stem:
            return "capture"
        if "serving" in stem:
            return "serving"

    raise ValueError(
        "Unable to determine Alembic target. Use alembic_capture.ini, alembic_serving.ini, "
        "or set ALEMBIC_DB_TARGET=capture|serving."
    )


def get_version_table(target: AlembicTarget) -> str:
    return f"alembic_version_{target}"


def load_target_metadata(target: AlembicTarget) -> MetaDataType:
    if target == "capture":
        from ..models.analysis_batch import AnalysisBatch  # noqa: F401
        from ..models.capture_batch import CaptureBatch  # noqa: F401
        from ..models.capture_endpoint_payload import CaptureEndpointPayload  # noqa: F401

        return CaptureBase.metadata

    from ..models.rate_limit import RateLimit  # noqa: F401
    from ..models.tier import Tier  # noqa: F401
    from ..models.user import User  # noqa: F401
    from .db.token_blacklist import TokenBlacklist  # noqa: F401

    return ServingBase.metadata
