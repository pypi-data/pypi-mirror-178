import "qrc:/resources/qml/components/911/DS3/" as DS3


DS3.InfoTitle {
    visible: hub && device.assigned_extender

    atomTitle {
        title: device.assigned_extender_name
        subtitle: device.is_assigned_extender_online ? tr.online : tr.offline
    }
    leftIcon.source: "qrc:/resources/images/Athena/views_icons/RexConnected-M.svg"
}
