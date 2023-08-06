import "qrc:/resources/qml/components/911/DS3" as DS3

DS3.InfoTitle {
    visible: ['CONTACT_DISRUPTION_BROKEN'].includes(device.external_contact_broken) && ['TWO_EOL', 'THREE_EOL'].includes(device.sensor_type)
    atomTitle {
        title: tr.sensor_state
        subtitle: tr.detectors_shorted_out
    }
    leftIcon.source: "qrc:/resources/images/Athena/views_icons/ExternalContact-M.svg"
    status: ui.ds3.status.ATTENTION
}
