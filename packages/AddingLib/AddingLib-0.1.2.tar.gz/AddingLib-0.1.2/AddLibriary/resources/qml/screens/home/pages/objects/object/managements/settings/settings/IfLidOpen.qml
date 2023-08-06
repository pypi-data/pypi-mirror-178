import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.SettingsSwitch {
    title: tr.if_siren_lid_open
    checked: device.tamper_aware == "TAMPER_AWARE_ENABLED"
}