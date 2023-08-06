import "qrc:/resources/qml/components/911/DS3/" as DS3


DS3.SettingsSliderIcon {
    value: device.brightness
    title: tr.keypad_brightness
    from: 0
    to: 5
    stepSize: 1
    sideIcons: [
        "qrc:/resources/images/Athena/common_icons/BrightnessLow-M.svg",
        "qrc:/resources/images/Athena/common_icons/BrightnessHigh-M.svg"
    ]
}