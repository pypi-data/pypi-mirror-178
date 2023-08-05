"""
Summary: models_factory module.

It provides callable class implementation for model factory pattern.
"""

from loguru import logger
from pydantic.main import ModelMetaclass


class ModelFactory:
    """Provide model factory functionality.

    Factory functionality for container models.
    For instance AROS.
    """

    def __call__(
        self, model: ModelMetaclass, field_name: str, type_: str, field_: str
    ) -> ModelMetaclass:
        """Callable method for ModelFactory.

        Args:
            model (ModelMetaclass): [description]
            field_name (str): [description]
            type_ (str): [description]
            field_ (str): [description]

        Returns:
            ModelMetaclass: [description]
        """
        try:
            args = {field_name: (eval(type_), eval(field_))}
        except Exception as e:
            logger.exception(e)
        else:
            model.add_fields(**args)
        return model
