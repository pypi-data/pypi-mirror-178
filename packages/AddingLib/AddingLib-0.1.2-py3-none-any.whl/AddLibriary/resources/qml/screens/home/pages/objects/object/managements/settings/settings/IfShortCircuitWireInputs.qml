import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.SettingsSwitch {
    property bool isEolMode: [2, 3].includes(extContactModeCombobox.currentIndex)

    title: tr.sabotage_alert_with_a_siren
    checked: device.siren_triggers.includes(2)
    visible: typeCombobox.currentIndex == 0 && isEolMode
}