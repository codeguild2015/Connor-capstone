from django.db import models

class Bar(models.Model):
	id = models.TextField(primary_key=True)
	google_id = models.TextField(default='')
	name = models.TextField(default='')
	latitude = models.IntegerField(null=True)
	longitude = models.IntegerField(null=True)
	vicinity = models.TextField(default='')
	price_level = models.IntegerField(null=True)
	rating = models.IntegerField(null=True)
	# creation_date = models.DateTimeField(null=True) # Dunno if that's what it's called
	# updated_date = models.DateTimeField(null=True)
	open_at_update = models.TextField(default='')


# current_bar = Bar(default='')
# current_bar.address = "123 Shithouse lane"
# current_bar.save(default='')