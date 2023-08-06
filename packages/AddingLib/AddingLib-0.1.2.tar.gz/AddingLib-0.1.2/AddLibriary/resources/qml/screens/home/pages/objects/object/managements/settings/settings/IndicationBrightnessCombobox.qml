import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.SettingsPickerTitleSecondary {
    visible: device.brightness_available && indication.checked
    atomTitle.title: tr.led_brightness
    model: [tr.brightness_max, tr.brightness_low]
    currentIndex: device.indication_brightness - 1
}