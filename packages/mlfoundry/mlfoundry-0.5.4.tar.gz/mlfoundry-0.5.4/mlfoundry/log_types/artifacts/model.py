import copy
import json
import logging
import os.path
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple, Union

from mlflow.entities import ArtifactType, CustomMetric, Model, ModelSchema
from mlflow.tracking import MlflowClient
from pydantic import BaseModel, Extra

from mlfoundry.artifact.truefoundry_artifact_repo import MlFoundryArtifactsRepository
from mlfoundry.enums import ModelFramework
from mlfoundry.exceptions import MlFoundryException
from mlfoundry.log_types.artifacts.constants import (
    FILES_DIR,
    INTERNAL_METADATA_PATH,
    MODEL_DIR_NAME,
    MODEL_SCHEMA_UPDATE_FAILURE_HELP,
)
from mlfoundry.log_types.artifacts.utils import (
    _copy_additional_files,
    _get_mlflow_client,
    _validate_artifact_metadata,
    _validate_description,
)

logger = logging.getLogger("mlfoundry")


# TODO: Add some progress indicators for upload and download
# TODO: Support async download and upload


class ModelVersionInternalMetadata(BaseModel):
    class Config:
        extra = Extra.allow

    files_dir: str  # relative to root
    model_dir: str  # relative to `files_dir`
    model_is_null: bool = False
    framework: ModelFramework = ModelFramework.UNKNOWN

    def dict(self, *args, **kwargs):
        dct = super().dict(*args, **kwargs)
        dct["framework"] = dct["framework"].value
        return dct


class ModelVersionDownloadInfo(BaseModel):
    download_dir: str
    model_dir: str
    model_framework: ModelFramework = ModelFramework.UNKNOWN


class ModelVersion:
    def __init__(self, fqn: str) -> None:
        self._mlflow_client = _get_mlflow_client()
        self._model_version = self._mlflow_client.get_model_version_by_fqn(fqn=fqn)
        self._model: Model = self._mlflow_client.get_model_by_id(
            model_id=self._model_version.model_id
        )
        self._mlfa_repo = MlFoundryArtifactsRepository(
            version_id=self._model_version.id, mlflow_client=self._mlflow_client
        )
        self._deleted = False
        self._description: str = ""
        self._metadata: Dict[str, Any] = {}
        self._model_schema: Optional[ModelSchema] = None
        self._set_mutable_attrs()

    def _ensure_not_deleted(self):
        if self._deleted:
            raise MlFoundryException(
                "Model Version was deleted, cannot perform updates on a deleted version"
            )

    def _set_mutable_attrs(self, refetch=False):
        if refetch:
            self._model_version = self._mlflow_client.get_model_version_by_id(
                version_id=self._model_version.id
            )
        self._description = self._model_version.description or ""
        self._metadata = copy.deepcopy(self._model_version.artifact_metadata)
        self._model_schema = copy.deepcopy(self._model_version.model_schema)

    def __repr__(self):
        return f"{self.__class__.__name__}(fqn={self.fqn!r}, model_schema={self._model_schema!r})"

    @property
    def name(self) -> str:
        return self._model.name

    @property
    def model_fqn(self) -> str:
        return self._model.fqn

    @property
    def version(self) -> int:
        return self._model_version.version

    @property
    def fqn(self) -> str:
        return self._model_version.fqn

    @property
    def step(self) -> Optional[int]:
        return self._model_version.step

    @property
    def description(self) -> Optional[str]:
        return self._description

    @description.setter
    def description(self, value: str):
        _validate_description(value)
        self._description = value

    @property
    def metadata(self) -> Dict[str, Any]:
        return self._metadata

    @metadata.setter
    def metadata(self, value: Dict[str, Any]):
        _validate_artifact_metadata(value)
        self._metadata = value

    @property
    def model_schema(self) -> Optional[ModelSchema]:
        return self._model_schema

    @model_schema.setter
    def model_schema(self, value: Union[Dict[str, Any], ModelSchema]):
        if not isinstance(value, ModelSchema):
            value = ModelSchema.parse_obj(value)
        self._model_schema = value

    def raw_download(self, path: Optional[Union[str, Path]]) -> str:
        logger.info("Downloading model version contents, this might take a while ...")
        return self._mlfa_repo.download_artifacts(artifact_path="", dst_path=path)

    def _download(
        self, path: Optional[Union[str, Path]]
    ) -> Tuple[ModelVersionInternalMetadata, ModelVersionDownloadInfo]:
        self._ensure_not_deleted()
        download_dir = self.raw_download(path=path)
        internal_metadata_path = os.path.join(download_dir, INTERNAL_METADATA_PATH)
        if not os.path.exists(internal_metadata_path):
            raise MlFoundryException(
                f"Model version seems to be corrupted or in invalid format due to missing model metadata. "
                f"You can still use .raw_download(path='/your/path/here') to download and inspect files."
            )
        with open(internal_metadata_path) as f:
            internal_metadata = ModelVersionInternalMetadata.parse_obj(json.load(f))
        download_info = ModelVersionDownloadInfo(
            download_dir=os.path.join(download_dir, internal_metadata.files_dir),
            model_dir=os.path.join(
                download_dir, internal_metadata.files_dir, internal_metadata.model_dir
            ),
            model_framework=internal_metadata.framework,
        )
        return internal_metadata, download_info

    def download(self, path: Optional[Union[str, Path]]) -> ModelVersionDownloadInfo:
        _, download_info = self._download(path=path)
        return download_info

    def load(self, **load_model_kwargs):
        from mlfoundry.frameworks import get_model_registry

        internal_metadata, download_info = self._download(path=None)
        if internal_metadata.model_is_null:
            raise MlFoundryException(
                f"Cannot load model as no model object was provided during logging."
            )
        if internal_metadata.framework == ModelFramework.UNKNOWN:
            raise MlFoundryException(
                "Cannot deserialize model as model framework is unknown. You can still download the "
                "contents by calling `.download(path='your/path/here') and load the model manually."
            )
        return get_model_registry(internal_metadata.framework).load_model(
            download_info.model_dir, **load_model_kwargs
        )

    def delete(self) -> bool:
        self._ensure_not_deleted()
        self._mlflow_client.delete_artifact_version(version_id=self._model_version.id)
        self._deleted = True
        return True

    def update(self):
        self._ensure_not_deleted()
        kwargs = {}
        if self.model_schema is not None:
            kwargs["model_schema"] = self.model_schema
        self._model_version = self._mlflow_client.update_model_version(
            version_id=self._model_version.id,
            description=self.description,
            artifact_metadata=self.metadata,
            **kwargs,
        )
        self._set_mutable_attrs()


