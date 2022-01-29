import pytest
import brutesleuth
# Testing functions of Base chain chains


@pytest.mark.parametrize("length,base", [
    (4, 2),
    (3, 8),
    (2, 16),
])
class TestBaseChain:
    def test_length(self, length, base):
        chain = brutesleuth.BaseChain(base, length)
        assert len(chain) == base ** length

    @pytest.mark.parametrize("index", [0, 2, 5, 12])
    def test_set_index(self, base, length, index):
        chain = brutesleuth.BaseChain(base, length)
        chain.setIndex(index)
        assert chain.__next__() == index

    def test_incremental_result(self, length, base):
        chain = brutesleuth.BaseChain(base, length)
        chain.setIndex(0)
        for result, expected in zip(chain, range(base ** length)):
            assert result == expected

# Testing handler functions


@pytest.mark.parametrize("format_string,format_frame", [
    ("SKY-{4aA}-{4d}", "SKY-{:4s}-{:4s}"),
    ("SKY-{4aA}-{:4d}", "SKY-{:4s}-{:4d}"),
    ("Password{2d}", "Password{:2s}"),
    ("Binary{:04b}", "Binary{:04b}"),
])
def test_init_formatting(format_string, format_frame):
    result, _ = brutesleuth.init_formatting(format_string)
    assert result == format_frame


@pytest.mark.parametrize("format_string,format_mask", [
    ("SKY-{4aA}-{4d}", "?l?u,SKY-?1?1?1?1-?d?d?d?d"),
    ("SKY-{4aA}-{:4d}", "?l?u,SKY-?1?1?1?1-?d?d?d?d"),
    ("Password{2d}", "Password?d?d"),
    ("Binary{:04b}", "01,Binary?1?1?1?1"),
])
def test_convert_to_mask(format_string, format_mask):
    assert brutesleuth.convert_to_mask(format_string) == format_mask


@pytest.mark.parametrize("format_string,real_string,expected_results", [
    ("SKY-{:4s}-{:4s}", "SKY-Aefa-0146", "Aefa_0146"),
    ("SKY-{:4s}-{:4d}", "SKY-Aefa-0146", "Aefa_0146"),
    ("Password{:2s}", "Password83", "83"),
    ("Binary{:04b}", "Binary0100", "0100")
])
def test_get_string_variations(format_string, real_string, expected_results):
    results = brutesleuth.get_string_variations(format_string, real_string)
    packing = "_".join(results)
    assert packing == expected_results
