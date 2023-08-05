#!../../../venv/bin/pytest

from example_config import Car

import pytest

def test__accelerate() -> None:
	c1 = Car()
	assert c1.speed == 0
	assert c1.speed_limit == 50

	c1.accelerate(49)
	assert c1.speed == 49
	c1.accelerate(1)
	assert c1.speed == 50
	with pytest.raises(ValueError):
		c1.accelerate(1)
	assert c1.speed == 50


def test__print_config(capsys: 'pytest.CaptureFixture[str]') -> None:
	c1 = Car()
	c1.print_config()
	captured = capsys.readouterr()
	assert captured.out == "traffic-law.speed-limit: 50\n"
