BASE_URL = 'http://www.basketball-reference.com'

import boxscores
import pbp
import seasons
import teams

from boxscores import BoxScore
from seasons import Season
from teams import Team

__all__ = [
    'BASE_URL',
    'boxscores', 'BoxScore',
    'pbp',
    'seasons', 'Season',
    'teams', 'Team',
]
