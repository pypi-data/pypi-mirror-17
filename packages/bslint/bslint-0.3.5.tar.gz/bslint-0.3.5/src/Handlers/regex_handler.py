import src.regexs as regexs
import re


class RegexHandler:

    @staticmethod
    def find_match(characters):
        for regex in regexs.List:
            match = re.match(regex[0], characters, re.IGNORECASE)
            if match:
                break
        if not match:
            raise ValueError('NO MATCH FOUND')
        return {"match": match, "token_type": regex[1], "indentation_level": regex[2]}