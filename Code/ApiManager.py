import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.upload import VkUpload
from vk_api.utils import get_random_id


class APIManager:

    def __init__(self, token):
        self.token = token
        self.session = vk_api.VkApi(token=self.token)
        self.vk = self.session.get_api()
        self.longpoll = VkLongPoll(self.session)
        self.upload = VkUpload(self.vk)

    def SendTextMessage(self, user_id, msg):
        self.vk.messages.send(
            user_id=user_id,
            message=msg,
            random_id=get_random_id()
        )

    def SendPhotoMessage(self, user_id, owner_id, photo_id, access_key):

        self.vk.messages.send(
            #message = msg,
            attachments= f'photo{owner_id}_{photo_id}_{access_key}',
            user_id=user_id,
            random_id=get_random_id()
        )

    def GetProfileInfo(self):
        return self.vk.account.getProfileInfo()

    def SetProfileInfo_first_name(self, value):
        value = str(value)
        self.vk.account.saveProfileInfo(first_name=value)
    def SetProfileInfo_last_name(self, value):
        value = str(value)
        self.vk.account.saveProfileInfo(last_name=value)
    def SetProfileInfo_bdate(self, value):
        value = str(value)
        self.vk.account.saveProfileInfo(bdate=value)
    def SetProfileInfo_home_town(self, value):
        value = str(value)
        self.vk.account.saveProfileInfo(home_town=value)
    def SetProfileInfo_sex(self, value):
        value = str(value)
        if value == "1" or value == "2":
            self.vk.account.saveProfileInfo(sex=value)
    def SetProfileInfo_bdate_visibility(self, value):
        value = str(value)
        if value == "1" or value == "2" or value == "0":
            self.vk.account.saveProfileInfo(bdate_visibility=value)
    def SetProfileInfo_relation(self, value):
        value = str(value)
        if value == "1" or value == "2" or value == "0" or value == "3" or value == "4" or value == "5" or value == "6" or value == "7" or value == "8":
            self.vk.account.saveProfileInfo(relation=value)
    def SetProfileInfo_status(self,value):
        value = str(value)
        self.vk.account.saveProfileInfo(status=value)

    def isMessage(self):
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW:
                if event.to_me:
                    _textMessage = event.text

                    if len(event.attachments):
                        _textMessage += " - Files: " + str(event.attachments)

                    return (_textMessage, event.user_id)
                else:
                    return None
            else:
                return None

    def Upload_photo(self, path):
        response = self.upload.photo_messages(path)[0]

        owner_id = response['owner_id']
        photo_id = response['id']
        access_key = response['access_key']

        return owner_id, photo_id, access_key
