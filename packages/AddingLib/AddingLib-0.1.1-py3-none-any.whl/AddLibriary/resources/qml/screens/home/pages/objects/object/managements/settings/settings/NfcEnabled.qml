import "qrc:/resources/qml/components/911/DS3" as DS3
import "qrc:/resources/js/desktop/popups.js" as DesktopPopups


DS3.SettingsSwitch {
    title: tr.nfc_enabled
    checked: device.nfc_enabled

    onSwitched: () => {
        checked = !checked

        if (checked) {
            DesktopPopups.text_popup(tr.keypad_settings_enable_nfc, tr.keypad_settings_enable_nfc_info)
        }
    }
}