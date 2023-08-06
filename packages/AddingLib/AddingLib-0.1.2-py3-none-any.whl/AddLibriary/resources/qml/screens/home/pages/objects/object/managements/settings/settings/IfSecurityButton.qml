import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.SettingsSwitch {
    visible: functionCombobox.currentIndex == 1
    title: tr.if_panic_button_is_pressed
    checked: device.siren_triggers.includes(1)
}
