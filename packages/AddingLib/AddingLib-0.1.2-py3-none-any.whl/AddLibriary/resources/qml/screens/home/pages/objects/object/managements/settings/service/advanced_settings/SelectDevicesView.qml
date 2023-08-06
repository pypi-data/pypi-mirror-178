import QtQuick 2.7
import QtQuick.Controls 2.2

import "qrc:/resources/qml/components/911/DS3" as DS3
import "qrc:/resources/js/images.js" as Images


ListView {
    id: devicesView

    property var selectDevicesRect: null
    property var devicesModel: null
//  A function for getting all needed devices and their data
    property var getDevices: () => {}
//  Does the device selection element display group data
    property var hasGroupData: false

    width: parent.width
    height: contentHeight

    clip: true
    cacheBuffer: 20000

    spacing: 1
    model: devicesModel
    interactive: false
    visible: devicesModel.length
    section.property: "room_name"
    section.delegate: Column {
        property var sectionRef: section
        property alias sectionText: sectionTitle.buttonText
        property var devices: devicesView.contentItem.children

        width: parent.width

        objectName: "section"
        DS3.TitleSection {
            id: sectionTitle

            // All the section devices
            readonly property var allSectionDevices: Array.from(devices)
                .filter((el) => { return el.objectName == "delegate" && el.roomName == section})

            width: parent.width
            height: textItem.height + 8

            forceTextToLeft: true
            text: section
            hasButton: true
            buttonText: {
                let selectedSectionDevicesCount = allSectionDevices.length
                let allSectionDevicesCount = allSectionDevices.filter((el) => {return el.checked}).length

                return allSectionDevicesCount == selectedSectionDevicesCount ? tr.cancel : tr.check_all
            }

            onButtonClicked: () => {
                const hasToBeChecked = sectionTitle.buttonText == tr.check_all
                for (let el of sectionTitle.allSectionDevices) {
                    el.checked = hasToBeChecked
                }
//                selectDevicesRect.verifying = get_devices()
            }
        }

        DS3.Spacing {
            width: parent.width
        }
    }

    delegate: DS3.DeviceSelectionMulti {
        property int indexRef: index
        property var roomName: room_name
        property var old_state: device.device_alarm_logic_type

        width: parent.width

        imageSource: {
            // handles the cases of different wired devices that are not just a set of color and id
            switch(device.obj_type) {
                // handling different WireInputs
                case "26":
                    return Images.get_image(device.input_is_tamper == 1 ? "26-wired-tamper" : "26-wired-intrusion", "Medium")
                // handling different YavirAccessControls
                case "28":
                    let yavir_keyboard_types = new Map([
                        [0, "28"],
                        [1, "28-keypad-yavir"],
                        [2, "28-reader-yavir"],
                    ])
                    return Images.get_image(yavir_keyboard_types.get(device.device_type), "Medium")
                // handling different WireInputMTs
                case "1d":
                    return Images.get_image(device.obj_type, "Medium", device.input_type, device.custom_alarm_available_v2 ? device.custom_alarm_S2 : device.custom_alarm)
                // handling different Sockets
                case "4c":
                    return Images.get_image(device.obj_type, "Medium", device.color, null, device.subtype)
                // handling different Light Switches
                case "44":
                    return Images.get_image(device.obj_type, "Medium", device.color, null, device.subtype)
            }
        }

        deviceImage.width: 40
        deviceImage.height: 40
        objectName: "delegate"
        atomTitle{
            title: device.name
            subtitle: util.insert(tr.device_index_911, [device.device_index])
        }
        description {
            visible: hasGroupData && device.group_id_bound != 0
            text: device.group_id_bound == 0 ? "" : `${management.groups.get_group(device.group_id_bound).name} (Group ID ${parseInt(device.group_id_bound, 16)})`
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
        checked: {
            if (device == undefined) {
                return false
            }
            let deviceId = device.device_id
            if (selectDevicesRect.verifying.length > 0 && selectDevicesRect.verifying[0]["choice"] != undefined){
                for(var i = 0; i < selectDevicesRect.verifying.length; i++) {
                    if (selectDevicesRect.verifying[i]["device_id"] == deviceId) {
                        return selectDevicesRect.verifying[i]["choice"]
                    }
                }
                return false
            }
            for(var i = 0; i < selectDevicesRect.verifying.length; i++) {
                if (selectDevicesRect.verifying[i][1] == device.device_id) {
                    return selectDevicesRect.verifying[i][2]
                }
            }
            return false
        }

        clickedArea.onClicked: {
            checked = !checked
            selectDevicesRect.verifying = getDevices()
        }
    }
}
