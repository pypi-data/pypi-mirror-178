import "qrc:/resources/qml/components/911/DS3" as DS3
import "qrc:/resources/qml/components/911/DS3/popups" as DS3Popups


DS3.InfoFooter {
    title.text: device.info_name
    subtitleUpper {
        text: {
            var device_qr = device.input_index.toString().substring(0, 2)
            return `${tr.input_for_multitransmitter} <a
                href="#" style="text-decoration:none; color:${
                    !!subtitleUpper.hoveredLink ? ui.ds3.figure.base : ui.ds3.figure.secondary
                }">
                    ${device_qr}
                </a>`
        }

        onLinkActivated: {
            var deviceIdCleaned = device.device_id.slice(0, 2) == "00" ?  device.device_id.slice(2) : device.device_id
            var deviceId = deviceIdCleaned + device.obj_type + (device.input_type == "TAMPER" ? "2" : "1")
            util.set_clipboard_text(deviceId)
            popupCopy.text = `${deviceId} ${tr.copied}`
            popupCopy.open()
        }
    }

    subtitleLower {
        text: util.insert(tr.device_index_911, [device.device_index])
    }

    DS3Popups.PopupCopy {
        id: popupCopy
    }
}
