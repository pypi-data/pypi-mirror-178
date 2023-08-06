import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.InfoTitle {
    atomTitle {
        title: tr.lock_switch_buttons_title
        subtitle: device.child_lock_enabled ? tr.yes : tr.no
    }
    leftIcon.source: "qrc:/resources/images/Athena/views_icons/LsBlocking-M.svg"
}