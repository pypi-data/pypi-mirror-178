import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS3" as DS3
import "qrc:/resources/js/images.js" as Images


DS3.DeviceSelectionMulti {
    Component.onCompleted: {
        if (scenario && scenario.get_checked_target(device.obj_type, device.device_id).length) {
            selectedDevices[device.id] = {"device": device}
            selectedDevicesChanged()
        }
    }

    width: parent.width

    checked: !!selectedDevices[device.id]

    imageSource: {
        // handles the cases of different wired devices that are not just a set of color and id
        switch(device.obj_type) {
            // handling different WireInputs
            case "26":
                return Images.get_image(device.input_is_tamper == 1 ? "26-wired-tamper" : "26-wired-intrusion", "Medium", "")
            // handling different YavirAccessControls
            case "28":
                let yavir_keyboard_types = new Map([
                    [0, "28"],
                    [1, "28-keypad-yavir"],
                    [2, "28-reader-yavir"],
                ])
                return Images.get_image(yavir_keyboard_types.get(device.device_type), "Medium", "")
            // handling different WireInputMTs
            case "1d":
                return Images.get_image(device.obj_type, "Medium", device.input_type, device.custom_alarm)
            // handling different Sockets
            case "4c":
                return Images.get_image(device.obj_type, "Medium", device.color, "0", device.subtype)
            // handling different Light Switches
            case "44":
                return Images.get_image(device.obj_type, "Medium", device.color, "0", device.subtype)
        }
    }

    deviceImage.width: 40
    deviceImage.height: 40

    atomTitle{
        title: device.name
        subtitle: util.insert(tr.device_index_911, [device.device_index])
    }
    isOnline: device.online
    deviceType: device.obj_type
    deviceColor: {
        if (device.obj_type == "26") {
            return ""
        }
        if (device.obj_type == "1d") {
            return device.custom_alarm
        }
        return device.color
    }

    clickedArea.onClicked: {
        if (!checked) {
            selectedDevices[device.id] = {"device": device}
        } else {
            delete selectedDevices[device.id]
        }
        selectedDevicesChanged()
    }
}
