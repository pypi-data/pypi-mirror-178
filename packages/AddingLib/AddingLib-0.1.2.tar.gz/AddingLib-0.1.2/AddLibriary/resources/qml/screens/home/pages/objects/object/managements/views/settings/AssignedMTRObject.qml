import "qrc:/resources/qml/components/911/DS3" as DS3

DS3.InfoTitle {
    visible: device.assigned_mtr > 0
    atomTitle {
        title: device.assigned_mtr_object ? device.assigned_mtr_object.name : ""
        subtitle: {
            if (device.assigned_mtr_object) {
                 return device.assigned_mtr_object.online ? tr.online: tr.offline
            }
            return ""
        }
    }
    leftIcon.source: "qrc:/resources/images/Athena/views_icons/MultiTransmitter-M.svg"
    status: ui.ds3.status.DEFAULT
}
