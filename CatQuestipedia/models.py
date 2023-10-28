from django.db import models
from django.contrib.auth.models import AbstractUser # , User
from django.conf import settings
from django.db.models.signals import post_save
from django.db.models import Q, F, OuterRef, Subquery, Value, CharField
from django.contrib.postgres.aggregates import ArrayAgg

# Create your models here.

class Users(AbstractUser):
    pass

class Tags(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Game(models.Model):
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to="games")
    synopsis = models.CharField(max_length=1000, null=True)
    new_features = models.CharField(max_length=500, null=True, blank=True)
    date_released = models.DateField(null=True)
    tags = models.ManyToManyField(Tags, blank=True)

    def __str__(self):
        return self.title
    
    def all_tags(self):
        tag_list = []
        for tag in self.tags.all():
            tag_list.append(tag.name)
        return tag_list
    
    @staticmethod
    def search_rank(query):
        rank = {}
        query_items = Game.objects.filter(Q(title__icontains=query) | Q(tags__name__iexact=query) | Q(synopsis__icontains=query)).annotate(game_title=F('title'), game_synopsis=F('synopsis'), game_tags=ArrayAgg("tags__name")).values("game_title", "game_synopsis", "game_tags")
        for item in query_items:
            item_rank = 0.0
            if query in item["game_title"]:
                item_rank += 1
            if query in item["game_tags"]:
                item_rank += 0.75
            if query in item["game_synopsis"]:
                item_rank += 0.25
            rank[item["game_title"]] = item_rank
        rank = sorted(rank.items(), key = lambda x: x[1])
        return rank

class Characters(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to="characters", null=True, blank=True)
    description = models.CharField(max_length=100, null=True)
    type = models.CharField(max_length=10, null=True)
    game = models.ForeignKey(Game, related_name="characters", on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tags, blank=True)

    def __str__(self):
        return self.name
    
    def all_tags(self):
        tag_list = []
        for tag in self.tags.all():
            tag_list.append(tag.name)
        return tag_list
    
    @staticmethod
    def search_rank(query):
        rank = {}
        query_items = Characters.objects.filter(Q(name__icontains=query) | Q(tags__name__iexact=query) | Q(description__icontains=query)).annotate(character_name=F('name'), character_id=F("id"), character_description=F('description'), character_tags=ArrayAgg("tags__name")).values("character_name", "character_id", "character_description", "character_tags")
        for item in query_items:
            item_rank = 0.0
            if query in item["character_name"]:
                item_rank += 1
            if query in item["character_tags"]:
                item_rank += 0.75
            if query in item["character_description"]:
                item_rank += 0.25
            rank[item["character_id"]] = item_rank
        rank = sorted(rank.items(), key = lambda x: x[1])
        return rank

class Enemies(models.Model):
    name = models.CharField(max_length=50)
    enemy = models.ImageField(upload_to="enemies", null=True, blank=True)
    attacks = models.CharField(max_length=100)
    weak_to = models.CharField(max_length=100, null=True, blank=True)
    game = models.ForeignKey(Game, related_name="enemies", on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tags, blank=True)

    def __str__(self):
        return self.name
    
    def all_tags(self):
        tag_list = []
        for tag in self.tags.all():
            tag_list.append(tag.name)
        return tag_list
    
    @staticmethod
    def search_rank(query):
        rank = {}
        query_items = Enemies.objects.filter(Q(name__icontains=query) | Q(tags__name__iexact=query) | Q(locations_found__name__icontains=query)).annotate(enemy_name=F('name'), enemy_id=F("id"), enemy_location=ArrayAgg('locations_found__name'), enemy_tags=ArrayAgg("tags__name")).values("enemy_name", "enemy_id", "enemy_location", "enemy_tags")
        for item in query_items:
            item_rank = 0.0
            if query in item["enemy_name"]:
                item_rank += 1
            if query in item["enemy_location"]:
                item_rank += 0.75
            if query in item["enemy_tags"]:
                item_rank += 0.125
            rank[item["enemy_id"]] = item_rank
        rank = sorted(rank.items(), key = lambda x: x[1])
        return rank

class Equipment(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to="equipment", null=True, blank=True)
    set = models.CharField(max_length=50, null=True)
    set_type = models.CharField(max_length=10, null=True)
    game = models.ForeignKey(Game, related_name="equipment", on_delete=models.CASCADE)
    type = models.CharField(max_length=50)
    defense = models.CharField(max_length=10)
    health = models.CharField(max_length=10)
    physicalattack = models.CharField(max_length=10)
    magic = models.CharField(max_length=10)
    otherbuffs = models.CharField(max_length=200, null=True, blank=True)
    otherdebuffs = models.CharField(max_length=200, null=True, blank=True)
    maxlvl = models.IntegerField()
    users = models.ManyToManyField(Users, through="UserEquipment")
    tags = models.ManyToManyField(Tags, blank=True)

    def __str__(self):
        return self.name
    
    def all_tags(self):
        tag_list = []
        for tag in self.tags.all():
            tag_list.append(tag.name)
        return tag_list
    
    @staticmethod
    def search_rank(query):
        rank = {}
        query_items = Equipment.objects.filter(Q(name__icontains=query) | Q(tags__name__iexact=query) | Q(set__icontains=query)).annotate(equipment=F('name'), equip_id=F("id"), equipment_set=F('set'), equipment_tags=ArrayAgg("tags__name")).values("equipment", "equip_id", "equipment_set", "equipment_tags")
        for item in query_items:
            item_rank = 0.0
            if query in item["equipment"]:
                item_rank += 1
            if query in item["equipment_set"]:
                item_rank += 0.75
            if query in item["equipment_tags"]:
                item_rank += 0.25
            rank[item["equip_id"]] = item_rank
        rank = sorted(rank.items(), key = lambda x: x[1])
        return rank

