"""
Summary: Model's data types for validation.

Custom data types for AROS csv files validation.
"""

from datetime import datetime, timezone
import enum
import re
from typing import Generator, Union


class MyEnumMeta(enum.EnumMeta):
    """Custom mixing class for Enum Types.

    Args:
        enum ([type]): [description]
    """

    @classmethod
    def __contains__(cls, item: str) -> bool:
        """Check enum memebers in a given class, by value.

        Args:
            item (str): [description]

        Returns:
            bool: [description]
        """
        if isinstance(item, str):
            return item.upper() in [v.value for v in cls.__members__.values()]
        else:
            return False

    def __getitem__(self, item: str) -> str:
        """Get attribute by name.

        Get attribute by name.

        Args:
            item (str): item name.

        Returns:
            str: item value after cleanning.
        """
        if isinstance(item, str):
            item = (
                item.upper()
                .replace(" ", "_")
                .replace(".", "")
                .replace("-", "")
                .replace("<", "LT")
                .replace(">", "GT")
                .replace("(", "")
                .replace(")", "")
            )
        return super().__getitem__(item).name

    # def __str__(self) -> str:
    #     """Format enum to string.
    #
    #     Returns:
    #         str: [description]
    #     """
    #     return str(self.name)

    def __call__(self, value: str) -> str:
        """Call __getitem__ method by value.

        Args:
            value (str): value to get.

        Returns:
            str: value string.
        """
        return self.__getitem__(value)


class PxC50Enum(enum.Enum, metaclass=MyEnumMeta):
    """Documentation for PxC50Enum.

    Args:
        enum (enum.Enum): custuom enum class.

    Returns:
        [type]: [description]
    """

    PIC50 = "PIC50"
    PEC50 = "PEC50"
    PMEC = "PMEC"

    def __str__(self) -> str:
        """Format enum values to string.

        Returns:
            str: [description]
        """
        return str(self.value)


class ControlsEnum(enum.Enum, metaclass=MyEnumMeta):
    """Documentation for ControlsEnum.

    Args:
        enum ([type]): [description]
        metaclass ([type], optional): [description]. Defaults to MyEnumMeta.

    Returns:
        [type]: [description]
    """

    SAMPLE = "SAMPLE"
    NEGATIVE_CONTROL = "NEGATIVE_CONTROL"
    POSITIVE_CONTROL = "POSITIVE_CONTROL"
    POSITIVE_CONTROL1 = "POSITIVE_CONTROL1"
    POSITIVE_CONTROL2 = "POSITIVE_CONTROL2"

    def __str__(self) -> str:
        """Format enum values to string.

        Returns:
            str: [description]
        """
        return str(self.value)


class CurveQCdescriptorCD(enum.Enum, metaclass=MyEnumMeta):
    """Documentation for CurveQCdescriptorCD.

    Args:
        enum ([type]): [description]
        metaclass ([type], optional): [description]. Defaults to MyEnumMeta.

    Returns:
        [type]: [description]
    """

    INACTIVE = "INACTIVE"
    PASSED_ALL_FIT_VALIDATORS = "PASSED_ALL_FIT_VALIDATORS"
    IRLS_SENSITIVITY_VALIDATION_FAILED = "IRLS_SENSITIVITY_VALIDATION_FAILED"
    HIGLY_ACTIVE = "HIGLY_ACTIVE"
    POORLY_ACTIVE = "POORLY ACTIVE"
    FAILED_XC50_CL_RATIO_THRESHOLD = "Failed XC50 CL Ratio Threshold"
    INSUFICIENT_NUMBER_OF_POINTS = "INSUFICIENT_NUMBER_OF_POINTS"
    INSUFFICIENT_NUMBER_OF_POINTS_AFTER_IRLS = (
        "Insufficient number of points after IRLS"
    )

    def __str__(self) -> str:
        """Format enum values to string.

        Returns:
            str: [description]
        """
        return str(self.value)


