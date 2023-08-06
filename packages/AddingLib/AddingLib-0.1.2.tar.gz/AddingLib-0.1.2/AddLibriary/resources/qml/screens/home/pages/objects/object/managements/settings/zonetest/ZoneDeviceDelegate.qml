import QtQuick 2.7
import QtQuick.Controls 2.1
import QtQuick.Layouts 1.3

import "qrc:/resources/js/images.js" as Images
import "qrc:/resources/qml/components/911/DS3/" as DS3


DS3.DeviceAction {
    property var deviceType: device.obj_type
    property var deviceColor: device.color
    property var deviceState: device.state

    Component.onDestruction: {
        if (device && ["DETECTION_AREA_TEST", "WAIT_DETECTION_AREA_TEST_START"].includes(deviceState)) {
            app.hub_management_module.device_command(device, "04")
        }
    }

    objectName: "delegate"
    atomTitle.title: device.name
    enabled: device.online &&
    [
         "NO_DEVICE_STATE_INFO",
         "PASSIVE",
         "ACTIVE",
         "DETECTION_AREA_TEST",
         "WAIT_DETECTION_AREA_TEST_START",
         "WAIT_DETECTION_AREA_TEST_END"
    ].includes(deviceState)

    atomTitle.subtitle: {
        if (!device.online) return tr.na
        if (["NO_DEVICE_STATE_INFO", "PASSIVE"].includes(deviceState)) return tr.ready
        if (deviceState == "DETECTION_AREA_TEST") return tr.testing
        if (deviceState == "WAIT_DETECTION_AREA_TEST_START") return tr.starting_test
        if (deviceState == "WAIT_DETECTION_AREA_TEST_END") return tr.stopping_test
        return tr.na
    }

    buttonMiniControl.visible: enabled &&
        [
            "NO_DEVICE_STATE_INFO",
            "ACTIVE",
            "PASSIVE",
            "DETECTION_AREA_TEST",
        ].includes(deviceState)

    buttonMiniControl.source: deviceState == "DETECTION_AREA_TEST" ?
        "qrc:/resources/images/Athena/views_icons/Stop-M.svg" :
        "qrc:/resources/images/Athena/views_icons/Start-M.svg"

    spinnerVisibility: ["WAIT_DETECTION_AREA_TEST_START", "WAIT_DETECTION_AREA_TEST_END"].includes(deviceState)

    imageSource: Images.get_image(deviceType, "Medium", deviceColor)

    buttonMiniControl.onClicked: {
        if ([
                "NO_DEVICE_STATE_INFO",
                "PASSIVE",
                "ACTIVE",
                "WAIT_DETECTION_AREA_TEST_END"
            ].includes(deviceState))
        {
            ["06", "13", "1a", "18"].includes(deviceType) ?
            app.hub_management_module.device_command(device, "11") :
            app.hub_management_module.device_command(device, "03")
        }
        else if (["DETECTION_AREA_TEST", "WAIT_DETECTION_AREA_TEST_START"].includes(deviceState))
        {
            app.hub_management_module.device_command(device, "04")
        }
    }
}