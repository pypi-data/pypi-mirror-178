import "qrc:/resources/qml/components/911/DS3" as DS3
import "qrc:/resources/qml/components/911/DS3/popups" as DS3Popups


DS3.InfoFooter {
    title.text: device.info_name
    subtitleUpper.text: {
        var hardware_version = "Hardware " + device.hardware_version + ", "
        var firmware_version_number = device.hub_type != "YAVIR" ? (device.RR || tr.na) + " " : ""
        var firmware_version = "Firmware " + firmware_version_number + "v" + device.firmware_version + ","
        return hardware_version + firmware_version
    }
    subtitleLower {
        text: `ID  <a
                href="#" style="text-decoration:none; color:${
                    !!subtitleLower.hoveredLink ? ui.ds3.figure.base : ui.ds3.figure.secondary
                }">
                    ${device.hub_id.toUpperCase()}
                </a>`
        onLinkActivated: () => {
            util.set_clipboard_text(device.hub_id)
            popupCopy.text = `${device.hub_id} ${tr.copied}`
            popupCopy.open()
        }
    }

    DS3Popups.PopupCopy {
        id: popupCopy
    }
}