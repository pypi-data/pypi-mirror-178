import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.InfoTitle {
    atomTitle {
        title: tr.tilt_sensor
        subtitle: device.accel_aware ? tr.enabled : tr.off
    }

    leftIcon.source: "qrc:/resources/images/Athena/views_icons/TiltSensor-M.svg"
}