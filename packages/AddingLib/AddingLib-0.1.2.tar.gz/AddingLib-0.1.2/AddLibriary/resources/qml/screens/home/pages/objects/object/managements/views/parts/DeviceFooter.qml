import "qrc:/resources/qml/components/911/DS3" as DS3
import "qrc:/resources/qml/components/911/DS3/popups" as DS3Popups


DS3.InfoFooter {
    property var showBusNumber: device.class_name.endsWith("fibra")
    property var customDeviceIndexForSpaceControl: {
        if (device.obj_type == "0b") {
            if (device.associated_user_id != "00000000") {
                var user = management.users.get_user(device.associated_user_id)
                return user === null ? device.device_index : user.index
            }
        }
        return device.device_index
    }
    property var deviceColorNumber: {
        if (!device || !device.color || device.obj_type == "44") return "0"
        if (device.color == "WHITE") return "1"
        if (device.color == "BLACK") return "2"
        if (device.color == "WHITE_LABEL_WHITE") return "3"
        if (device.color == "WHITE_LABEL_BLACK") return "4"
        return "0"
    }

    title.text: device.info_name
    subtitleUpper {
        visible: device.obj_type != "2e"
        text: {
            var RR = device.RR || tr.na
            var deviceIdCleaned = device.device_id.slice(0, 2) == "00" ?  device.device_id.slice(2) : device.device_id
            var device_qr = (deviceIdCleaned + device.obj_type + deviceColorNumber).toUpperCase()

            return `FW ${RR} v${device.firmware_version}, Device ID <a
                href="#" style="text-decoration:none; color:${
                    !!subtitleUpper.hoveredLink ? ui.ds3.figure.base : ui.ds3.figure.secondary
                }">
                    ${device_qr}
                </a>`
        }
        onLinkActivated: () => {
            let lastCharacter = "0"
            if (device.obj_type != "44") {
                lastCharacter = device.color == "WHITE" ? "1" : "2"
            }
            var deviceIdCleaned = device.device_id.slice(0, 2) == "00" ?  device.device_id.slice(2) : device.device_id
            var deviceId = deviceIdCleaned + device.obj_type + lastCharacter
            util.set_clipboard_text(deviceId)
            popupCopy.text = `${deviceId} ${tr.copied}`
            popupCopy.open()
        }
    }
    subtitleLower {
        text: {
            var bus_number = ""
            if (showBusNumber) {
                bus_number = device.bus_number == "N/A" ? tr.na : device.bus_number
                bus_number = "<br>" + util.insert(tr.bus_num_desktop, [bus_number])
            }
            return util.insert(tr.device_index_911, [customDeviceIndexForSpaceControl]) + bus_number
        }
    }

    DS3Popups.PopupCopy {
        id: popupCopy
    }
}