import "qrc:/resources/qml/components/911/DS3/" as DS3


DS3.SettingsSwitch {
    title: tr.if_rs_alarm_detected
    visible: device.roller_shutter_available && externalContact.checked && extraContactTypeCombobox.currentIndex == 1
    checked: device.siren_triggers.includes(5)
}