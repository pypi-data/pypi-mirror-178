"""
Summary: MPFC module.

Analysis and Experiment results nested data structure validation
pydantic models.
"""

import decimal
from typing import Literal, Optional

from pydantic import condecimal, conint, Field

from structured_data_validation.models.base import ModifiedBaseModel
from structured_data_validation.models.datatypes import (
    BooleanEnum,
    ControlsEnum,
    CurveIdPkiLogisticRegression4Params,
    CurveQCdescriptorCD,
    FitStatusEnum,
    IrlsEnum,
    LevelPlateId,
    ObjectId,
    PassFailEnum,
    Percentage,
    PlateId,
    PxC50Enum,
    Qualifier,
    ThresholdDigit,
)


class MPFCExperimentResult(ModifiedBaseModel):
    """MPFC Experiment Result Class.

    Args:
        ModifiedBaseModel ([type]): [description]
    """

    # analysis_type__name: Literal["Multiple Parameter Full Curve"] = Field(...,
    analysis_type__name: Literal["Multi Parameter Full Curve"] = Field(
        ..., description="", example="Multiple Parameter Full Curve"
    )
    ignore: Optional[bool] = Field(alias="ignore", description="", example="None")
    normalisation_group_1: Optional[float] = Field(
        alias="normalisation_group_1", description="", example="None"
    )
    normalisation_group_2: Optional[float] = Field(
        alias="normalisation_group_2", description="", example="None"
    )
    object_id: Optional[ObjectId] = Field(alias="object_id", description="", example="")
    plate_id: Optional[PlateId] = Field(
        alias="plate_id", description="", example="P00P7G6"
    )
    read1: Optional[condecimal(ge=0)] = Field(
        alias="read1", description="", example="None"
    )
    response: Optional[float] = Field(alias="response", description="", example="None")
    robust_corrected_transformed_raw: Optional[condecimal(ge=0)] = Field(
        alias="robust_corrected_transformed_raw", description="", example="None"
    )
    robust_weighted: Optional[BooleanEnum] = Field(
        alias="robust_weighted", description="", example="None"
    )
    transformed_raw: Optional[condecimal(ge=0)] = Field(
        alias="transformed_raw", description="", example="None"
    )


