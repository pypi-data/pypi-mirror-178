import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.SettingsSwitch {
    width: parent.width

    checked: device.indicator_light_mode == "STANDARD"
    title: tr.alarm_indication_off
}