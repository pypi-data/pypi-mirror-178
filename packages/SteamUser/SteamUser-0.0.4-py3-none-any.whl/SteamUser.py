import requests
class Steam:
    def __init__(self,ApiKey):
        self.SteamApiKey=ApiKey

    def GetUserInfo(self,SteamID):
        Requests = requests.get(f'https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key={self.SteamApiKey}&format=json&steamids={SteamID}',timeout=100)
        return Requests.json()['response']["players"][0]


    def GetGameHours(self,SteamID,AppID="None"):
        Requests = requests.get(f'https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={self.SteamApiKey}&steamid={SteamID}&format=json',timeout=100)
        if AppID == "None":
            return Requests.json()
        for X in Requests.json()["response"]["games"]:
            if X["appid"] == AppID:
                return X["playtime_forever"]
        return 

    def GetFriendList(self,SteamID):
        Requests = requests.get(f'https://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={self.SteamApiKey}&steamid={SteamID}&relationship=friend',timeout=100)
        return Requests.json()["friendslist"]["friends"]
        #for X in Requests.json()["response"]["games"]:
        

    def GetFriendData(self,SteamID):
        OrgData=self.GetFriendList(SteamID)
        FriendData=[]
        for X in OrgData:
            FriendData.append(self.GetUserInfo(X["steamid"]))
        return FriendData

    #def GetVehicleData(AppID,VehicleName):
        #RequestsMain = requests.get(f'https://api.steampowered.com/IPublishedFileService/QueryFiles/v1/?key={SteamApiKey}&appid={AppID}&search_text="{VehicleName}"&return_metadata=true&return_kv_tags=true&return_short_description=true',timeout=10000)
        #return RequestsMain.json()

#S=Steam("943C94FE678FEC0ADE4A59E58A8949CB")

#print(S.GetFriendData(76561198371768441))