def _log_model_version(
    run,
    name: str,
    model: Any,
    framework: ModelFramework,
    model_save_kwargs: Optional[Dict[str, Any]] = None,
    additional_files: Sequence[Tuple[Union[str, Path], Optional[str]]] = (),
    description: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None,
    model_schema: Optional[Union[Dict[str, Any], ModelSchema]] = None,
    custom_metrics: Optional[Union[List[Dict[str, Any]], CustomMetric]] = None,
    step: int = 0,
) -> ModelVersion:

    from mlfoundry.frameworks import get_model_registry

    custom_metrics = custom_metrics or []
    model_save_kwargs = model_save_kwargs or {}
    metadata = metadata or {}
    additional_files = additional_files or {}
    step = step or 0

    # validations
    if framework is None:
        framework = ModelFramework.UNKNOWN
    elif not isinstance(framework, ModelFramework):
        framework = ModelFramework(framework)

    if model is not None and framework == ModelFramework.UNKNOWN:
        raise MlFoundryException(
            "`framework` cannot be passed as 'unknown' when `model` is not None"
        )

    _validate_description(description)
    _validate_artifact_metadata(metadata)

    if model_schema is not None and not isinstance(model_schema, ModelSchema):
        model_schema = ModelSchema.parse_obj(model_schema)

    if custom_metrics and not model_schema:
        raise MlFoundryException(
            "Custom Metrics defined without adding the Model Schema"
        )
    custom_metrics = [
        CustomMetric.parse_obj(cm) if not isinstance(cm, CustomMetric) else cm
        for cm in custom_metrics
    ]

    logger.info("Logging model and additional files, this might take a while ...")
    mlflow_client: MlflowClient = run.mlflow_client
    temp_dir = tempfile.TemporaryDirectory(prefix="truefoundry-")

    internal_metadata = ModelVersionInternalMetadata(
        framework=framework,
        files_dir=FILES_DIR,
        model_dir=MODEL_DIR_NAME,
        model_is_null=model is None,
    )

    try:
        local_files_dir = os.path.join(temp_dir.name, internal_metadata.files_dir)
        os.makedirs(local_files_dir, exist_ok=True)

        # serialize model
        logger.info("Serializing model files to model version contents")
        local_model_dir = os.path.join(local_files_dir, internal_metadata.model_dir)
        if model is not None:
            model_registy = get_model_registry(framework)
            model_registy.save_model(
                model=model, path=local_model_dir, **model_save_kwargs
            )
        os.makedirs(
            local_model_dir, exist_ok=True
        )  # in case model was None, we still create an empty dir

        # verify additional files and paths, copy additional files
        if additional_files:
            logger.info("Adding `additional_files` to model version contents")
            _copy_additional_files(
                root_dir=temp_dir.name,
                files_dir=internal_metadata.files_dir,
                model_dir=internal_metadata.model_dir,
                additional_files=additional_files,
            )
    except Exception as e:
        temp_dir.cleanup()
        raise MlFoundryException("Failed to log model") from e

    # save internal metadata
    local_internal_metadata_path = os.path.join(temp_dir.name, INTERNAL_METADATA_PATH)
    os.makedirs(os.path.dirname(local_internal_metadata_path), exist_ok=True)
    with open(local_internal_metadata_path, "w") as f:
        json.dump(internal_metadata.dict(), f)

    # create entry
    version_id = mlflow_client.create_artifact_version(
        experiment_id=int(run._experiment_id),
        artifact_type=ArtifactType.MODEL,
        name=name,
    )
    artifacts_repo = MlFoundryArtifactsRepository(
        version_id=version_id, mlflow_client=mlflow_client
    )
    try:
        logger.info("Packaging and uploading files to remote ...")
        artifacts_repo.log_artifacts(local_dir=temp_dir.name, artifact_path=None)
    except Exception as e:
        mlflow_client.notify_failure_for_artifact_version(version_id=version_id)
        raise MlFoundryException("Failed to log model") from e
    finally:
        temp_dir.cleanup()
    mlflow_client.finalize_artifact_version(version_id=version_id, run_uuid=run.run_id)
    model_version = mlflow_client.create_model_version(
        artifact_version_id=version_id,
        description=description,
        artifact_metadata=metadata,
        data_path=INTERNAL_METADATA_PATH,
        step=step,
    )
    # update model schema at end
    if model_schema is not None:
        try:
            model_version = mlflow_client.update_model_version(
                version_id=version_id,
                model_schema=model_schema,
            )
            model_version = mlflow_client.add_custom_metrics_to_model_version(
                version_id=version_id, custom_metrics=custom_metrics
            )
        except Exception:
            # TODO (chiragjn): what is the best exception to catch here?
            logger.error(MODEL_SCHEMA_UPDATE_FAILURE_HELP.format(fqn=model_version.fqn))

    return ModelVersion(fqn=model_version.fqn)
