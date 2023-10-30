from django.shortcuts import render
from django.http import HttpResponse
from .models import Suggested_Levels, User, Level_Conversion, Units, Food, Journal_Entries, Has, Allergies, Allergies_User, Lab_Results, Test_Results, Comorbidities, Comorbidities_User

# this is just the basic index page that checks if the isAuth key has been stored yet and passes session variable
# session variable allows for dynamic changes based on if someone has logged in
def indexPageView(request):
    if not request.session.has_key('isAuth'):
        request.session['isAuth'] = False

    session = request.session
    context = {
        'session': session
    }
    return render(request, 'index.html', context)

# stats page shows stats based on journal_entries input
def statsPageView(request):
    if not request.session.has_key('isAuth'):
        request.session['isAuth'] = False
        session = request.session
        context = {
            'session': session,
            'errors': ["Don't do that"],
        }
        return render(request, 'login.html', context)

    session = request.session

    user = User.objects.filter(username = request.session['username'])
    users = User.objects.all()

    jE = Journal_Entries.objects.filter(user_id = user[0].user_id)

    # make sure some journal_entries have been added or redirect
    if len(jE) == 0:
        context = {
            'session': request.session,            
            'errors': ["User doesn't have any data"],
        }
        return render(request, 'index.html', context)

    # calculate all the different days and their aggregated values of eachnutrient
    dayDict = {}
    for el in jE:
        day = el.datetime.strftime("%Y/%m/%d")
        if not day in dayDict:
            dayDict[day] = {'Phosphorus':0, 'Sodium':0, 'Water':0, 'Potassium':0, 'Protein':0}
        dictKey = day

        has = Has.objects.filter(journal_entries_id = el.journal_entries_id)
        for entry in has:
            quantity = entry.quantity
            foodForJournal = Food.objects.filter(food_name = entry.food_id)[0]

            dayDict[dictKey]['Phosphorus'] += foodForJournal.phos
            dayDict[dictKey]['Sodium'] += foodForJournal.sodium
            dayDict[dictKey]['Water'] += foodForJournal.water
            dayDict[dictKey]['Potassium'] += foodForJournal.k
            dayDict[dictKey]['Protein'] += foodForJournal.protein

    test = dayDict.keys()
    keys = list(test)

    # get the 5 of the elements from dayDict or if there's less however many were stored
    topArr = []
    for i in range(0, 5 if len(keys) >= 5 else len(keys)):
        topArr.append(dayDict[keys[i]])
 
    context = {
        'session': session,
        'user': user[0],
        'users' : users,
        'keys': keys,
        'listDay': topArr,

        'recentKey': keys[-1],
        'recentDay': dayDict.get(keys[-1]),
        'recentVals': dayDict.get(keys[-1]).values()
    }
    return render(request, 'stats.html', context)

# this just displays the journal data, needs Food objects, and journal_entries for population
def journalPageView(request):
    if not request.session.has_key('isAuth'):
        request.session['isAuth'] = False
        context = {
            'session': request.session,            
            'errors': ["Don't do that"],
            }
        return render(request, 'login.html', context)

    food = Food.objects.all()
    user = User.objects.filter(username = request.session['username'])[0]
    journals = Journal_Entries.objects.filter(user_id = user)
    session = request.session
    context = {
        'session': session,
        'food' : food,
        'journals' : journals
    }
    return render(request, 'journal.html', context)

# just displays recommendations for the user
def recommendationPageView(request):
    if not request.session.has_key('isAuth'):
        request.session['isAuth'] = False
        context = {
            'session': request.session,            
            'errors': ["Don't do that"],
            }
        return render(request, 'login.html', context)

    session = request.session
    context = {
        'session': session
    }
    return render(request, 'recommendations.html', context)

# displays the account information input at creation and allows for allergy and comorbidity CRUD
def accountPageView(request):
    if not request.session.has_key('isAuth'):
        request.session['isAuth'] = False
        context = {
            'session': request.session,            
            'errors': ["Don't do that"],
            }
        return render(request, 'login.html', context)
    
    user = User.objects.filter(username = request.session['username'])
    allergyUsers = Allergies_User.objects.filter(user_id= user[0])
    comoUsers = Comorbidities_User.objects.filter(user_id= user[0])

    session = request.session
    context = {
        'session': session,
        'user': user[0],
        'allergyUsers': allergyUsers,
        'comoUsers': comoUsers
    }
    return render(request, 'account.html', context)
    
