from unicodedata import normalize as nm
import re


def normalize_html_text(text: str) -> str:
    if text is not None:
        t = text.strip()
        t = nm('NFKC', t)
        t = t.replace(' ', '')
        t = t.replace('\n', '')
        t = re.sub('^[\[][1-9]*[\]]$', '', t) # 将[12]这样的标签
        return t
    else:
        return ''
    
def is_all_chinese(strs: str):
    for _char in strs:
        if not '\u4e00' <= _char <= '\u9fa5':
            return False
    return True

def is_all_english(strs: str):
    return strs.encode('utf-8').isalpha()