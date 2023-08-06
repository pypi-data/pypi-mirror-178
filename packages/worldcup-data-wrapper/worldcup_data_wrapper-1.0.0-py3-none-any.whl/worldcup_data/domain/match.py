
from dataclasses import dataclass

@dataclass
class Match:

    datetime: str
    home_team_country: str
    away_team_country: str
    stage_name: str
    winner: str

    def from_json(json_content):
        return Match(
            json_content['datetime'],
            json_content['home_team_country'],
            json_content['away_team_country'],
            json_content['stage_name'],
            json_content['winner'],
        )

