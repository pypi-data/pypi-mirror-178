import "qrc:/resources/qml/components/911/DS3/" as DS3


DS3.SettingsSliderIcon {
    visible: indicationMode.currentIndex !== 0
    value: device.indication_brightness
    title: tr.led_brightness
    from: 1
    to: 15
    stepSize: 1
    doubleStepSizeFrom: 16
    sideIcons: [
        "qrc:/resources/images/Athena/common_icons/BrightnessLow-M.svg",
        "qrc:/resources/images/Athena/common_icons/BrightnessHigh-M.svg"
    ]
}