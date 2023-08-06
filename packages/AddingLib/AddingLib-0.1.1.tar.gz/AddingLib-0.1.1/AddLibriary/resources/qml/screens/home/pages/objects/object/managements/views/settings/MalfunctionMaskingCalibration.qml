import "qrc:/resources/qml/components/911/DS3/" as DS3
import "qrc:/resources/js/desktop/popups.js" as DesktopPopups


DS3.InfoTitleButtonIcon {
    visible: device.malfunctions.length > 0 && device.malfunctions.includes("SMOKE_DETECTOR_CAMERA_MALFUNCTION")
    atomTitle.title: tr.malfunctions
    leftIcon.source: "qrc:/resources/images/Athena/views_icons/Warning-M.svg"
    status: ui.ds3.status.ATTENTION
    buttonIcon {
        source: "qrc:/resources/images/Athena/views_icons/Info-M.svg"

        onClicked: {
            DesktopPopups.error_popup(device.malfunctions.includes("SMOKE_DETECTOR_CAMERA_MALFUNCTION") ? tr.malfunction_5_antimasking : "")
        }
    }
}