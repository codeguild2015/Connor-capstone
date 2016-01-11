from django.db import models

class Bar(models.Model):
	id = models.AutoField(primary_key=True)
	google_id = models.TextField(default='')
	name = models.TextField(default='')
	stripped_name = models.TextField(default='')
	latitude = models.TextField(default='')
	longitude = models.TextField(default='')
	vicinity = models.TextField(default='')
	price_level = models.TextField(default='')
	rating = models.TextField(default='')
	creation_date = models.DateTimeField(null=True) # Dunno if that's what it's called
	updated_date = models.DateTimeField(null=True)
	open_at_update = models.TextField(default='')

class Twitter(models.Model):
	id = models.AutoField(primary_key=True)