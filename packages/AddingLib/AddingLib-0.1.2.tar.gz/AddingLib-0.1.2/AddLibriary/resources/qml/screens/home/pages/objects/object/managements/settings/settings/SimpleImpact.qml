import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.SettingsSwitch {
    title: tr.ignore_simple_impact
    checked: device.ignore_simple_impact
    visible: shockSensor.checked
}