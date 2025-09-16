import json

import init_django_orm  # noqa: F401
from db.models import Race, Skill, Player, Guild


def main() -> None:
    with open("players.json", "r") as players:
        data_about_players = json.load(players)

    for player, data in data_about_players.items():
        player_name = player
        player_email = data.get("email")
        player_bio = data.get("bio")
        player_race = data.get("race")
        race_skills = player_race.get("skills")
        player_guild = data.get("guild")

        instance_race, create = Race.objects.get_or_create(
            name=player_race.get("name"),
            defaults={"description": player_race.get("description")}
        )

        if race_skills:
            for skill in player_race.get("skills"):
                Skill.objects.get_or_create(
                    name=skill.get("name"),
                    defaults={
                        "bonus": skill.get("bonus"),
                        "race": instance_race
                    }
                )

        if player_guild:
            instance_guild, created = Guild.objects.get_or_create(
                name=player_guild.get("name"),
                defaults={"description": player_guild.get("description")}
            )
        else:
            instance_guild = None

        Player.objects.get_or_create(
            nickname=player_name,
            defaults={
                "email": player_email,
                "bio": player_bio,
                "guild": instance_guild,
                "race": instance_race
            }
        )


if __name__ == "__main__":
    main()
