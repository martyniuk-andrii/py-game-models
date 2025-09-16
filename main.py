import json

import init_django_orm  # noqa: F401
from db.models import Race, Skill, Player, Guild


def main() -> None:
    with open("players.json", "r") as players:
        data_about_players = json.load(players)

    for player, data in data_about_players.items():
        name = player
        email = data.get("email")
        bio = data.get("bio")
        race = data.get("race")
        skills_in_race = race.get("skills") if race else None
        guild = data.get("guild")

        race_in_database, create = Race.objects.get_or_create(
            name=race.get("name"),
            defaults={"description": race.get("description")}
        )

        if skills_in_race:
            for skill in skills_in_race:
                Skill.objects.get_or_create(
                    name=skill.get("name"),
                    race=race_in_database,
                    defaults={
                        "bonus": skill.get("bonus"),

                    }
                )

        if guild:
            guild_in_database, created = Guild.objects.get_or_create(
                name=guild.get("name"),
                defaults={"description": guild.get("description")}
            )
        else:
            guild_in_database = None

        Player.objects.get_or_create(
            nickname=name,
            defaults={
                "email": email,
                "bio": bio,
                "guild": guild_in_database,
                "race": race_in_database
            }
        )


if __name__ == "__main__":
    main()
