# Refer to the CoinMarketCap documentation for additional info
# https://coinmarketcap.com/api/documentation/v1/

from flask import Flask, render_template, redirect, request, session
from google.cloud import storage
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

# Bucket settings for price info

storage_client = storage.Client()
blob_name = 'YOUR-PRICE-INFO-FILENAME'
bucket_name = 'YOUR-PRICE-INFO-BUCKETNAME'
bucket = storage_client.bucket(bucket_name)
blob = bucket.blob(blob_name)

# Supported crypto identifiers (will add functionality later)

supportedCryptos = {'1': 'Bitcoin', '2': 'Litecoin', '52': 'XRP', '74': 'Dogecoin', '1027': 'Ethereum', '2010': 'Cardano'}

# Get current crypto price and current circulating supply; defaults to BTC

def getCryptoData(cryptoId):
  cryptoData = {}
  try:
    json_data = json.loads(blob.download_as_string().decode('utf-8'))
    cryptoData['currPrice'] = round(json_data['data'][str(cryptoId)]['quote']['USD']['price'], 2)
    cryptoData['currSupply'] = round(json_data['data'][str(cryptoId)]['circulating_supply'])
    return cryptoData
  except (ConnectionError, Timeout, TooManyRedirects, ValueError) as e:
    return(e)

app = Flask(__name__)
app.secret_key = "PROBABLY DON'T HARDCODE THIS KEY EITHER"

@app.route("/")
def goToIndex():
  return redirect("/converter")

@app.route('/converter')
def index():
  return render_template("index.html")

@app.route('/convert/')
def getAmount():
  selected_crypto = request.args.get('cryptochoice')
  session["selected_crypto"] = selected_crypto
  return render_template("convert.html", cryptochoice=supportedCryptos[selected_crypto].lower())

@app.route('/data/', methods = ['POST'])
def converted():

  # Check to see if a user actually selected a crypto and thus a session exists; declare variable in function if so
  if "selected_crypto" in session:
    selected_crypto = session["selected_crypto"]

  if request.method == 'POST':
    cryptoAmount = request.form.get('cryptoAmount')

    # Gets a dictionary called cryptoData with currPrice and currSupply keys
    cryptoData = getCryptoData(selected_crypto)

    try:      
      # Must be a positive number and less than the max circulating supply
      if cryptoAmount and float(cryptoAmount) > float(0) and float(cryptoAmount) <= float(cryptoData['currSupply']):
        userTotal = '{:.2f}'.format(round(float(cryptoAmount) * float(cryptoData['currPrice']), 2))
        return render_template('data.html', cryptoAmount = cryptoAmount, userTotal = f'{float(userTotal):,}', cryptoName = supportedCryptos[selected_crypto].lower())
      else:
        raise TypeError()

    except Exception as e:
      print(e)
      return render_template('error.html', cryptoAmount = cryptoAmount)

if __name__ == "__main__":
  app.run(debug=True)