__version__ = "0.2.0"

from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.expanduser().resolve()

from torchsilk.modules import Module as Module  # noqa: E402
from torchsilk.type_defs import BaseConfig as BaseConfig  # noqa: E402
from torchsilk.type_defs import EmptyModel as EmptyModel  # noqa: E402
