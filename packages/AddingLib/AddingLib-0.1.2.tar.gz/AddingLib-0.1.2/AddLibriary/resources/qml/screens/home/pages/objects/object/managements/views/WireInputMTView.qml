import "qrc:/resources/qml/screens/home/pages/objects/object/managements/views/settings/" as Settings
import "qrc:/resources/qml/screens/home/pages/objects/object/managements/views/parts" as ViewsParts


ViewsParts.DeviceViewForRedesign {
    Settings.MalfunctionBadResistance {}
    Settings.DataImport {}
    Settings.DelayWhenEntering {}
    Settings.DelayWhenLeaving {}
    Settings.DelayWhenEnteringNightMode {}
    Settings.DelayWhenLeavingNightMode {}
    Settings.Tamper { visible: device.input_type == 2 }
    Settings.AssignedMTRObject {}
    Settings.ExternalSensorState {
        visible: device.input_type == 1 && device.external_contact_alarm_mode == 1
        isBad: device.external_contact_state == "CONTACT_DISRUPTED" || ['CONTACT_DISRUPTION_BROKEN'].includes(device.external_contact_broken)
        atomTitle.subtitle: {
            if (['CONTACT_DISRUPTION_BROKEN'].includes(device.external_contact_broken)) return tr.shorted_out_or_sabotage
            return {'NO_EXTERNAL_CONTACT_STATE': tr.na, 'CONTACT_NOT_AVAILABLE': tr.na, 'CONTACT_NORMAL': tr.ok}[device.external_contact_state_S2] || tr.alert
        }
    }
    Settings.AlwaysActive { visible: device.input_type == 1 }
    Settings.TemporaryDeactivation {}
}
