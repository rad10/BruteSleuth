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
