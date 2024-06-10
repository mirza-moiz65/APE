from django.shortcuts import render
import csv
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# from .models import Coin  # Import your model if defined

def coin_list(request):
    csv_filename = "coins_data.csv"  # Replace with your CSV file path
    coins = []

    with open(csv_filename, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        for row in reader:
            # Assuming CSV columns are in the order: Symbol, Price, 1h % change, 24h % change, 7d % change, Market Cap, Volume (24h), Circulating Supply
            name,symbol, current_price, total_volume,market_cap = row
            coin = {
                'symbol':symbol,
                'name': name,
                'price': current_price,
                'market_cap':market_cap,
                'volume': total_volume,
            }
            coins.append(coin)

    # Paginate the data
    paginator = Paginator(coins, 100)  # Show 20 items per page
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
