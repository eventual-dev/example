from eventual.dispatch.registry import Registry
from eventual_tortoise.work_unit import TortoiseWorkUnit

eventual_registry = Registry[TortoiseWorkUnit]()
