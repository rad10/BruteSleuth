import pytest
import brutesleuth


@pytest.mark.skip(reason="WIP need to complete")
class TestBruteChain:
    def test_length(self, length, iters):
        chain = brutesleuth.BruteChain(length, *iters)
        assert len(chain) == sum(iters, key=len)

    def test_set_index(self, length, iters, value):
        chain = brutesleuth.BruteChain(length, *iters)
        chain.setIndex(value)
        assert chain.__next__() == value

    @pytest.mark.skip(reason="WIP need to complete")
    def test_incremental_result(self, length, iters):
        pass


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

    def test_get_random(self, length, base):
        chain = brutesleuth.BaseChain(base, length)
        for i in range(10):
            assert(0 <= chain.getRandom() < base ** length)


@pytest.mark.parametrize("length", [
    2, 3, 5, 8, 10
])
class TestDecimalChain:
    def test_length(self, length):
        chain = brutesleuth.DecimalChain(length)
        assert len(chain) == 10 ** length

    @pytest.mark.parametrize("index", [0, 2, 5, 12, 18])
    def test_set_index(self, length, index):
        chain = brutesleuth.DecimalChain(length)
        chain.setIndex(index)
        assert chain.__next__() == f"{index:0{length:d}d}"

    def test_incremental_result(self, length):
        chain = brutesleuth.DecimalChain(length)
        chain.setIndex(0)
        for result, expected in zip(chain, map(
                lambda i: f"{i:0{length:d}d}", range(2 ** length))):
            assert result == expected

    def test_get_random(self, length):
        chain = brutesleuth.DecimalChain(length)
        for i in range(10):
            assert(0 <= int(chain.getRandom(), 10) < 10 ** length)


@pytest.mark.parametrize("length", [
    2, 3, 5, 8, 10
])
class TestHexadecimalChain:
    def test_length(self, length):
        chain = brutesleuth.HexadecimalChain(length)
        assert len(chain) == 16 ** length

    @pytest.mark.parametrize("index", [0, 2, 5, 12, 18])
    def test_set_index(self, length, index):
        chain = brutesleuth.HexadecimalChain(length)
        chain.setIndex(index)
        assert chain.__next__() == f"{index:0{length:d}x}"

    def test_incremental_result(self, length):
        chain = brutesleuth.HexadecimalChain(length)
        chain.setIndex(0)
        for result, expected in zip(chain, map(
                lambda i: f"{i:0{length:d}x}", range(2 ** length))):
            assert result == expected

    def test_get_random(self, length):
        chain = brutesleuth.HexadecimalChain(length)
        for i in range(10):
            assert(0 <= int(chain.getRandom(), 16) < 16 ** length)


@pytest.mark.parametrize("length", [
    2, 3, 5, 8, 20
])
class TestOctalChain:
    def test_length(self, length):
        chain = brutesleuth.OctalChain(length)
        assert len(chain) == 8 ** length

    @pytest.mark.parametrize("index", [0, 2, 5, 12, 18])
    def test_set_index(self, length, index):
        chain = brutesleuth.OctalChain(length)
        chain.setIndex(index)
        assert chain.__next__() == f"{index:0{length:d}o}"

    def test_incremental_result(self, length):
        chain = brutesleuth.OctalChain(length)
        chain.setIndex(0)
        for result, expected in zip(chain, map(
                lambda i: f"{i:0{length:d}o}", range(2 ** length))):
            assert result == expected

    def test_get_random(self, length):
        chain = brutesleuth.OctalChain(length)
        for i in range(10):
            assert(0 <= int(chain.getRandom(), 8) < 8 ** length)


@pytest.mark.parametrize("length", [
    4, 5, 6, 8, 10, 20
])
class TestBinaryChain:
    def test_length(self, length):
        chain = brutesleuth.BinaryChain(length)
        assert len(chain) == 2 ** length

    @pytest.mark.parametrize("index", [0, 2, 5, 12, 15])
    def test_set_index(self, length, index):
        chain = brutesleuth.BinaryChain(length)
        chain.setIndex(index)
        assert chain.__next__() == f"{index:0{length:d}b}"

    def test_incremental_result(self, length):
        chain = brutesleuth.BinaryChain(length)
        chain.setIndex(0)
        for result, expected in zip(chain, map(
                lambda i: f"{i:0{length:d}b}", range(2 ** length))):
            assert result == expected

    def test_get_random(self, length):
        chain = brutesleuth.BinaryChain(length)
        for i in range(10):
            assert(0 <= int(chain.getRandom(), 2) < 2 ** length)


@pytest.mark.skip(reason="WIP need to complete")
class TestIterativeProduct:
    def test_length(self, iterators):
        iter_chain = brutesleuth.iterative_product(*iterators)
        length = 1
        for i in iterators:
            length *= len(i)
        assert len(iter_chain) == length

    @pytest.mark.skip(
        reason="WIP still need to figure out how to configure this")
    def test_incremental_result(self, iterators):
        pass


@pytest.mark.skip(reason="WIP need to complete")
class TestBruteListChain:
    def test_length(self, fstring, gens):
        brutelist_chain = brutesleuth.BruteListChain(fstring, gens)
        length = 1
        for i in gens:
            length *= len(i)
        assert len(brutelist_chain) == length

    @pytest.mark.skip(
        reason="WIP still need to figure out how to configure this")
    def test_incremental_result(self, fstring, gens):
        pass

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
    results = brutesleuth.get_string_variations(
        format_string, real_string)
    if type(results) is str:
        packing = results
    else:
        packing = "_".join(results)
    assert packing == expected_results


@pytest.mark.parametrize("format_string,set_string", [
    ("SKY-{4aA}-{4d}", "SKY-Aefa-0146"),
    ("Hash{:02d}-{:04b}", "Hash02-1100"),
    ("Password{:2d}", "Password83"),
    ("Binary{:04b}", "Binary0100")
])
def test_set_position(format_string, set_string):
    format_frame, gens = brutesleuth.init_formatting(format_string)
    new_gens = brutesleuth.set_position(format_frame, set_string, gens)
    chain = brutesleuth.BruteListChain(format_frame, new_gens)
    assert chain.__next__() == set_string


@pytest.mark.parametrize("format_string", [
    "SKY-{4aA}-{4d}", "SKY-{4aA}-{:04d}",
    "Password{:2d}", "Binary{:04b}"
])
def test_print_random(format_string):
    format_frame, gens = brutesleuth.init_formatting(format_string)
    rand_result = brutesleuth.print_random(format_frame, gens)

    # checking if it can be extrapolated
    brutesleuth.get_string_variations(format_frame, rand_result)