class Spells(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to="spells", null=True, blank=True)
    game = models.ForeignKey(Game, related_name="spells", on_delete=models.CASCADE)
    effect = models.CharField(max_length=100)
    maxlvl = models.IntegerField()
    users = models.ManyToManyField(Users, through="UserSpells")
    tags = models.ManyToManyField(Tags, blank=True)

    def all_tags(self):
        tag_list = []
        for tag in self.tags.all():
            tag_list.append(tag.name)
        return tag_list

    def __str__(self):
        return self.name
    
    @staticmethod
    def search_rank(query):
        rank = {}
        query_items = Spells.objects.filter(Q(name__icontains=query) | Q(tags__name__iexact=query) | Q(effect__icontains=query)).annotate(spell=F('name'), spell_id=F('id'), spell_effect=F('effect'), spell_tags=ArrayAgg("tags__name")).values("spell", "spell_id", "spell_effect", "spell_tags")
        for item in query_items:
            item_rank = 0.0
            if query in item["spell"]:
                item_rank += 1
            if query in item["spell_tags"]:
                item_rank += 0.75
            if query in item["spell_effect"]:
                item_rank += 0.25
            rank[item["spell_id"]] = item_rank
        rank = sorted(rank.items(), key = lambda x: x[1])
        return rank

class Quests(models.Model):
    type_choices = (
        ("main", "Main Quest"),
        ("side", "Side Quest")
    )
    name = models.CharField(max_length=100)
    tasks = models.CharField(max_length=500, null=True, blank=True)
    game = models.ForeignKey(Game, related_name="game_name", on_delete=models.CASCADE)
    monster_list = models.ManyToManyField(Enemies, blank=True, related_name="regulargamequests")
    mew_game_monster = models.ManyToManyField(Enemies, blank=True, related_name="mewgamequests")
    character_list = models.ManyToManyField(Characters, blank=True)
    location = models.ForeignKey("Locations", related_name="location_name", on_delete=models.CASCADE, null=True, blank=True)
    type = models.CharField(max_length=4, choices=type_choices, null=True)
    lvl = models.IntegerField()
    quest_number = models.IntegerField()
    quest_line = models.CharField(max_length=100)
    xpreward = models.IntegerField(null=True, blank=True)
    goldreward = models.IntegerField(null=True, blank=True)
    miscreward = models.CharField(max_length=200, null=True, blank=True)
    user_quests = models.ManyToManyField(Users, through="UserQuests")
    tags = models.ManyToManyField(Tags, blank=True)

    def __str__(self):
        return self.name
    
    def all_tags(self):
        tag_list = []
        for tag in self.tags.all():
            tag_list.append(tag.name)
        return tag_list
    
    @staticmethod
    def search_rank(query):
        rank = {}
        query_items = Quests.objects.filter(Q(name__icontains=query) | Q(tags__name__iexact=query) | Q(quest_line__icontains=query) | Q(location__name__icontains=query) | Q(monster_list__name__icontains=query) | Q(character_list__name__icontains=query)).annotate(quest=F('name'), line=F('quest_line'), quest_tags=ArrayAgg("tags__name"), quest_loc=Subquery(Locations.objects.filter(id=OuterRef('location')).values('name')[:1]), monsters=ArrayAgg("monster_list__name"), characters=ArrayAgg("character_list__name")).values("quest", "line", "quest_tags", "quest_loc", "monsters", "characters")
        for item in query_items:
            item_rank = 0.0
            if query in item["quest"]:
                item_rank += 1
            if query in item["quest_tags"]:
                item_rank += 0.75
            if query in item["line"]:
                item_rank += 0.25
            if query in item["quest_loc"]:
                item_rank += 0.125
            if query in item["monsters"]:
                item_rank += 0.125
            if query in item["characters"]:
                item_rank += 0.125
            rank[item["quest"]] = item_rank
        rank = sorted(rank.items(), key = lambda x: x[1])
        return rank

