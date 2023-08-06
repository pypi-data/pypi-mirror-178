import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.SettingsSwitch {
    visible: !device.blink_while_armed_and_max_volume_available
    checked: [2, 3].includes(device.blink_while_armed)
    title: tr.blink_while_armed
}