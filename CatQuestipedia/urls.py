from django.urls import path, include
from CatQuestipedia import views


urlpatterns = [
    path('', views.home, name="home"),
    path("why/", views.index, name="index"),
    path("search/", views.search, name="search"),
    path("create account/", views.create, name="create"),
    path("profile/", views.profile, name="profile"),
    path("new playthrough/", views.new_playthrough, name="new_playthrough"),
    path("playthrough/<int:id>/mass update/", views.mass_update, name="mass_update"),
    path('', include("django.contrib.auth.urls")),
    path("<str:gameid>/", include(
            [
                path("", views.catquestversion, name="catquestversion"),
                path("characters/", include(
                        [
                            path("", views.characters, name="characters"),
                            path("<str:characterid>/", views.character_detail, name="character-detail"),
                        ]
                    ),
                ),
                path("enemies/", include(
                        [
                            path("", views.enemies, name="enemies"),
                            path("<str:enemyid>/", views.enemy_detail, name="enemy-detail"),
                        ]
                    ),
                ),
                path("equipment/", include(
                        [
                            path("", views.equipment, name="equipment"),
                            path("<str:itemid>/", views.equipmentitem, name="equipment-item"),
                        ]
                    ),
                ),
                path("spells/", include(
                    [
                        path("", views.spells, name="spells"),
                        path("<str:spellid>/", views.spell_detail, name="spell-detail"),
                    ]
                    ),
                ),
                path("quests/", include(
                    [
                        path("", views.quests, name="quests"),
                        path("<str:questid>/", views.quest_detail, name="quest-detail")
                    ]
                ),
                ),
                path("locations/", include(
                        [
                            path("", views.locations, name="locations"),
                            path("<str:locationid>/", views.location_detail, name="location-detail"),
                        ]
                    ),
                ),
                path("mewgame/", include (
                    [
                        path("", views.mewgame, name="mewgame"),
                        path("<str:mewgameid>/", views.mewgame_detail, name="mewgame-detail"),
                    ]
                )),
            ]
        ),
    ),
]