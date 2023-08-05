"""
Summary: SPFC module.

Analysis and Experiment Results validation models for
single Parameter Full Curve experiments.
"""

import decimal
from typing import Literal, Optional

from pydantic import condecimal, conint, constr, Field

from structured_data_validation.models.base import ModifiedBaseModel
from structured_data_validation.models.datatypes import (
    BooleanEnum,
    ControlsEnum,
    CurveIdPkiLogisticRegression4Params,
    CurveQCdescriptorCD,
    CustomAROSDateFormat,
    ExclussionEnum,
    FitStatusEnum,
    IrlsEnum,
    LevelPlateId,
    ObjectId,
    PassFailEnum,
    Percentage,
    PlateId,
    PlateWell,
    PxC50Enum,
    Qualifier,
    ThresholdDigit,
)


class SPFCExperimentResult(ModifiedBaseModel):
    """SPFC Experiment Result pydantic class.

    Args:
        ModifiedBaseModel ([type]): [description]
    """

    analysis_type__name: Literal["Single Parameter Full Curve"] = Field(
        ..., description="", example="Single Parameter Full Curve"
    )
    exclusion_date: Optional[CustomAROSDateFormat] = Field(
        alias="exclusion_date", description="", example=""
    )
    exclusion_reason: Optional[ExclussionEnum] = Field(
        alias="exclusion_reason", description="", example=""
    )
    exclusion_user: Optional[constr(max_length=100, min_length=20)] = Field(
        alias="exclusion_user", description="", example=""
    )
    ignore: Optional[bool] = Field(alias="ignore", description="", example="0")  # ?
    normalisation_group_1: Optional[float] = Field(
        alias="normalisation_group_1", description="", example="71.11"
    )
    object_id: Optional[ObjectId] = Field(
        alias="object_id", description="", example="OBJECT0001"
    )
    plate_id: Optional[PlateId] = Field(
        alias="plate_id", description="", example="U5H665A"
    )
    read1: Optional[condecimal(ge=0)] = Field(
        alias="read1", description="", example="3087"
    )
    read2: Optional[condecimal(ge=0)] = Field(
        alias="read2", description="", example="12776"
    )
    response: Optional[float] = Field(alias="response", description="", example="71.11")
    robust_corrected_transformed_raw: Optional[condecimal(ge=0)] = Field(
        alias="robust_corrected_transformed_raw", description="", example="0.24"
    )  # ?
    robust_weighted: Optional[BooleanEnum] = Field(
        alias="robust_weighted", description="", example="No"
    )
    transformed_raw: Optional[condecimal(ge=0)] = Field(
        alias="transformed_raw", description="", example="0.24"
    )


