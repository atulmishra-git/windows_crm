from collections import namedtuple


ATTACHMENT_KINDS = {
    'AB': 'offer',
    'AG-B': 'offer confirmation',
    'M-B': 'install',
    'RG': 'invoice'
}

CALL_NOTE_PRIORITY = namedtuple('CALL_NOTE_PRIORITY', 'high medium low')(*range(3))
