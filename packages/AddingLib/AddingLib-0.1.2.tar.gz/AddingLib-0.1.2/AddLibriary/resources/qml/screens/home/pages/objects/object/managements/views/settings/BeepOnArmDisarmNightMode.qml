import "qrc:/resources/qml/components/911/DS3/" as DS3


DS3.InfoTitle {
    visible: hub.firmware_version_dec > 211100
    atomTitle {
        title: tr.beep_when_arming_disarming_in_night_mode
        subtitle: device.beep_on_arm_disarm_v2.includes("BEEP_ON_NIGHT_ARM") || device.beep_on_arm_disarm_v2.includes("BEEP_ON_NIGHT_DISARM") ?
            tr.yes :
            tr.no
    }
    leftIcon.source: "qrc:/resources/images/Athena/views_icons/BeepWhenArmingDisarmingNightMode-M.svg"
}