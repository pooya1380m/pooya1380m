import pytest
from dialux_agent import calc, compliance, photometry

_h = ["Co", "1", "Name"] + ["0"] * 22 + ["1"]
LDT = "\n".join(_h + ["2", "1", "4000", "830", "80", "40"]) + "\n"

IES = """IESNA:LM-63-2002
[LUMCAT] TEST1
TILT=NONE
1 3000 1 3 1 1 2 0.5 0.5 0
1 1 30
0 45 90
100 80 50
"""


def test_ldt():
    l = photometry.parse_ldt(LDT)
    assert l.luminous_flux_lm == 8000 and l.power_w == 40 and l.efficacy_lm_per_w == 200


def test_ies():
    l = photometry.parse_ies(IES)
    assert l.luminous_flux_lm == 3000 and l.power_w == 30 and l.max_intensity_cd == 100


def test_calc():
    n = calc.luminaires_needed(500, 6, 5, 4000, 2.0)
    assert 8 <= n <= 14
    assert calc.average_illuminance(n, 4000, 6, 5, calc.utilance_estimate(calc.room_index(6, 5, 2.0))) >= 500
    with pytest.raises(ValueError):
        calc.luminaires_needed(500, 0, 5, 4000, 2.0)


def test_compliance():
    assert compliance.check("Office", 520, 0.65, 18, 80) == []
    assert len(compliance.check("office", 300, 0.4)) == 2
    with pytest.raises(KeyError):
        compliance.check("moon", 1, 1)
