import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.SettingsSwitch {
    title: tr.primary_sensor
    checked: device.reed_contact_aware
}