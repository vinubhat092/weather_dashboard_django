from django.shortcuts import render
from django.http import HttpResponse
from dashboard.forms import CityForm

import requests
# Create your views here.
def get_weather_data(city_name):
	url = 'https://api.openweathermap.org/data/2.5/weather'
	params = {
	 'q':city_name,
	 'appid':'8935b185c67e4c7e075740d121122be9',
	 'units':'metric',
	}
	response = requests.get(url, params=params)
	print(response.status_code)
	json_response = response.json()

	weather_data = {
			'temp':json_response['main']['temp'] ,
			'temp_min':json_response['main']['temp_min'],
			'temp_max':json_response['main']['temp_max'] ,
			'city_name':json_response['name'],
			'country':json_response['sys']['country'],
			'lat':json_response['coord']['lat'],
			'lon':json_response['coord']['lon'] ,
			'weather':json_response['weather'][0]['main'] ,
			'weather_desc':json_response['weather'][0]['description'] , 
			'pressure':json_response['main']['pressure'],
			'humidity':json_response['main']['humidity'] ,
			'windspeed':json_response['wind']['speed'] ,
			}
	return weather_data



def home(request):
	form = CityForm()
	if request.method == 'POST':
		form = CityForm(request.POST)
		if form.is_valid():
			form.save()
			city_name = form.cleaned_data.get('city_name')
			weather_data = get_weather_data(city_name)
			


	elif request.method == 'GET':
		city_name = City.objects.latest('date_added').city_name
		weather_data = get_weather_data(city_name)



	template_name='home.html'
	context = {'form':form, 'weather_data':weather_data}
	return render(request,template_name,context=context)
