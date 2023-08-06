import "qrc:/resources/qml/components/911/DS3/" as DS3


DS3.SettingsSwitch {
    title: tr.block_keypad
    checked: device.blocking_enabled
}