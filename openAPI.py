import os
import csv
import math


def modifyCSV():
    with open('public_office_openAPI.csv', 'r') as csvFile:
        with open('public_office_data_pluspot.csv', 'w', newline='') as newCsv:
            reader = csv.DictReader(csvFile)
            writer = csv.writer(newCsv)

            # name : FCLTY_NM, lat : X, lng : Y, regionDepth : RN_ADRES, street : RN_ADRES, detail: regionDepth[3], zibun : ADRES, geoPoint : [X, Y], spotGroupType : 'virtualSpotOnly', status : 'visible'
            data = [['name', 'lat', 'lng', 'regionDepth1', 'regionDepth2', 'regionDepth3',
                     'detail', 'street', 'zibun', 'geoPoint', 'spotGroupType', 'status', 'description']]

            for row in reader:
                name = row['FCLTY_NM']
                lat = (float(row['Y']) * 180) / 20037508.34
                lat = (math.atan(math.pow(math.e, lat * (math.pi / 180)))
                       * 360) / math.pi - 90
                lng = (float(row['X']) * 180) / 20037508.34
                geoPoint = 'POINT (' + str(lng) + ' ' + str(lat) + ')'
                spotGroupType = 'virtualSpotOnly'
                status = 'visible'

                street = row['RN_ADRES']
                zibun = row['RN_ADRES']

                splitAdres = zibun.split()
                regionDepth = ['' for i in range(4)]
                for idx in range(len(splitAdres)):
                    if (idx == 4):
                        break
                    regionDepth[idx] = splitAdres[idx]

                for idx in range(4, len(splitAdres)):
                    regionDepth[3] = regionDepth[3] + ' ' + splitAdres[idx]

                description = row['FCLTY_TY'] + ',' + row['TELNO']

                data.append([name, lat, lng, regionDepth[0], regionDepth[1], regionDepth[2],
                            regionDepth[3], street, zibun, geoPoint, spotGroupType, status, description])

            writer.writerows(data)


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
    numOfRows = 10000
    pageNo = 0
    Fclty_Cd = 501010  # If you want story information 509010
    dataType = "json"

    data = []

    try:
        while (True):
            pageNo += 1
            print("Page[", pageNo, "] data request...")
            # OPEN_API_KEY is stored not git repository but local enviorment value
            params = {
                "serviceKey": serviceKey,
                "numOfRows": numOfRows,
                "pageNo": pageNo,
                "dataType": dataType,
                "Fclty_Cd": Fclty_Cd
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

        if len(data) != 0:
            jsonToCSV(data)

    except requests.exceptions.RequestException as e:
        print("An error occurred:", e)


def main():
    requestOpenAPI()
    modifyCSV()  # Modify raw csv file to pluspot format


if __name__ == "__main__":
    main()
