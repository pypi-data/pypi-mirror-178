import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.SettingsSwitch {
    title: tr.partial_arming
    checked: device.perimeter_protection_group
}