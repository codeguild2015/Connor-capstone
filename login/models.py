from django.db import models

class Item(models.Model):
	text = models.TextField(default='')

# class Bar(model.Model):
# 	name = models.TextField(required=true)
# 	address = models.TextField(required=true)
# 	creation_date = models.Date() # Dunno if that's what it's called

# current_bar = Bar()
# current_bar.address = "123 Shithouse lane"
# current_bar.save()