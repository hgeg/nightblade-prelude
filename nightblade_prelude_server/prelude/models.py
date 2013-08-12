from django.db import models
from helpers import create_uid,roll

class Author(models.Model):
    access_token = models.CharField(max_length=18,null=True)
    last_access  = models.DateTimeField(auto_now=True)
    username     = models.CharField(max_length=50,primary_key=True)
    password     = models.CharField(max_length=32)
    character    = models.ForeignKey('Character',null=True)

class Item(models.Model):
    uid    = models.CharField(max_length=12,default=create_uid(),primary_key=True)
    health = models.IntegerField(default=990)
    power  = models.IntegerField(default=10)
    otype  = models.IntegerField(default=-1)
    mtype  = models.IntegerField(default=-1)
    name   = models.CharField(max_length=50)
    value  = models.IntegerField(default=0)

    def data(self):
        return {'name':self.name,'hp':self.health,'pow':self.power,'otype':self.otype,
                'mtype':self.mtype,'val':self.value,'uid':self.uid}

class Spell(models.Model):
    stype  = models.IntegerField(default=-1)
    name   = models.CharField(max_length=50)
    power  = models.IntegerField(default=0)

class Creature(models.Model):
    uid    = models.CharField(max_length=12,default=create_uid(),primary_key=True)
    name   = models.CharField(max_length=25)
    health = models.IntegerField(default=10)
    power  = models.IntegerField(default=2)

    def data(self):
        return {'name':self.name,'hp':self.hp,'power':self.power,'uid':self.uid}

class Character(models.Model):
    uid  = models.CharField(max_length=12,default=create_uid(),primary_key=True)
    name = models.CharField(max_length=25)
    '''race = models.CharField(max_length=10)

    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)'''

    st = models.IntegerField(default=1)
    dx = models.IntegerField(default=1)
    iq = models.IntegerField(default=1)
    ht = models.IntegerField(default=1)
    xp = models.IntegerField(default=100)
    hp = models.IntegerField(default=10)

    gold = models.IntegerField(default=50)

    state = models.IntegerField(default=0)
    timer = models.DateTimeField(null=True)

    left  = models.ForeignKey(Item, related_name='+',null=True)
    right = models.ForeignKey(Item, related_name='+',null=True)
    armor = models.ForeignKey(Item, related_name='+',null=True)
    inventory = models.ManyToManyField(Item)

    place = models.ForeignKey('Place')

    def data(self):
        tdata = self.timer.strftime('%d/%m/%Y %H:%M') if self.timer else 'None'
        lhand = self.left.uid if self.left else 'None'
        rhand = self.right.uid if self.right else 'None'
        armor = self.armor.uid if self.armor else 'None'
        return {'name':self.name,'hp':self.hp,'stats':(self.st,self.dx,self.iq,self.ht),'gold':self.gold,
                'state':self.state,'timer':tdata,'lhand':lhand,
                'rhand':rhand,'armor':armor,'place':self.place.uid,'uid':self.uid}

class Place(models.Model):
    uid    = models.CharField(max_length=12,default=create_uid(),primary_key=True)
    name   = models.CharField(max_length=50)
    people = models.ManyToManyField(Character,related_name='people')
    arena  = models.BooleanField(default=False)
    gates  = models.ManyToManyField('Place',related_name='gates',symmetrical=True)
    biome  = models.CharField(default='000000',max_length=6)

    def data(self):
        return {'name':self.name,'people':[p.uid for p in people],'isarena':self.arena,'biome':self.biome,'uid':self.uid}