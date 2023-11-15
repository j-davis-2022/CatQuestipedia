from django.shortcuts import render, redirect
from django.apps import apps
from .models import *
import os
import datetime
from .forms import create_account_form
from django.contrib import messages
from django.utils.safestring import mark_safe
# from django import request
# from django.contrib.auth import login, authenticate
# from django.http import HttpResponse

datestamps = []
for root, y, files in os.walk("CatQuestipedia"):
    for file in files:
        timestamp = os.path.getmtime(os.path.join(root, file))
        date = datetime.datetime.fromtimestamp(timestamp)
        datestamps.append(date)

for root, y, files in os.walk("templates"):
    for file in files:
            timestamp = os.path.getmtime(os.path.join(root, file))
            date = datetime.datetime.fromtimestamp(timestamp)
            datestamps.append(date)
datestamp = max(datestamps)

complete_lvl = {}
for item in Game.objects.all():
    game_lvl = Equipment.objects.filter(game=item).count()
    game_lvl += Spells.objects.filter(game=item).count()
    game_lvl += Quests.objects.filter(game=item).count()
    for value in Equipment.objects.filter(game=item).all():
        game_lvl += value.maxlvl
    for value in Spells.objects.filter(game=item):
         game_lvl += value.maxlvl
    complete_lvl[item] = game_lvl

e_complete_lvl = {}
for item in Game.objects.all():
    game_lvl = Equipment.objects.filter(game=item).count()
    for value in Equipment.objects.filter(game=item).all():
        game_lvl += value.maxlvl
    e_complete_lvl[item] = game_lvl

s_complete_lvl = {}
for item in Game.objects.all():
    game_lvl = Spells.objects.filter(game=item).count()
    for value in Spells.objects.filter(game=item):
         game_lvl += value.maxlvl
    s_complete_lvl[item] = game_lvl

q_complete_lvl = {}
for item in Game.objects.all():
    game_lvl = Quests.objects.filter(game=item).count()
    q_complete_lvl[item] = game_lvl

games = Game.objects.values()

# Create your views here.

def home(response):
    gentle_img = OtherImages.objects.get(name="gentlebros")
    return render(response, 'CatQuestipedia/home.html', {"Game": games, "modified": datestamp, "gentle_img": gentle_img, })

def index(response):
    return render(response, 'CatQuestipedia/base-template.html', {"Game": games, "modified": datestamp, })

def login(response):
    return render(response, 'registration/login.html', {"Game": games, "modified": datestamp, })

def create(response):
    if response.method == "POST":
        request_form = create_account_form(response.POST)
        if request_form.is_valid():
            request_form.save()
            return redirect("home")
    else:
        request_form = create_account_form()
    return render(response, 'CatQuestipedia/create-account.html', {"Game": games, "modified": datestamp, "form": request_form, })

def profile(request):
    user = request.user
    if user.is_authenticated:
        playthroughs = Playthroughs.objects.filter(user=user)
        playthroughs_list = {}
        height = Equipment.objects.all().order_by("-image_height")[:1]
        print(height[0].image_height)
        for item in playthroughs:
            max_completion = complete_lvl[item.game]
            e_max_completion = e_complete_lvl[item.game]
            s_max_completion = s_complete_lvl[item.game]
            q_max_completion = q_complete_lvl[item.game]
            completion = item.user_equipment.count()
            e_completion = item.user_equipment.count()
            s_completion = item.user_spells.count()
            q_completion = item.user_quests.count()
            completion += item.user_spells.count()
            completion += item.user_quests.count()
            for value in item.user_equipment.all():
                completion += value.equipment_level
                e_completion += value.equipment_level
            for value in item.user_spells.all():
                completion += value.spell_level
                s_completion += value.spell_level
            completion = 100*completion/max_completion
            e_completion = 100*e_completion/e_max_completion
            s_completion = 100*s_completion/s_max_completion
            q_completion = 100*q_completion/q_max_completion
            playthroughs_list[item] = {"total": completion, "equipment": e_completion, "spells": s_completion, "quests": q_completion, }
    else:
        playthroughs_list = {}
        height = [0]
    return render(request, 'CatQuestipedia/profile.html', {"Game": games, "modified": datestamp, "playthroughs": playthroughs_list, "height": height[0].image_height, }) #type: ignore

