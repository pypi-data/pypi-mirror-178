"""
Summary: MPSC module.

Analysis and Experiment result validation pydantic
models for Multi Parameter Single Curve.
"""

from typing import Literal, Optional

from pydantic import condecimal, Field

from structured_data_validation.models.base import ModifiedBaseModel
from structured_data_validation.models.datatypes import (
    BooleanEnum,
    ControlsEnum,
    HitEnum,
    IrlsEnum,
    ObjectId,
    PassFailEnum,
    Percentage,
    PlateId,
    PxC50Enum,
    ResponseTypeEnum,
)


class MPSCExperimentResult(ModifiedBaseModel):
    """MPSC Experiment Result pydantic class.

    Args:
        ModifiedBaseModel ([type]): [description]
    """

    analysis_type__name: Literal["Multi Parameter Single Concentration"] = Field(
        ..., description="", example="Multiple Parameter Single Concentration"
    )
    ignore: Optional[bool] = Field(alias="ignore", description="", example="0")
    object_id: Optional[ObjectId] = Field(
        alias="object_id", description="", example="OBJECT0001"
    )
    plate_id: Optional[PlateId] = Field(
        alias="plate_id", description="", example="H005Q7A"
    )
    read1: Optional[condecimal(ge=0)] = Field(
        alias="read1", description="", example="2559308.79"
    )
    response: Optional[float] = Field(
        alias="response", description="", example="-18.64"
    )
    response_type: Optional[ResponseTypeEnum] = Field(
        alias="response_type", description="", example="PERCENT INHIBITION"
    )
    robust_corrected_transformed_raw: Optional[condecimal(ge=0)] = Field(
        alias="robust_corrected_transformed_raw", description="", example="2559308.79"
    )
    robust_weighted: Optional[BooleanEnum] = Field(
        alias="robust_weighted", description="", example="No"
    )
    transformed_raw: Optional[condecimal(ge=0)] = Field(
        alias="transformed_raw", description="", example="2559308.79"
    )


class MPSCAnalysisResult(ModifiedBaseModel):
    """MPSC Analysis Result pydantic class.

    Args:
        ModifiedBaseModel ([type]): [description]
    """

    analysis_type__name: Literal["Multi Parameter Single Concentration"] = Field(
        ..., description="", example="Multiple Parameter Single Concentration"
    )
    ce_gesd_outliers: Optional[bool] = Field(
        alias="ce_gesd_outliers", description="", example="False"
    )
    control: Optional[str] = Field(alias="control", description="", example="")
    hc_auto_exclusion_tag: Optional[str] = Field(
        alias="hc_auto_exclusion_tag", description="", example=""
    )
    hc_final_exclusion_tag: Optional[str] = Field(
        alias="hc_final_exclusion_tag", description="", example=""
    )
    hc_user_exclusion_tag: Optional[str] = Field(
        alias="hc_user_exclusion_tag", description="", example=""
    )
    hc_user_pre_processing_exclusion_tag: Optional[str] = Field(
        alias="hc_user_pre_processing_exclusion_tag", description="", example=""
    )
    hit: Optional[HitEnum] = Field(alias="hit", description="", example="ROBUST-ACTIVE")
    irls: Optional[IrlsEnum] = Field(alias="irls", description="", example="Untagged")
    mapped_well_type: Optional[ControlsEnum] = Field(
        alias="mapped_well_type", description="", example="None"
    )
    normalisation_group_1: Optional[float] = Field(
        alias="normalisation_group_1", description="", example="-18.64"
    )
    object_id: Optional[ObjectId] = Field(
        alias="object_id", description="", example="OBJECT0001"
    )
    percent_cv: Optional[Percentage] = Field(
        alias="percent_cv", description="", example="None"
    )
    percent_left_tail: Optional[Percentage] = Field(
        alias="percent_left_tail", description="", example="0.3"
    )
    percent_left_tail_cutoff: Optional[Percentage] = Field(
        alias="percent_left_tail_cutoff", description="", example="-61.73"
    )
    percent_right_tail: Optional[Percentage] = Field(
        alias="percent_right_tail", description="", example="6.08"
    )
    percent_right_tail_cutoff: Optional[Percentage] = Field(
        alias="percent_right_tail_cutoff", description="", example="78.13"
    )
    plate_based_qc: Optional[PassFailEnum] = Field(
        alias="plate_based_qc", description="", example="Pass"
    )
    plate_id: Optional[PlateId] = Field(
        alias="plate_id", description="", example="H005Q7A"
    )
    pxc50_type: Optional[PxC50Enum] = Field(
        alias="pxc50_type", description="", example="pIC50"
    )
    rcw_flag: Optional[PassFailEnum] = Field(
        alias="rcw_flag", description="", example="None"
    )
    robust_hit_percent_cutoff: Optional[Percentage] = Field(
        alias="robust_hit_percent_cutoff", description="", example="40.26"
    )
    robust_statistics_mean: Optional[condecimal(ge=0)] = Field(
        alias="robust_statistics_mean", description="", example="None"
    )
    robust_statistics_standard_deviation: Optional[condecimal(ge=0)] = Field(
        alias="robust_statistics_standard_deviation", description="", example="None"
    )
    robust_weighted_control_transformed_raw: Optional[condecimal(ge=0)] = Field(
        alias="robust_weighted_control_transformed_raw", description="", example="None"
    )
    robust_zprime: Optional[float] = Field(
        alias="robust_z_prime", description="", example="0.7"
    )  # Inconsistent naming robust_z_prime
    ss_qc_tag: Optional[str] = Field(
        alias="ss_qc_tag", description="", example=""
    )  # No idea
    test_level_qc: Optional[PassFailEnum] = Field(
        alias="test_level_qc", description="", example="Pass"
    )
    well_level_qc_summary: Optional[PassFailEnum] = Field(
        alias="well_level_qc_summary", description="", example="Pass"
    )
    z_prime_cutoff: Optional[float] = Field(
        alias="z_prime_cutoff", description="", example="0.4"
    )  # Inconsistent naming
