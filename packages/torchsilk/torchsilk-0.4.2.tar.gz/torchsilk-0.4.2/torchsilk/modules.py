"""Type definitions / aliases for the sbft API."""
import json
import typing as t

import attrs
import functorch as ft
import lovely_tensors as lt  # type: ignore
import torch
import typing_extensions as te
import yaml
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table

from torchsilk import type_defs as tdf


def json_to_yaml(x: str) -> str:
    """Convert a json string to yaml."""
    return yaml.safe_dump(json.loads(x))


@attrs.define()
class NamedBuffers(t.Mapping[str, torch.Tensor]):
    """Allows one to access buffers as attributes.

    Example:

    >>> class MyModule(torch.nn.Module):
    ...     def __init__(self):
    ...         super().__init__()
    ...         self.register_buffer("foo", torch.tensor(1))
    ...         self.register_buffer("bar", torch.tensor(2))
    ...     def forward(self, x):
    ...         return x
    ... buffers = NamedBuffers.from_module(MyModule())
    ... assert torch.allclose(buffers.foo, torch.tensor(1))
    ... assert torch.allclose(buffers.bar, torch.tensor(2))
    """

    buffers: t.Mapping[str, torch.Tensor]

    @classmethod
    def from_module(cls, module: torch.nn.Module) -> "NamedBuffers":
        return cls(dict(module.named_buffers()))

    def evolve_from_values(self, values: tuple[torch.Tensor]) -> "NamedBuffers":
        """Create a new NamedBuffers with the same keys but new values."""
        assert len(values) == len(self.buffers)
        return attrs.evolve(self, buffers=dict(zip(self.buffers.keys(), values)))

    def evolve(self, values: dict[str, torch.Tensor]) -> "NamedBuffers":
        """Create a new NamedBuffers with the same keys but new values."""
        return attrs.evolve(self, buffers={**self.buffers, **values})

    def as_table(
        self, name_column_width: int = 24, buffers_column_width: int = 56
    ) -> Table:
        """Return a rich Table representation of the buffer."""
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Name", style="dim", width=name_column_width)
        table.add_column(
            "Buffers",
            style="dim",
            width=buffers_column_width,
            justify="center",
        )
        for name, buffer in self.buffers.items():
            table.add_row(name, str(lt.lovely(buffer)))
        return table

    def show(self) -> None:
        """Show a pretty representation of the buffer."""
        console = Console()
        console.print(
            self.as_table(name_column_width=24, buffers_column_width=console.width - 24)
        )

    def __getattr__(self, name: str) -> torch.Tensor:
        try:
            return self.buffers[name]
        except KeyError:
            raise AttributeError(f"Module has no buffer {name}") from None

    def __getitem__(self, name: str) -> torch.Tensor:
        return self.buffers[name]

    def __iter__(self) -> t.Iterator[str]:
        return iter(self.buffers)

    def __len__(self) -> int:
        return len(self.buffers)


class FunctionalModuleWithoutBuffers(t.Protocol[tdf.P, tdf.R]):
    """A module that can be called like a function.

    A type-safe version of functorch's FunctionalModule which is obtained from the
    result of calling functorch.make_functional(...).
    """

    def __call__(
        self,
        parameters: tuple[torch.nn.Parameter, ...],
        *args: tdf.P.args,
        **kwargs: tdf.P.kwargs,
    ) -> tdf.R:
        ...


class FunctionalModuleWithBuffers(t.Protocol[tdf.P, tdf.R]):
    """A module that can be called like a function.

    A type-safe version of functorch's FunctionalModuleWithBuffers which is obtained
    from the result of calling functorch.make_functional(...).
    """

    def __call__(
        self,
        parameters: tuple[torch.nn.Parameter, ...],
        buffers: tuple[torch.Tensor, ...],
        *args: tdf.P.args,
        **kwargs: tdf.P.kwargs,
    ) -> tdf.R:
        ...


