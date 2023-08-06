import QtQuick 2.7

import "qrc:/resources/js/images.js" as Images
import "qrc:/resources/js/popups.js" as Popups
import "qrc:/resources/qml/components/911/DS3/" as DS3
import "qrc:/resources/qml/components/911/DS3/popups" as DS3Popups
import "qrc:/resources/qml/screens/home/pages/objects/object/managements/views/parts" as ViewsParts


DS3Popups.PopupStep {
    property var chimesItem: null
    property var sideMargin: 24
    property var state: device.state

    sidePadding: 24
    title: device.obj_type == "4d" ? tr.fire_new_self_test : tr.fireprotect_self_test

    DS3.Spacing {
        height: 24
    }

    DS3.DeviceHeaderInfo {
        imagePath: Images.get_image(device.obj_type, "Large", device.color, "0", device.subtype)
    }

    ViewsParts.DeviceNameRoom {}

    DS3.Text {
        id: attenuationTestInfo

        width: parent.width - 40

        anchors.horizontalCenter: parent.horizontalCenter

        wrapMode: Text.WordWrap
        horizontalAlignment: Text.AlignHCenter
        text: ["FIRE_PROTECT2_PLUS", "FIRE_PROTECT2_PLUS_SB"].includes(device.subtype) ?
            tr.smoke_co_test_fire_descr :
            tr.smoke_test_fire_descr
        style: ui.ds3.text.body.LRegular
        color: ui.ds3.figure.secondary
    }

    DS3.Spacing {
        height: 24
    }

    footer: DS3.ButtonBar {
        buttonText: tr.start

        button.onClicked: {
            if (device.obj_type == "4d") goBack()
            testFireNav.testFireStarted()
            app.hub_management_module.device_command(device, 10)
        }
    }
}