class SPFCAnalysisResult(ModifiedBaseModel):
    """SPFC Analysis Result pydantic class.

    Args:
        ModifiedBaseModel ([type]): [description]
    """

    analysis_type__name: Literal["Single Parameter Full Curve"] = Field(
        ..., description="", example="Single Parameter Full Curve"
    )
    asym_max_cl_lower_validated: Optional[float] = Field(
        alias="asym_max_cl_lower_validated", description="", example="109.8"
    )
    asym_max_cl_upper_validated: Optional[int] = Field(
        alias="asym_max_cl_upper_validated", description="", example="120"
    )
    asym_max_validated: Optional[int] = Field(
        alias="asym_max_validated", description="", example="120"
    )
    asym_min_cl_lower_validated: Optional[float] = Field(
        alias="asym_min_cl_lower_validated", description="", example="-8.36"
    )
    asym_min_cl_upper_validated: Optional[float] = Field(
        alias="asym_min_cl_upper_validated", description="", example="-4.04"
    )
    asym_min_validated: Optional[float] = Field(
        alias="asym_min_validated", description="", example="-6.22"
    )
    ce_gesd_outliers: Optional[bool] = Field(
        alias="ce_gesd_outliers", description="", example="False"
    )
    cmpd_qc_flag: Optional[PassFailEnum] = Field(
        alias="cmpd_qc_flag", description="", example="PASS"
    )
    control: Optional[str] = Field(alias="control", description="", example="")
    curve_exclusion_flag_threshold: Optional[bool] = Field(
        alias="curve_exclusion_flag_threshold", description="", example="True"
    )
    curve_id_pki_logistic_regression_4_param: Optional[
        CurveIdPkiLogisticRegression4Params
    ] = Field(
        alias="curve_id_pki_logistic_regression_4_param",
        description="",
        example="id5f379701eaa34305ba1d2f36459ce2f2-351",
    )
    curve_qc_descriptor: Optional[CurveQCdescriptorCD] = Field(
        alias="curve_qc_descriptor", description="", example="Passed All Fit Validators"
    )
    ec50_log10_pki_logistic_regression_4_param: Optional[float] = Field(
        alias="ec50_log10_pki_logistic_regression_4_param",
        description="",
        example="-4.11",
    )
    ec50_lower_95_percent_interval_pki_logistic_regression_4_param: Optional[
        decimal.Decimal
    ] = Field(
        alias="ec50_lower_95_percent_interval_pki_logistic_regression_4_param",
        description="",
        example="7.16e-05",
    )
    ec50_pki_logistic_regression_4_param: Optional[decimal.Decimal] = Field(
        alias="ec50_pki_logistic_regression_4_param", description="", example="7.75e-05"
    )
    ec50_upper_95_percent_interval_pki_logistic_regression_4_param: Optional[
        decimal.Decimal
    ] = Field(
        alias="ec50_upper_95_percent_interval_pki_logistic_regression_4_param",
        description="",
        example="8.45e-05",
    )
    exclusion_date: Optional[CustomAROSDateFormat] = Field(
        alias="exclusion_date", description="", example=""
    )
    exclusion_reason: Optional[ExclussionEnum] = Field(
        alias="exclusion_reason", description="", example=""
    )
    exclusion_user: Optional[constr(max_length=100, min_length=20)] = Field(
        alias="exclusion_user", description="", example=""
    )
    fc_qc_tag: Optional[str] = Field(alias="fc_qc_tag", description="", example="")
    fit_status_pki_logistic_regression_4_param: Optional[FitStatusEnum] = Field(
        alias="fit_status_pki_logistic_regression_4_param", description="", example="OK"
    )
    hc_auto_exclusion_tag: Optional[str] = Field(
        alias="hc_auto_exclusion_tag", description="", example=""
    )
    hc_final_exclusion_tag: Optional[str] = Field(
        alias="hc_final_exclusion_tag", description="", example=""
    )
    hc_user_exclusion_tag: Optional[str] = Field(
        alias="hc_user_exclusion_tag", description="", example=""
    )
    hc_user_preprocessing_exclusion_tag: Optional[str] = Field(
        alias="hc_user_preprocessing_exclusion_tag", description="", example=""
    )
    hill_pki_logistic_regression_4_param: Optional[float] = Field(
        alias="hill_pki_logistic_regression_4_param", description="", example="1.82"
    )
    inflection_pki_logistic_regression_4_param: Optional[float] = Field(
        alias="inflection_pki_logistic_regression_4_param",
        description="",
        example="0.0",
    )
    irls: Optional[IrlsEnum] = Field(alias="irls", description="", example="Untagged")
    irls_weights: Optional[condecimal(ge=0, le=1)] = Field(
        alias="irls_weights", description="", example="1"
    )
    is_gesd_within_specific_limits: Optional[bool] = Field(
        alias="is_gesd_within_specific_limits", description="", example="False"
    )
    is_max_response_gtoe_to_inactive_threshold: Optional[bool] = Field(
        alias="is_max_response_gtoe_to_inactive_threshold",
        description="",
        example="True",
    )
    is_max_response_lt_poorly_active_threshold: Optional[bool] = Field(
        alias="is_max_response_lt_poorly_active_threshold",
        description="",
        example="True",
    )
    is_min_response_ltoe_to_highly_active_threshold: Optional[bool] = Field(
        alias="is_min_response_ltoe_to_highly_active_threshold",
        description="",
        example="True",
    )
    is_xc50_cl_ratio_gt_cl_ratio_threshold: Optional[bool] = Field(
        alias="is_xc50_cl_ratio_gt_cl_ratio_threshold", description="", example="False"
    )
    level_plate_id: Optional[LevelPlateId] = Field(
        alias="level_plate_id",
        description="",
        example="[U5H665A].[OBJECT0001].[NM208292-118A4]",
    )
    mapped_well_type: Optional[ControlsEnum] = Field(
        alias="mapped_well_type", description="", example="None"
    )
    max_concentration_tested: Optional[condecimal(ge=0)] = Field(
        alias="max_concentration_tested", description="", example="4"
    )
    max_lower_95_percent_interval_pki_logistic_regression_4_param: Optional[
        float
    ] = Field(
        alias="max_lower_95_percent_interval_pki_logistic_regression_4_param",
        description="",
        example="109.8",
    )
    max_pki_logistic_regression_4_param: Optional[condecimal(ge=0)] = Field(
        alias="max_pki_logistic_regression_4_param", description="", example="120"
    )
    max_response_concentration: Optional[condecimal(ge=0)] = Field(
        alias="max_response_concentration", description="", example="0.0001"
    )
    max_response_samples: Optional[decimal.Decimal] = Field(
        alias="max_response_samples", description="", example="71.11"
    )
    max_upper_95_percent_interval_pki_logistic_regression_4_param: Optional[
        condecimal(ge=0)
    ] = Field(
        alias="max_upper_95_percent_interval_pki_logistic_regression_4_param",
        description="",
        example="120",
    )
    min_concentration_tested: Optional[condecimal(ge=0)] = Field(
        alias="min_concentration_tested", description="", example="7.01"
    )
    min_lower_95_percent_interval_pki_logistic_regression_4_param: Optional[
        float
    ] = Field(
        alias="min_lower_95_percent_interval_pki_logistic_regression_4_param",
        description="",
        example="-8.36",
    )
    min_pki_logistic_regression_4_param: Optional[float] = Field(
        alias="min_pki_logistic_regression_4_param", description="", example="-6.22"
    )
    min_response_concentration: Optional[condecimal(ge=0)] = Field(
        alias="min_response_concentration", description="", example="3.91e-07"
    )
    min_response_samples: Optional[float] = Field(
        alias="min_response_samples", description="", example="-12.75"
    )  # ?
    min_upper_95_percent_interval_pki_logistic_regression_4_param: Optional[
        float
    ] = Field(
        alias="min_upper_95_percent_interval_pki_logistic_regression_4_param",
        description="",
        example="-4.04",
    )
    normalisation_group_1: Optional[float] = Field(
        alias="normalisation_group_1", description="", example="71.11"
    )
    number_curve_points: Optional[conint(ge=0)] = Field(
        alias="number_curve_points", description="", example="11"
    )
    number_curve_points_after_irls: Optional[conint(ge=0)] = Field(
        alias="number_curve_points_after_irls", description="", example="11"
    )
    number_of_curve_points_gtoe_min_number_points: Optional[bool] = Field(
        alias="number_of_curve_points_gtoe_min_number_points",
        description="",
        example="True",
    )
    number_sample_curve_points: Optional[conint(ge=0)] = Field(
        alias="number_sample_curve_points", description="", example="11"
    )
    number_sample_curve_points_after_irls: Optional[conint(ge=0)] = Field(
        alias="number_sample_curve_points_after_irls", description="", example="11"
    )
    number_sample_curve_points_after_irls_gtoe_min_number_points: Optional[
        bool
    ] = Field(
        alias="number_sample_curve_points_after_irls_gtoe_min_number_points",
        description="",
        example="True",
    )
    object_id: Optional[ObjectId] = Field(
        alias="object_id", description="", example="OBJECT0001"
    )
    percent_cv: Optional[Percentage] = Field(
        alias="percent_cv", description="", example="None"
    )
    percent_cv_cutoff: Optional[Percentage] = Field(
        alias="percent_cv_cutoff", description="", example=""
    )
    plate_based_qc: Optional[PassFailEnum] = Field(
        alias="plate_based_qc", description="", example="Pass"
    )
    plate_id: Optional[PlateId] = Field(
        alias="plate_id", description="", example="U5H665A"
    )
    # plate_well: Optional[constr(regex=r"^(?P<head>[H]{1})(?P<mid>\d{3})\
    # (?P<tail>[G]{1}\w{2})(?P<sep>:)(?P<wellid>\w{1}\d{1,2})")] =
    # Field(alias='plate_well', description='', example='U5H665A:A1')
    plate_well: Optional[PlateWell] = Field(
        alias="plate_well", description="", example="U5H665A:A1"
    )
    # pxc50: Optional[constr(regex=r"^(?P<symbol>[<>=]{0,1})(?P<space>\s{0,1})\
    # (?P<posdigit>\d+)(?P<sep>.{0,1})(?P<decimal>\d+)$")]
    # = Field(alias='pxc50', description='', example='< 4.11')
    pxc50: Optional[ThresholdDigit] = Field(
        alias="pxc50", description="", example="< 4.11"
    )
    pxc50_cl_lower_validated: Optional[float] = Field(
        alias="pxc50_cl_lower_validated", description="", example="4.14"
    )
    pxc50_cl_upper_validated: Optional[float] = Field(
        alias="pxc50_cl_upper_validated", description="", example="4.07"
    )
    pxc50_number: Optional[float] = Field(
        alias="pxc50_number", description="", example="4.11"
    )
    pxc50_number_validated: Optional[float] = Field(
        alias="pxc50_number_validated", description="", example="4.11"
    )
    pxc50_type: Optional[PxC50Enum] = Field(
        alias="pxc50_type", description="", example="pIC50"
    )
    # pxc50_validated: Optional[constr(regex=r"^(?P<symbol>[<>]{0,1})
    # (?P<space>\s{0,1})(?P<posdigit>\d+)(?P<sep>.{0,1})(?P<decimal>\d+)")] =
    # Field(alias='pxc50_validated', description='', example='4.11')
    pxc50_validated: Optional[ThresholdDigit] = Field(
        alias="pxc50_validated", description="", example="4.11"
    )
    qualifier: Optional[Qualifier] = Field(
        alias="qualifier", description="", example="="
    )
    r_squared_pki_logistic_regression_4_param: Optional[float] = Field(
        alias="r_squared_pki_logistic_regression_4_param",
        description="",
        example="0.98",
    )
    rcw_flag: Optional[PassFailEnum] = Field(
        alias="rcw_flag", description="", example="None"
    )
    response: Optional[float] = Field(alias="response", description="", example="71.11")
    robust_corrected_transformed_raw: Optional[float] = Field(
        alias="robust_corrected_transformed_raw", description="", example="0.24"
    )
    robust_statistics_mean: Optional[condecimal(ge=0)] = Field(
        alias="robust_statistics_mean", description="", example="None"
    )
    robust_statistics_standard_deviation: Optional[condecimal(ge=0)] = Field(
        alias="robust_statistics_standard_deviation", description="", example="None"
    )
    robust_weighted: Optional[BooleanEnum] = Field(
        alias="robust_weighted", description="", example="No"
    )
    robust_weighted_control_transformed_raw: Optional[condecimal(ge=0)] = Field(
        alias="robust_weighted_control_transformed_raw", description="", example="None"
    )
    robust_zprime: Optional[float] = Field(
        alias="robust_zprime", description="", example="0.76"
    )
    robust_zprime_cutoff: Optional[float] = Field(
        alias="robust_zprime_cutoff", description="", example="0"
    )
    slope_validated: Optional[float] = Field(
        alias="slope_validated", description="", example="1.82"
    )
    test_level_qc: Optional[PassFailEnum] = Field(
        alias="test_level_qc", description="", example="Pass"
    )
    # Create concentration data type.
    third_concentration_tested: Optional[condecimal(ge=0)] = Field(
        alias="third_concentration_tested", description="", example="4.6"
    )
    top_concentration: Optional[condecimal(ge=0)] = Field(
        alias="top_concentration", description="", example="0.0001"
    )
    transformed_raw: Optional[condecimal(ge=0)] = Field(
        alias="transformed_raw", description="", example="0.24"
    )
    xc50_cl_ratio: Optional[condecimal(ge=0)] = Field(
        alias="xc50_cl_ratio", description="", example="0.0718"
    )