class _ModuleStateWithoutBuffers(t.Generic[tdf.P, tdf.R]):
    """A container for a stateless module and its parameters.

    Example:

    .. code-block:: python

    >>> import torch
    ... import functorch as ft
    ... module = torch.nn.Sequential(
    ...     torch.nn.Linear(3, 3),
    ...     torch.nn.ReLU(),
    ...     torch.nn.Linear(3, 3),
    ... )
    ... x = torch.randn(4, 3)
    ... m = _ModuleStateWithoutBuffers.from_torch_module(module)
    ... exp_res = m(x)
    ... func_module, params = ft.make_functional(module)
    ... act_res = func_module(params, x)
    ... assert torch.allclose(exp_res, act_res)
    """

    def __init__(
        self,
        module: FunctionalModuleWithoutBuffers[tdf.P, tdf.R],
        parameters: tuple[torch.nn.Parameter, ...],
    ) -> None:
        """NOTE: Not intended to be called directly. Use `from_torch_module` instead."""
        self._module = module
        self._parameters = parameters

    @classmethod
    def from_torch_module(cls: type[te.Self], torch_module: torch.nn.Module) -> te.Self:
        """Create a `_ModuleStateWithoutBuffers` from a torch module.

        This is the main way to create a `_ModuleStateWithoutBuffers` instance.

        Example:

        .. code-block:: python

        >>> import torch
        ... import functorch as ft
        ... class MyModule(torch.nn.Module):
        ...     def __init__(self):
        ...         super().__init__()
        ...         self.linear = torch.nn.Linear(3, 3)
        ...         self.relu = torch.nn.ReLU()
        ...     def forward(self, x):
        ...         return self.relu(self.linear(x))
        ... module = MyModule()
        ... x = torch.randn(4, 3)
        ... m = _ModuleStateWithoutBuffers.from_torch_module(module)
        ... act_res = m(x)
        ... func_module, params = ft.make_functional(module)
        ... exp_res = func_module(params, x)
        ... assert torch.allclose(exp_res, act_res)

        >>> import torch
        ... import functorch as ft
        ... import pytest
        ... class MyModule(torch.nn.Module):
        ...     def __init__(self):
        ...         super().__init__()
        ...         self.linear = torch.nn.Linear(3, 2)
        ...         self.relu = torch.nn.ReLU()
        ...     def forward(self, x, y, *, z=0):
        ...         return self.relu(self.linear(x) + y) + z
        ... module = MyModule()
        ... x = torch.randn(4, 3)
        ... y = torch.randn(4, 2)
        ... z = torch.randn(4, 2)
        ... m = _ModuleStateWithoutBuffers.from_torch_module(module)
        ... act_res = m(x, y, z=z)
        ... func_module, params = ft.make_functional(module)
        ... exp_res = func_module(params, x, y, z=z)
        ... assert torch.allclose(exp_res, act_res)
        ... act_res = m(x, y)
        ... exp_res = func_module(params, x, y)
        ... assert torch.allclose(exp_res, act_res)
        ... also_act_res = m(x, y, z=1)
        ... also_exp_res = func_module(params, x, y, z=1)
        ... assert torch.allclose(also_exp_res, also_act_res)
        ... with pytest.raises(TypeError):
        ...     m(x, y, z=z, w=1)
        """
        func, parameters = ft.make_functional(
            torch_module, disable_autograd_tracking=True
        )
        return cls(
            t.cast(FunctionalModuleWithoutBuffers[tdf.P, tdf.R], func), parameters
        )

    @property
    def module(self) -> FunctionalModuleWithoutBuffers[tdf.P, tdf.R]:
        """Return the underlying stateless module."""
        return self._module

    @property
    def parameters(self) -> tuple[torch.nn.Parameter, ...]:
        """Return the parameters of the underlying stateless module."""
        return self._parameters

    def __call__(self, *args: tdf.P.args, **kwargs: tdf.P.kwargs) -> tdf.R:
        return self.module(self.parameters, *args, **kwargs)


