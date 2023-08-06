import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.SettingsSwitch {
    title: tr.if_CO_detected
    checked: device.siren_triggers.includes(4)
    visible: alarmCoEnabled.checked
}