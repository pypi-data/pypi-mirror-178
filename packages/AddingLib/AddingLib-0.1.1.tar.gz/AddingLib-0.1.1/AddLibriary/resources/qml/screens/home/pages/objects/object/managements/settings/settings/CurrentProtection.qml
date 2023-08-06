import "qrc:/resources/qml/components/911/DS3/" as DS3


DS3.SettingsSwitch {
    title: tr.current_protection
    checked: device.current_protection
}