def search(response):
    searched = ""
    search_results = {}
    if response.method == "GET":
        searched = response.GET.get('searchedfor')
        if searched != "": 
            searched = searched.split(", ")
            games_search_results = {}
            for iteration in searched:
                for key, value in Game.search_rank(iteration):
                    item = Game.objects.get(title=key)
                    games_search_results[item.title] = {"rank": value, "tags": item.all_tags(), "url_name": "catquestversion", "url_param_1": key, "url_param_2": "none"}
            search_results["Games"] = games_search_results

            character_search_results = {}
            for iteration in searched:
                for key, value in Characters.search_rank(iteration):
                    item = Characters.objects.get(id=key)
                    character_search_results[item] = {"rank": value, "tags": item.all_tags(), "url_name": "character-detail", "url_param_1": item.game, "url_param_2": item.name}
            search_results["Characters"] = character_search_results

            enemy_search_results = {}
            for iteration in searched:
                for key, value in Enemies.search_rank(iteration):
                    item = Enemies.objects.get(id=key)
                    enemy_search_results[item] = {"rank": value, "tags": item.all_tags(), "url_name": "enemy-detail", "url_param_1": item.game, "url_param_2": item.name}
            search_results["Enemies"] = enemy_search_results

            equipment_search_results = {}
            for iteration in searched:
                for key, value in Equipment.search_rank(iteration):
                    item = Equipment.objects.get(id=key)
                    equipment_search_results[item] = {"rank": value, "tags": item.all_tags(), "url_name": "equipment-item", "url_param_1": item.game, "url_param_2": item.name}
            search_results["Equipment"] = equipment_search_results

            spell_search_results = {}
            for iteration in searched:
                for key, value in Spells.search_rank(iteration):
                    item = Spells.objects.get(id=key)
                    spell_search_results[item] = {"rank": value, "tags": item.all_tags(), "url_name": "spell-detail", "url_param_1": item.game, "url_param_2": item.name}
            search_results["Spells"] = spell_search_results

            quest_search_results = {}
            for iteration in searched:
                for key, value in Quests.search_rank(iteration):
                    item = Quests.objects.get(name=key)
                    quest_search_results[item] = {"rank": value, "tags": item.all_tags(), "url_name": "quest-detail", "url_param_1": item.game, "url_param_2": item.name}
            search_results["Quests"] = quest_search_results

            location_search_results = {}
            for iteration in searched:
                for key, value in Locations.search_rank(iteration):
                    item = Locations.objects.get(id=key)
                    location_search_results[item] = {"rank": value, "tags": item.all_tags(), "url_name": "location-detail", "url_param_1": item.game, "url_param_2": item.name}
            search_results["Locations"] = location_search_results

            mewgame_search_results = {}
            for iteration in searched:
                for key, value in MewGame.search_rank(iteration):
                    item = MewGame.objects.get(id=key)
                    mewgame_search_results[item.name] = {"rank": value, "tags": item.all_tags(), "url_name": "mewgame-detail", "url_param_1": item.game, "url_param_2": item.name}
            search_results["MewGame"] = mewgame_search_results
    return render(response, 'CatQuestipedia/search.html', {"Game": games, "searched_for": searched, "search": search_results,"modified": datestamp, })


def catquestversion(response, gameid):
    gameidvar = Game.objects.get(title=gameid)
    img = gameidvar.image
    return render(response, 'CatQuestipedia/game.html', {"name": gameid, "Game": games, "Gameid": gameidvar, "img": img,  "modified": datestamp, })


def characters(response, gameid):
    gameidvar = Game.objects.get(title=gameid)
    return render(response, 'CatQuestipedia/characters.html', {"game": str(gameid), "Game": games, "Gameid": gameidvar, "modified": datestamp, })

def character_detail(response, gameid, characterid):
    gameidvar = Game.objects.get(title=gameid)
    character = Characters.objects.get(name=characterid, game=gameidvar)
    boss = character.bosses_set.first() #type:ignore
    return render(response, "CatQuestipedia/character-detail.html", {"game": str(gameid), "Game": games, "Character": character, "boss": boss, "modified": datestamp, })

def enemies(response, gameid):
    gameidvar = Game.objects.get(title=gameid)
    return render(response, 'CatQuestipedia/enemies.html', {"game": str(gameid), "Game": games, "Gameid": gameidvar, "modified": datestamp, })

