import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.InfoTitle {
    visible: device.gb_allowed
    atomTitle {
        title: tr.glass_shutter_protection_always_active
        subtitle: device.gb_always_active ? tr.yes : tr.no
    }
    leftIcon.source: "qrc:/resources/images/Athena/views_icons/AlwaysActive-M.svg"
}