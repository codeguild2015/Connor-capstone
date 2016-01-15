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
	creation_date = models.DateTimeField(null=True)
	updated_date = models.DateTimeField(null=True)
	open_at_update = models.TextField(default='')

class Twitter(models.Model):
	google_id = models.TextField(primary_key=True)
	screen_name = models.TextField(default='')
	created_at = models.DateTimeField(null=True)
	location = models.TextField(default='')
	profile_image = models.TextField(default='')
	profile_banner = models.TextField(default='')
	profile_link_color = models.TextField(default='')
	website = models.TextField(default='')