def enemy_detail(response, gameid, enemyid):
    gameidvar = Game.objects.get(title=gameid)
    enemy = Enemies.objects.get(name=enemyid, game=gameidvar)
    attacks = enemy.attacks.split(", ")
    return render(response, 'CatQuestipedia/enemy-detail.html', {"game": str(gameid), "Game": games, "Gameid": gameidvar, "enemy": enemy, "attacks": attacks, "modified": datestamp, })


def equipment(response, gameid):
    gameidvar = Game.objects.get(title=gameid)
    values = []
    height = Equipment.objects.filter(game=gameidvar).order_by("-image_height")[:1]
    for item in Equipment.objects.filter(game=gameidvar).filter(set_type="not full").values():
        if item["set"] not in values:
            value = item["set"]
            values.append(value)
    return render(response, 'CatQuestipedia/equipment.html', {"game": str(gameid), "Gameid": gameidvar, "Game": games, "height": height[0].image_height, "Not_full_set": values, "modified": datestamp})


def equipmentitem(request, gameid, itemid):
    gameidvar = Game.objects.get(title=gameid)
    item = Equipment.objects.filter(game=gameidvar).get(name=itemid)
    user = request.user
    if user.is_authenticated:
        user_playthroughs = Playthroughs.objects.filter(user=user).filter(game=gameidvar)
        playthrough_levels = {}
        for it in user_playthroughs:
            if it.user_equipment.filter(playthrough=it).filter(equipment=item).exists():
                playthrough_level = it.user_equipment.filter(playthrough=it).get(equipment=item)
                playthrough_levels[it.name] = playthrough_level.equipment_level
            else:
                playthrough_levels[it.name] = 0
        if request.method == "POST":
            playthrough = Playthroughs.objects.filter(user=user).filter(game=gameidvar).get(name = request.POST.get(item.name + "2"))
            entry = UserEquipment.objects.filter(user=user).filter(playthrough=playthrough).filter(equipment=item)
            if item.name + "1" in request.POST and entry.exists() == True:
                edit = UserEquipment.objects.filter(user=user).filter(playthrough=playthrough).get(equipment=item)
                edit.equipment_level = int(request.POST.get(item.name + "3"))
                edit.save()
            elif item.name + "1" in request.POST and entry.exists() == False:
                new = UserEquipment.objects.create(user=user, playthrough=playthrough, equipment=item, equipment_level=int(request.POST.get(item.name + "3")))
                new.save()
                playthrough.user_equipment.add(new)
                playthrough.save()
    else:
        user_playthroughs = None
        playthrough_levels = {}
    return render(request, "CatQuestipedia/equipment-item.html", {"game": str(gameid), "item": item, "Game": games, "modified": datestamp, "user_playthroughs": user_playthroughs, "playthrough_levels": playthrough_levels})


def spells(response, gameid):
    game_spells = Game.objects.get(title=gameid)
    return render(response, "CatQuestipedia/spells.html", {"game": str(gameid), "Game": games, "Gameid": game_spells, "modified": datestamp, })


def spell_detail(request, gameid, spellid):
    game_spells = Game.objects.get(title=gameid)
    spell = Spells.objects.get(name=spellid, game=game_spells)
    user = request.user
    if user.is_authenticated:
        user_playthroughs = Playthroughs.objects.filter(user=user).filter(game=game_spells)
        playthrough_levels = {}
        for it in user_playthroughs:
            if it.user_spells.filter(playthrough=it).filter(spell=spell).exists():
                playthrough_level = it.user_spells.filter(playthrough=it).get(spell=spell)
                playthrough_levels[it.name] = playthrough_level.spell_level
            else:
                playthrough_levels[it.name] = 0
        if request.method == "POST":
            playthrough = Playthroughs.objects.get(user=user, game = game_spells, name=request.POST.get(spell.name + "2"))
            entry = UserSpells.objects.filter(user=user, playthrough=playthrough, spell=spell)
            if spell.name + "1" in request.POST and entry.exists() == True:
                edit = UserSpells.objects.get(user=user, playthrough=playthrough, spell=spell)
                edit.spell_level = int(request.POST.get(spell.name + "3"))
                edit.save()
            elif spell.name + "1" in request.POST and entry.exists() == False:
                new = UserSpells.objects.create(user=user, playthrough=playthrough, spell=spell, spell_level=int(request.POST.get(spell.name + "3")))
                new.save()
                playthrough.user_spells.add(new)
                playthrough.save()
    else:
        user_playthroughs = None
        playthrough_levels = {}
    return render(request, "CatQuestipedia/spell-detail.html", {"game": str(gameid), "Game": games, "Gameid": game_spells, "spell":spell, "user_playthroughs": user_playthroughs, "playthrough_levels": playthrough_levels, "modified": datestamp, })


