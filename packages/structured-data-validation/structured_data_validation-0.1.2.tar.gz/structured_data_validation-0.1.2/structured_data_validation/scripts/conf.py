"""
Summary: allow configuration files.

Allows configuration files for main modules logic.
"""

import logging

import hydra
from omegaconf import DictConfig, OmegaConf


log = logging.getLogger(__name__)


@hydra.main(version_base=None, config_path="../../conf", config_name="config")
def my_app(cfg: DictConfig) -> None:
    """Create configuration logic.

    Args:
        cfg (DictConfig): [description]
    """
    log.info(OmegaConf.to_yaml(cfg))
    print(cfg.model)


def main() -> None:
    """Call main hydra function.

    Allow the custom functionality and parameters.
    """
    my_app()


if __name__ == "__main__":
    main()
