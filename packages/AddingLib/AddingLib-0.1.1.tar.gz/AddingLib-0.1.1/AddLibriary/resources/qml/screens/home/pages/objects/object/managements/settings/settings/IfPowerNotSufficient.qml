import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.SettingsSwitch {
    title: tr.if_buses_supply_lost
    checked: device.lost_external_power_aware == "LOST_EXTERNAL_POWER_AWARE_ENABLED"
}