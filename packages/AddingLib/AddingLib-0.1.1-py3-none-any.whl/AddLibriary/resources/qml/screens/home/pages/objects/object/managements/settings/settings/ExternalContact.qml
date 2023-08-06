import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.SettingsSwitch {
    width: parent.width

    checked: device.extra_contact_aware
    title: tr.external_contact
}