class _ModuleStateWithBuffers(t.Generic[tdf.P, tdf.R]):
    """A container for a stateless module, its parameters and its buffers.

    Example:

    .. code-block:: python

    >>> import torch
    ... import functorch as ft
    ... class ModuleWithBuffers(torch.nn.Module):
    ...     def __init__(self):
    ...         super().__init__()
    ...         self.register_buffer("x", torch.randn(3))
    ...     def forward(self, x):
    ...         return x + self.x
    ... module = ModuleWithBuffers()
    ... x = torch.randn(4, 3)
    ... m = _ModuleStateWithBuffers.from_torch_module(module)
    ... act_res = m(x)
    ... func_module, params, buffers = ft.make_functional_with_buffers(module)
    ... exp_res = func_module(params, buffers, x)
    ... assert torch.allclose(exp_res, act_res)
    ... assert torch.allclose(m.named_buffers.x, buffers[0])
    """

    def __init__(
        self,
        module: FunctionalModuleWithBuffers[tdf.P, tdf.R],
        parameters: tuple[torch.nn.Parameter, ...],
        buffers: tuple[torch.Tensor, ...],
        named_buffers: NamedBuffers,
    ) -> None:
        self._module = module
        self._parameters = parameters
        self._buffers = buffers
        self._named_buffers = named_buffers

    @classmethod
    def from_torch_module(cls: type[te.Self], torch_module: torch.nn.Module) -> te.Self:
        """Create a `_ModuleStateWithBuffers` from a torch module.

        This is the main way to create a `_ModuleStateWithBuffers` instance.

        Examples:

        .. code-block:: python

        >>> import torch
        ... import functorch as ft
        ... class ModuleWithBuffers(torch.nn.Module):
        ...     def __init__(self):
        ...         super().__init__()
        ...         self.register_buffer("x", torch.randn(3))
        ...     def forward(self, x):
        ...         return x + self.x
        ... module = ModuleWithBuffers()
        ... x = torch.randn(4, 3)
        ... m = _ModuleStateWithBuffers.from_torch_module(module)
        ... act_res = m(x)
        ... func_module, params, buffers = ft.make_functional_with_buffers(module)
        ... exp_res = func_module(params, buffers, x)
        ... assert torch.allclose(exp_res, act_res)
        ... assert torch.allclose(m.named_buffers.x, buffers[0])
        """
        named_buffers = NamedBuffers.from_module(torch_module)
        func, parameters, buffers = ft.make_functional_with_buffers(
            torch_module, disable_autograd_tracking=True
        )
        return cls(
            module=t.cast(FunctionalModuleWithBuffers[tdf.P, tdf.R], func),
            parameters=parameters,
            buffers=buffers,
            named_buffers=named_buffers.evolve_from_values(buffers),
        )

    @property
    def module(self) -> FunctionalModuleWithBuffers[tdf.P, tdf.R]:
        return self._module

    @property
    def parameters(self) -> tuple[torch.nn.Parameter, ...]:
        return self._parameters

    @property
    def buffers(self) -> tuple[torch.Tensor, ...]:
        return self._buffers

    @property
    def named_buffers(self) -> NamedBuffers:
        return self._named_buffers

    def __call__(self, *args: tdf.P.args, **kwargs: tdf.P.kwargs) -> tdf.R:
        return self.module(self.parameters, self.buffers, *args, **kwargs)


