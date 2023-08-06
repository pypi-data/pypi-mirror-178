import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.SettingsSwitch {
    visible: hub.firmware_version_dec >= 206000 && hub.firmware_version_dec < 211100 && (alarmDelaySeconds.value || armDelaySeconds.value) && partialArm.checked
    title: tr.applyTimeoutsToPerimeter
    checked: device.apply_timeouts_to_perimeter
}