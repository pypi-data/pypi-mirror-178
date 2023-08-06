import "qrc:/resources/qml/components/911/DS3/" as DS3


DS3.InfoContainer {
    titleComponent.text: device.name
    descComponent.visible: !!device.room_name
    descComponent.text: device.room_name || ""
}