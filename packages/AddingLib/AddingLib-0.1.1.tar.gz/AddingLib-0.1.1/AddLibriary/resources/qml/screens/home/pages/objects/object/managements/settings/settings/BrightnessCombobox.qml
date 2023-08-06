import "qrc:/resources/qml/components/911/DS3" as DS3

DS3.SettingsPickerTitleSecondary {
    atomTitle.title: tr.led_brightness
    model: [tr.brightness_off, tr.brightness_low, tr.brightness_max]
    currentIndex: {
        return {
            4: 2,
            2: 1,
            1: 0,
        }[device.brightness] || 0
    }
}