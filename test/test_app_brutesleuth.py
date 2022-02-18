import pytest
import subprocess
import brutesleuth
import os

bin_location = os.path.join(".", "bin", "brutesleuth")
root_location = os.path.join(".", "fbrutesleuth.py")


@pytest.mark.skip("Use of subprocess makes github actions fail for some reason")
def test_bin_basecase():
    format_string = "{4d}"
    result = "\n".join([f"{a:04d}" for a in range(10 ** 4)])+"\n"
    assert result == subprocess.check_output(
        [bin_location, format_string]).decode("utf-8")


@pytest.mark.skip("Use of subprocess makes github actions fail for some reason")
def test_bin_length():
    length = 20
    format_string = "SKY-{4a}-{4d}"
    result = "\n".join([f"SKY-aaaa-{a:04d}" for a in range(length)])+"\n"
    assert result == subprocess.check_output(
        [bin_location, format_string, "-l", str(length)]).decode("utf-8")


@pytest.mark.skip("Use of subprocess makes github actions fail for some reason")
def test_bin_setpoint():
    length = 20
    start_num = 250
    format_string = "SKY-abcd-{:04d}"
    result = "\n".join([format_string.format(start_num + a)
                        for a in range(length)])+"\n"
    assert result == subprocess.check_output(
        [bin_location, "SKY-{4a}-{4d}", "-l", str(length), "-s",
         format_string.format(start_num)]).decode("utf-8")


@pytest.mark.skip("Use of subprocess makes github actions fail for some reason")
def test_bin_random():
    format_string = "SKY-{4aA}-{4d}"
    internal_format = brutesleuth.init_formatting(format_string)[0]
    tool_output = subprocess.check_output(
        [bin_location, format_string, "--random"]).decode("utf-8").rstrip()
    brutesleuth.get_string_variations(internal_format, tool_output)


@pytest.mark.skip("Use of subprocess makes github actions fail for some reason")
def test_bin_mask():
    format_string = "SKY-{4aA}-{4d}"
    mask = "?l?u,SKY-?1?1?1?1-?d?d?d?d"
    tool_output = subprocess.check_output(
        [bin_location, format_string, "--mask"]).decode("utf-8").rstrip()
    assert tool_output == mask


def test_root_basecase():
    format_string = "{4d}"
    result = "\n".join([f"{a:04d}" for a in range(10 ** 4)])+"\n"
    assert result == subprocess.check_output(
        [root_location, format_string]).decode("utf-8")


def test_root_length():
    length = 20
    format_string = "SKY-{4a}-{4d}"
    result = "\n".join([f"SKY-aaaa-{a:04d}" for a in range(length)])+"\n"
    assert result == subprocess.check_output(
        [root_location, format_string, "-l", str(length)]).decode("utf-8")


def test_root_setpoint():
    length = 20
    start_num = 250
    format_string = "SKY-abcd-{:04d}"
    result = "\n".join([format_string.format(start_num + a)
                        for a in range(length)])+"\n"
    assert result == subprocess.check_output(
        [root_location, "SKY-{4a}-{4d}", "-l", str(length), "-s",
         format_string.format(start_num)]).decode("utf-8")


def test_root_random():
    format_string = "SKY-{4aA}-{4d}"
    internal_format = brutesleuth.init_formatting(format_string)[0]
    tool_output = subprocess.check_output(
        [root_location, format_string, "--random"]).decode("utf-8").rstrip()
    brutesleuth.get_string_variations(internal_format, tool_output)


def test_root_mask():
    format_string = "SKY-{4aA}-{4d}"
    mask = "?l?u,SKY-?1?1?1?1-?d?d?d?d"
    tool_output = subprocess.check_output(
        [root_location, format_string, "--mask"]).decode("utf-8").rstrip()
    assert tool_output == mask
