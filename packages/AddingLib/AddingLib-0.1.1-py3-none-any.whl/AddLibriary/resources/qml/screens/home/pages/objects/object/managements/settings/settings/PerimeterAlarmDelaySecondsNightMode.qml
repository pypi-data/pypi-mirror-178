import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.SettingsSliderValue {
    title: tr.delay_when_entering_in_night_mode_sec
    value: device.perimeter_alarm_delay_seconds
    from: 0
    to: 120
    stepSize: 5
    doubleStepSizeFrom: 30
    suffix: tr.sec
    visible: hub.firmware_version_dec >= 211100 && partialArm.checked
}