from django.db import models

# class Item(models.Model):
# 	text = models.TextField(default='')

class Bar(models.Model):
	gId = models.TextField(primary_key=True, max_length=500)
	name = models.TextField(required=True, max_length=500)
	latitude = models.IntegerField(required=True, max_length=500)
	longitude = models.IntegerField(required=True, max_length=500)
	vicinity = models.TextField(required=True, max_length=500)
	price_level = models.IntegerField(required=True, max_length=500)
	rating = models.IntegerField(required=True, max_length=500)
	creation_date = models.Date(, max_length=500) # Dunno if that's what it's called
	updated_date = models.Date(, max_length=500)
	open_at_update = models.TextField(, max_length=500)


# current_bar = Bar()
# current_bar.address = "123 Shithouse lane"
# current_bar.save()