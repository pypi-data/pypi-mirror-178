import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.InfoTitle {
    atomTitle {
        title: tr.alert_if_moved
        subtitle: device.is_acceleration_aware ? tr.yes : tr.no
    }
    leftIcon.source: "qrc:/resources/images/Athena/views_icons/AlertIfMoved-M.svg"
}
