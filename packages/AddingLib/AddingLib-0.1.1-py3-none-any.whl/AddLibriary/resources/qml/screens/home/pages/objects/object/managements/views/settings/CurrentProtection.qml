import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.InfoTitle {
    atomTitle {
        title: tr.current_protection
        subtitle: device.current_protection ? tr.on : tr.off
    }
    leftIcon.source: "qrc:/resources/images/Athena/views_icons/CurrentProtection-M.svg"
}
