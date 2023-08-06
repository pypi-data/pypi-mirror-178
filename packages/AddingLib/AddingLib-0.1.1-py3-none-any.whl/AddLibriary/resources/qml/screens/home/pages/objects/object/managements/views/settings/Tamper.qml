import "qrc:/resources/qml/components/911/DS3" as DS3

DS3.InfoTitle {
    property bool isBad: device.tampered == 1

    atomTitle {
        title: tr.lid_state
        subtitle: {
            if (device.tampered == "N/A") {
                return tr.na
            }
            if (device.tampered == 0) {
                return tr.closed
            }
            return tr.opened
        }
    }
    leftIcon.source: "qrc:/resources/images/Athena/views_icons/Lid-M.svg"
    status: isBad ? ui.ds3.status.ATTENTION : ui.ds3.status.DEFAULT
}
