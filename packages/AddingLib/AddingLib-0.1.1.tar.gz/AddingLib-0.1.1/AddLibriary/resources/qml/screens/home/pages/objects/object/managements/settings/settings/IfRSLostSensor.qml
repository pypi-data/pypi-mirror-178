import "qrc:/resources/qml/components/911/DS3/" as DS3


DS3.SettingsSwitch {
    title: tr.if_rs_lost
    checked: device.siren_triggers.includes(6)
    visible: device.roller_shutter_available && externalContact.checked && extraContactTypeCombobox.currentIndex == 1
}