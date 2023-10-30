from django.contrib import admin
from .models import Suggested_Levels, User, Level_Conversion, Units, Food, Journal_Entries, Has, Allergies, Allergies_User, Lab_Results, Test_Results, Comorbidities, Comorbidities_User

# Register your models here.
admin.site.register(Suggested_Levels)
admin.site.register(User)
admin.site.register(Level_Conversion)
admin.site.register(Units)
admin.site.register(Food)
admin.site.register(Journal_Entries)
admin.site.register(Has)
admin.site.register(Allergies)
admin.site.register(Allergies_User)
admin.site.register(Comorbidities)
admin.site.register(Comorbidities_User)
admin.site.register(Test_Results)
admin.site.register(Lab_Results)