def quests(response, gameid):
    game = Game.objects.values()
    gameidvar = Game.objects.get(title=gameid)
    game_quests = Quests.objects.filter(game=gameidvar)
    values = []
    for item in Quests.objects.filter(game=gameidvar).filter(type="side").values():
        if item["quest_line"] not in values:
            values.append(item["quest_line"])
    return render(response, 'CatQuestipedia/quests.html', {"game": str(gameid), "Game": game, "Gameid": gameidvar, "game_quests": game_quests, "Side_Quest_lines": values, "modified": datestamp, })


def quest_detail(request, gameid, questid):
    game = Game.objects.values()
    gameidvar = Game.objects.get(title=gameid)
    quest = Quests.objects.filter(game=gameidvar).get(name=questid)
    task = quest.tasks
    tasks = str(task).split(", ")
    user = request.user
    if user.is_authenticated:
        user_playthroughs = Playthroughs.objects.filter(user=user).filter(game=gameidvar)
        playthrough_levels = {}
        for it in user_playthroughs:
            if it.user_quests.filter(playthrough=it, quest=quest).exists():
                playthrough_levels[it.name] = 1
            else:
                playthrough_levels[it.name] = 0
        print(playthrough_levels)
        if request.method == "POST":
            playthrough = Playthroughs.objects.get(user=user, game = gameidvar, name = request.POST.get(quest.name + "1"))
            entry = UserQuests.objects.filter(user=user).filter(playthrough=playthrough).filter(quest=quest)
            if (quest.name + "2") in request.POST and entry.exists() == True:
                delete = UserQuests.objects.get(quest=quest, playthrough=playthrough, user=user)
                playthrough.user_quests.remove(delete)
                delete.delete()
            elif str(quest.name + "2") in request.POST and entry.exists() == False:
                new = UserQuests.objects.create(user=user, playthrough=playthrough, quest=quest)
                new.save()
                playthrough.user_quests.add(new)
                playthrough.save()
    else:
        user_playthroughs = None
        playthrough_levels = {}
    return render(request, 'CatQuestipedia/quest-detail.html', {"game": str(gameid), "Game": game, "quest": quest, "tasks": tasks, "user_playthroughs": user_playthroughs, "playthrough_levels": playthrough_levels, "modified": datestamp, })

def locations(response, gameid):
    gameidvar = Game.objects.get(title=gameid)
    return render(response, 'CatQuestipedia/locations.html', {"game": str(gameid), "Game": games, "Gameid": gameidvar, "modified": datestamp, })

def location_detail(response, gameid, locationid):
    gameidvar = Game.objects.get(title=gameid)
    location = Locations.objects.filter(game=gameidvar).get(name=locationid)
    quests = Quests.objects.filter(game=gameidvar, location=location)
    return render(response, 'CatQuestipedia/location-detail.html', {"game": str(gameid), "Game": games, "Gameid": gameidvar, "location": location, "quests": quests, "modified": datestamp, })


def mewgame(response, gameid):
    gameidvar = Game.objects.get(title=gameid)
    return render(response, 'CatQuestipedia/mew-game.html', {"game": str(gameid), "Game": games, "Gameid": gameidvar, "modified": datestamp})

def mewgame_detail(response, gameid, mewgameid):
    gameidvar = Game.objects.get(title=gameid)
    mode = MewGame.objects.filter(game=gameidvar).get(name=mewgameid)
    return render(response, 'CatQuestipedia/mewgame-detail.html', {"game": str(gameid), "Game": games, "Gameid": gameidvar, "mode": mode, "modified": datestamp})

def edit_game(request, gameid):
    gameidvar = Game.objects.get(title=gameid)
    if request.method == "POST":
        new_content = request.POST.get("user-content")
        gameidvar.user_edits = new_content
        gameidvar.save()
        messages.add_message(request, messages.INFO, mark_safe(gameid + " has been updated. See <a href='/admin/CatQuestipedia/game/%s/change'>here</a>."%(gameidvar.id))) #type:ignore
    return render(request, "CatQuestipedia/edit.html", {"game": str(gameid), "Game": games, "modified": datestamp, "article": gameidvar, })

