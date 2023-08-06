import QtQuick 2.7
import QtQuick.Controls 2.1
import QtQuick.Layouts 1.3

import "qrc:/resources/qml/components/911/DS3" as DS3
import "qrc:/resources/js/images.js" as Images


DS3.DeviceRegular {
    id: deviceRegular

    width: parent.width
    height: 104

    opacity: device.online ? 1.0 : 0.3
    color: ui.ds3.figure.transparent
    deviceType: device.obj_type
    deviceColor: device.color
    deviceImage {
        width: 80
        height: 80
    }
    description.text: device.room_name
    atomTitle {
        title: device.name
        subtitle: util.insert(tr.device_index_911, [device.device_index, ])
    }
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
            // handling Light Switch
            case "44":
                return Images.get_image(device.obj_type, "Medium", device.color, "0", device.subtype)
            // handling Fire Protect 2
            case "4d":
                return Images.get_image(device.obj_type, "Medium", device.color, "0", device.subtype)
        }
    }
}
