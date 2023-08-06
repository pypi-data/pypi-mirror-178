import "qrc:/resources/qml/components/911/DS3/" as DS3


DS3.InfoTitle {
    atomTitle {
        title: tr.active
        subtitle: {
            if (device.real_state.includes("NO_SWITCH_STATE_INFO")) {
                return tr.na
            }
            return device.real_state.includes("SWITCHED_OFF") ? tr.no : tr.yes
        }
    }
    leftIcon.source: "qrc:/resources/images/Athena/views_icons/SwitchOn-M.svg"
}