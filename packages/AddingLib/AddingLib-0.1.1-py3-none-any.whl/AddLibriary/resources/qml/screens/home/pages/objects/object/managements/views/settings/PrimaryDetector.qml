import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.InfoTitle {
    atomTitle {
        title: tr.primary_sensor
        subtitle: {
            if (!device.reed_contact_aware) {
                return tr.off
            }
            if (device.reed_closed == "N/A") {
                return tr.na
            }
            if (device.reed_closed == 1) {
                return tr.closed
            }
            return tr.opened
        }
    }
    leftIcon.source: "qrc:/resources/images/Athena/views_icons/PrimaryDetector-M.svg"
}