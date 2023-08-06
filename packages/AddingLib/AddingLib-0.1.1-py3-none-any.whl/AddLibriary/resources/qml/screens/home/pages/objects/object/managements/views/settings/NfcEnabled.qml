import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.InfoTitle {
    atomTitle {
        title: tr.nfc_enabled
        subtitle: device.nfc_enabled ? tr.on : tr.off
    }
    leftIcon.source: "qrc:/resources/images/Athena/views_icons/PassTagReading-M.svg"
}