class MPFCAnalysisResult(ModifiedBaseModel):
    """MPFC Analysis Result Class.

    Args:
        ModifiedBaseModel ([type]): Validators List
    """

    # analysis_type__name: Literal["Multiple Parameter Full Curve"] = Field(...,
    analysis_type__name: Literal["Multi Parameter Full Curve"] = Field(
        ..., description="", example="Multiple Parameter Full Curve"
    )
    asym_max_cl_lower_validated: Optional[float] = Field(
        alias="asym_max_cl_lower_validated", description="", example="None"
    )
    asym_max_cl_upper_validated: Optional[int] = Field(
        alias="asym_max_cl_upper_validated", description="", example="None"
    )
    asym_max_validated: Optional[int] = Field(
        alias="asym_max_validated", description="", example="None"
    )
    asym_min_cl_lower_validated: Optional[float] = Field(
        alias="asym_min_cl_lower_validated", description="", example="None"
    )
    asym_min_cl_upper_validated: Optional[float] = Field(
        alias="asym_min_cl_upper_validated", description="", example="None"
    )
    asym_min_validated: Optional[float] = Field(
        alias="asym_min_validated", description="", example="None"
    )
    ce_gesd_outliers: Optional[bool] = Field(
        alias="ce_gesd_outliers", description="", example="False"
    )
    cmpd_qc_flag: Optional[PassFailEnum] = Field(
        alias="cmpd_qc_flag", description="", example="None"
    )
    curve_exclusion_flag_threshold: Optional[bool] = Field(
        alias="curve_exclusion_flag_threshold", description="", example="None"
    )
    curve_id_pki_logistic_regression_4_param: Optional[
        CurveIdPkiLogisticRegression4Params
    ] = Field(
        alias="curve_id_pki_logistic_regression_4_param", description="", example="None"
    )
    curve_qc_descriptor: Optional[CurveQCdescriptorCD] = Field(
        alias="cuve_qc_descriptor", description="", example="None"
    )
    ec50_log10_pki_logistic_regression_4_param: Optional[float] = Field(
        alias="ec50_log10_pki_logistic_regression_4_param",
        description="",
        example="None",
    )
    ec50_lower_95_percent_interval_pki_logistic_regression_4_param: Optional[
        decimal.Decimal
    ] = Field(
        alias="ec50_lower_95_percent_interval_pki_logistic_regression_4_param",
        description="",
        example="None",
    )
    ec50_pki_logistic_regression_4_param: Optional[decimal.Decimal] = Field(
        alias="ec50_pki_logistic_regression_4_param", description="", example="None"
    )
    ec50_upper_95_percent_interval_pki_logistic_regression_4_param: Optional[
        decimal.Decimal
    ] = Field(
        alias="ec50_upper_95_percent_interval_pki_logistic_regression_4_param",
        description="",
        example="None",
    )
    fc_qc_tag: Optional[str] = Field(alias="fc_qc_tag", description="", example="")
    fit_status_pki_logistic_regression_4_param: Optional[FitStatusEnum] = Field(
        alias="fit_status_pki_logistic_regression_4_param",
        description="",
        example="None",
    )
    hc_auto_exclusion_tag: Optional[str] = Field(
        alias="hc_auto_exclusion_tag", description="", example=""
    )
    hc_final_exclusion_tag: Optional[str] = Field(
        alias="hc_final_exclusion_tag", description="", example=""
    )
    hill_pki_logistic_regression_4_param: Optional[float] = Field(
        alias="hill_pki_logistic_regression_4_param", description="", example="None"
    )
    inflection_pki_logistic_regression_4_param: Optional[float] = Field(
        alias="inflection_pki_logistic_regression_4_param",
        description="",
        example="None",
    )
    irls: Optional[IrlsEnum] = Field(alias="irls", description="", example="Untagged")
    irls_weights: Optional[condecimal(ge=0, le=1)] = Field(
        alias="irls_weights", description="", example="None"
    )
    is_gesd_within_specific_limits: Optional[bool] = Field(
        alias="is_gesd_within_specific_limits", description="", example="None"
    )
    is_max_response_gtoe_to_threshold: Optional[bool] = Field(
        alias="is_max_response_gtoe_to_threshold", description="", example="None"
    )
    is_max_response_lt_poorly_active_threshold: Optional[bool] = Field(
        alias="is_max_response_lt_poorly_active_threshold",
        description="",
        example="None",
    )
    is_min_response_ltoe_to_highly_active_threshold: Optional[bool] = Field(
        alias="is_min_response_ltoe_to_highly_active_threshold",
        description="",
        example="None",
    )
    is_xc50_cl_ratio_gt_cl_ratio_threshold: Optional[bool] = Field(
        alias="is_xc50_cl_ratio_gt_cl_ratio_threshold", description="", example="None"
    )
    level_plate_id: Optional[LevelPlateId] = Field(
        alias="level_plate_id",
        description="",
        example="[P00P7G6].[Median FL2-A of IL-10].[].[]",
    )
    mapped_well_type: Optional[ControlsEnum] = Field(
        alias="mapped_well_type", description="", example="None"
    )
    max_concentration_tested: Optional[condecimal(ge=0)] = Field(
        alias="max_concentration_tested", description="", example="None"
    )
    max_lower_95_percent_interval_pki_logistic_regression_4_param: Optional[
        float
    ] = Field(
        alias="max_lower_95_percent_interval_pki_logistic_regression_4_param",
        description="",
        example="None",
    )
    max_pki_logistic_regression_4_param: Optional[condecimal(ge=0)] = Field(
        alias="max_pki_logistic_regression_4_param", description="", example="None"
    )
    max_response_concentration: Optional[condecimal(ge=0)] = Field(
        alias="max_response_concentration", description="", example="None"
    )
    max_response_samples: Optional[decimal.Decimal] = Field(
        alias="max_response_samples", description="", example="None"
    )
    max_upper_95_percent_interval_pki_logistic_regression_4_param: Optional[
        condecimal(ge=0)
    ] = Field(
        alias="max_upper_95_percent_interval_pki_logistic_regression_4_param",
        description="",
        example="None",
    )
    min_concentration_tested: Optional[condecimal(ge=0)] = Field(
        alias="min_concentration_tested", description="", example="None"
    )
    min_lower_95_percent_interval_pki_logistic_regression_4_param: Optional[
        float
    ] = Field(
        alias="min_lower_95_percent_interval_pki_logistic_regression_4_param",
        description="",
        example="None",
    )
    min_pki_logistic_regression_4_param: Optional[float] = Field(
        alias="min_pki_logistic_regression_4_param", description="", example="None"
    )
    min_response_concentration: Optional[condecimal(ge=0)] = Field(
        alias="min_response_concentration", description="", example="None"
    )
    min_response_samples: Optional[float] = Field(
        alias="min_response_samples", description="", example="None"
    )
    min_upper_95_percent_interval_pki_logistic_regression_4_param: Optional[
        float
    ] = Field(
        alias="min_upper_95_percent_interval_pki_logistic_regression_4_param",
        description="",
        example="None",
    )
    normalisation_group_1: Optional[float] = Field(
        alias="normalisation_group_1", description="", example="None"
    )
    number_curve_points: Optional[conint(ge=0)] = Field(
        alias="number_curve_points", description="", example="0"
    )
    number_curve_points_after_irls: Optional[conint(ge=0)] = Field(
        alias="number_curve_points_after_irls", description="", example="0"
    )
    number_of_curve_points_gtoe_min_number_points: Optional[bool] = Field(
        alias="number_of_curve_points_gtoe_min_number_points",
        description="",
        example="None",
    )
    number_sample_curve_points: Optional[conint(ge=0)] = Field(
        alias="number_sample_curve_points", description="", example="None"
    )
    number_sample_curve_points_after_irls: Optional[conint(ge=0)] = Field(
        alias="number_sample_curve_points_after_irls", description="", example="None"
    )
    number_sample_curve_points_after_irls_gtoe_min_number_points: Optional[
        bool
    ] = Field(
        alias="number_sample_curve_points_after_irls_gtoe_min_number_points",
        description="",
        example="None",
    )
    object_id: Optional[ObjectId] = Field(alias="object_id", description="", example="")
    percent_cv: Optional[Percentage] = Field(
        alias="percent_cv", description="", example="None"
    )
    percent_cv_cutoff: Optional[Percentage] = Field(
        alias="percent_cv_cutoff", description="", example="None"
    )
    plate_based_qc: Optional[PassFailEnum] = Field(
        alias="plate_based_qc", description="", example="Fail"
    )
    plate_id: Optional[PlateId] = Field(
        alias="plate_id", description="", example="P00P7G6"
    )
    # plate_well: Optional[PlateWell] = Field(
    #     alias='plate_well', description='', example='None')
    plate_well: Optional[str] = Field(
        alias="plate_well", description="", example="None"
    )
    pxc50: Optional[ThresholdDigit] = Field(
        alias="pxc50", description="", example="None"
    )
    pxc50_cl_lower_validated: Optional[float] = Field(
        alias="pxc50_cl_lower_validated", description="", example="None"
    )
    pxc50_cl_upper_validated: Optional[float] = Field(
        alias="pxc50_cl_upper_validated", description="", example="None"
    )
    pxc50_number: Optional[float] = Field(
        alias="pxc50_number", description="", example="None"
    )
    pxc50_number_validated: Optional[float] = Field(
        alias="pxc50_number_validated", description="", example="None"
    )
    pxc50_type: Optional[PxC50Enum] = Field(
        alias="pxc50_type", description="", example="pEC50"
    )
    pxc50_validated: Optional[ThresholdDigit] = Field(
        alias="pxc50_validated", description="", example="None"
    )
    qualifier: Optional[Qualifier] = Field(
        alias="qualifier", description="", example="None"
    )
    r_squared_pki_logistic_regression_4_param: Optional[float] = Field(
        alias="r_squared_pki_logistic_regression_4_param",
        description="",
        example="None",
    )
    rcw_flag: Optional[PassFailEnum] = Field(
        alias="rcw_flag", description="", example="None"
    )
    response: Optional[float] = Field(alias="response", description="", example="None")
    robust_corrected_transformed_raw: Optional[condecimal(ge=0)] = Field(
        alias="robust_corrected_transformed_raw", description="", example="None"
    )
    robust_weighted: Optional[BooleanEnum] = Field(
        alias="robust_weighted", description="", example="None"
    )
    robust_weighted_control_transformed_raw: Optional[condecimal(ge=0)] = Field(
        alias="robust_weighted_control_transformed_raw", description="", example="None"
    )
    robust_zprime: Optional[float] = Field(
        alias="robust_zprime", description="", example="-0.82"
    )
    robust_zprime_cutoff: Optional[float] = Field(
        alias="robust_zprime_cutoff", description="", example="0"
    )
    slope_validated: Optional[float] = Field(
        alias="slope_validated", description="", example="None"
    )
    test_level_qc: Optional[PassFailEnum] = Field(
        alias="test_level_qc", description="", example="Fail"
    )
    top_concentration: Optional[condecimal(ge=0)] = Field(
        alias="top_concentration", description="", example="None"
    )
    transformed_raw: Optional[condecimal(ge=0)] = Field(
        alias="transformed_raw", description="", example="None"
    )
    xc50_cl_ratio: Optional[condecimal(ge=0)] = Field(
        alias="xc50_cl_ratio", description="", example="None"
    )
