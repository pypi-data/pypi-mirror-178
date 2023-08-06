import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.InfoTitle {
    property bool isBad: device.external_power == 0 && !["13", "14", "74", "1b"].includes(device.obj_type)

    atomTitle {
        title: tr.external_power
        subtitle: {
            return {
                "-1": tr.na,
                "0": tr.disconnected,
                "1": tr.connected,
            }[device.external_power]
        }
    }
    leftIcon.source: "qrc:/resources/images/Athena/views_icons/ExternalPower-M.svg"
    status: isBad ? ui.ds3.status.ATTENTION : ui.ds3.status.DEFAULT
}
