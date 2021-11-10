
iaqi_list = [0, 50, 100, 150, 200, 300, 400, 500]

so2_list = [0, 50, 150, 475, 800, 1600, 2100, 2620]
no2_list = [0, 40, 80, 180, 280, 565, 750, 940]
pm10_list = [0, 50, 150, 250, 350, 420, 500, 600]
pm25_list = [0, 35, 75, 115, 150, 250, 350, 500]
co_list = [0, 2, 4, 14, 24, 36, 48, 60]
o3_list = [0, 100, 160, 215, 265, 800, 1000, 1200]
standard_lists = [pm25_list, pm10_list, so2_list, no2_list, co_list, o3_list]

def aqi_cal(pm25, pm10, so2, no2, co, o3):
    values = [pm25, pm10, so2, no2, co, o3]
    final_aqi = 0
    for i in range(len(values)):
        standard = standard_lists[i]
        cp = values[i]
        for j in range(len(standard)):
            if cp >= standard[j]:
                b_h = standard[j + 1]
                b_l = standard[j]
                i_h = iaqi_list[j + 1]
                i_l = iaqi_list[j]
                break
        current_aqi = (cp - b_l)*((i_h - i_l)/(b_h - b_l))
        final_aqi = max(final_aqi, current_aqi)
    return round(final_aqi,2)

def wind_speed_cal(u, v):
    return round((u**2 + v**2)**(1/2),2)
    
def processing_line(line, data):
    values = line.split(",")
    pm25 = float(values[0])
    pm10 = float(values[1])
    so2 = float(values[2])
    no2 = float(values[3])
    co = float(values[4])
    o3 = float(values[5])
    u = float(values[6])
    v = float(values[7])
    temp = float(values[8])
    rh = float(values[9])
    psfc = float(values[10])
    lat = float(values[11])
    lon = float(values[12])
    aqi = aqi_cal(pm25, pm10, so2, no2, co, o3)
    wind_speed = wind_speed_cal(u, v)
    data.write(f"{pm25},{pm10},{so2},{no2},{co},{o3},{u},{v},{temp},{rh},{psfc},{lat},{lon},{aqi},{wind_speed}\n")
    return


def processing_line_for_province(line, province_dict, province_lines, index):
    values = line.split(",")
    pm25 = float(values[0])
    pm10 = float(values[1])
    so2 = float(values[2])
    no2 = float(values[3])
    co = float(values[4])
    o3 = float(values[5])
    # u = float(values[6])
    # v = float(values[7])
    temp = float(values[8])
    rh = float(values[9])
    psfc = float(values[10])

    aqi = float(values[13])
    wind_speed = float(values[14].strip())

    index_list = [pm25,pm10,so2,no2,co,o3,temp,rh,psfc,aqi,wind_speed]
    province = province_lines[index].split(",")[2].strip()

    if province in province_dict:
        for i in range(0, len(index_list)):
            province_dict[province][i] += index_list[i]
    else:
        province_dict[province] = [0]*11


def process_daily_files():
    file_names = []
    for i in range(1, 10):
        file_names.append(f"./201301/CN-Reanalysis-daily-2013010{i}00.csv")
    for i in range(10, 32):
        file_names.append(f"./201301/CN-Reanalysis-daily-201301{i}00.csv")

    for i in range(len(file_names)):
        file_name = file_names[i]
        f = open(file_name, "r", encoding="utf-8")
        if i < 10:
            data = open(f"./201301_daily_processed/2013010{i+1}.csv", "w", encoding="utf-8")
        else:
            data = open(f"./201301_daily_processed/201301{i+1}.csv", "w", encoding="utf-8")

        data.write("PM2.5,PM10,SO2,NO2,CO,O3,U,V,TEMP,RH,PSFC,lat,lon,AQI,ws\n")

        lines = f.readlines()
        for i in range(1, len(lines)):
        # for i in range(1, 10):
            line = lines[i]
            processing_line(line, data)
            if i%1000 == 0:
                print(f"{file_name}: {i}/{len(lines)}")
        f.close()
        data.close()


def process_for_province():
    file_names = []
    for i in range(1, 10):
        file_names.append(f"./201301_daily_processed/2013010{i}.csv")
    for i in range(10, 32):
        file_names.append(f"./201301_daily_processed/201301{i}.csv")

    province_file = open('province_lon_lat.csv', "r", encoding='gbk')
    province_lines = province_file.readlines()
    province_count = dict()
    for i in range(1, len(province_lines)):
        line = province_lines[i]
        province = line.split(",")[2].strip()
        if province in province_count:
            province_count[province] += 1
        else:
            province_count[province] = 1

    # print(province_count)

    for i in range(len(file_names)):
        file_name = file_names[i]
        print(file_name)
        f = open(file_name, "r", encoding="utf-8")
        if i + 1 < 10:
            data = open(f"./201301_province/2013010{i+1}.csv", "w", encoding="gbk")
        else:
            data = open(f"./201301_province/201301{i+1}.csv", "w", encoding="gbk")

        data.write("province,avg_PM2.5, avg_PM10,avg_SO2,avg_NO2,avg_CO,avg_O3,avg_TEMP,avg_RH,avg_PSFC,avg_AQI,avg_windspeed,degree\n")
        lines = f.readlines()
        province_dict = dict()
        for i in range(1, len(lines)):
            line = lines[i]
            processing_line_for_province(line, province_dict, province_lines, i)
            # if i%1000 == 0:
            #     print(f"{file_name}: {i}/{len(lines)}")
        f.close()

        del province_dict["中华人民共和国"]
        del province_dict["[]"]

        for key in province_dict:
            degree = -1
            data.write(f"{key}")
            for i in range(len(province_dict[key])):
                province_dict[key][i] = round(province_dict[key][i]/province_count[key],2)
                data.write(f",{province_dict[key][i]}")
                if i == 9:
                    if province_dict[key][i] <= 50:
                        degree = 1
                    elif province_dict[key][i] <= 100:
                        degree = 2
                    elif province_dict[key][i] <= 150:
                        degree = 3
                    elif province_dict[key][i] <= 200:
                        degree = 4
                    elif province_dict[key][i] <= 300:
                        degree = 5
                    else:
                        degree = 6
            data.write(f",{degree}\n")
        data.close()

if __name__ == "__main__":
    # f = open("./201301_province/20130101.csv", "r", encoding="gbk")
    # lines = f.readlines()
    # for line in lines:
    #     print(line)
    process_for_province()
