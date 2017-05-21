from digital_logic.experiment.reading import get_section_obj


def test_get_section_obj_success():
    section = get_section_obj('preface')
    assert section['name'] == 'preface'

