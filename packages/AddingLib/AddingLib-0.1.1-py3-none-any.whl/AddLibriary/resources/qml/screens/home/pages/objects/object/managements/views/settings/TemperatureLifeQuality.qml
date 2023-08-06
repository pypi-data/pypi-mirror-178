import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.InfoTitle {
    property string colorStatus: device.temperature_color_status

    atomTitle {
        title: tr.temperature
        subtitle: device.is_temperature_and_humidity_sensor_broken
            ? tr.malfunction
            : device.is_in_waiting_for_data
                ? tr.na
                : temperature_converter.new(
                    device.actual_temperature, "metric", 1
                ).convert("auto").addSign().addUnit().value
    }
    leftIcon.source: "qrc:/resources/images/Athena/views_icons/Temperature-M.svg"
    status: ui.ds3.status[colorStatus] || ui.ds3.status.DEFAULT
}