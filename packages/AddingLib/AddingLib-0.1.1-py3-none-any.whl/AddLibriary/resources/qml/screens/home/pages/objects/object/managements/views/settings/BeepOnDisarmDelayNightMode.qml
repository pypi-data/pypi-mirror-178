import "qrc:/resources/qml/components/911/DS3/" as DS3


DS3.InfoTitle {
    visible: hub.firmware_version_dec > 211100 && device.beep_on_delay_available
    atomTitle {
        title: tr.beep_on_entry_delay_in_night_mode_info
        subtitle: device.beep_on_delay_v2.includes("BEEP_ON_NIGHT_DISARM_DELAY") ? tr.yes : tr.no
    }
    leftIcon.source: "qrc:/resources/images/Athena/views_icons/BeepOnEntryNightModeDelay-M.svg"
}
