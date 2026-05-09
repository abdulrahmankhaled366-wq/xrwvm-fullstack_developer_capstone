from django.contrib.auth.models import User
from django.contrib.auth import logout, login, authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import logging
import json
from .models import CarMake, CarModel
from .populate import initiate
from django.http import JsonResponse

logger = logging.getLogger(__name__)

@csrf_exempt
def login_user(request):
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    user = authenticate(username=username, password=password)
    data = {"userName": username}
    if user is not None:
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
    return JsonResponse(data)
def get_cars(request):
    count = CarMake.objects.filter().count()
    if(count == 0):
        initiate()
    car_models = CarModel.objects.select_related('car_make')
    cars = []
    for car_model in car_models:
        cars.append({"CarModel": car_model.name, "CarMake": car_model.car_make.name})
    return JsonResponse({"CarModels":cars})
    
def logout_request(request):
    logout(request)
    data = {"userName": ""}
    return JsonResponse(data)

@csrf_exempt
def registration(request):
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    first_name = data['firstName']
    last_name = data['lastName']
    email = data['email']
    username_exists = False
    try:
        User.objects.get(username=username)
        username_exists = True
    except User.DoesNotExist:
        logger.debug("{} is new user".format(username))

    if not username_exists:
        user = User.objects.create_user(
            username=username, 
            first_name=first_name, 
            last_name=last_name, 
            password=password, 
            email=email
        )
        login(request, user)
        return JsonResponse({"userName": username, "status": "Authenticated"})
    else:
        return JsonResponse({"userName": username, "error": "Already Registered"})