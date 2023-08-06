import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.InfoTitle {
    visible: device.high_diff == "1"
    atomTitle {
        title: tr.rapid_temperature_rise
        subtitle: tr.alert
    }
    leftIcon.source: "qrc:/resources/images/Athena/views_icons/TemperatureRiseAlert-M.svg"
    status: ui.ds3.status.ATTENTION
}