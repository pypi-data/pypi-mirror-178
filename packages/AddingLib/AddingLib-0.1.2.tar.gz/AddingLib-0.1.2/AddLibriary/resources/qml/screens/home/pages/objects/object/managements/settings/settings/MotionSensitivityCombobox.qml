import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.SettingsPickerTitleSecondary {
    currentIndex: device.sensitivity
    model: [tr.low, tr.normal, tr.high]
    atomTitle.title: ["08", "68"].includes(device.obj_type) ?
        tr.motion_sensor_sensitivity :
        tr.sensitivity
}