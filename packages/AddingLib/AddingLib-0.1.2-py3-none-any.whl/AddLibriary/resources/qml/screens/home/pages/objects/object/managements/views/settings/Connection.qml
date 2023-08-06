import "qrc:/resources/qml/components/911/DS3" as DS3

DS3.InfoTitle {
    atomTitle {
        title: device.is_fibra ?
            tr.fibra_connection_state :
            tr.jeweller_connection_state
        subtitle: {
            return {
                "-1": tr.na,
                "0": tr.offline,
                "1": tr.online,
            }[device.devOnline]
        }
    }
    leftIcon.source: device.is_fibra ?
        "qrc:/resources/images/Athena/views_icons/Fibra-M.svg" :
        "qrc:/resources/images/Athena/views_icons/Jeweller-M.svg"
    status: device.devOnline == 0 ? ui.ds3.status.ATTENTION : ui.ds3.status.DEFAULT
}