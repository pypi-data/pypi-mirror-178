import "qrc:/resources/qml/components/911/DS3/" as DS3


DS3.SettingsSliderValue {
    value: device.current_protection_threshold
    title: tr.current_protection_threshold
    from: 1
    to: 16
    stepSize: 1
}