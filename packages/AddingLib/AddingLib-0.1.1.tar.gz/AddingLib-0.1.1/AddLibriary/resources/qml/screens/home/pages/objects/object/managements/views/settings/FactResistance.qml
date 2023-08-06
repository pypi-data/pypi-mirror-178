import "qrc:/resources/qml/components/911/DS3" as DS3

DS3.InfoTitle {
    visible: ['EOL', 'TWO_EOL', 'THREE_EOL'].includes(device.sensor_type)
    atomTitle {
        title: tr.device_average_resistance
        subtitle: device.fact_resistance > 45 ? '>45' + tr.resistance_value : device.fact_resistance + tr.resistance_value
    }
    leftIcon.source: "qrc:/resources/images/Athena/views_icons/WireResistance-M.svg"
    status: ui.ds3.status.DEFAULT
}
