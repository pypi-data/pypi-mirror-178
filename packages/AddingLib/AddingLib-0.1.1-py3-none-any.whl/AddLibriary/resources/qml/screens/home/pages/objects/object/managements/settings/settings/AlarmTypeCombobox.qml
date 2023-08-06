import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.SettingsPickerTitleSecondary {
    visible: device.obj_type == "0c" ?
        device.custom_alarm_available && buttonModeCombobox.currentIndex == 0 :
        device.custom_alarm_available
    atomTitle.title: tr.alarm_type
    model: device.custom_alarm_available_v2 ?
        [tr.burglary_alarm, tr.fire_alarm, tr.medical_alarm, tr.panic_alarm, tr.gas_alarm,
        tr.malfunction, tr.leakage_alarm, tr.custom_not_alarm_mtr] :
        [tr.burglary_alarm, tr.fire_alarm, tr.medical_alarm, tr.panic_alarm, tr.gas_alarm]
    currentIndex: ({
        "NO_CUSTOM_ALARM_TYPE": -1,
        "BURGLARY": 0,
        "FIRE": 1,
        "MEDICAL": 2,
        "PANIC": 3,
        "GAS": 4,
        "MALFUNCTION": 5,
        "LEAK": 6,
        "SERVICE": 7,
    }[device.custom_alarm_type])
    commentText: ["0c", "11"].includes(device.obj_type) ? tr.custom_event_descr : null
}