from django import template
from ..models import *
register = template.Library()


@register.filter
def kebabify(string):
    new_string1 = string.lower()
    new_string2 = new_string1.replace(" ", "-")
    new_string = new_string2.translate({ord(i): None for i in ":"})
    return new_string


@register.filter
def order_db(db, field):
    return db.order_by(field)


@register.simple_tag
def new_features(game):
    features = Game.objects.get(title=game)
    new = str(features.new_features).split(", ")
    return new


@register.simple_tag
def filter_equipment_by_set(game_name, equipment_set):
    return Equipment.objects.filter(game=game_name).filter(set=equipment_set)


@register.simple_tag
def filter_quests_by_line(game_name, quest_line):
    return Quests.objects.filter(game=game_name).filter(quest_line=quest_line)

@register.filter
def get_dict_value(dictionary, key):
    return dictionary.get(key)

@register.filter
def get_dict_count(dictionary, key):
    return len(dictionary[key])

@register.filter
def total_length(dictionary):
    return dictionary.len()
