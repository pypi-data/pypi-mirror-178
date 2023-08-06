import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.SettingsPickerTitleSecondary {
    atomTitle.title: tr.alarm_type
    enabled: devEnable
    model: [
        tr.not_assigned_output,
        tr.burglary_alarm,
        tr.fire_alarm,
        tr.medical_alarm,
        tr.panic_alarm,
        tr.any_alarm,
        tr.malfunction,
        tr.lost_external_power_vhfBridge,
        tr.low_battery_vhfBridge,
        tr.lost_external_power_hub,
        tr.low_battery_hub,
        tr.lid_state,
        tr.arm_disarm_state,
        tr.confirmed_intrusion_alarm,
        tr.confirmed_hold_up_alarm,
        tr.connection_via_jeweller_lost_vhfBridge,
    ]
    currentIndex: device._get_int_alarm_type(output_number)
}