class FitStatusEnum(enum.Enum, metaclass=MyEnumMeta):
    """Documentation for FitStatusEnum.

    Args:
        enum ([type]): [description]
        metaclass ([type], optional): [description]. Defaults to MyEnumMeta.

    Returns:
        [type]: [description]
    """

    EXCLUDED_BY_PREFILTERING = "Excluded by pre-filtering"
    IRLS_SENSITIVITY_VALIDATION_FAILED = "IRLS SENTITIVITY VALIDATION FAILED"
    OK_UNABLE_TO_COMPUTE_CONFIDENCE_INTERVALS = (
        "OK. Unable to compute confidence intervals"
    )
    OK = "OK"

    def __str__(self) -> str:
        """Format enum values to string.

        Returns:
            str: [description]
        """
        return str(self.value)


class IrlsEnum(enum.Enum, metaclass=MyEnumMeta):
    """Documentation for IrlsEnum.

    Args:
        enum ([type]): [description]
        metaclass ([type], optional): [description]. Defaults to MyEnumMeta.

    Returns:
        [type]: [description]
    """

    UNTAGGED = "Untagged"
    IRLS_EXCLUDED = "IRLS Excluded"
    IRLS_WEIGHT_LT_05 = "IRLS weight < 0.5"

    def __str__(self) -> str:
        """Format enum values to string.

        Returns:
            str: [description]
        """
        return str(self.value)


class ExclussionEnum(enum.Enum, metaclass=MyEnumMeta):
    """Documentation for ExclussionEnum.

    Args:
        enum ([type]): [description]
        metaclass ([type], optional): [description]. Defaults to MyEnumMeta.

    Returns:
        [type]: [description]
    """

    INSTRUMENT_ERROR = "Instrument error"
    MANUAL_EXCLUDED = "Manual excluded"
    EXCLUDED = "Excluded"

    def __str__(self) -> str:
        """Format enum values to string.

        Returns:
            str: [description]
        """
        return str(self.value)


class PassFailEnum(enum.Enum, metaclass=MyEnumMeta):
    """Documentation for PassFailEnum.

    Args:
        enum ([type]): [description]
        metaclass ([type], optional): [description]. Defaults to MyEnumMeta.

    Returns:
        [type]: [description]
    """

    PASS = "PASS"
    FAIL = "FAIL"
    FAILED = "Failed"
    SUCCESSFULLY = "Successfully"
    ROBUST_FAILED = "ROBUST_FAILED"

    def __str__(self) -> str:
        """Format enum values to string.

        Returns:
            str: [description]
        """
        return str(self.value)


class ResponseTypeEnum(enum.Enum, metaclass=MyEnumMeta):
    """Documentation for ResponseTypeEnum.

    Args:
        enum ([type]): [description]
        metaclass ([type], optional): [description]. Defaults to MyEnumMeta.

    Returns:
        [type]: [description]
    """

    PERCENT_INHIBITION = "PERCENT INHIBITION"

    def __str__(self) -> str:
        """Format enum values to string.

        Returns:
            str: [description]
        """
        return str(self.value)


class CompundGroupEnum(enum.Enum, metaclass=MyEnumMeta):
    """Documentation for CompundGroupEnum.

    Args:
        enum ([type]): [description]
        metaclass ([type], optional): [description]. Defaults to MyEnumMeta.

    Returns:
        [type]: [description]
    """

    CGX = "CGX"

    def __str__(self) -> str:
        """Format enum values to string.

        Returns:
            str: [description]
        """
        return str(self.value)