class Locations(models.Model):
    type_choices= (
        ("cave", "Cave"),
        ("ruins", "Ruins"),
        ("town", "Town"),
        ("overworld", "Overworld"),
    )
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=9, choices=type_choices)
    enemies_there = models.ManyToManyField(Enemies, blank=True, related_name="regulargamelocations")
    mew_game_enemy = models.ManyToManyField(Enemies, blank=True, related_name="mewgamelocations")
    normal_chests = models.IntegerField()
    key_chests = models.IntegerField()
    completion_chests = models.IntegerField()
    game = models.ForeignKey(Game, related_name="location", on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tags, blank=True)

    def __str__(self):
        return self.name
    
    def all_tags(self):
        tag_list = []
        for tag in self.tags.all():
            tag_list.append(tag.name)
        return tag_list
    
    @staticmethod
    def search_rank(query):
        rank = {}
        query_items = Locations.objects.filter(Q(name__icontains=query) | Q(tags__name__iexact=query) | Q(type__icontains=query) | Q(enemies_there__name__icontains=query)).annotate(location=F('name'), location_type=F('type'), location_id=F("id"), location_tags=ArrayAgg("tags__name"), enemy_list=ArrayAgg("enemies_there__name")).values("location", "location_type", "location_id", "location_tags", "enemy_list")
        for item in query_items:
            item_rank = 0.0
            if query in item["location"]:
                item_rank += 1
            if query in item["location_tags"]:
                item_rank += 0.75
            if query in item["location_type"]:
                item_rank += 0.25
            if query in item["enemy_list"]:
                item_rank += 0.125
            rank[item["location_id"]] = item_rank
        rank = sorted(rank.items(), key = lambda x: x[1])
        return rank

class MewGame(models.Model):
    game = models.ForeignKey(Game, related_name="mewgame", on_delete=models.CASCADE)
    mode_name = models.CharField(max_length=50, null=True, blank=True)
    mode_description = models.CharField(max_length=200, null=True, blank=True)
    rewards = models.BooleanField(null=True, blank=True)
    tags = models.ManyToManyField(Tags, blank=True)

    def __str__(self):
        return self.mode_name
    
    def all_tags(self):
        tag_list = []
        for tag in self.tags.all():
            tag_list.append(tag.name)
        return tag_list
    
    @staticmethod
    def search_rank(query):
        rank = {}
        query_items = MewGame.objects.filter(Q(mode_name__icontains=query) | Q(tags__name__iexact=query) | Q(mode_description=query)).annotate(name=F('mode_name'), description=F('mode_description'), mewgame_tags=ArrayAgg("tags__name")).values("name", "description", "mewgame_tags")
        for item in query_items:
            item_rank = 0.0
            if query in item["name"]:
                item_rank += 1
            if query in item["mewgame_tags"]:
                item_rank += 0.75
            if query in item["description"]:
                item_rank += 0.25
            rank[item["name"]] = item_rank
        rank = sorted(rank.items(), key = lambda x: x[1])
        return rank

class UserEquipment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, to_field="username", on_delete=models.CASCADE)
    playthrough = models.ForeignKey("Playthroughs", related_name="equipment_playthrough", null=True, on_delete=models.CASCADE)
    equipment = models.ForeignKey(Equipment, related_name="equipment_name", on_delete=models.CASCADE)
    equipment_level = models.IntegerField()
    
    def __str__(self):
        return self.user.username

class UserSpells(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, to_field="username", on_delete=models.CASCADE)
    playthrough = models.ForeignKey("Playthroughs", related_name="spell_playthrough", null=True, on_delete=models.CASCADE)
    spell = models.ForeignKey(Spells, related_name="spell_name", on_delete=models.CASCADE)
    spell_level = models.IntegerField()

    def __str__(self):
        return self.user.username

class UserQuests(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, to_field="username", on_delete=models.CASCADE)
    playthrough = models.ForeignKey("Playthroughs", related_name="quest_playthrough", null=True, on_delete=models.CASCADE)
    quest = models.ForeignKey(Quests, related_name="quest_name", on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.username

class Playthroughs(models.Model):
    name = models.CharField(max_length=200)
    game = models.ForeignKey(Game, related_name="playthroughs", null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="playthrough_user", null=True, on_delete=models.CASCADE)
    user_equipment = models.ManyToManyField(UserEquipment, blank=True)
    user_spells = models.ManyToManyField(UserSpells, blank=True)
    user_quests = models.ManyToManyField(UserQuests, blank=True)

    class Meta:
        unique_together = ("name", "game", "user")

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, to_field="username", on_delete=models.CASCADE)
    playthroughs = models.ManyToManyField("Playthroughs", blank=True)
    
    def __str__(self):
        return self.user.username

class OtherImages(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="other")

    def __str__(self):
        return self.name

def CreateProfile(sender, instance, created, **kwargs):
    if created:
        new_profile = UserProfile.objects.create(user=instance)
        new_profile.save()
        for item in Game.objects.all():
            new_playthrough = Playthroughs.objects.create(name="Main Playthrough", user=instance)
            new_playthrough.save()
            new_playthrough.game = item
            new_playthrough.save()

post_save.connect(CreateProfile, sender=Users)
