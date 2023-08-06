import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.InfoTitle {
    property bool isBad: device.temperature_alarm == 1

    visible: device.temperature_alarm_enable
    atomTitle {
        title: tr.temperature_alarm_state
        subtitle: {
            if (device.temperature_alarm == "N/A") return tr.na
            return device.temperature_alarm == 1 ? tr.alert : tr.no
        }
    }
    leftIcon.source: "qrc:/resources/images/Athena/views_icons/TemperatureAlarm-M.svg"
    status: isBad ? ui.ds3.status.ATTENTION : ui.ds3.status.DEFAULT
}