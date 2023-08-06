import "qrc:/resources/qml/components/911/DS3/" as DS3


DS3.InfoTitle {
    atomTitle {
        title: tr.beep_when_arming_disarming
        subtitle: {
            if (hub.firmware_version_dec > 211100) {
                device.beep_on_arm_disarm_v2.includes("BEEP_ON_ARM") || device.beep_on_arm_disarm_v2.includes("BEEP_ON_DISARM") ? tr.yes : tr.no
            } else {
                device.act_on_arming ? tr.yes : tr.no
            }
        }
    }
    leftIcon.source: "qrc:/resources/images/Athena/views_icons/BeepWhenArmingDisarming-M.svg"
}
