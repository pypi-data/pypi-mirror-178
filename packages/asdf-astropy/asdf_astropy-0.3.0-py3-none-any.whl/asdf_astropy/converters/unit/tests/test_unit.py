import warnings

import asdf
import pytest
from asdf.tests import helpers
from astropy import units


def vounit_compatible(unit):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=units.UnitsWarning)
        try:
            unit.to_string(format="vounit")
            return True
        except Exception:
            return False


def create_units():
    return [u for u in list(units.__dict__.values()) if isinstance(u, units.UnitBase) and vounit_compatible(u)]


@pytest.mark.parametrize("unit", create_units())
# Ignore warnings due to VOUnit deprecations
@pytest.mark.filterwarnings("ignore::astropy.units.core.UnitsWarning")
def test_serialization(unit, tmp_path):
    file_path = tmp_path / "test.asdf"
    with asdf.AsdfFile() as af:
        af["unit"] = unit
        af.write_to(file_path)

    with asdf.open(file_path) as af:
        assert af["unit"].is_equivalent(unit)


def test_read():
    yaml = """
unit: !unit/unit-1.0.0 "2.1798721  10-18kg m2 s-2"
    """
    buff = helpers.yaml_to_asdf(yaml)
    with asdf.open(buff) as af:
        assert af["unit"].is_equivalent(units.Ry)


def create_non_vounits():
    return [u for u in list(units.__dict__.values()) if isinstance(u, units.UnitBase) and not vounit_compatible(u)]


@pytest.mark.parametrize("unit", create_non_vounits())
def test_error(unit, tmp_path):
    file_path = tmp_path / "test.asdf"
    with asdf.AsdfFile() as af:
        af["unit"] = unit
        with pytest.raises(
            ValueError, match=r"Unit '.*' is not representable as VOUnit and cannot be serialized to ASDF"
        ):
            af.write_to(file_path)