class SignalsWorkflowEnum(enum.Enum, metaclass=MyEnumMeta):
    """Documentation for SignalsWorkflowEnum.

    Args:
        enum ([type]): [description]
        metaclass ([type], optional): [description]. Defaults to MyEnumMeta.

    Returns:
        [type]: [description]
    """

    UK_TOLDC_LIKE_5PARAMETER_FC = "UK_TOLDC_LIKE_5Parameter_FC"
    P384_FLEXPLEX_SS_2C = "384 FLEXPLEX SS 2C"
    UK_TRPM3_FLIPR_PREG_AG_FC = "UK_TRPM3_FLIPR_PREG_AG_FC"

    def __str__(self) -> str:
        """Format enum values to string.

        Returns:
            str: [description]
        """
        return str(self.value)


class HitEnum(enum.Enum, metaclass=MyEnumMeta):
    """Documentation for HitEnum.

    Args:
        enum ([type]): [description]
        metaclass ([type], optional): [description]. Defaults to MyEnumMeta.

    Returns:
        [type]: [description]
    """

    ROBUST_ACTIVE = "ROBUST-ACTIVE"
    ROBUST_INACTIVE = "ROBUST-INACTIVE"

    def __str__(self) -> str:
        """Format enum values to string.

        Returns:
            str: [description]
        """
        return str(self.value)


class BooleanEnum(enum.Enum, metaclass=MyEnumMeta):
    """Documentation for BooleanEnum.

    Args:
        enum ([type]): [description]
        metaclass ([type], optional): [description]. Defaults to MyEnumMeta.

    Returns:
        [type]: [description]
    """

    YES = "YES"
    NO = "NO"
    Y = "Y"
    N = "N"

    def __str__(self) -> str:
        """Format enum values to string.

        Returns:
            str: [description]
        """
        return str(self.value)


class EmptyEnum(enum.Enum, metaclass=MyEnumMeta):
    """Documentation for EmptyEnum.

    Args:
        enum ([type]): [description]
        metaclass ([type], optional): [description]. Defaults to MyEnumMeta.

    Returns:
        [type]: [description]
    """

    EMPTY = "(EMPTY)"
    NA = "NA"
    NAN = "NAN"
    NAT = "NAT"
    NULL = "NULL"
    NONE = "NONE"
    FALSE = "FALSE"

    def __str__(self) -> str:
        """Format enum values to string.

        Returns:
            str: [description]
        """
        return str(self.value)


class AnalysisResultType(enum.Enum, metaclass=MyEnumMeta):
    """Documentation for AnalysisResultType.

    Args:
        enum ([type]): [description]
        metaclass ([type], optional): [description]. Defaults to MyEnumMeta.

    Returns:
        [type]: [description]
    """

    SINGLE_PARAMETER_FULL_CURVE_ANALYSIS_RESULT = (
        "SPFC"  # "Single Parameter Full Curve Analysis Result"
    )
    MULTI_PARAMETER_FULL_CURVE_ANALYSIS_RESULT = (
        "MPFC"  # "Multi Parameter Full Curve Analysis Result"
    )
    SINGLE_PARAMETER_SINGLE_CONCENTRATION_ANALYSIS_RESULT = (
        "SPSC"  # "Single Parameter Single Concentration Analysis Result"
    )
    MULTI_PARAMETER_SINGLE_CONCENTRATION_ANALYSIS_RESULT = (
        "MPSC"  # "Multiple Parameter Single Concentration Analysis Result"
    )

    def __str__(self) -> str:
        """Format enum values to string.

        Returns:
            str: [description]
        """
        return str(self.value)


class AnalysisTypeName(enum.Enum, metaclass=MyEnumMeta):
    """Documentation for 'analysis_type.name'.

    Args:
        enum ([type]): [description]
        metaclass ([type], optional): [description]. Defaults to MyEnumMeta.

    Returns:
        [type]: [description]
    """

    SINGLE_PARAMETER_FULL_CURVE = "Single Parameter Full Curve"
    MULTI_PARAMETER_FULL_CURVE = "Multi Parameter Full Curve"
    SINGLE_PARAMETER_SINGLE_CONCENTRATION = "Single Parameter Single Concentration"
    MULTI_PARAMETER_SINGLE_CONCENTRATION = "Multi Parameter Single Concentration"

    def __str__(self) -> str:
        """Format enum values to string.

        Returns:
            str: [description]
        """
        return str(self.value)


