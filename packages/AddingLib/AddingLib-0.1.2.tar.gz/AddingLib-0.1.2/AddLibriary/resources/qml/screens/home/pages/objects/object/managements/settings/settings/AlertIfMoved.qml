import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.SettingsSwitch {
    width: parent.width

    title: tr.alert_if_moved_1
    checked: device.remove_aware
}