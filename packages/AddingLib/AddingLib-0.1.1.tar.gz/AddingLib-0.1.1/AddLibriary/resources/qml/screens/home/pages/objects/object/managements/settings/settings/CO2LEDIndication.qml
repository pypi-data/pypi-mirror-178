import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.SettingsSwitch {
    title: tr.blink_co_high_level
    checked: device.co2_indication == "CO2_INDICATION_ON"
}
