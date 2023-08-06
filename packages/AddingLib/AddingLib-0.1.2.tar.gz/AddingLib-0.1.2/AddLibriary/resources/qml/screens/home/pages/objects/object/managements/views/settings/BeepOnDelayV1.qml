import "qrc:/resources/qml/components/911/DS3/" as DS3


DS3.InfoTitle {
    visible: device.beep_on_delay_available && hub.firmware_version_dec >= 205000 && hub.firmware_version_dec <= 211100
    atomTitle {
        title: tr.beep_on_delay
        subtitle: device.beep_on_delay ? tr.yes : tr.no
    }
    leftIcon.source: "qrc:/resources/images/Athena/views_icons/BeepOnExitDelay-M.svg"
}
