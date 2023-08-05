"""
Summary: AROS validation model.

AROS files validation models.
"""

from typing import Dict, Optional, Tuple, Union
import uuid

import pandas as pd
from pydantic import (
    BaseModel,
    condecimal,
    conint,
    constr,
    EmailStr,
    Field,
    FileUrl,
    NameEmail,
    validator,
)
from pydantic.fields import ModelField

from structured_data_validation.models.datatypes import (
    AnalysisResultType,
    AnalysisTypeName,
    CoorporateId,
    CustomAROSDateFormat,
    EmptyEnum,
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


class AROS(BaseModel):
    """Documentation for AROS data model.

    Documentation for AROS data model.

    Args:
        BaseModel: Inherits from pydantic BaseModel.
    """

    analysis__analysis_method_fk: Optional[float] = Field(
        alias="analysis.analysis_method_fk", description="", example="nan"
    )
    analysis__analysis_status_fk: Optional[float] = Field(
        alias="analysis.analysis_status_fk", description="", example="nan"
    )
    analysis__annotations: Optional[float] = Field(
        alias="analysis.annotations", description="", example="nan"
    )
    analysis__comments: Optional[constr(max_length=256)] = Field(
        alias="analysis.comments", description="", example="nan"
    )
    analysis__corporate_id: Optional[uuid.UUID] = Field(
        ...,
        alias="analysis.corporate_id",
        description="",
        example="00fc61f5-2ccf-4741-8db3-6ec4d0ff1b4b",
    )  # **
    analysis__date_start: Optional[CustomAROSDateFormat] = Field(
        alias="analysis.date_start", description="", example="nan"
    )
    analysis__description: Optional[constr(min_length=0, max_length=256)] = Field(
        alias="analysis.description", description="", example="nan"
    )  # ?
    analysis__etag: Optional[float] = Field(
        alias="analysis.etag", description="", example="nan"
    )
    analysis__experiment_fk: Optional[float] = Field(
        alias="analysis.experiment_fk", description="", example="nan"
    )
    analysis__hash_code: Optional[uuid.UUID] = Field(
        alias="analysis.hash_code", description="", example="nan"
    )  # ?
    analysis__modified: Optional[float] = Field(
        alias="analysis.modified", description="", example="nan"
    )
    analysis__name: Optional[float] = Field(
        alias="analysis.name", description="", example="nan"
    )
    analysis__parent_id: Optional[float] = Field(
        alias="analysis.parent_id", description="", example="nan"
    )
    analysis__software_version_fk: Optional[float] = Field(
        alias="analysis.software_version_fk", description="", example="nan"
    )
    analysis__transaction_fk: Optional[float] = Field(
        alias="analysis.transaction_fk", description="", example="nan"
    )
    analysis_result__analysis_result_guid: Optional[float] = Field(
        alias="analysis_result.analysis_result_guid", description="", example="nan"
    )
    analysis_result__analysis_result_set_fk: Optional[float] = Field(
        alias="analysis_result.analysis_result_set_fk", description="", example="nan"
    )
    analysis_result__annotations: Optional[str] = Field(
        alias="analysis_result.annotations", description="", example="nan"
    )
    analysis_result__comments: Optional[str] = Field(
        alias="analysis_result.comments", description="", example="nan"
    )
    analysis_result__data: Union[
        MPFCAnalysisResult, MPSCAnalysisResult, SPFCAnalysisResult, SPSCAnalysisResult
    ] = Field(
        ..., alias="analysis_result.data", discriminator="analysis_type__name"
    )  # **
    analysis_result__hash_code: Optional[uuid.UUID] = Field(
        alias="analysis_result.hash_code", description="", example="nan"
    )  # ?
    analysis_result__modified: Optional[float] = Field(
        alias="analysis_result.modified", description="", example="nan"
    )
    analysis_result__ordinal: Optional[conint(ge=0)] = Field(
        alias="analysis_result.ordinal", description="", example="nan"
    )
    analysis_result__parameter_fk: Optional[float] = Field(
        alias="analysis_result.parameter_fk", description="", example="nan"
    )
    analysis_result__transaction_fk: Optional[float] = Field(
        alias="analysis_result.transaction_fk", description="", example="nan"
    )
    analysis_result_set__analysis_fk: Optional[float] = Field(
        alias="analysis_result_set.analysis_fk", description="", example="nan"
    )
    analysis_result_set__analysis_result_type_fk: Optional[float] = Field(
        alias="analysis_result_set.analysis_result_type_fk",
        description="",
        example="nan",
    )
    analysis_result_set__annotations: Optional[float] = Field(
        alias="analysis_result_set.annotations", description="", example="nan"
    )
    analysis_result_set__comments: Optional[float] = Field(
        alias="analysis_result_set.comments", description="", example="nan"
    )
    analysis_result_set__date_acquired: Optional[CustomAROSDateFormat] = Field(
        alias="analysis_result_set.date_acquired", description="", example="nan"
    )
    analysis_result_set__description: Optional[float] = Field(
        alias="analysis_result_set.description", description="", example="nan"
    )
    analysis_result_set__external_id: Optional[uuid.UUID] = Field(
        alias="analysis_result_set.external_id",
        description="",
        example="00fc61f5-2ccf-4741-8db3-6ec4d0ff1b4b",
    )
    analysis_result_set__file_fk: Optional[float] = Field(
        alias="analysis_result_set.file_fk", description="", example="nan"
    )
    analysis_result_set__modified: Optional[float] = Field(
        alias="analysis_result_set.modified", description="", example="nan"
    )
    analysis_result_set__name: Optional[float] = Field(
        alias="analysis_result_set.name", description="", example="nan"
    )
    analysis_result_set__schema_version_fk: Optional[float] = Field(
        alias="analysis_result_set.schema_version_fk", description="", example="nan"
    )
    analysis_result_set__transaction_fk: Optional[float] = Field(
        alias="analysis_result_set.transaction_fk", description="", example="nan"
    )
    analysis_result_substance__analysis_result_fk: Optional[float] = Field(
        alias="analysis_result_substance.analysis_result_fk",
        description="",
        example="nan",
    )
    analysis_result_substance__comments: Optional[float] = Field(
        alias="analysis_result_substance.comments", description="", example="nan"
    )
    analysis_result_substance__substance_fk: Optional[float] = Field(
        alias="analysis_result_substance.substance_fk", description="", example="nan"
    )
    analysis_result_substance__substance_role_fk: Optional[float] = Field(
        alias="analysis_result_substance.substance_role_fk",
        description="",
        example="nan",
    )
    analysis_result_type__analysis_method_fk: Optional[float] = Field(
        alias="analysis_result_type.analysis_method_fk", description="", example="nan"
    )
    analysis_result_type__annotations: Optional[float] = Field(
        alias="analysis_result_type.annotations", description="", example="nan"
    )
    analysis_result_type__comments: Optional[float] = Field(
        alias="analysis_result_type.comments", description="", example="nan"
    )
    analysis_result_type__description: Optional[str] = Field(
        alias="analysis_result_type.description", description="", example="nan"
    )
    analysis_result_type__modified: Optional[float] = Field(
        alias="analysis_result_type.modified", description="", example="nan"
    )
    analysis_result_type__name: Optional[AnalysisResultType] = Field(
        alias="analysis_result_type.name",
        description="",
        example="Single Parameter Full Curve Analysis Result",
    )
    analysis_result_type__schema_fk: Optional[float] = Field(
        alias="analysis_result_type.schema_fk", description="", example="nan"
    )
    analysis_type__analysis_category_fk: Optional[float] = Field(
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
    )  # **
    container__annotations: Optional[float] = Field(
        alias="container.annotations", description="", example="nan"
    )
    container__barcode: Optional[str] = Field(
        ..., alias="container.barcode", description="", example="U5H665A"
    )  # **
    container__container_type_fk: Optional[float] = Field(
        alias="container.container_type_fk", description="", example="nan"
    )
    container__description: Optional[float] = Field(
        alias="container.description", description="", example="nan"
    )
    container__name: Optional[float] = Field(
        alias="container.name", description="", example="nan"
    )
    container__category_description: Optional[float] = Field(
        alias="container_category.description", description="", example="nan"
    )
    container__category_name: Optional[str] = Field(
        alias="container_category.name", description="", example="Plate"
    )
    container_type__container_category_fk: Optional[float] = Field(
        alias="container_type.container_category_fk", description="", example="nan"
    )
    container_type__description: Optional[float] = Field(
        alias="container_type.description", description="", example="nan"
    )
    container_type__name: Optional[str] = Field(
        ..., alias="container_type.name", description="", example="Plate 384"
    )  # **
    container_type__position_schema: Optional[float] = Field(
        alias="container_type.position_schema", description="", example="nan"
    )
    experiment__annotations: Optional[float] = Field(
        alias="experiment.annotations", description="", example="nan"
    )
    experiment__comments: Optional[float] = Field(
        alias="experiment.comments", description="", example="nan"
    )
    experiment__corporate_id: Optional[str] = Field(
        ..., alias="experiment.corporate_id", description="", example="ELN21"
    )  # **
    experiment__date_start: Optional[CustomAROSDateFormat] = Field(
        ...,
        alias="experiment.date_start",
        description="",
        example="2022-07-20 00:00:00 +0000 UTC",
    )  # **
    experiment__description: Optional[str] = Field(
        alias="experiment.description", description="", example="nan"
    )  # ?
    experiment__etag: Optional[str] = Field(
        alias="experiment.etag", description="", example="nan"
    )
    experiment__experiment_type_fk: Optional[str] = Field(
        alias="experiment.experiment_type_fk", description="", example="nan"
    )
    experiment__hash_code: Optional[uuid.UUID] = Field(
        alias="experiment.hash_code", description="", example="nan"
    )  # ? UUID
    experiment__instrument_settings_fk: Optional[float] = Field(
        alias="experiment.instrument_settings_fk", description="", example="nan"
    )
    experiment__modified: Optional[float] = Field(
        alias="experiment.modified", description="", example="nan"
    )
    experiment__name: Optional[float] = Field(
        alias="experiment.name", description="", example="nan"
    )
    experiment__protocol_fk: Optional[float] = Field(
        alias="experiment.protocol_fk", description="", example="nan"
    )
    experiment__reference_id: Optional[float] = Field(
        alias="experiment.reference_id", description="", example="nan"
    )
    experiment__study_fk: Optional[float] = Field(
        alias="experiment.study_fk", description="", example="nan"
    )
    experiment__transaction_fk: Optional[float] = Field(
        alias="experiment.transaction_fk", description="", example="nan"
    )
    experiment_analysis_result__analysis_result_fk: Optional[float] = Field(
        alias="experiment_analysis_result.analysis_result_fk",
        description="",
        example="nan",
    )
    experiment_analysis_result__experiment_result_fk: Optional[float] = Field(
        alias="experiment_analysis_result.experiment_result_fk",
        description="",
        example="nan",
    )
    experiment_result__annotations: Optional[float] = Field(
        alias="experiment_result.annotations", description="", example="nan"
    )
    experiment_result__comments: Optional[float] = Field(
        alias="experiment_result.comments", description="", example="nan"
    )
    experiment_result__container_fk: Optional[float] = Field(
        alias="experiment_result.container_fk", description="", example="nan"
    )
    experiment_result__data: Union[
        MPFCExperimentResult,
        MPSCExperimentResult,
        SPFCExperimentResult,
        SPSCExperimentResult,
    ] = Field(
        ..., alias="experiment_result.data", discriminator="analysis_type__name"
    )  # **
    experiment_result__etag: Optional[float] = Field(
        alias="experiment_result.etag", description="", example="nan"
    )
    experiment_result__experiment_result_set_fk: Optional[float] = Field(
        alias="experiment_result.experiment_result_set_fk",
        description="",
        example="nan",
    )
    experiment_result__hash_code: Optional[float] = Field(
        alias="experiment_result.hash_code", description="", example="nan"
    )
    experiment_result__modified: Optional[float] = Field(
        alias="experiment_result.modified", description="", example="nan"
    )
    experiment_result__ordinal: Optional[int] = Field(
        alias="experiment_result.ordinal", description="", example="1"
    )
    experiment_result__parent_id: Optional[float] = Field(
        alias="experiment_result.parent_id", description="", example="nan"
    )
    experiment_result__sample_location: Optional[float] = Field(
        alias="experiment_result.sample_location", description="", example="nan"
    )
    experiment_result__timepoint_fk: Optional[float] = Field(
        alias="experiment_result.timepoint_fk", description="", example="nan"
    )
    experiment_result__transaction_fk: Optional[float] = Field(
        alias="experiment_result.transaction_fk", description="", example="nan"
    )
    experiment_result_sample__annotations: Optional[float] = Field(
        alias="experiment_result_sample.annotations", description="", example="nan"
    )
    experiment_result_sample__comments: Optional[float] = Field(
        alias="experiment_result_sample.comments", description="", example="nan"
    )
    experiment_result_sample__data: Optional[float] = Field(
        alias="experiment_result_sample.data", description="", example="nan"
    )
    experiment_result_sample__experiment_result_fk: Optional[float] = Field(
        alias="experiment_result_sample.experiment_result_fk",
        description="",
        example="nan",
    )
    experiment_result_sample__sample_fk: Optional[float] = Field(
        alias="experiment_result_sample.sample_fk", description="", example="nan"
    )
    experiment_result_sample__sample_role_fk: Optional[float] = Field(
        alias="experiment_result_sample.sample_role_fk", description="", example="nan"
    )
    experiment_result_set__annotations: Optional[float] = Field(
        alias="experiment_result_set.annotations", description="", example="nan"
    )
    experiment_result_set__comments: Optional[float] = Field(
        alias="experiment_result_set.comments", description="", example="nan"
    )
    experiment_result_set__date_acquired: Optional[CustomAROSDateFormat] = Field(
        alias="experiment_result_set.date_acquired", description="", example="nan"
    )
    experiment_result_set__description: Optional[float] = Field(
        alias="experiment_result_set.description", description="", example="nan"
    )
    experiment_result_set__experiment_result_type_fk: Optional[float] = Field(
        alias="experiment_result_set.experiment_result_type_fk",
        description="",
        example="nan",
    )
    experiment_result_set__experiment_run_fk: Optional[float] = Field(
        alias="experiment_result_set.experiment_run_fk", description="", example="nan"
    )
    experiment_result_set__external_id: Optional[str] = Field(
        alias="experiment_result_set.external_id", description="", example="newGhost"
    )
    experiment_result_set__file_fk: Optional[float] = Field(
        alias="experiment_result_set.file_fk", description="", example="nan"
    )
    experiment_result_set__modified: Optional[float] = Field(
        alias="experiment_result_set.modified", description="", example="nan"
    )
    experiment_result_set__name: Optional[float] = Field(
        alias="experiment_result_set.name", description="", example="nan"
    )
    experiment_result_set__schema_version_fk: Optional[float] = Field(
        alias="experiment_result_set.schema_version_fk", description="", example="nan"
    )
    experiment_result_set__transaction_fk: Optional[float] = Field(
        alias="experiment_result_set.transaction_fk", description="", example="nan"
    )
    experiment_result_type__annotations: Optional[float] = Field(
        alias="experiment_result_type.annotations", description="", example="nan"
    )
    experiment_result_type__comments: Optional[float] = Field(
        alias="experiment_result_type.comments", description="", example="nan"
    )
    experiment_result_type__description: Optional[float] = Field(
        alias="experiment_result_type.description", description="", example="nan"
    )
    experiment_result_type__experiment_method_fk: Optional[float] = Field(
        alias="experiment_result_type.experiment_method_fk",
        description="",
        example="nan",
    )
    experiment_result_type__modified: Optional[float] = Field(
        alias="experiment_result_type.modified", description="", example="nan"
    )
    experiment_result_type__name: Optional[str] = Field(
        alias="experiment_result_type.name", description="", example="Assay Result"
    )
    experiment_result_type__schema_fk: Optional[float] = Field(
        alias="experiment_result_type.schema_fk", description="", example="nan"
    )
    experiment_result_well__experiment_result_fk: Optional[float] = Field(
        alias="experiment_result_well.experiment_result_fk",
        description="",
        example="nan",
    )
    experiment_result_well__index: Optional[float] = Field(
        alias="experiment_result_well.index", description="", example="nan"
    )
    experiment_result_well__well_column: Optional[int] = Field(
        ..., alias="experiment_result_well.well_column", description="", example="1"
    )  # **
    experiment_result_well__well_position: Optional[str] = Field(
        ..., alias="experiment_result_well.well_position", description="", example="A1"
    )  # **
    experiment_result_well__well_row: Optional[str] = Field(
        ..., alias="experiment_result_well.well_row", description="", example="A"
    )  # **
    experiment_result_well__well_row_index: Optional[int] = Field(
        ..., alias="experiment_result_well.well_row_index", description="", example="1"
    )  # **
    experiment_result_well__well_type_fk: Optional[float] = Field(
        alias="experiment_result_well.well_type_fk", description="", example="nan"
    )
    experiment_run__annotations: Optional[float] = Field(
        alias="experiment_run.annotations", description="", example="nan"
    )
    experiment_run__comments: Optional[float] = Field(
        alias="experiment_run.comments", description="", example="nan"
    )
    experiment_run__data: Optional[float] = Field(
        alias="experiment_run.data", description="", example="nan"
    )
    experiment_run__date_start: Optional[CustomAROSDateFormat] = Field(
        alias="experiment_run.date_start", description="", example="nan"
    )
    experiment_run__description: Optional[float] = Field(
        alias="experiment_run.description", description="", example="nan"
    )
    experiment_run__experiment_fk: Optional[float] = Field(
        alias="experiment_run.experiment_fk", description="", example="nan"
    )
    experiment_run__experiment_method_fk: Optional[float] = Field(
        alias="experiment_run.experiment_method_fk", description="", example="nan"
    )
    experiment_run__external_id: Optional[str] = Field(
        alias="experiment_run.external_id", description="", example="newGhost"
    )
    experiment_run__instrument_fk: Optional[float] = Field(
        alias="experiment_run.instrument_fk", description="", example="nan"
    )
    experiment_run__modified: Optional[float] = Field(
        alias="experiment_run.modified", description="", example="nan"
    )
    experiment_run__name: Optional[float] = Field(
        alias="experiment_run.name", description="", example="nan"
    )
    experiment_run__transaction_fk: Optional[float] = Field(
        alias="experiment_run.transaction_fk", description="", example="nan"
    )
    human__annotations: Optional[float] = Field(
        alias="human.annotations", description="", example="nan"
    )
    human__comments: Optional[float] = Field(
        alias="human.comments", description="", example="nan"
    )
    human__corporate_id: Optional[CoorporateId] = Field(
        ..., alias="human.corporate_id", description="", example="BROUGS00"
    )  # ? external source **
    human__data: Optional[float] = Field(
        alias="human.data", description="", example="nan"
    )
    human__email: Optional[EmailStr] = Field(
        alias="human.email", description="", example="nan"
    )
    human__first_name: Optional[NameEmail] = Field(
        alias="human.first_name", description="", example="nan"
    )
    human__is_active: Optional[bool] = Field(
        alias="human.is_active", description="", example="nan"
    )
    human__last_name: Optional[str] = Field(
        alias="human.last_name", description="", example="nan"
    )
    human_role__description: Optional[float] = Field(
        alias="human_role.description", description="", example="nan"
    )
    human_role__name: Optional[str] = Field(
        alias="human_role.name", description="", example="Scientist"
    )  # ? Enum
    project__alliance_fk: Optional[str] = Field(
        alias="project.alliance_fk", description="", example="nan"
    )
    project__annotations: Optional[str] = Field(
        alias="project.annotations", description="", example="nan"
    )
    project__corporate_id: Optional[str] = Field(
        ..., alias="project.corporate_id", description="", example="AP1122334v5"
    )  # ? EXTERNAL SOURCE **
    project__created: Optional[float] = Field(
        alias="project.created", description="", example="nan"
    )
    project__description: Optional[float] = Field(
        alias="project.description", description="", example="nan"
    )
    project__modified: Optional[float] = Field(
        alias="project.modified", description="", example="nan"
    )
    project__name: Optional[str] = Field(
        alias="project.name", description="", example="AP1122334v5"
    )  # ? EXTERNAL SOURCE
    project__pact_id: Optional[str] = Field(
        ..., alias="project.pact_id", description="", example="AP1122334v5"
    )  # ? EXTERNAL SOURCE **
    project__program: Optional[float] = Field(
        alias="project.program", description="", example="nan"
    )
    project__protocol_id: Optional[float] = Field(
        alias="project.protocol_id", description="", example="nan"
    )
    project__role: Optional[float] = Field(
        alias="project.role", description="", example="nan"
    )
    protocol__annotations: Optional[float] = Field(
        alias="protocol.annotations", description="", example="nan"
    )
    protocol__comments: Optional[float] = Field(
        alias="protocol.comments", description="", example="nan"
    )
    protocol__corporate_id: Optional[str] = Field(
        ..., alias="protocol.corporate_id", description="", example="1536 CORE FC 2C"
    )  # ? EXTERNAL SOURCE **
    protocol__description: Optional[float] = Field(
        alias="protocol.description", description="", example="nan"
    )
    protocol__name: Optional[float] = Field(
        alias="protocol.name", description="", example="nan"
    )
    protocol__version: Optional[float] = Field(
        alias="protocol.version", description="", example="nan"
    )
    sample__amount: Optional[str] = Field(
        ..., alias="sample.amount", description="", example="0.04"
    )  # **
    sample__amount_units: Optional[float] = Field(
        alias="sample.amount_units", description="", example="nan"
    )
    sample__annotations: Optional[float] = Field(
        alias="sample.annotations", description="", example="nan"
    )
    sample__concentration: Optional[condecimal(ge=0)] = Field(
        ..., alias="sample.concentration", description="", example="1.00E-004"
    )  # **
    sample__concentration_units: Optional[float] = Field(
        alias="sample.concentration_units", description="", example="nan"
    )
    sample__corporate_id: Optional[float] = Field(
        alias="sample.corporate_id", description="", example="nan"
    )
    sample__data: Optional[float] = Field(
        alias="sample.data", description="", example="nan"
    )
    sample__date_created: Optional[CustomAROSDateFormat] = Field(
        alias="sample.date_created", description="", example="nan"
    )
    sample__description: Optional[float] = Field(
        alias="sample.description", description="", example="nan"
    )
    sample__dlution_buffer: Optional[float] = Field(
        alias="sample.dlution_buffer", description="", example="nan"
    )
    sample__modified: Optional[float] = Field(
        alias="sample.modified", description="", example="nan"
    )
    sample__name: Optional[float] = Field(
        alias="sample.name", description="", example="nan"
    )
    sample__parent_id_fk: Optional[float] = Field(
        alias="sample.parent_id_fk", description="", example="nan"
    )
    sample__reference_id: Optional[float] = Field(
        alias="sample.reference_id", description="", example="nan"
    )
    sample__sample_type_fk: Optional[float] = Field(
        alias="sample.sample_type_fk", description="", example="nan"
    )
    sample__substance_fk: Optional[float] = Field(
        alias="sample.substance_fk", description="", example="nan"
    )
    sample__substance_role_fk: Optional[float] = Field(
        alias="sample.substance_role_fk", description="", example="nan"
    )
    sample__role_description: Optional[float] = Field(
        alias="sample_role.description", description="", example="nan"
    )
    sample__role_name: Optional[str] = Field(
        alias="sample_role.name", description="", example="PERTURBATION"
    )  # ? ENUM
    substance__annotations: Optional[float] = Field(
        alias="substance.annotations", description="", example="nan"
    )
    substance__comments: Optional[float] = Field(
        alias="substance.comments", description="", example="nan"
    )
    # substance__corporate_id: Optional[GSKcompoundId] = Field(
    #     ..., alias='substance.corporate_id', description=''
    #     , example='GSK1580675A')   # ? EXTERNAL SOURCE **
    substance__corporate_id: Optional[str] = Field(
        ..., alias="substance.corporate_id", description="", example="GSK1580675A"
    )  # ? EXTERNAL SOURCE **
    substance__data: Optional[str] = Field(
        alias="substance.data", description="", example="nan"
    )
    substance__lnb_ref: Optional[str] = Field(
        alias="substance.lnb_ref", description="", example="nan"
    )
    substance__lot_id: Optional[str] = Field(
        ..., alias="substance.lot_id", description="", example="NM208292-118A4"
    )  # ? EXTERNAL SOURCE **
    substance__modified: Optional[float] = Field(
        alias="substance.modified", description="", example="nan"
    )
    substance__name: Optional[str] = Field(
        alias="substance.name", description="", example="nan"
    )
    substance__substance_type_fk: Optional[float] = Field(
        alias="substance.substance_type_fk", description="", example="nan"
    )
    substance__synonyms: Optional[float] = Field(
        alias="substance.synonyms", description="", example="nan"
    )
    system_user_human__annotations: Optional[float] = Field(
        alias="system_user_human.annotations", description="", example="nan"
    )
    system_user_human__comments: Optional[float] = Field(
        alias="system_user_human.comments", description="", example="nan"
    )
    system_user_human__corporate_id: Optional[float] = Field(
        alias="system_user_human.corporate_id", description="", example="nan"
    )
    system_user_human__data: Optional[float] = Field(
        alias="system_user_human.data", description="", example="nan"
    )
    system_user_human__email: Optional[EmailStr] = Field(
        alias="system_user_human.email", description="", example="nan"
    )
    system_user_human__first_name: Optional[NameEmail] = Field(
        alias="system_user_human.first_name", description="", example="nan"
    )
    system_user_human__is_active: Optional[bool] = Field(
        alias="system_user_human.is_active", description="", example="nan"
    )
    system_user_human__last_name: Optional[NameEmail] = Field(
        alias="system_user_human.last_name", description="", example="nan"
    )
    transaction__annotations: Optional[str] = Field(
        alias="transaction.annotations", description="", example="nan"
    )
    transaction__application_fk: Optional[float] = Field(
        alias="transaction.application_fk", description="", example="nan"
    )
    transaction__application_version: Optional[str] = Field(
        alias="transaction.application_version", description="", example="nan"
    )
    transaction__comments: Optional[str] = Field(
        alias="transaction.comments", description="", example="nan"
    )
    transaction__host_os: Optional[str] = Field(
        alias="transaction.host_os", description="", example="nan"
    )
    transaction__hostname: Optional[str] = Field(
        alias="transaction.hostname", description="", example="nan"
    )
    transaction__human_fk: Optional[str] = Field(
        alias="transaction.human_fk", description="", example="nan"
    )
    transaction__job_id: Optional[int] = Field(
        alias="transaction.job_id", description="", example="nan"
    )
    transaction__procedure_date: Optional[CustomAROSDateFormat] = Field(
        alias="transaction.procedure_date", description="", example="nan"
    )
    transaction__procedure_id: Optional[float] = Field(
        alias="transaction.procedure_id", description="", example="nan"
    )
    transaction__procedure_name: Optional[str] = Field(
        alias="transaction.procedure_name", description="", example="nan"
    )
    transaction__procedure_path: Optional[FileUrl] = Field(
        alias="transaction.procedure_path", description="", example="nan"
    )
    transaction__procedure_version: Optional[str] = Field(
        alias="transaction.procedure_version", description="", example="nan"
    )
    transaction__transaction_guid: Optional[uuid.UUID] = Field(
        alias="transaction.transaction_guid",
        description="",
        example="82fd34db-3bf4-4b25-9d60-ddebfade260d",
    )
    transaction__transaction_type_fk: Optional[str] = Field(
        alias="transaction.transaction_type_fk", description="", example="nan"
    )
    well_type__description: Optional[str] = Field(
        alias="well_type.description", description="", example="nan"
    )
    well_type__name: Optional[str] = Field(
        ..., alias="well_type.name", description="", example="SAMPLE"
    )  # ? ENUM  **

    class Config:
        """Pydantic config class.

        Required parameters added.
        """

        anystr_strip_whitespace = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {CustomAROSDateFormat: CustomAROSDateFormat.to_str}

    @validator("*", pre=True)
    def standarize_empty_null_str_values(cls, value: Optional[str]) -> Optional[str]:
        """Remove flanking whitespace characters and return None\
        if empty and standarize Empty values.

        Args:
            value (Any): [description]

        Returns:
            Any: [description]
        """
        if isinstance(value, str):
            if not len(value.strip()):
                value = None
            elif value.upper() in [i.value for i in EmptyEnum.__members__.values()]:
                value = None
        elif pd.isna(value):
            value = None
        return value

    @classmethod
    def add_fields(cls, **field_definitions: Dict) -> None:
        """Add fields from arguments.

        Add new fields to model after instantiation.

        Args:
            field_definitions (Dict): named arguments

        Raises:
            Exception: [description]
        """
        new_fields: Dict[str, ModelField] = {}
        new_annotations: Dict[str, Optional[type]] = {}

        for f_name, f_def in field_definitions.items():
            if isinstance(f_def, tuple):
                try:
                    f_annotation, f_value = f_def
                except ValueError as e:
                    raise Exception(
                        "field definitions should either be a tuple of "
                        "(<type>, <default>) or just a "
                        "default value, unfortunately this means tuples as "
                        "default values are not allowed"
                    ) from e
            else:
                f_annotation, f_value = None, f_def

            if f_annotation:
                new_annotations[f_name] = f_annotation

            new_fields[f_name] = ModelField.infer(
                name=f_name,
                value=f_value,
                annotation=f_annotation,
                class_validators=None,
                config=cls.__config__,
            )

        cls.__fields__.update(new_fields)
        cls.__annotations__.update(new_annotations)

    @classmethod
    def add_fields_dict(cls, field_definitions: Dict[str, Tuple[str]]) -> None:
        """Validate and add model fields in a dict.

        Args:
            field_definitions (Dict[str, Tuple[str]]): [description]

        Raises:
            Exception: [description]
        """
        new_fields: Dict[str, ModelField] = {}
        new_annotations: Dict[str, Optional[type]] = {}

        for f_name, f_def in field_definitions.items():
            if isinstance(f_def, tuple):
                try:
                    f_annotation, f_value = f_def
                except ValueError as e:
                    raise Exception(
                        "field definitions should either be a tuple of "
                        "(<type>, <default>) or just a "
                        "default value, unfortunately this means tuples as "
                        "default values are not allowed"
                    ) from e
            else:
                f_annotation, f_value = None, f_def

            if f_annotation:
                new_annotations[f_name] = f_annotation

            new_fields[f_name] = ModelField.infer(
                name=f_name,
                value=f_value,
                annotation=f_annotation,
                class_validators=None,
                config=cls.__config__,
            )

        cls.__fields__.update(new_fields)
        cls.__annotations__.update(new_annotations)
