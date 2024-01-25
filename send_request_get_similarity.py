import requests

if __name__=='__main__':
    # Change to host of your server
    host = "127.0.0.1"
    # Change to port of your server
    port = 5000
    # Change to wallets of your interest
    # wallet_list = 

    # Change to thresholds of your interest
    lower_threshold=0.5
    upper_threshold=0.71

    # Change to preferable response format. Possible are csv, json.
    response_format = "json"

    response = requests.get('http://'+str(host)+':' + str(port)+'/similarity',
                            params={
                                "wallet_list": wallet_list,
                                "lower_threshold": lower_threshold,
                                "upper_threshold": upper_threshold,
                                "response_format": response_format
                            })
    print(response.text)


