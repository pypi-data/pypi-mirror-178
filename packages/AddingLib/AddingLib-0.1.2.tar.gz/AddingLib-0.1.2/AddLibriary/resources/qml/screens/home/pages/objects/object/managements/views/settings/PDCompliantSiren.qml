import "qrc:/resources/qml/components/911/DS3/" as DS3
import "qrc:/resources/js/desktop/popups.js" as DesktopPopups


DS3.InfoTitleButtonIcon {
    visible: hub.two_stage_arming_state && !device.pd_available
    atomTitle.title: tr.some_devices_not_PD_certified
    leftIcon.source: "qrc:/resources/images/Athena/views_icons/Pd-M.svg"
    status: ui.ds3.status.WARNING
    buttonIcon.source: "qrc:/resources/images/Athena/views_icons/Info-M.svg"

    onRightControlClicked: {
        DesktopPopups.error_popup(tr.devices_not_PD_certified_tip)
    }
}