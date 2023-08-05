import dataclasses
from datetime import datetime
from typing import Any, List, Type, TypeVar

import pydantic

from chalk.features import DataFrame, Feature, Filter
from chalk.features.feature_field import HasOnePathObj
from chalk.features.resolver import Cron, OfflineResolver, OnlineResolver, SinkResolver
from chalk.parsed.duplicate_input_gql import (
    UpsertDataFrameGQL,
    UpsertFeatureGQL,
    UpsertFeatureIdGQL,
    UpsertFeatureReferenceGQL,
    UpsertFeatureTimeKindGQL,
    UpsertFilterGQL,
    UpsertHasManyKindGQL,
    UpsertHasOneKindGQL,
    UpsertReferencePathComponentGQL,
    UpsertResolverGQL,
    UpsertResolverOutputGQL,
    UpsertScalarKindGQL,
    UpsertSinkResolverGQL,
    UpsertStreamResolverGQL,
)
from chalk.streams._internal import StreamResolver
from chalk.utils import paths

T = TypeVar("T")


try:
    import attrs
except ImportError:
    attrs = None


@dataclasses.dataclass
class _ConvertedType:
    name: str
    bases: List[str]


def _get_qualified_class_name(cls: Type[Any]):
    mod = cls.__module__
    return cls.__qualname__ if mod == "builtins" else f"{mod}.{cls.__qualname__}"


def _convert_type(underlying_type: Type) -> _ConvertedType:
    assert isinstance(underlying_type, type), f"Underlying type is not a type: '{str(underlying_type)}'"
    base_classes = [x.__name__ for x in type.mro(underlying_type)]

    # Attrs and Dataclasses don't technically have base classes
    # Pydantic calls their base class BaseModel which is way too generic for string comparison
    # For simplicity on the server-side validation, we'll come up with our own "base class" names
    if dataclasses.is_dataclass(underlying_type):
        base_classes.append("__dataclass__")
    if attrs is not None and isinstance(underlying_type, type) and attrs.has(underlying_type):
        base_classes.append("__attrs__")
    if issubclass(underlying_type, pydantic.BaseModel):
        base_classes.append("__pydantic__")

    return _ConvertedType(
        name=underlying_type.__name__,
        bases=base_classes,
    )


def _get_feature_id(s: Feature):
    assert s.name is not None, "Could not find feature name"
    assert s.namespace is not None, "Could not find feature namespace"
    return UpsertFeatureIdGQL(
        fqn=s.fqn,
        name=s.name,
        namespace=s.namespace,
    )


def _convert_df(df: Type[DataFrame]) -> UpsertDataFrameGQL:
    return UpsertDataFrameGQL(
        columns=[_get_feature_id(f) for f in df.columns if not f.is_autogenerated],
        filters=[convert_type_to_gql(f) for f in df.filters],
    )


def _get_path_component(pc: HasOnePathObj) -> UpsertReferencePathComponentGQL:
    assert isinstance(pc.parent, Feature), f"Parent in relationship path not a feature, but {type(pc).__name__}"
    return UpsertReferencePathComponentGQL(
        parent=_get_feature_id(pc.parent),
        child=_get_feature_id(pc.child),
        parentToChildAttributeName=pc.parent_to_child_attribute_name,
    )


def convert_type_to_gql(t: Any):
    if isinstance(t, StreamResolver):
        return UpsertStreamResolverGQL(
            fqn=t.fqn,
            kind="stream",
            sourceClassName=_get_qualified_class_name(t.source.__class__),
            sourceConfig=t.source.config_to_json(),
            functionDefinition=t.function_definition,
            environment=[t.environment] if isinstance(t.environment, str) else t.environment,
            doc=t.fn.__doc__,
            machineType=t.machine_type,
        )

    if isinstance(t, SinkResolver):
        return UpsertSinkResolverGQL(
            fqn=t.fqn,
            functionDefinition=t.function_definition,
            inputs=[
                UpsertFeatureReferenceGQL(
                    underlying=_get_feature_id(f),
                    path=[_get_path_component(p) for p in f.path or []],
                )
                for f in t.inputs
                if not f.is_autogenerated
            ],
            environment=t.environment,
            tags=t.tags,
            doc=t.doc,
            machineType=t.machine_type,
            bufferSize=t.buffer_size,
            debounce=t.debounce,
            maxDelay=t.max_delay,
            upsert=t.upsert,
        )

    if isinstance(t, (OnlineResolver, OfflineResolver)):
        cron = t.cron
        if isinstance(cron, Cron):
            assert t.cron.schedule is not None, "`Cron` object must be constructed with a `schedule` property."
            cron = cron.schedule
        return UpsertResolverGQL(
            fqn=t.fqn,
            kind="offline" if isinstance(t, OfflineResolver) else "online",
            functionDefinition=t.function_definition,
            inputs=[
                UpsertFeatureReferenceGQL(
                    underlying=_get_feature_id(f),
                    path=[_get_path_component(p) for p in f.path or []],
                )
                for f in t.inputs
                if not f.is_autogenerated
            ],
            output=UpsertResolverOutputGQL(
                features=[
                    _get_feature_id(f)
                    for f in t.output.features
                    if (not isinstance(f, type) or not issubclass(f, DataFrame)) and not f.is_autogenerated
                ],
                dataframes=[
                    _convert_df(f) for f in t.output.features if isinstance(f, type) and issubclass(f, DataFrame)
                ],
            ),
            environment=t.environment,
            tags=t.tags,
            doc=t.doc,
            cron=cron,
            machineType=t.machine_type,
        )

    if isinstance(t, Feature):
        assert t.name is not None, "Feature has no name"
        assert t.namespace is not None, "Feature has no namespace"
        scalar_kind_gql = None
        has_one_kind_gql = None
        has_many_kind_gql = None
        feature_time_kind_gql = None
        if t.is_autogenerated:
            raise RuntimeError("Autogenerated features should not be converted")
        if t.is_has_one:
            has_one_kind_gql = UpsertHasOneKindGQL(join=convert_type_to_gql(t.join))
        elif t.is_has_many:
            has_many_kind_gql = UpsertHasManyKindGQL(
                join=convert_type_to_gql(t.join),
                columns=None,
                filters=None,
            )
        elif t.is_feature_time:

            assert t.typ is not None, "Feature time has no type assigned"
            assert issubclass(t.typ.underlying, datetime), "Feature time is not of type datetime"
            feature_time_kind_gql = UpsertFeatureTimeKindGQL()
        else:
            assert t.typ is not None
            converted_type = _convert_type(t.typ.underlying)
            scalar_kind_gql = UpsertScalarKindGQL(
                scalarKind=converted_type.name,
                primary=t.primary,
                baseClasses=converted_type.bases,
                version=t.version,
                hasEncoderAndDecoder=t.encoder is not None and t.decoder is not None,
            )

        return UpsertFeatureGQL(
            id=UpsertFeatureIdGQL(
                fqn=t.fqn,
                name=t.name,
                namespace=t.namespace,
            ),
            maxStaleness=t.max_staleness,
            description=t.description,
            owner=t.owner,
            etlOfflineToOnline=t.etl_offline_to_online,
            tags=t.tags,
            hasOneKind=has_one_kind_gql,
            hasManyKind=has_many_kind_gql,
            scalarKind=scalar_kind_gql,
            featureTimeKind=feature_time_kind_gql,
            namespacePath=str(paths.get_classpath(t.features_cls)),
        )

    if isinstance(t, Filter):
        return UpsertFilterGQL(
            lhs=_get_feature_id(t.lhs),
            op=t.operation,
            rhs=_get_feature_id(t.rhs),
        )

    return t
