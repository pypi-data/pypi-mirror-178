import "qrc:/resources/qml/components/911/DS3/" as DS3
import "qrc:/resources/js/desktop/popups.js" as DesktopPopups


DS3.InfoTitleButtonIcon {
    visible: device.malfunctions && device.malfunctions.length > 0
    atomTitle.title: tr.malfunctions
    leftIcon.source: "qrc:/resources/images/Athena/views_icons/Warning-M.svg"
    status: ui.ds3.status.ATTENTION
    buttonIcon.source: "qrc:/resources/images/Athena/views_icons/Info-M.svg"

    onRightControlClicked: {
        let out = []

        if (device.malfunctions.includes("BAD_INPUT_RESISTANCE")) {
            out.push(tr.malfunction_8)
        }

        DesktopPopups.error_popup(out.join("\n"))
    }
}