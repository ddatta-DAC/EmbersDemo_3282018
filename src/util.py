import re

def clean_entity_name( e_name ):
    regex = re.compile(r"\(.*\)")
    def strip_brackets(_e_name):
        _text = _e_name
        while (regex.findall(_text)):
            for m in regex.findall(_text):
                _text = _text.replace(m, "").strip()
        _text = filter(lambda x: x not in set(['the']), _text.split())
        return " ".join(_text).strip()

    res = strip_brackets(e_name)

    # print res
    return res
