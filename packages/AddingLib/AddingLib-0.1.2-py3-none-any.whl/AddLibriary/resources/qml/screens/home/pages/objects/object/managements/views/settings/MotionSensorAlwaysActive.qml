import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.InfoTitle {
    visible: device.motion_allowed
    atomTitle {
        title: tr.motion_sensor_always_active
        subtitle: device.motion_sensor_always_active ? tr.yes : tr.no
    }
    leftIcon.source: "qrc:/resources/images/Athena/views_icons/AlwaysActive-M.svg"
}