def edit_item(request, gameid, modelid, itemid):
    gameidvar = Game.objects.get(title=gameid)
    article = apps.get_model("CatQuestipedia", modelid.capitalize()).objects.get(name=itemid, game=gameidvar)
    if request.method == "POST":
        new_content = request.POST.get("user-content")
        article.user_edits = new_content # type: ignore
        article.save()
        messages.add_message(request, messages.INFO, mark_safe(itemid + " has been updated. See <a href='/admin/CatQuestipedia/%s/%s/change'>here</a>."%(modelid.lower(), article.id))) #type:ignore
    return render(request, "CatQuestipedia/edit.html", {"game": str(gameid), "Game": games, "modified": datestamp, "article": article, })

def mass_update(request, id):
    playthrough = Playthroughs.objects.get(id=id)
    game = playthrough.game
    equipment = Equipment.objects.filter(game=game)
    spells = Spells.objects.filter(game=game)
    quests = Quests.objects.filter(game=game)
    user = request.user
    completed_quests = []
    owned_equipment = {}
    known_spells = {}
    for item in playthrough.user_equipment.all().values("equipment", "equipment_level"):
        owned_equipment[item["equipment"]] = item["equipment_level"]
    for item in playthrough.user_spells.all().values("spell", "spell_level"):
        known_spells[item["spell"]] = item["spell_level"]
    for item in playthrough.user_quests.all():
        completed_quests.append(item.quest)
    if user.is_authenticated:
        if request.method == "POST":
            for item in equipment:
                entry = UserEquipment.objects.filter(user=user).filter(playthrough=playthrough).filter(equipment=item)
                if "equipment-" + item.name + "1" in request.POST and entry.exists() == True:
                    edit = UserEquipment.objects.filter(user=user).filter(playthrough=playthrough).get(equipment=item)
                    edit.equipment_level = int(request.POST.get("equipment-" + item.name + "2"))
                    edit.save()
                elif "equipment-" + item.name + "1" in request.POST and entry.exists() == False:
                    new = UserEquipment.objects.create(user=user, playthrough=playthrough, equipment=item, equipment_level=int(request.POST.get("equipment-" + item.name + "2")))
                    new.save()
                    playthrough.user_equipment.add(new)
                    playthrough.save()
            for item in spells:
                entry = UserSpells.objects.filter(user=user).filter(playthrough=playthrough).filter(spell=item)
                if "spells-" + item.name + "1" in request.POST and entry.exists() == True:
                    edit = UserSpells.objects.filter(user=user).filter(playthrough=playthrough).get(spell=item)
                    edit.spell_level = int(request.POST.get("spells-" + item.name + "2"))
                    edit.save()
                elif "spells-" + item.name + "1" in request.POST and entry.exists() == False:
                    new = UserSpells.objects.create(user=user, playthrough=playthrough, spell=item, spell_level=int(request.POST.get("spells-" + item.name + "2")))
                    new.save()
                    playthrough.user_spells.add(new)
                    playthrough.save()
            for item in quests:
                entry = UserQuests.objects.filter(user=user).filter(playthrough=playthrough).filter(quest=item)
                if item.name in request.POST and entry.exists() == True:
                    delete = UserQuests.objects.filter(user=user).filter(playthrough=playthrough).get(quest=item)
                    playthrough.user_quests.remove(delete)
                    delete.delete()
                elif item.name in request.POST and entry.exists() == False:
                    new = UserQuests.objects.create(user=user, playthrough=playthrough, quest=item)
                    new.save()
                    playthrough.user_quests.add(new)
                    playthrough.save()
    return render(request, 'CatQuestipedia/mass-update.html', {"Game": games, "modified": datestamp, "equipment": equipment, "spells": spells, "quests": quests, "owned_equipment": owned_equipment, "known_spells": known_spells, "completed_quests": completed_quests, "playthrough": playthrough, })

def new_playthrough(request):
    if request.method == "POST":
        user = request.user
        new_name = request.POST.get("playthrough-name")
        new_game = Game.objects.get(title=request.POST.get("playthrough-game"))
        print(new_game)
        new = Playthroughs.objects.create(name=new_name, user=user)
        new.save()
        new.game = new_game
        new.save()
    return render(request, "Catquestipedia/new-playthrough.html", {"Game": games, "modified": datestamp, })
