import "qrc:/resources/qml/components/911/DS3" as DS3

DS3.InfoTitle {
    atomTitle {
        title: tr.connection_state
        subtitle: {
            return {
                "-1": tr.na,
                "0": tr.offline,
                "1": tr.online,
            }[device.devOnline]
        }
    }
    leftIcon.source: "qrc:/resources/images/Athena/views_icons/Wires-M.svg"
    status: device.devOnline == 0 ? ui.ds3.status.ATTENTION : ui.ds3.status.DEFAULT
}