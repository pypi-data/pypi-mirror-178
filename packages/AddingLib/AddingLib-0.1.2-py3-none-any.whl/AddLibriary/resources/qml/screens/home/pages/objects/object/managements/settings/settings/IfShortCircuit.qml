import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.SettingsSwitch {
    title: tr.power_supply_sabotage_alert_with_a_siren
    checked: device.siren_triggers.includes(1)
}