class CustomAROSDateFormat(str):
    """AI is creating summary for CustomAROSDateFormat.

    Args:
        str ([type]): [description]

    Raises:
        ValueError: [description]

    Returns:
        [type]: [description]

    Yields:
        [type]: [description]
    """

    @classmethod
    def __get_validators__(cls) -> Generator:
        """Return validators generator.

        Yields:
            Generator: [description]
        """
        yield cls.validate_date_format
        yield cls.ensure_tzinfo

    @classmethod
    def validate_date_format(cls, date_string: str) -> datetime:
        """Validate custom data format.

        Args:
            date_string (str): [description]

        Raises:
            ValueError: [description]

        Returns:
            datetime: [description]
        """
        try:
            parsed_datetime = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S %z %Z")
        except Exception as e:
            raise ValueError(
                f"Invalid date format: {date_string}. Validate by custom field."
            ) from e
        return parsed_datetime

    @classmethod
    def ensure_tzinfo(cls, v: datetime) -> datetime:
        """Check tzinfo is correctly provided.

        Args:
            v (datetime): [description]

        Returns:
            datetime: [description]
        """
        # if TZ isn't provided, we assume UTC, but you can do w/e you need
        if v.tzinfo is None:
            return v.replace(tzinfo=timezone.utc)
        # else we convert to utc
        return v.astimezone(timezone.utc)

    @staticmethod
    def to_str(value: datetime) -> str:
        """Return datatime in isoformat.

        Replace with w/e format you want.

        Args:
            value (datetime): [description]

        Returns:
            str: [description]
        """
        return value.strftime("%Y-%m-%d %H:%M:%S %z %Z")


class ThresholdDigit(str):
    """Documentation for ThresholdDigit.

    Args:
        str ([type]): [description]

    Raises:
        ValueError: [description]

    Returns:
        [type]: [description]

    Yields:
        [type]: [description]
    """

    @classmethod
    def __get_validators__(cls) -> Generator:
        """Return validators generator.

        Yields:
            Generator: [description]
        """
        yield cls.validate_str_pattern

    @classmethod
    def validate_str_pattern(cls, value: Union[str, int, float]) -> str:
        """Docstring for validate_str_pattern.

        Args:
            value (Union[str, int, float]): [description]

        Raises:
            ValueError: [description]

        Returns:
            str: [description]
        """
        regex = r"^(?P<symbol>[<>=]\s)?(?P<posdigit>\d+)(?P<sep>\.)?(?P<decimal>\d+)*$"
        if re.match(regex, str(value)) is not None:
            res = value
        else:
            raise ValueError(f"Invalid pattern validation: {regex}")
        return res


# class GSKcompoundId(str):

#     @classmethod
#     def __get_validators__(cls) -> Generator:
#         yield cls.validate_str_pattern
#         yield cls.validate_db_match

#     @classmethod
#     def validate_str_pattern(cls, value: str) -> str:
#         regex = r'^(?P<source>[A-Z]){2,3}(?P<sep1>[-])*\
#                   (?P<code1>[0-9A-Z]){3,}(?P<sep2>[-])*(?P<code2>[A-Z0-9])*$'
#         if re.match(regex, value) is not None:
#             res = value
#         else:
#             raise ValueError(f"Invalid pattern validation: {regex}")
#         return res

#     @classmethod
#     def validate_db_match(cls, value: str) -> str:
#         if not get_compound_id(value):
#             raise ValueError(f"Invalid compound id: {value}. Not found in DB.")
#         return value


