import pytest
from preconstruct.sources import NeurobankSource, MemorySource


@pytest.fixture
def nbank_stimuli():
    return [
        "ztqee46x",
        "g29wxi4q",
        "mrel2o09",
        "vekibwgj",
        "l1a3ltpy",
        "igmi8fxa",
        "c95zqjxq",
        "w08e1crn",
        "jkexyrd5",
        "p1mrfhop",
    ]


@pytest.fixture
def nbank_responses():
    return ["P120_1_1_c92"]


@pytest.fixture
def nbank_url():
    return "https://gracula.psyc.virginia.edu/neurobank/"


async def test_neurobank(nbank_responses, nbank_stimuli, nbank_url):
    source = await NeurobankSource.create(nbank_url, nbank_stimuli, nbank_responses)
    assert len(source.get_responses()) == 1
    assert len(source.get_stimuli()) == len(nbank_stimuli)


async def test_neurobank_autonames(nbank_responses, nbank_stimuli, nbank_url):
    source = await NeurobankSource.create(
        nbank_url, [], nbank_responses, infer_stimuli=True
    )
    assert len(source.get_responses()) == 1
    assert len(source.get_stimuli()) == len(nbank_stimuli)


async def test_neurobank_from_file(nbank_responses, nbank_stimuli, nbank_url, tmp_path):
    stim_file = tmp_path / "stims"
    stim_file.write_text("\n".join(nbank_stimuli))
    resp_file = tmp_path / "resps"
    resp_file.write_text("\n".join(nbank_responses))
    source = await NeurobankSource.create(nbank_url, stim_file, resp_file)
    assert len(source.get_responses()) == 1
    assert len(source.get_stimuli()) == len(nbank_stimuli)


async def test_show_stimuli(nbank_responses, nbank_stimuli, nbank_url):
    source = await NeurobankSource.create(nbank_url, [], nbank_responses)
    assert source.stimuli_names_from_pprox() == set(nbank_stimuli)


async def test_bad_order(nbank_responses, nbank_stimuli, nbank_url):
    source = await NeurobankSource.create(nbank_url, nbank_responses, nbank_stimuli)
    with pytest.raises(ValueError):
        source.get_responses()
