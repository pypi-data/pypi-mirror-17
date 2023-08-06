import re
import time

from dateutil import parser


def read_asset(asset_string):
    re_asset = re.compile(r'(?P<number>\d*\.?\d+)\s?(?P<unit>[a-zA-Z]+)')
    res = re_asset.match(asset_string)
    return {'value': float(res.group('number')), 'symbol': res.group('unit')}


def parse_payout(payout):
    return read_asset(payout)['value']


def time_diff(time1, time2):
    time1 = parser.parse(time1 + "UTC").timestamp()
    time2 = parser.parse(time2 + "UTC").timestamp()
    return time2 - time1


def is_comment(item):
    if item['permlink'][:3] == "re-":
        return True

    return False


def time_elapsed(post):
    created_at = parser.parse(post['created'] + "UTC").timestamp()
    now_adjusted = time.time()
    return now_adjusted - created_at
