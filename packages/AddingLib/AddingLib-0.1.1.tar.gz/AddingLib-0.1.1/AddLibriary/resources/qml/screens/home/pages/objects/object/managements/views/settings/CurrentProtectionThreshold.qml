import "qrc:/resources/qml/components/911/DS3/" as DS3


DS3.InfoTitle {
    atomTitle {
        title: tr.current_protection_threshold
        subtitle: device.current_protection_threshold + " A"
    }
    leftIcon.source: "qrc:/resources/images/Athena/views_icons/CurrentProtection-M.svg"
}
