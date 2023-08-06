import "qrc:/resources/qml/components/911/DS3" as DS3

DS3.InfoTitle {
    visible: {
        if (!device.nfc_enabled && !device.ble_enabled) return false
        if (hub.groups_enabled) return groups.get_index(device) != -1
        return true
    }
    atomTitle {
        title: tr.arm_inversion
        subtitle: device.arm_inversion ? tr.on : tr.off
    }
    leftIcon.source: "qrc:/resources/images/Athena/views_icons/EasyArmedMode-M.svg"
}