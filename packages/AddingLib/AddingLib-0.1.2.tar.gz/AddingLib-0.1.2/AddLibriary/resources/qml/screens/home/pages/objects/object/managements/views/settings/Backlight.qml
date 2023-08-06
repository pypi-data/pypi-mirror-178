import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.InfoTitle {
    atomTitle {
        title: tr.backlight_lightswitch
        subtitle: device.led_indication_enabled ? tr.on : tr.off
    }

    leftIcon.source: "qrc:/resources/images/Athena/views_icons/BrightnessHigh-M.svg"
}