class CurveIdPkiLogisticRegression4Params(str):
    """Documentation for CurveIdPkiLogisticRegression4Params.

    Args:
        str ([type]): [description]

    Raises:
        ValueError: [description]

    Returns:
        [type]: [description]

    Yields:
        [type]: [description]
    """

    min_length = 30
    max_length = 40

    @classmethod
    def __get_validators__(cls) -> Generator:
        """Return validators generator.

        Yields:
            Generator: [description]
        """
        yield cls.validate_str_pattern

    @classmethod
    def validate_str_pattern(cls, value: str) -> str:
        """Validate provided string against pattern.

        Args:
            value (str): [description]

        Raises:
            ValueError: [description]

        Returns:
            str: [description]
        """
        length = len(value)
        regex = r"^(?P<head>(id)[a-z0-9]{32})(?P<sep>[-]{1})(?P<tail>\d{1,3})$"
        assert cls.min_length <= length <= cls.max_length, ValueError(
            f"Invalid length validation: {length}. \
                Allowed values: {cls.min_length} <-> {cls.max_length}."
        )
        if re.match(regex, value) is not None:
            res = value
        else:
            raise ValueError(f"Invalid pattern validation: {regex}")
        return res


class LevelPlateId(str):
    """Documentation for LevelPlateId.

    Args:
        str ([type]): [description]

    Raises:
        ValueError: [description]

    Returns:
        [type]: [description]

    Yields:
        [type]: [description]
    """

    @classmethod
    def __get_validators__(cls) -> Generator:
        """Return validators generator.

        Yields:
            Generator: [description]
        """
        yield cls.validate_str_pattern

    @classmethod
    def validate_str_pattern(cls, value: str) -> str:
        """Validate provided string against pattern.

        Args:
            value (str): [description]

        Raises:
            ValueError: [description]

        Returns:
            str: [description]
        """
        regex = re.compile(
            r"^\[(?P<first>[A-Z0-9]{5,15})\]"
            r"(?P<second>\.\[[a-zA-Z0-9\s\*\/-]{0,50}\]){1,4}$"
        )
        if re.match(regex, value) is not None:
            res = value
        else:
            raise ValueError(f"Invalid pattern validation: {regex}")
        return res


class ObjectId(str):
    """Documentation for ObjectId.

    Args:
        str ([type]): [description]

    Raises:
        ValueError: [description]

    Returns:
        [type]: [description]

    Yields:
        [type]: [description]
    """

    @classmethod
    def __get_validators__(cls) -> Generator:
        """Return validators generator.

        Yields:
            Generator: validators generator.
        """
        yield cls.validate_str_pattern

    @classmethod
    def validate_str_pattern(cls, value: str) -> str:
        """Validate provided string against pattern.

        #regex = r'^(?P<object>OBJECT)(?P<wellid>[0]{0,3}[1-9]{1,4})$'
        constr(regex=r"^(?P<object>OBJECT)(?P<wellid>[0]{0,3}[1-9]{1,4})$")

        Args:
            value (str): string to be validated.

        Raises:
            ValueError: invalid pattern matching.

        Returns:
            str: validated string.
        """
        regex = r"^(?P<object>OBJECT)(?P<wellid>[0-9]{4})$"
        if re.match(regex, value) is not None:
            res = value
        else:
            raise ValueError(f"Invalid pattern validation: {regex}")
        return res


class PlateId(str):
    """Documentation for PlateId data type.

    Args:
        str ([type]): [description]

    Raises:
        ValueError: [description]

    Returns:
        [type]: [description]

    Yields:
        [type]: [description]
    """

    @classmethod
    def __get_validators__(cls) -> Generator:
        """Return validators generator.

        Yields:
            Generator: [description]
        """
        yield cls.validate_str_pattern

    @classmethod
    def validate_str_pattern(cls, value: str) -> str:
        """Documentation for validate_str_pattern.

        Args:
            value (str): [description]

        Raises:
            ValueError: [description]

        Returns:
            str: [description]
        """
        regex = r"^(?P<pattern>[\d\w]{5,10})$"
        if re.match(regex, value) is not None:
            res = value
        else:
            raise ValueError(f"Invalid pattern validation: {regex}")
        return res


