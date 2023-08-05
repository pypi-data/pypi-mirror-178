"""
Summary: AROS validation model.

AROS files validation models.
"""

from typing import Optional, Union
import uuid

from pydantic import (
    BaseModel,
    conint,
    constr,
    Field,
)

from structured_data_validation.models.datatypes import (
    AnalysisResultType,
    AnalysisTypeName,
    CustomAROSDateFormat,
)
from structured_data_validation.models.MPFC import (
    MPFCAnalysisResult,
    MPFCExperimentResult,
)
from structured_data_validation.models.MPSC import (
    MPSCAnalysisResult,
    MPSCExperimentResult,
)
from structured_data_validation.models.SPFC import (
    SPFCAnalysisResult,
    SPFCExperimentResult,
)
from structured_data_validation.models.SPSC import (
    SPSCAnalysisResult,
    SPSCExperimentResult,
)


class Analysis(BaseModel):
    """Analysis represent.

    Description for Analysis
    """

    analysis_method_fk: Optional[float] = Field(
        alias="analysis.analysis_method_fk", description="", example="nan"
    )
    analysis_status_fk: Optional[float] = Field(
        alias="analysis.analysis_status_fk", description="", example="nan"
    )
    annotations: Optional[float] = Field(
        alias="analysis.annotations", description="", example="nan"
    )
    comments: Optional[constr(max_length=256)] = Field(
        alias="analysis.comments", description="", example="nan"
    )
    corporate_id: Optional[uuid.UUID] = Field(
        ...,
        alias="analysis.corporate_id",
        description="",
        example="00fc61f5-2ccf-4741-8db3-6ec4d0ff1b4b",
    )  # **
    date_start: Optional[CustomAROSDateFormat] = Field(
        alias="analysis.date_start", description="", example="nan"
    )
    description: Optional[constr(min_length=0, max_length=256)] = Field(
        alias="analysis.description", description="", example="nan"
    )  # ?
    etag: Optional[float] = Field(alias="analysis.etag", description="", example="nan")
    experiment_fk: Optional[float] = Field(
        alias="analysis.experiment_fk", description="", example="nan"
    )
    hash_code: Optional[uuid.UUID] = Field(
        alias="analysis.hash_code", description="", example="nan"
    )  # ?
    modified: Optional[float] = Field(
        alias="analysis.modified", description="Boolean, date, Enum?", example="nan"
    )
    name: Optional[float] = Field(alias="analysis.name", description="", example="nan")
    parent_id: Optional[float] = Field(
        alias="analysis.parent_id", description="", example="nan"
    )
    software_version_fk: Optional[float] = Field(
        alias="analysis.software_version_fk", description="", example="nan"
    )
    transaction_fk: Optional[float] = Field(
        alias="analysis.transaction_fk", description="", example="nan"
    )


class AnalysisResult(BaseModel):
    """AnalysisResult represent.

    Description
    """

    analysis_result_guid: Optional[float] = Field(
        alias="analysis_result.analysis_result_guid", description="", example="nan"
    )
    analysis_result_set_fk: Optional[float] = Field(
        alias="analysis_result.analysis_result_set_fk", description="", example="nan"
    )
    annotations: Optional[str] = Field(
        alias="analysis_result.annotations", description="", example="nan"
    )
    comments: Optional[str] = Field(
        alias="analysis_result.comments", description="", example="nan"
    )
    data: Union[
        MPFCAnalysisResult, MPSCAnalysisResult, SPFCAnalysisResult, SPSCAnalysisResult
    ] = Field(
        ...,
        alias="analysis_result.data",
        description="AnalysisResultData class abstraction.",
        discriminator="analysis_type__name",
    )  # **
    hash_code: Optional[uuid.UUID] = Field(
        alias="analysis_result.hash_code", description="", example="nan"
    )  # ?
    modified: Optional[float] = Field(
        alias="analysis_result.modified", description="", example="nan"
    )
    ordinal: Optional[conint(ge=0)] = Field(
        alias="analysis_result.ordinal", description="", example="nan"
    )
    parameter_fk: Optional[float] = Field(
        alias="analysis_result.parameter_fk", description="", example="nan"
    )
    transaction_fk: Optional[float] = Field(
        alias="analysis_result.transaction_fk", description="", example="nan"
    )


