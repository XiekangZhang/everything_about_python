import requests

if __name__ == "__main__":
    new_headers = {'Authorization': 'Basic lD69EkKLTKmNqy9DCMLjdKyMqcpaOjyuo5-a4R91n04T6E1QuoHNtxt20h2peJ7q',
                   'Accept': 'application/json'}

    # response = requests.get('https://api.eu.cloud.talend.com/tmc/v2.6/subscription', data = {'key':'value'}, proxies=proxies, headers = new_headers)
    response = requests.get('https://api.eu.cloud.talend.com/tmc/v2.6/environments', headers=new_headers, verify=False)

    print(response)
