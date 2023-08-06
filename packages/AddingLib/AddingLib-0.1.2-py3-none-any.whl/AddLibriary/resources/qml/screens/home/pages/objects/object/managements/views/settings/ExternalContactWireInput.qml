import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.InfoTitle {
    property bool isBad: device.ext_contact_state != 2

    visible: device.input_is_tamper == 0 && device.ext_contact_alarm_mode != 2

    atomTitle {
        title: tr.secondary_sensor
        subtitle: {
            if (device.ext_contact_state == 2) {
                return tr.ok
            }
            return tr.alert
        }
    }
    leftIcon.source: "qrc:/resources/images/Athena/views_icons/ExternalContact-M.svg"
    status: isBad ? ui.ds3.status.ATTENTION : ui.ds3.status.DEFAULT
}
