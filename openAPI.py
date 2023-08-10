import requests
import os
import csv


def jsonToCSV(data):
    csv_filename = "public_office_openAPI.csv"

    print("Write json data to csv file : ", csv_filename)
    # Write JSON data to CSV
    with open(csv_filename, 'w', newline='') as csvfile:
        csv_writer = csv.DictWriter(
            csvfile, fieldnames=data[0].keys())

        # Write header
        csv_writer.writeheader()

        # Write data rows
        csv_writer.writerows(data)


def requestOpenAPI():

    base_url = "https://safemap.go.kr/openApiService/data/getPublicInstitutionsData.do"
    # OPEN_API_KEY is not stored at git repository
    serviceKey = os.getenv('OPEN_API_KEY')
    numOfRows = 10000  # If you want total data, set 108567
    pageNo = 0
    dataType = "json"

    data = []

    try:
        while (True):
            pageNo += 1
            print("Page[", pageNo, "] data request...")
            # OPEN_API_KEY is not stored at git repository
            params = {
                "serviceKey": serviceKey,
                "numOfRows": numOfRows,
                "pageNo": pageNo,
                "dataType": dataType
            }
            response = requests.get(base_url, params=params)

            if response.status_code == 200:
                print("Request successful!")
                response_data = response.json()['response']

                result_code = response_data['header']['resultCode']
                if result_code == '02':
                    print('SERVICE SUCCESS BUT NO DATA')
                    break
                else:
                    print('SERVICE SUCCESS WITH DATA')
                    data += response_data['body']['items']
            else:
                print(
                    f"Request failed with status code: {response.status_code}")
                break

        jsonToCSV(data)

    except requests.exceptions.RequestException as e:
        print("An error occurred:", e)


def main():
    requestOpenAPI()


if __name__ == "__main__":
    main()
