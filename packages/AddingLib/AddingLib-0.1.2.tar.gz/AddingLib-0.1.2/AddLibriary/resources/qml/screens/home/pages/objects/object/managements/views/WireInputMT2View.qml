import "qrc:/resources/qml/screens/home/pages/objects/object/managements/views/settings/" as Settings
import "qrc:/resources/qml/screens/home/pages/objects/object/managements/views/parts" as ViewsParts
import "qrc:/resources/js/desktop/popups.js" as DesktopPopups


ViewsParts.DeviceViewForRedesign {
    property var wireInputSensorIconsMapper: {
        "BURGLARY_ALARM": "qrc:/resources/images/Athena/views_icons/WIIntrusion-M.svg",
        "FIRE_ALARM": "qrc:/resources/images/Athena/views_icons/WIFire-M.svg",
        "MEDICAL_ALARM": "qrc:/resources/images/Athena/views_icons/WIMedicalHelp-M.svg",
        "PANIC_ALARM": "qrc:/resources/images/Athena/views_icons/WIAlarm-M.svg",
        "GAS_ALARM": "qrc:/resources/images/Athena/views_icons/WIGasAlarm-M.svg",
        "TAMPER_ALARM": "qrc:/resources/images/Athena/views_icons/WITamper-M.svg",
        "MALFUNCTION_ALARM": "qrc:/resources/images/Athena/views_icons/WIMalfunction-M.svg",
        "LEAK_ALARM": "qrc:/resources/images/Athena/views_icons/WILeakage-M.svg",
        "SERVICE_EVENT": "qrc:/resources/images/Athena/views_icons/WIInfo-M.svg"
    }
    property var sensorTypeMapper: {
        "BURGLARY_ALARM": tr.intrusion_sensor,
        "FIRE_ALARM": tr.fire_sensor,
        "MEDICAL_ALARM": tr.med_help_sensor,
        "PANIC_ALARM": tr.panic_sensor,
        "GAS_ALARM": tr.gas_sensor,
        "TAMPER_ALARM": tr.tamper_sensor,
        "MALFUNCTION_ALARM": tr.malf_sensor,
        "LEAK_ALARM": tr.leakage_sensor,
        "SERVICE_EVENT": tr.custom_sensor
    }
    property var alwaysActiveSensorMapper: {
        "BURGLARY_ALARM": tr.intrusion_sensor_always_active,
        "FIRE_ALARM": tr.fire_sensor_always_active,
        "MEDICAL_ALARM": tr.medical_sensor_always_active,
        "PANIC_ALARM": tr.panic_sensor_always_active,
        "GAS_ALARM": tr.gas_sensor_always_active,
        "TAMPER_ALARM": tr.tamper_sensor_always_active,
        "MALFUNCTION_ALARM": tr.malf_sensor_always_active,
        "LEAK_ALARM": tr.leakage_sensor_always_active,
        "SERVICE_EVENT": tr.custom_sensor_always_active
    }

    Settings.MalfunctionBadResistance {}
    Settings.DataImport {}
    Settings.DelayWhenEntering {}
    Settings.DelayWhenLeaving {}
    Settings.DelayWhenEnteringNightMode {}
    Settings.DelayWhenLeavingNightMode {}
    Settings.AssignedMTRObject {}
    Settings.OneEOLDeviceState {}
    Settings.WIMT2DeviceState {}
    Settings.WIFirstSensor {
        iconsWrapper: wireInputSensorIconsMapper
        typeMapper: sensorTypeMapper
    }
    Settings.WISecondSensor {
        iconsWrapper: wireInputSensorIconsMapper
        typeMapper: sensorTypeMapper
    }
    Settings.WIThirdSensor {
        iconsWrapper: wireInputSensorIconsMapper
        typeMapper: sensorTypeMapper
    }
    Settings.AlwaysActive {
        atomTitle.subtitle: {
            if (['WITHOUT_EOL', 'EOL'].includes(device.sensor_type)) {
                return device.always_active_S2 ? tr.yes : tr.no
            } else if ('TWO_EOL' == device.sensor_type) {
                if (device.always_active_S1 && device.always_active_S2) {return tr.all_sensors}
                if (device.always_active_S1) return alwaysActiveSensorMapper[device.custom_alarm_S1]
                if (device.always_active_S2) return alwaysActiveSensorMapper[device.custom_alarm_S2]
                return tr.no
            } else if ('THREE_EOL' == device.sensor_type) {
                if (device.always_active_S1 && device.always_active_S2 && device.always_active_S3) {return tr.all_sensors}
                let sensors = []
                if (device.always_active_S1) { sensors.push(alwaysActiveSensorMapper[device.custom_alarm_S1])}
                if (device.always_active_S2) { sensors.push(alwaysActiveSensorMapper[device.custom_alarm_S2])}
                if (device.always_active_S3) { sensors.push(alwaysActiveSensorMapper[device.custom_alarm_S3])}
                if (sensors.length > 0) {return sensors.join(', ')}
                return tr.no
            } else tr.no
        }
    }
    Settings.FactResistance {}
    Settings.TemporaryDeactivation {}
}
