import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS3" as DS3
import "qrc:/resources/js/images.js" as Images


DS3.DeviceTwoLinesSelectionMulti {
    Component.onCompleted: {
        if (!scenario) return
        let checked_targets = scenario.get_checked_target(device.obj_type, device.device_id).filter(target => {
            return ["button1", "button2"].includes(target)
        })
        if (currentDevice.id == device.id && selectedButtonIndex == 0) {
            checked_targets = checked_targets.filter(button => button != "button1")
        }
        if (currentDevice.id == device.id && selectedButtonIndex == 1) {
            checked_targets = checked_targets.filter(button => button != "button2")
        }
        if (checked_targets.length) {
            selectedDevices[device.id] = {"device": device, "selected_buttons": checked_targets}
            selectedDevicesChanged()
        }
    }

    width: parent.width

    firstButtonChecked: !!selectedDevices[device.id] && selectedDevices[device.id].selected_buttons.includes("button1")
    checkItemFirstButton.enabled: currentDevice.id != device.id || selectedButtonIndex != 0
    secondButtonChecked: !!selectedDevices[device.id] && selectedDevices[device.id].selected_buttons.includes("button2")
    checkItemSecondButton.enabled: currentDevice.id != device.id || selectedButtonIndex != 1
    imageSource: {
        // handles the cases of different wired devices that are not just a set of color and id
        switch(device.obj_type) {
            // handling different WireInputs
            case "26":
                return Images.get_image(device.input_is_tamper == 1 ? "26-wired-tamper" : "26-wired-intrusion", "Small", "")
            // handling different YavirAccessControls
            case "28":
                let yavir_keyboard_types = new Map([
                    [0, "28"],
                    [1, "28-keypad-yavir"],
                    [2, "28-reader-yavir"],
                ])
                return Images.get_image(yavir_keyboard_types.get(device.device_type), "Small", "")
            // handling different WireInputMTs
            case "1d":
                return Images.get_image(device.obj_type, "Small", device.input_type, device.custom_alarm)
            // handling different Sockets
            case "4c":
                return Images.get_image(device.obj_type, "Small", device.color, "0", device.subtype)
            // handling different Light Switches
            case "44":
                return Images.get_image(device.obj_type, "Small", device.color, "0", device.subtype)
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
    deviceSubtype: device.subtype
    deviceColor: device.color
    firstButtonName: device.button1_name || ""
    secondButtonName: device.button2_name || ""

    firstButtonClickedArea.onClicked: {
        if (!firstButtonChecked) {
            if (!selectedDevices[device.id]) {
                selectedDevices[device.id] = {"device": device, "selected_buttons": ["button1"]}
            } else {
                selectedDevices[device.id].selected_buttons.push("button1")
            }
        } else {
            selectedDevices[device.id].selected_buttons = selectedDevices[device.id].selected_buttons.filter(btn => btn != "button1")
            if (!selectedDevices[device.id].selected_buttons.length) delete selectedDevices[device.id]
        }
        selectedDevicesChanged()
    }

    secondButtonClickedArea.onClicked: {
        if (!secondButtonChecked) {
            if (!selectedDevices[device.id]) {
                selectedDevices[device.id] = {"device": device, "selected_buttons": ["button2"]}
            } else {
                selectedDevices[device.id].selected_buttons.push("button2")
            }
        } else {
            selectedDevices[device.id].selected_buttons = selectedDevices[device.id].selected_buttons.filter(btn => btn != "button2")
            if (!selectedDevices[device.id].selected_buttons.length) delete selectedDevices[device.id]
        }
        selectedDevicesChanged()
    }
}
