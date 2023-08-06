import "qrc:/resources/qml/components/911/DS3" as DS3

DS3.InfoTitle {
    property var iconsWrapper: ({})
    property var typeMapper: ({})
    property bool isBad: !['NO_EXTERNAL_CONTACT_STATE', 'CONTACT_NOT_AVAILABLE', 'CONTACT_NORMAL'].includes(device.external_contact_state_S3)

    visible: ["THREE_EOL"].includes(device.sensor_type)
    atomTitle {
        title: typeMapper[device.custom_alarm_S3]
        subtitle: {
            return {'NO_EXTERNAL_CONTACT_STATE': tr.na, 'CONTACT_NOT_AVAILABLE': tr.na, 'CONTACT_NORMAL': tr.ok}[device.external_contact_state_S3] || tr.alert
        }
    }
    leftIcon.source: iconsWrapper[device.custom_alarm_S3] || ""
    status: isBad ? ui.ds3.status.ATTENTION : ui.ds3.status.DEFAULT
}
