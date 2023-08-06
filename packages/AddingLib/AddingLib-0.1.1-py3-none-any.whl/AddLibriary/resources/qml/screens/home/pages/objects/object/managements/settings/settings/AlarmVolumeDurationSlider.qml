import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.SettingsSliderValue {
    value: ["14", "15", "1b", "74", "75", "7b", "27"].includes(device.obj_type) ? device.alarm_duration: device.time_to_act_seconds
    title: tr.alarm_duration
    from: 3
    to: device.is_extended_siren_alarm_periods_available ?
        900 :
        180
    stepSize: 3
    doubleStepSizeFrom: device.is_extended_siren_alarm_periods_available ?
        180 :
        30
    doubleStepMultiplicator: device.is_extended_siren_alarm_periods_available ?
        10 :
        2
}