import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.InfoTitle {
    property string colorStatus: device.co2_color_status

    atomTitle {
        title: tr.co_level_lq_value
        subtitle: device.is_co2_sensor_broken
            ? tr.malfunction
            : device.is_in_waiting_for_data
                ? tr.na
                : `${device.actual_co2} ${tr.ppm_co_level_value}`
    }
    leftIcon.source: "qrc:/resources/images/Athena/common_icons/CO2-M.svg"
    status: ui.ds3.status[colorStatus] || ui.ds3.status.DEFAULT
}