class AnalysisResultSet(BaseModel):
    """AnalysisResultSet represent.

    Descripttion
    """

    analysis_fk: Optional[float] = Field(
        alias="analysis_result_set.analysis_fk", description="", example="nan"
    )
    analysis_result_type_fk: Optional[float] = Field(
        alias="analysis_result_set.analysis_result_type_fk",
        description="",
        example="nan",
    )
    annotations: Optional[float] = Field(
        alias="analysis_result_set.annotations", description="", example="nan"
    )
    comments: Optional[float] = Field(
        alias="analysis_result_set.comments", description="", example="nan"
    )
    date_acquired: Optional[CustomAROSDateFormat] = Field(
        alias="analysis_result_set.date_acquired", description="", example="nan"
    )
    description: Optional[float] = Field(
        alias="analysis_result_set.description", description="", example="nan"
    )
    external_id: Optional[uuid.UUID] = Field(
        alias="analysis_result_set.external_id",
        description="",
        example="00fc61f5-2ccf-4741-8db3-6ec4d0ff1b4b",
    )
    file_fk: Optional[float] = Field(
        alias="analysis_result_set.file_fk", description="", example="nan"
    )
    modified: Optional[float] = Field(
        alias="analysis_result_set.modified", description="", example="nan"
    )
    name: Optional[float] = Field(
        alias="analysis_result_set.name", description="", example="nan"
    )
    schema_version_fk: Optional[float] = Field(
        alias="analysis_result_set.schema_version_fk", description="", example="nan"
    )
    transaction_fk: Optional[float] = Field(
        alias="analysis_result_set.transaction_fk", description="", example="nan"
    )


class AnalysisResultSubstance(BaseModel):
    """AnalysisResultSubstance decumenation.

    Description
    """

    analysis_result_fk: Optional[float] = Field(
        alias="analysis_result_substance.analysis_result_fk",
        description="",
        example="nan",
    )
    comments: Optional[float] = Field(
        alias="analysis_result_substance.comments", description="", example="nan"
    )
    substance_fk: Optional[float] = Field(
        alias="analysis_result_substance.substance_fk", description="", example="nan"
    )
    substance_role_fk: Optional[float] = Field(
        alias="analysis_result_substance.substance_role_fk",
        description="",
        example="nan",
    )


class AnalysisResultType(BaseModel):
    """AnalysisResultType.

    Description
    """

    analysis_method_fk: Optional[float] = Field(
        alias="analysis_result_type.analysis_method_fk", description="", example="nan"
    )
    annotations: Optional[float] = Field(
        alias="analysis_result_type.annotations", description="", example="nan"
    )
    comments: Optional[float] = Field(
        alias="analysis_result_type.comments", description="", example="nan"
    )
    description: Optional[str] = Field(
        alias="analysis_result_type.description", description="", example="nan"
    )
    modified: Optional[float] = Field(
        alias="analysis_result_type.modified", description="", example="nan"
    )
    name: Optional[AnalysisResultType] = Field(
        alias="analysis_result_type.name",
        description="",
        example="Single Parameter Full Curve Analysis Result",
    )
    schema_fk: Optional[float] = Field(
        alias="analysis_result_type.schema_fk", description="", example="nan"
    )


class AnalysisType(BaseModel):
    """AnalysisType.

    Description
    """

    analysis_category_fk: Optional[float] = Field(
        alias="analysis_type.analysis_category_fk", description="", example="nan"
    )
    analysis_type__description: Optional[float] = Field(
        alias="analysis_type.description", description="", example="nan"
    )
    analysis_type__name: Optional[AnalysisTypeName] = Field(
        ...,
        alias="analysis_type.name",
        description="",
        example="Single Parameter Full Curve",
    )


class Container(BaseModel):
    """Container.

    Description
    """

    annotations: Optional[float] = Field(
        alias="container.annotations", description="", example="nan"
    )
    barcode: Optional[str] = Field(
        ..., alias="container.barcode", description="", example="U5H665A"
    )  # **
    container_type_fk: Optional[float] = Field(
        alias="container.container_type_fk", description="", example="nan"
    )
    description: Optional[float] = Field(
        alias="container.description", description="", example="nan"
    )
    name: Optional[float] = Field(alias="container.name", description="", example="nan")


class ContainerCategory(BaseModel):
    """ContainerCategory.

    Description
    """

    category_description: Optional[float] = Field(
        alias="container_category.description", description="", example="nan"
    )
    category_name: Optional[str] = Field(
        alias="container_category.name", description="", example="Plate"
    )


class ContainerType(BaseModel):
    """ContainerType.

    Description.
    """

    container_category_fk: Optional[float] = Field(
        alias="container_type.container_category_fk", description="", example="nan"
    )
    description: Optional[float] = Field(
        alias="container_type.description", description="", example="nan"
    )
    name: Optional[str] = Field(
        ..., alias="container_type.name", description="", example="Plate 384"
    )  # **
    position_schema: Optional[float] = Field(
        alias="container_type.position_schema", description="", example="nan"
    )


