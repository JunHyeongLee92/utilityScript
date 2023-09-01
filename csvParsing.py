import csv
import os


def csvParsing(file_name):
    with open(file_name, 'r') as csvFile:
        with open('pluspot_' + file_name, 'w', newline='') as newCsv:
            reader = csv.DictReader(csvFile)
            writer = csv.writer(newCsv)

            data = [['name', 'lat', 'lng', 'regionDepth1', 'regionDepth2', 'regionDepth3',
                     'detail', 'street', 'zibun', 'geoPoint', 'spotGroupType', 'status', 'description']]

            for row in reader:
                name = row['공원명']
                lat = row['위도']
                lng = row['경도']
                geoPoint = 'POINT (' + str(lng) + ' ' + str(lat) + ')'
                spotGroupType = 'virtualSpotOnly'
                status = 'visible'

                streetName = '소재지도로명주소'  # 세종 = 소재지도로명주소, 수원 = 소재지지번주소
                street = row[streetName]
                zibun = row[streetName]

                splitAdres = zibun.split()
                regionDepth = ['' for i in range(4)]
                for idx in range(len(splitAdres)):
                    if (idx == 4):
                        break
                    regionDepth[idx] = splitAdres[idx]

                for idx in range(4, len(splitAdres)):
                    regionDepth[3] = regionDepth[3] + ' ' + splitAdres[idx]

                description = row['공원구분'] + ',' + row['전화번호']

                data.append([name, lat, lng, regionDepth[0], regionDepth[1], regionDepth[2],
                            regionDepth[3], street, zibun, geoPoint, spotGroupType, status, description])

            writer.writerows(data)
    print('Success!')


def main():
    os.chdir('데이터산출물')
    file_name = '도시공원정보_세종특별자치시_20230831' + '.csv'
    csvParsing(file_name)


if __name__ == "__main__":
    main()
