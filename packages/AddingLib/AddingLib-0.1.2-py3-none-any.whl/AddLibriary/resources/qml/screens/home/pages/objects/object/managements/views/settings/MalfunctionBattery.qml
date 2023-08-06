import "qrc:/resources/qml/components/911/DS3/" as DS3
import "qrc:/resources/js/desktop/popups.js" as DesktopPopups


DS3.InfoTitleButtonIcon {
    visible: device.malfunctions.length > 0 && (device.malfunctions.includes("BATTERY_MALFUNCTION") || device.malfunctions.includes("BAD_INPUT_RESISTANCE"))
    atomTitle.title: tr.malfunctions
    leftIcon.source: "qrc:/resources/images/Athena/views_icons/Warning-M.svg"
    status: ui.ds3.status.ATTENTION
    buttonIcon {
        source: "qrc:/resources/images/Athena/views_icons/Info-M.svg"

        onClicked: {
            let out = []

            if (device.malfunctions.includes("BATTERY_MALFUNCTION") ||
                    device.malfunctions.includes("BATTERY_CHARGE_ERROR")) {
                out.push(tr.malfunction_28)
            }
            if (device.malfunctions.includes("MALF_CHRG_BIT")) {
                out.push(tr.battery_is_charging_too_long)
            }
            DesktopPopups.error_popup(out.join("\n"))
        }
    }
}