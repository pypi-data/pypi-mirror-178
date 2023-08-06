import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.InfoTitle {
    atomTitle {
        title: tr.alarm_duration
        subtitle: device.time_to_act_seconds
    }
    leftIcon.source: "qrc:/resources/images/Athena/views_icons/AlarmDuration-M.svg"
}
