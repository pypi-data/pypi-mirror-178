import "qrc:/resources/qml/components/911/DS3/" as DS3


DS3.InfoTitle {
    visible: hub.chimes_available && device.chime_play_available
    atomTitle {
        title: tr.chime_play
        subtitle: device.chimes_enabled ? tr.yes : tr.no
    }
    leftIcon.source: "qrc:/resources/images/Athena/views_icons/Bell-M.svg"
}
