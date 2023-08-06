import "qrc:/resources/qml/components/911/DS3/" as DS3


DS3.SettingsColorSlider {
    title: tr.current_protection_threshold
    value: device.current_protection_threshold
    to: 16
    stepSize: 1
    suffix: "A"
    colorStops: ({
        0: ui.ds3.figure.interactive,
        14: ui.ds3.figure.attention
    })
}