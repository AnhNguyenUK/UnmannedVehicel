from PySide2.QtCore import QObject, Qt, Slot, Property
from PySide2.QtGui import QStandardItemModel, QStandardItem 
import time

class ElementRoles:
    deviceIdRole = Qt.UserRole
    latitudeRole = Qt.UserRole + 1
    longitudeRole = Qt.UserRole + 2

class ElementModel(QStandardItemModel, ElementRoles):
    
    def __init__(self, parent=None):
        super(ElementModel, self).__init__(parent)
        roles = {
            ElementRoles.deviceIdRole: b'modelRobotId',
            ElementModel.latitudeRole: b'modelCurrLat',
            ElementModel.longitudeRole: b'modelCurrLong'
        }
        self.setItemRoleNames(roles)

    @Slot(str, str, str)
    def addElement(self, deviceId, currLat, currLong):
        item = QStandardItem()
        print("Add elements")
        self.beginResetModel()
        item.setData(deviceId, ElementModel.deviceIdRole)
        item.setData(currLat, ElementModel.latitudeRole)
        item.setData(currLong, ElementModel.longitudeRole)
        self.appendRow(item)
        self.endResetModel()

class Manager(QObject):
    def __init__(self, parent=None):
        super(Manager, self).__init__(parent)
        self._model = ElementModel()

    def addData(self, data):
        self._model.addElement(data[0],data[1],data[2])  
    
    @Property(QObject, constant=True)
    def model(self):
        return self._model