# login page allows for login and createAccount
def loginPageView(request):
    if not request.session.has_key('isAuth'):
        request.session['isAuth'] = False
        context = {
            'session': request.session,            
            'errors': ["Don't do that"],
            }
        return render(request, 'login.html', context)

    
    session = request.session
    context = {
        'session': session
    }
    return render(request, 'login.html', context)

#  saves user session info and authenticates browser when logged in
def loginAccount(request):
    errors = []
    try:
        if (
            request.POST['username'] is None or
            request.POST['password'] is None):
            print ('Yay')
    except:
        errors.append("Please enter all fields")

    data = User.objects.filter(username = request.POST['username'])

    if data.count() <= 0:
        errors.append("Please enter all fields")
        
        context = {
            'session': request.session,            
            'errors': errors
        }

        return render(request, 'login.html', context)

    if data[0].password == request.POST['password']:
        # save login info in the session to be accessed until logged out or hard stopped session
        request.session['username'] = data[0].username
        request.session['isAuth'] = True

        
        session = request.session
        context = {
            'session': session
        }
        return render(request, 'index.html', context)
        
    else:
        errors.append("Password is incorrect")
        context = {
            'session': request.session,            
            'errors' : errors,
        }
        return render(request, 'login.html', context)

# add journal entry route from the journalPageView
def addJournal(request):
    import datetime
    
    errors = []
    maxCounter = 0
    
    while True:
        
        foodStr = 'newitem' + str(maxCounter) if maxCounter != 0 else 'newitem'
        quanStr = 'quantity' + str(maxCounter) if maxCounter != 0 else 'quantity'
        try:
            if(request.POST[foodStr] is not None and request.POST[quanStr] is not None):
                maxCounter += 1
                
        except:
            break
    
    # Form validation has passed
    # create instance of journal using the passed data
        
    NewJournal = Journal_Entries()

    journalDate = datetime.datetime.now()
    NewJournal.datetime = journalDate
    mealType = request.POST['mealType']
    NewJournal.meal_name = mealType
    NewJournal.note = request.POST['note']

    # user item
    user = User.objects.filter(username= request.session['username'])[0]
    NewJournal.user_id = user
    
    try:
        NewJournal.save()
    except:
        errors.append('Something went wrong when adding a new Journal Entry')
        context = {
            'session': request.session,            
            'errors' : errors
        }
        return journalPageView(request)
    # add the has table connecting journal and food items together. has dynamic number of 
    # items that can be added
    try:
        for i in range(0, maxCounter):
            foodStr = 'newitem' + str(i) if i != 0 else 'newitem'
            quanStr = 'quantity' + str(i) if i != 0 else 'quantity'
            
            NewHas = Has()
            NewHas.quantity = request.POST[quanStr]
            
            food = Food.objects.filter(food_name = request.POST[foodStr])[0]
            NewHas.food_id = food
            
            journal = Journal_Entries.objects.filter(user_id = user, meal_name = mealType)
            mostRecent = Journal_Entries()
            for el in journal:
                if mostRecent.datetime is None:
                    mostRecent = el
                else:
                    if mostRecent.datetime < el.datetime:
                        mostRecent = el
            NewHas.journal_entries_id = mostRecent

            NewHas.save()
    except:
        errors.append('Something went wrong when adding a Has Table')
    
    context = {
            'session': request.session,            
            'errors' : errors
        }
    return journalPageView(request)

# this isn't referenced in the html currently, it is an api call that will add food to the database based on the url
def addFood(request):
    import requests
    errors = []
    pageCounter = 0

    while True:
        pageCounter += 1
        url = f'https://api.nal.usda.gov/fdc/v1/foods/list?api_key=KfVSBcdEhQffPPckbSrUXCrZ8OvHfc3zXhceyVBj&dataType=Foundation&pageSize=200&pageNumber={pageCounter}'
        res = requests.get(url)
        data = res.json()
        for foodItem in data:
            food_name = foodItem.get("description")
            phos = 0
            k = 0
            water = 0
            na = 0
            protein = 0
            for nutrient in foodItem.get("foodNutrients"):
                nutrientName = nutrient.get('name')

                if nutrientName == "Sodium, Na":
                    na = nutrient.get('amount')
                elif nutrientName == "Protein":
                    protein = nutrient.get('amount')
                elif nutrientName == "Potassium, K":
                    k = nutrient.get('amount')
                elif nutrientName == "Phosphorus, P":
                    phos = nutrient.get('amount')
                elif nutrientName == "Water":
                    water = nutrient.get('amount')

            NewFood = Food()
            NewFood.food_name = food_name
            NewFood.sodium = round(na,2)
            NewFood.protein = round(protein,2)
            NewFood.water = round(water,2)
            NewFood.phos = round(phos,2)
            NewFood.k = round(k,2)
            
            try:
                NewFood.save()
                print(f"{food_name} added!")
            except:
                errors.append(f'Error adding: {food_name}')


        if len(data) != 200 :
            break

    context = {
            'session': request.session,            
            'errors' : errors
    }
    return render (request, 'index.html', context)