class PlateWell(str):
    """Documentation for PlateWell.

    Args:
        str ([type]): [description]

    Raises:
        ValueError: [description]

    Returns:
        [type]: [description]

    Yields:
        [type]: [description]
    """

    @classmethod
    def __get_validators__(cls) -> Generator:
        """Return validators generator.

        Yields:
            Generator: [description]
        """
        yield cls.validate_str_pattern

    @classmethod
    def validate_str_pattern(cls, value: str) -> str:
        """Validate string against provided pattern.

        Args:
            value (str): [description]

        Raises:
            ValueError: [description]

        Returns:
            str: [description]
        """
        regex = re.compile(
            r"(?P<head>[UH]{1})(?P<mid>\d{1,3})"
            r"(?P<tail>[HG]{1}\d{1,5}\w{1,2})"
            r"(?P<sep>:)(?P<wellid>\w{1,2}\d{1,2})"
        )
        if re.match(regex, value) is not None:
            res = value
        else:
            raise ValueError(f"Invalid pattern validation: {regex}")
        return res


class Qualifier(str):
    """Documentation for Qualifier.

    Args:
        str ([type]): [description]

    Raises:
        ValueError: [description]

    Returns:
        [type]: [description]

    Yields:
        [type]: [description]
    """

    @classmethod
    def __get_validators__(cls) -> Generator:
        """Return validators generator.

        Yields:
            Generator: [description]
        """
        yield cls.validate_str_pattern

    @classmethod
    def validate_str_pattern(cls, value: str) -> str:
        """Validate string against custom pattern.

        constr(regex=r"^[<>=]{1}$")

        Args:
            value (str): [description]

        Raises:
            ValueError: [description]

        Returns:
            str: [description]
        """
        regex = r"^[<>=]{1}$"
        if re.match(regex, value) is not None:
            res = value
        else:
            raise ValueError(f"Invalid pattern validation: {regex}")
        return res


class Percentage(float):
    """Documentation for Percentage.

    Args:
        float ([type]): [description]

    Returns:
        [type]: [description]

    Yields:
        [type]: [description]
    """

    min_val = 0
    max_val = 100

    @classmethod
    def __get_validators__(cls) -> Generator:
        """Return validators generator.

        Yields:
            Generator: [description]
        """
        yield cls.validate_range

    @classmethod
    def validate_range(cls, value: float) -> float:
        """Documentation for validate_range.

        Args:
            value (float): [description]

        Returns:
            float: [description]
        """
        assert cls.min_val <= value <= cls.max_val, ValueError(
            f"Value range: {cls.min_val}:{cls.max_val}. Got {value}."
        )
        return value


class CoorporateId(str):
    """AI is creating summary for CoorporateId.

    Args:
        str ([type]): [description]
    """

    min_length = 5
    max_length = 50

    @classmethod
    def __get_validators__(cls) -> Generator:
        """Return validators generator.

        Yields:
            Generator: [description]
        """
        yield cls.validate_str_length
        yield cls.validate_str_pattern

    @classmethod
    def validate_str_length(cls, value: str) -> str:
        """AI is creating summary for validate_str_length.

        Args:
            value (str): [description]

        Returns:
            str: [description]
        """
        assert cls.min_length <= len(value) <= cls.max_length, ValueError(
            f"Length range is incorrect. Expected between: {cls.min_length},\
                {cls.max_length}, provided: '{len(value)}'."
        )
        return value

    @classmethod
    def validate_str_pattern(cls, value: str) -> str:
        """Valisdate string against custom pattern.

        Args:
            value (str): [description]

        Raises:
            ValueError: [description]

        Returns:
            str: [description]
        """
        regex = r"^(?P<str>[A-Z]+)(?P<dig>[0-9]+)$"
        if re.match(regex, value) is not None:
            res = value
        else:
            raise ValueError(f"Invalid pattern validation: {regex}")
        return res
