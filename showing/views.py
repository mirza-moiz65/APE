from django.shortcuts import render
import csv
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Crypto  # Import your model if defined
from .custom_scraper import chrome_scrape
from django.http import HttpResponse


def upload_csv(request):
    # Scrape data using chrome_scrape function
    scrapper_result = chrome_scrape()
    print(scrapper_result)  # For debugging purposes
    
    csv_filename = "coins_data.csv"  # Replace with your CSV file path

    with open(csv_filename, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        for row in reader:
            # Assuming CSV columns are in the order: Name, Symbol, Current Price, Total Volume, Market Cap
            name, symbol, current_price, total_volume, market_cap = row
            
            # Create or update Crypto objects based on CSV data
            crypto_obj, created = Crypto.objects.get_or_create(
                symbol=symbol,
                defaults={
                    'name': name,
                    'price': float(current_price),
                    'market_cap': float(market_cap),
                    'volume': float(total_volume),
                    'posts': 0  # Initialize posts to 0
                }
            )
            
            # Find corresponding scrapper_result object by name
            matching_objects = [obj for obj in scrapper_result if obj['name'] == name]
            if matching_objects:
                # Assuming scrapper_result has exactly one matching object
                scrapper_data = matching_objects[0]
                # Update posts attribute based on scrapper result
                crypto_obj.posts = scrapper_data.get('count', 0)  # Update posts attribute

            # Save the Crypto object with updated posts attribute
            crypto_obj.save()

    return HttpResponse("CSV uploaded successfully!")


def coin_list(request):
    # Fetch all the coin records from the Crypto model
    coins = Crypto.objects.all()

    # Paginate the data
    paginator = Paginator(coins, 100)  # Show 100 items per page
    page_number = request.GET.get('page')
    try:
        paginated_coins = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_coins = paginator.page(1)  # If page is not an integer, deliver first page.
    except EmptyPage:
        paginated_coins = paginator.page(paginator.num_pages)  # If page is out of range, deliver last page.

    context = {
        'coins': paginated_coins,
    }
    return render(request, 'coin_list.html', context)
