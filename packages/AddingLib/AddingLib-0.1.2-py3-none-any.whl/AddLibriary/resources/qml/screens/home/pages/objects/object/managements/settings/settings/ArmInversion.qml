import "qrc:/resources/qml/components/911/DS3/" as DS3
import "qrc:/resources/js/desktop/popups.js" as DesktopPopups


DS3.SettingsSwitch {
    visible: (!hub.groups_enabled || groupAssociatedCombobox.currentIndex) && nfcEnabled.checked
    title: hub.groups_enabled ? tr.arm_inversion_groups : tr.arm_inversion
    checked: device.arm_inversion

    onSwitched: () => {
        if (!checked) {
            DesktopPopups.popupByPath("qrc:/resources/qml/components/911/DS3/popups/Dialog.qml", {
                title: tr.information,
                text: hub.groups_enabled ? tr.arm_inversion_groups_info : tr.arm_inversion_info,
            })
        }
        checked = !checked
    }
}