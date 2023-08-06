import "qrc:/resources/qml/components/911/DS3" as DS3

DS3.InfoTitle {
    property string extContactState: {
        return {
            'NO_EXTERNAL_CONTACT_STATE': tr.na,
            'CONTACT_NOT_AVAILABLE': tr.na,
            'CONTACT_NORMAL': tr.ok
        }[device.external_contact_state_S2] || tr.alert
    }

    property string extContactBroken: {
        ['CONTACT_DISRUPTION_BROKEN'].includes(device.external_contact_broken) && device.sensor_type === "EOL"
            ? tr.shorted_out_or_sabotage
            : ""
    }

    property bool isBad: !['NO_EXTERNAL_CONTACT_STATE', 'CONTACT_NOT_AVAILABLE', 'CONTACT_NORMAL'].includes(device.external_contact_state_S2) ||
        ['CONTACT_DISRUPTION_BROKEN'].includes(device.external_contact_broken)

    visible: ["EOL", "WITHOUT_EOL"].includes(device.sensor_type)
    atomTitle {
        title: tr.sensor_state
        subtitle: {
            if (extContactState === tr.alert && extContactBroken === tr.shorted_out_or_sabotage) return extContactState + ", " + extContactBroken
            if (extContactState && extContactBroken) return extContactBroken
            return extContactState
        }
    }
    leftIcon.source: "qrc:/resources/images/Athena/views_icons/ExternalContact-M.svg"
    status: isBad ? ui.ds3.status.ATTENTION : ui.ds3.status.DEFAULT
}
