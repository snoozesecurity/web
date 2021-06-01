from google.cloud import storage
from google.cloud import secretmanager
from requests import Request, Session
import json

# Gets API Key from Secret Manager
client = secretmanager.SecretManagerServiceClient()
secret_name = "YOUR-SECRET"
project_id = "YOUR-PROJECT-ID"
request = {"name": f"projects/{project_id}/secrets/{secret_name}/versions/latest"}
response = client.access_secret_version(request)
COIN_MKT_KEY = response.payload.data.decode("UTF-8")

# Sets up required fields for CoinMarketCap API call
url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
parameters = {
  'id':'1,2,52,74,1027,2010'
}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': COIN_MKT_KEY,
}

# Initiates Session and GCS connection
session = Session()
session.headers.update(headers)
storage_client = storage.Client()
bucket_name = 'YOUR-PRICE-INFO-BUCKETNAME'
bucket = storage_client.bucket(bucket_name)

# API call to CoinMarketCap to grab latest BTC price info
def getLatestPrice(event, context):
  blob_name = "YOUR-PRICE-INFO-FILENAME"
  try:
    response = session.get(url, params=parameters)
    priceJson = response.json()
  except (ConnectionError, Timeout, TooManyRedirects, ValueError) as e:
    print(e)

  # Replace (update) BTC price info in latest_prices.json file
  blob = bucket.blob(blob_name)
  try:
    blob = bucket.blob('YOUR-PRICE-INFO-FILENAME')
    blob.upload_from_string(json.dumps(priceJson))
    print("replaced YOUR-PRICE-INFO-FILENAME with latest info")
  except:
    print("could not update YOUR-PRICE-INFO-FILENAME")