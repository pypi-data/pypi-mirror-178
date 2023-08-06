import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.InfoTitle {
    property bool isBad: device.extra_contact_aware

    atomTitle {
        title: tr.secondary_sensor
        subtitle: {
            if (!device.extra_contact_aware) {
                return tr.off
            }
            if (device.extra_contact_closed == "N/A") {
                return tr.na
            }
            if (device.extra_contact_closed == "1") {
                return tr.closed
            }
            return tr.opened
        }
    }
    leftIcon.source: "qrc:/resources/images/Athena/views_icons/ExternalContact-M.svg"
    status: isBad ? ui.ds3.status.ATTENTION : ui.ds3.status.DEFAULT
}
