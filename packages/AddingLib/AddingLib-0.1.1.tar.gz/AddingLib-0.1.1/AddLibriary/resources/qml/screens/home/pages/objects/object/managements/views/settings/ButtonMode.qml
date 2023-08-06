import "qrc:/resources/qml/components/911/DS3/" as DS3


DS3.InfoTitle {
    atomTitle {
        title: tr.button_mode
        subtitle: {
            var items = [tr.na, tr.panic_button_enabled, tr.smart_button_enabled, tr.interconnect_delay_button_mode]
            return items[device.button_mode]
        }
    }
    leftIcon.source: "qrc:/resources/images/Athena/views_icons/SwitchOn-M.svg"
}