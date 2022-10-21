
class CWRFile:

    path = "";
    encoding = "";

    def __init__(self, path, encoding="utf8"):
        self.path = path
        self.encoding = encoding

    def readAll(self):
        with open(self.path, 'r', encoding= self.encoding) as file:
            return file.read()

    def read(self, i):
        with open(self.path, 'r', encoding= self.encoding) as file:
            return file.read(i)

    def write(self, text):
        with open(self.path, 'w', encoding= self.encoding) as file:
            file.write(text)

    def append(self, text):
        with open(self.path, 'a', encoding= self.encoding) as file:
            file.write(text)



class CWRItem:

    path = "";
    encoding = "";

    def __init__(self, path, encoding="utf8"):
        self.path = path
        self.encoding = encoding

    def __read__(self):
        with open(self.path, 'r', encoding= self.encoding) as file:
            return file.read()

    def __write__(self, text):
        with open(self.path, 'w', encoding= self.encoding) as file:
            file.write(text)

    def __append__(self, text):
        with open(self.path, 'a', encoding= self.encoding) as file:
            file.write(text)

    def getItem(self, item):
        text = self.__read__()
        return text.split("<" + item + ">")[1].split("</" + item + ">")[0]

    def getItems(self):
        list_1 = self.__read__().split("</")
        list_2 = []
        for i in list_1:
            list_2.append(i.split(">")[0])
        list_1.clear()
        for i in range(len(list_2) - 1):
            list_1.append(list_2[i + 1])

        return list_1

    def containsItem(self, item):
        for i in self.getItems():
            if i == item:
                return True
        return False

    def SetOrAddItem(self, item, value):
        if self.containsItem(item):
            self.setItem(item, value)
        else:
            self.addItem(item, value)

    def setItem(self, item, value):
        if self.containsItem(item):
            text = self.__read__().split("<" + str(item) + ">")[0] + "<" + str(item) + ">" + str(value) + "</" + str(item) + ">" + self.__read__().split("</" + str(item) + ">")[1]
            self.__write__(text)

    def addItem(self, item, value):
        if not self.containsItem(item):
            self.__append__("\n<" + str(item) + ">" + str(value) + "</" + str(item) + ">")

    def removeItem(self, item):
        text = self.__read__().split("<" + str(item) + ">")[0] + self.__read__().split("</" + str(item) + ">")[1]
        self.__write__(text)


