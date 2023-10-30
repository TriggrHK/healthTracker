from django.db import models
class Suggested_Levels(models.Model):
    # suggested_levels_id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    current_stage = models.IntegerField()
    gender = models.CharField(max_length=1)

    min_sodium_intake = models.IntegerField() # milligrams
    max_sodium_intake = models.IntegerField()
    
    min_protein_intake = models.IntegerField() # milligrams per Kilogram
    
    water_intake = models.DecimalField(max_digits=5, decimal_places=2) # Liters

    min_k_intake = models.IntegerField() # milligrams
    max_k_intake = models.IntegerField()

    min_phos_intake = models.IntegerField() # milligrams
    max_phos_intake = models.IntegerField()
    
    min_internal_k = models.DecimalField(max_digits=5, decimal_places=2) # miligrams / deciliter
    max_internal_k = models.DecimalField(max_digits=5, decimal_places=2)

    min_internal_phos = models.DecimalField(max_digits=5, decimal_places=2) # miligrams / deciliter
    max_internal_phos = models.DecimalField(max_digits=5, decimal_places=2) 
    
    min_internal_na = models.IntegerField() # mEq/L milliequivalent per Liter
    max_internal_na = models.IntegerField() # mEq/L milliequivalent per Liter
    
    min_internal_creatinine = models.DecimalField(max_digits=4,decimal_places=2) # miligrams per deciliter
    
    internal_albumin = models.IntegerField() # miligrams per deciliter
    
    min_internal_sugar = models.IntegerField() # miligrams per deciliter
    max_internal_sugar = models.IntegerField() # miligrams per deciliter

    def __str__(self):
        return (f" Stage {self.current_stage} for {self.gender}")
    class Meta:
        db_table = 'suggested_levels'
        constraints = [
            models.UniqueConstraint(fields=['gender', 'current_stage'], name="suggested_levels_CPK")
        ]

class Person (models.Model):
    f_name = models.CharField(max_length=30)
    m_name = models.CharField(max_length=30)
    l_name = models.CharField(max_length=30)
    gender = models.ForeignKey(Suggested_Levels, on_delete=models.CASCADE)
    date_of_birth = models.DateField(auto_now=False, auto_now_add=False)
    street_address = models.CharField(max_length=50)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=2)
    zip = models.CharField(max_length=10)
    county = models.CharField(max_length=20)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    username = models.CharField(max_length=15)
    password = models.CharField(max_length=100)
    
    def __str__(self):
        return (f'Person: {self.f_name}')
    class Meta:
        db_table = 'person'
        
class User (Person):
    user_id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='User ID')
    # gender = models.ForeignKey(Suggested_Levels, on_delete=models.CASCADE)
    current_stage = models.ForeignKey(Suggested_Levels, on_delete=models.CASCADE)
    current_height = models.IntegerField() #centimeters
    current_weight = models.DecimalField(max_digits=5, decimal_places=2) #kg
    race = models.CharField(max_length=10)

    def __str__(self):
        return (self.f_name + " " + self.l_name)
    class Meta:
        db_table = 'user'
        

class Level_Conversion(models.Model):
    nutrient = models.CharField(max_length=30)
    isIntake = models.BooleanField() #intake or serum/internal
    measurement_unit = models.CharField(max_length=10)

    def __str__(self):
        return (f'{self.nutrient} tested from {"Intake" if self.isIntake else "Serum"} and measured in {self.measurement_unit}')
    class Meta:
        db_table = 'level_conversion'

class Units(models.Model):
    attribute = models.CharField(max_length=30)
    measurement_unit = models.CharField(max_length=3)

    def __str__(self):
        return (f'{self.attribute} is measured in {self.measurement_unit}')
    class Meta:
        db_table = 'units'

class Food (models.Model):
    food_id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='Food ID')
    food_name = models.CharField(max_length=200)
    sodium = models.DecimalField(max_digits = 8, decimal_places = 2) # milligrams
    protein = models.DecimalField(max_digits=8, decimal_places=2) # milligrams
    water = models.DecimalField(max_digits=8, decimal_places=2) # milligrams
    k = models.DecimalField(max_digits=8, decimal_places=2) # milligrams
    phos = models.DecimalField(max_digits=8, decimal_places=2) # milligrams
    # serving_size = models.DecimalField(5,2)
    
    def __str__(self):
        return (self.food_name)
    class Meta:
        db_table = 'food'

class Journal_Entries (models.Model):
    journal_entries_id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='Journal Entry ID')
    datetime = models.DateTimeField(auto_now=False, auto_now_add=True)
    meal_name = models.CharField(max_length=25)
    note = models.CharField(max_length=255, null=True, blank=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return (f'{self.meal_name} at {self.datetime}')
    class Meta:
        db_table = 'journal_entries'

class Has (models.Model):
    quantity = models.DecimalField(max_digits=5, decimal_places=2)
    journal_entries_id = models.ForeignKey(Journal_Entries, on_delete=models.CASCADE)
    food_id = models.ForeignKey(Food, on_delete=models.CASCADE)

    def __str__(self):
        return (f'{self.food_id} {self.quantity}')
    class Meta:
        db_table = 'has'
class Allergies(models.Model):
    severity = models.CharField(max_length=15)
    allergy_name = models.CharField(max_length=30)
    allergies_id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='Allergy ID')

    def __str__(self):
        return (self.allergy_name)
    class Meta:
        db_table = 'allergies'
        
class Allergies_User(models.Model):
    allergies_id = models.ForeignKey(Allergies, on_delete=models.CASCADE)
    # allergy_name = models.CharField(max_length = 30)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return (f'{self.allergies_id} {self.user_id}')
    class Meta:
        db_table = 'allergies_user'

class Lab_Results(models.Model):
    date_time = models.DateTimeField(auto_now=False, auto_now_add=False)
    test_type = models.CharField(max_length = 30)
    company = models.CharField(max_length = 50)
    test_id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='Lab Results ID')

    def __str__(self):
        return (self.date_time)

    class Meta:
        db_table = 'lab_results'
        
class Test_Results(models.Model):
    substance = models.CharField(max_length = 30)
    level = models.DecimalField(max_digits=6, decimal_places=2)
    test_id = models.ForeignKey(Lab_Results, on_delete=models.CASCADE)

    def __str__(self):
        return(self.substance)
    class Meta:
        db_table = 'test_results'
    
class Comorbidities(models.Model):
    comorbidities_id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='Comorbidities ID')
    risk_name = models.CharField(max_length=30)
    description = models.CharField(max_length=100)
    
    def __str__(self):
        return (self.risk_name)
    class Meta:
        db_table = 'comorbidities'

class Comorbidities_User(models.Model):
    comorbidities_id = models.ForeignKey(Comorbidities, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return (f'{self.comorbidities_id} {self.user_id}')
    class Meta:
        db_table = 'comorbidities_user'