# add comorbidities route, also adds comorbidities_user. 
# One person can't have the same Comorbidity risk_name
def addComo(request):
    errors = []
    try:
        if (request.POST['risk_name'] is None or request.POST['description'] is None):
            pass
    except:
        errors.append('Please enter all fields')
        context = {
            'session': request.session,            
            'errors' : errors
        }
        return accountPageView(request)


    user = User.objects.filter(username = request.session['username'])[0]
    comoUser = Comorbidities_User.objects.filter(user_id = user)
    for item in comoUser:
        if item.comorbidities_id.risk_name == request.POST['risk_name']:
            errors.append("You can't enter the same risk twice!")
        context = {
            'session': request.session,            
            'errors' : errors
        }
        return accountPageView(request)

    try:
        NewComo = Comorbidities()
        NewComo.risk_name = request.POST['risk_name']
        NewComo.description = request.POST['description']

        NewComo.save()

        linker = Comorbidities_User()
        como = Comorbidities.objects.filter(description = request.POST['description'], risk_name = request.POST['risk_name'])[0]
        linker.comorbidities_id = como

        user = User.objects.filter(username =  request.session['username'])[0]
        linker.user_id = user

        linker.save()
    except:
        errors.append('Error adding Comorbidity')
    
    context = {
            'session': request.session,            
            'errors' : errors
        }
    return accountPageView(request)

# allows for editing of comorbidities
def editComo(request):
    errors = []
    try:
        if (request.POST['risk_name'] is None or request.POST['description'] is None):
            pass
    except:
        errors.append('Please enter all fields')
        context = {
            'session': request.session,            
            'errors' : errors
        }
        return accountPageView(request)

    try:
        oldComo = Comorbidities.objects.filter(comorbidities_id = request.POST['comorbidities_id'])[0]
        oldComo.risk_name = request.POST['risk_name']
        oldComo.description = request.POST['description']

        oldComo.save()
    except:
        errors.append('Error editing Comorbidity')
    
    context = {
            'session': request.session,            
            'errors' : errors
        }
    return accountPageView(request)

# simply deletes the comorbidity
def deleteComo(request):
    errors = []
    try:
        oldComo = Comorbidities.objects.filter(comorbidities_id = request.POST['comorbidities_id'])[0]

        oldComo.delete()
    except:
        errors.append('Error deleting Comorbidity')
    
    context = {
            'session': request.session,            
            'errors' : errors
        }
    return accountPageView(request)

# add allergy route, also adds allergies_user. 
# One person can't have the same allergy_name
def addAllergy(request):
    errors = []
    try:
        if (request.POST['allergy_name'] is None or request.POST['severity'] is None):
            pass
    except:
        errors.append('Please enter all fields')
        context = {
            'session': request.session,            
            'errors' : errors
        }
        return accountPageView(request)

    user = User.objects.filter(username = request.session['username'])[0]
    allergyUser = Allergies_User.objects.filter(user_id = user)
    for item in allergyUser:
        if item.allergies_id.allergy_name == request.POST['allergy_name']:
            errors.append("You can't enter the same allergy twice!")
        context = {
            'session': request.session,            
            'errors' : errors
        }
        return accountPageView(request)
        
    try:
        NewAllergy = Allergies()
        NewAllergy.allergy_name = request.POST['allergy_name']
        NewAllergy.severity = request.POST['severity']

        NewAllergy.save()

        linker = Allergies_User()
        allergy = Allergies.objects.filter(severity = request.POST['severity'], allergy_name = request.POST['allergy_name'])[0]
        linker.allergies_id = allergy

        user = User.objects.filter(username =  request.session['username'])[0]
        linker.user_id = user

        linker.save()
    except:
        errors.append('Error adding Allergy')
    
    context = {
            'session': request.session,            
            'errors' : errors
        }
    return accountPageView(request)

