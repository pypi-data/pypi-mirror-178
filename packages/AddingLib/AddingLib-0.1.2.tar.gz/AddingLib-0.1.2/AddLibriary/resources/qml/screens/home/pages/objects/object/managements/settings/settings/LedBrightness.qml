import "qrc:/resources/qml/components/911/DS3/" as DS3


DS3.SettingsSliderIcon {
    title: tr.led_brightness
    value: device.led_brightness
    from: 1
    to: 10
    stepSize: 1
    sideIcons: [
        "qrc:/resources/images/Athena/common_icons/BrightnessLow-M.svg",
        "qrc:/resources/images/Athena/common_icons/BrightnessHigh-M.svg"
    ]
}