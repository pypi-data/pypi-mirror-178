import "qrc:/resources/qml/components/911/DS3/" as DS3


DS3.SettingsSwitch {
    visible: externalContact.checked
    title: tr.if_external_contact_opened
    checked: {
        if (["04", "64"].includes(device.obj_type)) return device.siren_triggers.includes(1) // Glass
        if (["01", "0f", "61", "6f"].includes(device.obj_type)) return device.siren_triggers.includes(2) // Door
    }
}