# allows for allergy_name and severity to be updated
def editAllergy(request):
    errors = []
    try:
        if (request.POST['allergy_name'] is None or request.POST['severity'] is None):
            pass
    except:
        errors.append('Please enter all fields')
        context = {
            'session': request.session,            
            'errors' : errors
        }
        return accountPageView(request)

    try:
        oldAllergy = Allergies.objects.filter(allergies_id = request.POST['allergies_id'])[0]
        oldAllergy.allergy_name = request.POST['allergy_name']
        oldAllergy.severity = request.POST['severity']

        oldAllergy.save()
    except:
        errors.append('Error editing Allergy')
    
    context = {
            'session': request.session,            
            'errors' : errors
        }
    return accountPageView(request)

# allows for allergy to be deleted
def deleteAllergy(request):
    errors = []
    try:
        oldAllergy = Allergies.objects.filter(allergies_id = request.POST['allergies_id'])[0]

        oldAllergy.delete()
    except:
        errors.append('Error deleting Allergy')
    
    context = {
            'session': request.session,            
            'errors' : errors
        }
    return accountPageView(request)

# other option for logging in, if all fields are valid then they create account in the database
# then they have the capability of tracking foods and logging in
def createAccount(request):
    
    errors = []
    try:
        if ( request.POST['firstName'] is None or
        request.POST['lastName'] is None or
        request.POST['sex'] is None or
        request.POST['dob'] is None or
        request.POST['address']  is None or
        request.POST['township']  is None or
        request.POST['state'] is None or
        request.POST['zip'] is None or
        request.POST['county'] is None or
        request.POST['username'] is None or
        request.POST['password'] is None or
        request.POST['current_stage'] is None or
        request.POST['current_height'] is None or
        request.POST['current_weight'] is None or
        request.POST['race'] is None or
        request.POST['email'] is None or
        request.POST['phone'] is None):
            print ('Yay')
    except:
        errors.append("Please enter all fields")
        context = {
            'session': request.session,            
            'errors':errors
        }
        return render (request, 'login.html', context )

    if (len( request.POST['password'] ) < 6):
        errors.append("Password should be at least 6 characters long")

    if (request.POST['password'] != request.POST['password2']):
        errors.append("Passwords do not match")

    # Check for unchecked check boxes
    if ( len(errors) > 0):
        context = {
            'session': request.session,            
            'errors' : errors
        }
        return render (request, 'login.html', context )

    else:
        # Form validation has passed
        try:
            if request.POST['middleName'] is None:
               pass
        except:
            print("They didn't enter a middlename")
            request.POST['middleName'] = ''

        # create instance of user using the passed data
        NewUser = User()
        NewUser.f_name = request.POST['firstName'].strip().capitalize()
        NewUser.m_name = request.POST['middleName'].strip().capitalize()
        NewUser.l_name = request.POST['lastName'].strip().capitalize()
        
        NewUser.date_of_birth = request.POST['dob']
        NewUser.street_address = request.POST['address'].strip()
        NewUser.city = request.POST['township'].strip().capitalize()
        NewUser.state = request.POST['state'].strip().upper()
        NewUser.zip = request.POST['zip'].strip()
        NewUser.county = request.POST['county'].strip().capitalize()
        NewUser.username = request.POST['username'].strip()
        NewUser.password = request.POST['password'].strip()
        
        NewUser.current_height = request.POST['current_height']
        NewUser.current_weight = request.POST['current_weight']
        NewUser.race = request.POST['race'].strip().capitalize()
        NewUser.phone = request.POST['phone'].strip()
        NewUser.email = request.POST['email'].strip()
        
        # create/find instance of suggested level using the passed data
        suggestedLevel = Suggested_Levels.objects.filter(current_stage = request.POST['current_stage'], gender = request.POST['sex'].strip().capitalize())[0]

        NewUser.current_stage = suggestedLevel
        NewUser.gender = suggestedLevel

        try:
            NewUser.save()
        except:
            errors.append('Something went wrong when adding a new user')
            context = {
                'session': request.session,            
                'errors' : errors
            }
            return render (request, 'login.html', context )
    context = {
            'session': request.session,            
            'errors' : []
        }
    return render (request, 'login.html', context )

# just delete the request session object forcing the user to only see the home page or
# the login page
def logout(request):
    del request.session['username']
    del request.session['isAuth']

    context= {
        'session': request.session,            
        'errors': []
    }
    return loginPageView(request)