class Experiment(BaseModel):
    """Experiment.

    Description
    """

    comments: Optional[float] = Field(
        alias="experiment.comments", description="", example="nan"
    )
    corporate_id: Optional[str] = Field(
        ..., alias="experiment.corporate_id", description="", example="ELN21"
    )  # **
    date_start: Optional[CustomAROSDateFormat] = Field(
        ...,
        alias="experiment.date_start",
        description="",
        example="2022-07-20 00:00:00 +0000 UTC",
    )  # **
    description: Optional[str] = Field(
        alias="experiment.description", description="", example="nan"
    )  # ?
    etag: Optional[str] = Field(alias="experiment.etag", description="", example="nan")
    experiment_type_fk: Optional[str] = Field(
        alias="experiment.experiment_type_fk", description="", example="nan"
    )
    hash_code: Optional[uuid.UUID] = Field(
        alias="experiment.hash_code", description="", example="nan"
    )  # ? UUID
    instrument_settings_fk: Optional[float] = Field(
        alias="experiment.instrument_settings_fk", description="", example="nan"
    )
    modified: Optional[float] = Field(
        alias="experiment.modified", description="", example="nan"
    )
    name: Optional[float] = Field(
        alias="experiment.name", description="", example="nan"
    )
    protocol_fk: Optional[float] = Field(
        alias="experiment.protocol_fk", description="", example="nan"
    )
    reference_id: Optional[float] = Field(
        alias="experiment.reference_id", description="", example="nan"
    )
    study_fk: Optional[float] = Field(
        alias="experiment.study_fk", description="", example="nan"
    )
    transaction_fk: Optional[float] = Field(
        alias="experiment.transaction_fk", description="", example="nan"
    )


class ExperimentAnalysisResult(BaseModel):
    """ExperimentAnalysisResult.

    Example of model for a relational database ... no needed.
    """

    analysis_result_fk: Optional[float] = Field(
        alias="experiment_analysis_result.analysis_result_fk",
        description="",
        example="nan",
    )
    experiment_result_fk: Optional[float] = Field(
        alias="experiment_analysis_result.experiment_result_fk",
        description="",
        example="nan",
    )


class ExperimentResult(BaseModel):
    """ExperimentResult.

    Description
    """

    annotations: Optional[float] = Field(
        alias="experiment_result.annotations", description="", example="nan"
    )
    comments: Optional[float] = Field(
        alias="experiment_result.comments", description="", example="nan"
    )
    container_fk: Optional[float] = Field(
        alias="experiment_result.container_fk", description="", example="nan"
    )
    data: Union[
        MPFCExperimentResult,
        MPSCExperimentResult,
        SPFCExperimentResult,
        SPSCExperimentResult,
    ] = Field(
        ..., alias="experiment_result.data", discriminator="analysis_type__name"
    )  # **
    etag: Optional[float] = Field(
        alias="experiment_result.etag", description="", example="nan"
    )
    experiment_result_set_fk: Optional[float] = Field(
        alias="experiment_result.experiment_result_set_fk",
        description="",
        example="nan",
    )
    hash_code: Optional[float] = Field(
        alias="experiment_result.hash_code", description="", example="nan"
    )
    modified: Optional[float] = Field(
        alias="experiment_result.modified", description="", example="nan"
    )
    ordinal: Optional[int] = Field(
        alias="experiment_result.ordinal", description="", example="1"
    )
    parent_id: Optional[float] = Field(
        alias="experiment_result.parent_id", description="", example="nan"
    )
    sample_location: Optional[float] = Field(
        alias="experiment_result.sample_location", description="", example="nan"
    )
    timepoint_fk: Optional[float] = Field(
        alias="experiment_result.timepoint_fk", description="", example="nan"
    )
    transaction_fk: Optional[float] = Field(
        alias="experiment_result.transaction_fk", description="", example="nan"
    )


class AROS(BaseModel):
    """AROS.

    Description
    """

    analysis: Analysis
    analysis_type: AnalysisType
    analysis_result: AnalysisResult
    analysis_result_type: AnalysisResultType
    anslysis_result_set: AnalysisResultSet
    analysis_result_substance: AnalysisResultSubstance
    container: Container  # The following two are probably nested
    container_category: ContainerCategory
    container_type: ContainerType
    experiment: Experiment
    experiment_analysis_result: ExperimentAnalysisResult
    experiment_result: ExperimentResult