class ModuleState(t.Generic[tdf.P, tdf.R]):
    """A container for a stateless module, its parameters and its buffers if it has any.

    NOTE: Do not initialize this directly. Use ModuleState.from_torch_module.

    Example:
    1. A module without buffers
    >>> import torch
    ... import functorch as ft
    ... class ModuleWithoutBuffers(torch.nn.Module):
    ...     def __init__(self):
    ...         super().__init__()
    ...         self.linear = torch.nn.Linear(3, 4)
    ...     def forward(self, x, y):
    ...         return self.linear(x) + y
    ... torch_module = ModuleWithoutBuffers()
    ... module_state = ModuleState.from_torch_module(torch_module)
    ... x = torch.randn(4, 3)
    ... y = torch.randn(4, 4)
    ... act_res = module_state(x, y)
    ... func_module, params = ft.make_functional(torch_module)
    ... exp_res = func_module(params, x, y)
    ... assert torch.allclose(exp_res, act_res)

    2. A module with buffers
    >>> import torch
    ... import functorch as ft
    ... class ModuleWithBuffers(torch.nn.Module):
    ...     def __init__(self):
    ...         super().__init__()
    ...         self.register_buffer("x", torch.randn(3))
    ...     def forward(self, x):
    ...         return x + self.x
    ... torch_module = ModuleWithBuffers()
    ... module_state = ModuleState.from_torch_module(torch_module)
    ... x = torch.randn(4, 3)
    ... act_res = module_state(x)
    ... func_module, params, buffers = ft.make_functional_with_buffers(torch_module)
    ... exp_res = func_module(params, buffers, x)
    ... assert torch.allclose(exp_res, act_res)
    ... assert torch.allclose(module_state.named_buffers.x, buffers[0])
    """

    def __init__(
        self,
        module_state: _ModuleStateWithoutBuffers[tdf.P, tdf.R]
        | _ModuleStateWithBuffers[tdf.P, tdf.R],
    ) -> None:
        self._module_state = module_state
        self._has_buffers = isinstance(module_state, _ModuleStateWithBuffers)
        self._buffers = (
            module_state.buffers
            if isinstance(module_state, _ModuleStateWithBuffers)
            else t.cast(tuple[torch.Tensor, ...], tuple())
        )
        self._named_buffers = (
            module_state.named_buffers
            if isinstance(module_state, _ModuleStateWithBuffers)
            else NamedBuffers({})
        )

    @classmethod
    def from_torch_module(cls: type[te.Self], torch_module: torch.nn.Module) -> te.Self:
        if next(torch_module.buffers(recurse=True), None) is not None:
            # If the module has buffers, use _ModuleStateWithBuffers.
            return cls(
                _ModuleStateWithBuffers[tdf.P, tdf.R].from_torch_module(torch_module)
            )
        else:
            # Otherwise, use _ModuleStateWithoutBuffers.
            return cls(
                _ModuleStateWithoutBuffers[tdf.P, tdf.R].from_torch_module(torch_module)
            )

    @property
    def module(
        self,
    ) -> FunctionalModuleWithoutBuffers[tdf.P, tdf.R] | FunctionalModuleWithBuffers[
        tdf.P, tdf.R
    ]:
        return self._module_state.module

    @property
    def parameters(self) -> tuple[torch.nn.Parameter, ...]:
        return self._module_state.parameters

    @property
    def buffers(self) -> tuple[torch.Tensor, ...]:
        return self._buffers

    @property
    def named_buffers(self) -> NamedBuffers:
        return self._named_buffers

    @property
    def has_buffers(self) -> bool:
        return self._has_buffers

    def __call__(self, *args: tdf.P.args, **kwargs: tdf.P.kwargs) -> tdf.R:
        return self._module_state(*args, **kwargs)

    def __str__(self) -> str:
        return str(self._module_state)


class ModuleSetupNotImplemented(NotImplementedError):
    """Raised when Module.__setup_... functions are not implemented."""


