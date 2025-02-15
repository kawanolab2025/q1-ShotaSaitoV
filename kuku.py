import requests
import json
from datetime import datetime
import datetime as dt


def urlMake():
    date_list=["Weekday","SaturdayHoliday"] 
    tozai_stationList=["Nakano","Iidabashi","Toyocho","Urayasu","NishiFunabashi"]

    key=""
    #駅の指定
    trainLine="&odpt:station=odpt.Station:TokyoMetro.Tozai.NishiFunabashi"
    #平日ダイヤWeekday／土休日ダイヤSaturdayHoliday
    def selDay():
        wk_date=dt.datetime.now().replace(second=0, microsecond=0)
        if(wk_date.isoweekday()>=6):
            return date_list[1]
        else:
            return date_list[0]
    date="&odpt:calendar=odpt.Calendar:"+selDay()
    #行先方向の指定
    trainDirection="&odpt:railDirection=odpt.RailDirection:TokyoMetro.Nakano"
   
    url= "https://api.odpt.org/api/v4/odpt:StationTimetable?odpt:operator=odpt.Operator:TokyoMetro"+trainLine+date+trainDirection+"&acl:consumerKey="+key
    return url

def makeJson(): #URLをもとにAPIを呼び出し、JSON形式に変換したデータを返す
    response=requests.get(urlMake())
    if response.status_code==200:
        data=response.json()
        json_dict=json.loads(json.dumps(data)) #JSONデータをテキストに変換しそれを辞書型として格納する。
        return json_dict
    else:
        print("Error",response.status_code)

def compTime(json_dict): #現在時刻と、APIによって呼び出されたJSONデータのうち発車時刻を比較し、一番近い要素の値を返す
    current_time = dt.datetime.now().replace(second=0, microsecond=0)
    i=0
    flag=1
    while(True):
        if flag==0:
            break
        else:
            string_time=json_dict[0]["odpt:stationTimetableObject"][i]["odpt:departureTime"]
            time_obj = dt.datetime.strptime(string_time, "%H:%M")
            if time_obj.time() > current_time.time():
                flag=0
            else:
                i+=1
    return i
            

def printTrain(train_dict,i): #辞書データと取り出す要素の最初の番号を引数として、JSON内のデータを人が見てわかりやすい言葉として出力する。
    now=dt.datetime.now().replace(second=0, microsecond=0)
    
    print("東京メトロ東西線西船橋駅：現在",str(now.month),"月"+str(now.day),"日",str(now.hour),":",str(now.minute))
    for j in range(3): 
        
        
        if j==0:
            print("先　発：",end="")
        elif j==1:
            print("次　発：",end="")
        else:
            print("次々発：",end="")
        print(train_dict[0]["odpt:stationTimetableObject"][i]["odpt:trainNumber"],end=" ") 
        if(train_dict[0]["odpt:stationTimetableObject"][i]["odpt:trainType"]=='odpt.TrainType:TokyoMetro.Local'):
            print("[普　　通]",end=" ")
        elif(train_dict[0]["odpt:stationTimetableObject"][i]["odpt:trainType"]=='odpt.TrainType:TokyoMetro.Rapid'):
            print("[快　　速]",end=" ")
        elif(train_dict[0]["odpt:stationTimetableObject"][i]["odpt:trainType"]=='odpt.TrainType:TokyoMetro.CommuterRapid'):
            print("[通勤快速]",end=" ")
        else:
            print("E")
        
        if (train_dict[0]["odpt:stationTimetableObject"][i]["odpt:destinationStation"][0]=="odpt.Station:JR-East.ChuoSobuLocal.Mitaka"):
            print("三　鷹",end="：")
        elif (train_dict[0]["odpt:stationTimetableObject"][i]["odpt:destinationStation"][0]=="odpt.Station:TokyoMetro.Tozai.Nakano"):
            print("中　野",end="：")
        elif (train_dict[0]["odpt:stationTimetableObject"][i]["odpt:destinationStation"][0]=="odpt.Station:TokyoMetro.Tozai.Toyocho"):
            print("東陽町",end="：")
        else:
            print("未実装",end="")
            
        print(train_dict[0]["odpt:stationTimetableObject"][i]["odpt:departureTime"],end="") 
        
        try :
            (train_dict[0]["odpt:stationTimetableObject"][i]["odpt:isOrigin"]==True)
            print("　＊当駅始発＊",end="")
        except KeyError:
            pass
        
        try :
            (train_dict[0]["odpt:stationTimetableObject"][i]["odpt:isLast"]==True)
            print("　＊終　電＊",end="")
        except KeyError:
            pass
        print()
        i+=1

printTrain(makeJson(),compTime(makeJson()))
