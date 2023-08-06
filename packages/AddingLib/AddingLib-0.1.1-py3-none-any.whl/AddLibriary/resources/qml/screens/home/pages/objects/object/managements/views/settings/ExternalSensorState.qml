import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.InfoTitle {
    property bool isBad: !["N/A", "0"].includes(device.external_contact_alert)

    width: parent.width

    visible: device.external_contact_alarm_mode == 1
    atomTitle {
        title: tr.external_sensor_state
        subtitle: {
            if (device.external_contact_alert == "N/A") {
                return tr.na
            }
            if (device.external_contact_alert == 0) {
                return tr.ok
            }
            return tr.alert
        }
    }
    leftIcon.source: "qrc:/resources/images/Athena/views_icons/ExternalContact-M.svg"
    status: isBad ? ui.ds3.status.ATTENTION : ui.ds3.status.DEFAULT
}