import "qrc:/resources/qml/components/911/DS3" as DS3
import "qrc:/resources/js/desktop/popups.js" as DesktopPopups


DS3.SettingsNavigationTitlePrimary {
    title: tr.duress_code

    onEntered: DesktopPopups.popupByPath(
        "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/ChangeKeyPadPassword.qml",
        {"force": true, "device": device}
    )
}