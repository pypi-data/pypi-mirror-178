#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" View Generator: Entity Spans for Long-Range Synonym Swapping """


from pprint import pprint
from typing import List

from collections import defaultdict

from baseblock import EnvIO
from baseblock import BaseObject


class GeneratePlusSpans(BaseObject):
    """ View Generator: Entity Spans for Long-Range Synonym Swapping """

    def __init__(self):
        """ Change Log

        Created:
            25-Nov-2022
            craigtrim@gmail.com
            *   https://github.com/craigtrim/owl-finder/issues/4
        Updated:
            28-Nov-2022
            craigtrim@gmail.com
            *   use hash to ensure uniqueness in spans
                https://github.com/craigtrim/owl-finder/issues/4#issuecomment-1329990189
        """
        BaseObject.__init__(self, __name__)

    def _to_dict(self,
                 canon: str,
                 tokens: list) -> dict:

        tokens = sorted(set(tokens), reverse=False)
        if not len(tokens):
            return None

        # TODO: all these values have to be default only when not otherwise specified
        distance = EnvIO.int_or_default('SPAN_DISTANCE', 3)
        return {
            'content': tokens,
            'distance': distance,
            'forward': True,
            'reverse': True,
            'canon': canon
        }

    def process(self,
                d_results: dict) -> dict:

        hashes = set()
        d_spans = defaultdict(list)

        for entity in d_results:

            synonyms = d_results[entity]
            synonyms = [x for x in synonyms if '+' in x]

            for synonym in synonyms:

                tokens = synonym.split('+')
                d_result = self._to_dict(entity, tokens[1:])

                # 20221128; Ensure Uniqueness
                # https://github.com/craigtrim/owl-finder/issues/4#issuecomment-1329990189
                hash_d_result = hash(''.join([
                    str(x) for x in d_result.values()
                ]))

                if hash_d_result not in hashes:
                    d_spans[tokens[0]].append(d_result)
                    hashes.add(hash_d_result)

        return dict(d_spans)
