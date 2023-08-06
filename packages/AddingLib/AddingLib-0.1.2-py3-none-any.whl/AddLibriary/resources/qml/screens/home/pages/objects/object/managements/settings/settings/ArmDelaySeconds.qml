import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.SettingsSliderValue {
    title: tr.delay_when_leaving_sec
    value: device.arm_delay_seconds
    from: 0
    to: 120
    stepSize: 5
    doubleStepSizeFrom: 30
    suffix: tr.sec
    visible: hub.is_arm_alarm_delays_available
}