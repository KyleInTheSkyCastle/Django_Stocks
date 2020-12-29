from django.shortcuts import render,redirect
from .models import Stock
from django.contrib import messages
from .forms import StockForm
import requests
import json


# request is a browser request
def home(request):

	if request.method == 'POST':
		ticker = request.POST['ticker']
		# pk_74cd4d03d660401ba132a6c69609a3cf 
		api_request = requests.get("https://cloud.iexapis.com/stable/stock/" + ticker + "/quote?token=pk_74cd4d03d660401ba132a6c69609a3cf")

		try:
			api = json.loads(api_request.content)
		except Exception as e:
			api = "Error..."

		return render(request, 'home.html', {'api':api})

	else:
		return render(request, 'home.html', {'ticker':'Enter a ticker in the above seatch quote.'})



def about(request):
	return render(request, 'about.html', {})


def portfolio(request):
	if request.method == 'POST':
		form = StockForm(request.POST or None)

		if form.is_valid():
			form.save()
			messages.success(request, ('Stock Has Been Added.'))
			return redirect('portfolio')

	else:
		ticker = Stock.objects.all()
		output = []
		for ticker_item in ticker:

			api_request = requests.get("https://cloud.iexapis.com/stable/stock/" + str(ticker_item) + "/quote?token=pk_74cd4d03d660401ba132a6c69609a3cf")

			try:
				api = json.loads(api_request.content)
				output.append(api)
			except Exception as e:
				api = "Error..."

		return render(request, 'portfolio.html', {'ticker': ticker, 'output': output})


def delete(request, stock_id):
	item = Stock.objects.get(pk=stock_id)
	item.delete()
	messages.success(request, ("Stock Has Been Deleted."))
	return redirect('portfolio')









