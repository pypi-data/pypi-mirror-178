import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.InfoTitle {
    atomTitle {
        title: tr.shock_sensor
        subtitle: device.shock_sensor_aware ? tr.enabled : tr.off
    }

    leftIcon.source: "qrc:/resources/images/Athena/views_icons/ShockSensor-M.svg"
}