class Module(t.Generic[tdf.PydanticModel, tdf.P, tdf.R]):
    """Opinionated wrapper around torch.nn.Module that acts like a stateless model.

    To construct a stateless model, you must implement either subclass either
    __setup_module_state__ or __setup_torch_module__. If you implement both, then
    __setup_module_state__ will be used.

    Examples:

    1. Model that doesn't have any parametrizable layers.

    >>> import torch
    ... import functorch as ft
    ... import torchsilk as tsk
    ... class MyModule(Module[tdf.EmptyModel, torch.Tensor, torch.Tensor]):
    ...     @classmethod
    ...     def __setup_torch_module__(cls, config) -> torch.nn.Module:
    ...         return torch.nn.Linear(1, 1)
    ... tsk_module = MyModule()
    ... torch_module = MyModule.__setup_torch_module__(tsk.BaseConfig())
    ... func_module, _ = ft.make_functional(torch_module)
    ... x = torch.randn(4, 1)
    ... assert torch.allclose(func_module(tsk_module.parameters, x), tsk_module(x))

    2. Model that has parametrizable layers.

    >>> import torch
    ... import torchsilk as tsk
    ... from pydantic import validator
    ... class MyFeedForwardConfig(tsk.BaseConfig):
    ...     in_features: int
    ...     out_features: int
    ...     hidden_features: list[int]
    ...     hidden_activations: list[str | torch.nn.Module]
    ...     @validator('hidden_activations')
    ...     def check_activations(cls, v: t.Any) -> list[torch.nn.Module]:
    ...         return [getattr(torch.nn, a) for a in v]
    ... class MyFeedForward(Module[MyFeedForwardConfig, torch.Tensor, torch.Tensor]):
    ...     @classmethod
    ...     def __setup_torch_module__(self, config) -> torch.nn.Module:
    ...         layers = []
    ...         for i, (in_features, out_features, activation) in enumerate(
    ...             zip(
    ...                 [config.in_features, *config.hidden_features],
    ...                 [*config.hidden_features, config.out_features],
    ...                 [*config.hidden_activations, torch.nn.Identity],
    ...             )
    ...         ):
    ...             layers.append(torch.nn.Linear(in_features, out_features))
    ...             if activation != "linear":
    ...                 layers.append(activation())
    ...         return torch.nn.Sequential(*layers)
    ... config = MyFeedForwardConfig(
    ...     in_features=1,
    ...     out_features=1,
    ...     hidden_features=[2, 3],
    ...     hidden_activations=["ReLU", "ReLU"]
    ... )
    ... tsk_module = MyFeedForward(config)
    ... torch_module = MyFeedForward.__setup_torch_module__(config)
    ... func_module, _ = ft.make_functional(torch_module)
    ... x = torch.randn(4, config.in_features)
    ... assert torch.allclose(func_module(tsk_module.parameters, x), tsk_module(x))

    3. Model that has buffers.

    >>> import torch
    ... import torchsilk as tsk
    ... class MyModule(Module[tdf.EmptyModel, [torch.Tensor], torch.Tensor]):
    ...     @classmethod
    ...     def __setup_torch_module__(cls, config) -> torch.nn.Module:
    ...         class _MyModule(torch.nn.Module):
    ...             def __init__(self):
    ...                 super().__init__()
    ...                 self.register_buffer("bias", torch.randn(1))
    ...             def forward(self, x):
    ...                 return x + self.bias
    ...         return _MyModule()
    ...
    """

    def __init__(self, config: tdf.BaseConfig = tdf.BaseConfig()) -> None:
        self.config = config
        try:
            self._module_state = self.__setup_module_state__(self.config)
        except ModuleSetupNotImplemented:
            try:
                torch_module = self.__setup_torch_module__(self.config)
            except ModuleSetupNotImplemented:
                raise ModuleSetupNotImplemented(
                    "Both __setup_module_state__ and __setup_torch_module__ are not"
                    + " implemented."
                ) from None
            else:
                self._module_state = ModuleState[tdf.P, tdf.R].from_torch_module(
                    torch_module
                )

    @classmethod
    def __setup_module_state__(
        cls, config: tdf.PydanticModel
    ) -> ModuleState[tdf.P, tdf.R]:
        raise ModuleSetupNotImplemented(
            f"{cls}.__setup_module_state__ not implemented."
        )

    @classmethod
    def __setup_torch_module__(cls, config: tdf.PydanticModel) -> torch.nn.Module:
        raise ModuleSetupNotImplemented(
            f"{cls}.__setup_torch_module__ not implemented."
        )

    @property
    def module(
        self,
    ) -> FunctionalModuleWithoutBuffers[tdf.P, tdf.R] | FunctionalModuleWithBuffers[
        tdf.P, tdf.R
    ]:
        return self._module_state.module

    @property
    def parameters(self) -> tuple[torch.nn.Parameter, ...]:
        return self._module_state.parameters

    @property
    def buffers(self) -> tuple[torch.Tensor, ...]:
        return self._module_state.buffers

    @property
    def named_buffers(self) -> NamedBuffers:
        return self._module_state.named_buffers

    def __call__(self, *args: tdf.P.args, **kwargs: tdf.P.kwargs) -> tdf.R:
        return self._module_state(*args, **kwargs)

    def show(self, max_n_params: int = 2) -> None:
        """Show a pretty representation of self."""
        console = Console()
        console.rule(f"{self.__class__.__name__}")
        console.print(
            Panel(
                Syntax(json_to_yaml(self.config.json()), lexer="yaml"),
                title=f"Config: {self.config.__class__.__name__}",
                border_style="blue",
            )
        )
        console.print(
            Panel(str(self._module_state.module), title="Module", border_style="yellow")
        )
        if max_n_params > 0:
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Parameters", width=console.width, justify="center")
            for param in self._module_state.parameters[:max_n_params]:
                table.add_row(str(lt.lovely(param)))
            console.print(table)
        if self._module_state.has_buffers:
            console.print(
                self.named_buffers.as_table(
                    name_column_width=24, buffers_column_width=console.width - 24
                )
            )
