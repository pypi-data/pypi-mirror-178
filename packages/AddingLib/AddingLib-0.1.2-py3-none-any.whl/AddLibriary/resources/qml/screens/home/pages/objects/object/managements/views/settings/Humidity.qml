import "qrc:/resources/qml/components/911/DS3" as DS3

DS3.InfoTitle {
    property string colorStatus: device.humidity_color_status

    atomTitle {
        title: tr.humidity_lq_value
        subtitle: device.is_temperature_and_humidity_sensor_broken
            ? tr.malfunction
            : device.is_in_waiting_for_data
                ? tr.na
                : `${device.actual_humidity}%`
    }
    leftIcon.source: "qrc:/resources/images/Athena/common_icons/Humidity-M.svg"
    status: ui.ds3.status[colorStatus] || ui.ds3.status.DEFAULT
}