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
    title: tr.siren_volume

    Component.onDestruction: {
        changesChecker.changeInitialValues()
    }

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
        text: tr.siren_volume_test_descr
        opacity: 0.5
        style: ui.ds3.text.body.LRegular
    }

    DS3.Spacing {
        height: 24
    }

    footer: DS3.ButtonBar {
        buttonText: tr.start

        button.onClicked: {
            Popups.text_popup(tr.test_about_start, util.insert(
                device.mute_available && device.volume == 32 ?
                    tr.test_about_start_siren_no_volume_descr :
                    tr.test_about_start_siren_descr,
                [hub.frame_length])
            )
            app.hub_management_module.device_command(device, 8)
        }
    }
}