import "qrc:/resources/qml/components/911/DS3/" as DS3
import "qrc:/resources/js/desktop/popups.js" as DesktopPopups


DS3.InfoTitleButtonIcon {
    visible: !device.has_same_version_as_hub
    atomTitle.title: tr.some_devices_not_PD_certified
    status: ui.ds3.status.WARNING
    leftIcon.source: "qrc:/resources/images/Athena/views_icons/Warning-M.svg"
    buttonIcon {
        source: "qrc:/resources/images/Athena/views_icons/Info-M.svg"
        color: ui.ds3.figure.warningContrast
    }

    onRightControlClicked: {
        DesktopPopups.error_popup(tr.rex_fw_not_match_with_hub_fw)
    }
}
