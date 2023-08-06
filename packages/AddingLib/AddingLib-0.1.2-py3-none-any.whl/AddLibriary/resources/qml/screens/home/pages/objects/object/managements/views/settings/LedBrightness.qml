
import "qrc:/resources/qml/components/911/DS3/" as DS3

DS3.InfoTitle {
    atomTitle {
        title: tr.led_brightness
        subtitle: {
            if (device.brightness == 1) return tr.brightness_off
            if (device.brightness == 2) return tr.brightness_low
            if (device.brightness == 4) return tr.brightness_max
            return tr.na
        }
    }
    leftIcon.source: "qrc:/resources/images/Athena/views_icons/BrightnessHigh-M.svg"
}