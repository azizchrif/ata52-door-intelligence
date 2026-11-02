from src.transform.clean_sdr import model_family, normalize_make


def test_normalize_make_merges_bombardier():
    assert normalize_make("CNDAIR") == "BOMBARDIER"
    assert normalize_make("BOMBDR") == "BOMBARDIER"


def test_normalize_make_handles_case_and_spaces():
    assert normalize_make(" boeing ") == "BOEING"


def test_normalize_make_keeps_unknown():
    assert normalize_make("CESSNA") == "CESSNA"


def test_model_family_airbus():
    assert model_family("A321231") == "A321"
    assert model_family("A321253NX") == "A321"
    assert model_family("A320*") == "A320"


def test_model_family_boeing():
    assert model_family("737823") == "737-800"
    assert model_family("7377H4") == "737-700"
    assert model_family("757232") == "757-200"


def test_model_family_crj():
    assert model_family("CL6002D24") == "CRJ900"
    assert model_family("CL6002B19") == "CRJ200"