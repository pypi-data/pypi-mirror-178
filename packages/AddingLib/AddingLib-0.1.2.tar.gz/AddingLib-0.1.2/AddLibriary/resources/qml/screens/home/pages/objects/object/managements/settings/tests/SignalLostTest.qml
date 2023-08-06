import QtQuick 2.7
import QtQuick.Controls 2.2
import QtGraphicalEffects 1.12

import "qrc:/resources/qml/components/desktop/"
import "qrc:/resources/js/images.js" as Images
import "qrc:/resources/js/popups.js" as Popups
import "qrc:/resources/qml/components/911/DS" as DS
import "qrc:/resources/qml/components/911/DS3/" as DS3
import "qrc:/resources/js/desktop/popups.js" as DesktopPopups
import "qrc:/resources/qml/components/911/DS3/popups" as DS3Popups


DS3Popups.PopupStep {
    property var chimesItem: null
    property var sideMargin: 24
    property var state: device.state

    sidePadding: 24

//    title: tr.attenuation_test

    DS3.Spacing {
        height: 24
    }

    DS3.Text {
        anchors.horizontalCenter: parent.horizontalCenter

        text: tr.attenuation_test
        style: ui.ds3.text.title.LBold
    }

    DS3.Spacing {
        height: 48
    }

    Image {
        id: attenuationTestImage

        width: sourceSize.width * 0.7
        height: sourceSize.height * 0.7

        source: Images.get_image(device.obj_type, "Large", device.color)
        anchors.horizontalCenter: parent.horizontalCenter
    }

    DS3.Text {
        id: deviceNameLabel

        width: parent.width - 32

        anchors.horizontalCenter: parent.horizontalCenter

        text: device.info_name
        style: ui.ds3.text.title.SBold
        horizontalAlignment: Text.AlignHCenter
    }

    AjaxSettingsCombobox {
        id: powerManagementField

        miniText: tr.power_management
        model: [tr.auto, tr.alt_6db, tr.max]

        currentIndex: {
            if (device.transmission_power_mode == 3) return 2
            return device.transmission_power_mode
        }

        anchors.horizontalCenter: parent.horizontalCenter

        combobox.onActivated: {
            if (currentIndex != 0) {
                Popups.text_popup(tr.information, tr.attenuation_test_warning)
            }
        }
    }

    DS3.Spacing {
        height: 48
    }

    DS3.Text {
        id: attenuationTestInfo

        width: parent.width - 40

        anchors.horizontalCenter: parent.horizontalCenter

        wrapMode: Text.WordWrap
        horizontalAlignment: Text.AlignHCenter
        text: tr.attenuation_test_hint
        opacity: 0.5
        style: ui.ds3.text.body.SRegular
    }

    DS3.Spacing {
        height: 24
    }

    footer: DS3.ButtonBar {
        buttonText: tr.save

        button.onClicked: {
            var powerMode = powerManagementField.currentIndex
            if (powerMode == 2) {
                powerMode += 1
            }

            var settings = {
                "common_part": {
                    "device_transmission_power_mode": powerMode,
                },
                "_params": {
                    "alt_action_success": true,
                },
            }

            DesktopPopups.please_wait_popup(tr.request_send, 30, [app.altActionSuccess, app.actionFailed])
            app.hub_management_module.apply_update(management, device, settings)
        }
    }

    Timer {
        id: aboutToHideTimer

        interval: 1500

        onTriggered: {
            goBack()
        }
    }

    Connections {
        target: app

        onAltActionSuccess: {
            aboutToHideTimer.start()
        }
    }
}