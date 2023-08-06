import QtQuick 2.7
import QtQuick.Controls 2.2
import QtGraphicalEffects 1.12

import "qrc:/resources/qml/components/desktop"
import "qrc:/resources/js/images.js" as Images
import "qrc:/resources/js/popups.js" as Popups
import "qrc:/resources/qml/components/911/DS3/" as DS3
import "qrc:/resources/qml/components/911/DS" as DS

Rectangle {
    anchors.fill: parent
    color: ui.backgrounds.base
    radius: 12
    property var sideMargin: 24

    DS3.NavBarModal {
        id: bypassBar

        headerText: tr.bypass_mode
        showCloseIcon: false
        showBackArrow: true
        showManualIcon: true
        onBackAreaClicked: {
            popup.width = 360
            testLoader.source = ""
        }
        onManualAreaClicked: {
            var link = app.hub_management_module.get_manual_link_bypass()
            Qt.openUrlExternally(link)
        }
    }

    AjaxSettingsCombobox {
        id: bypassModeField
        anchors.top: bypassBar.bottom

        miniText: tr.bypass_mode
        model: bypassModeField.hasTamper ? [tr.no, tr.bypass_on, tr.bypass_tamper_on] : [tr.no, tr.bypass_on]
        currentIndex: {
            // ON, OFF for Wire Input
            return {
                "OFF": 0,
                "ON": 1,
                "NO_BYPASS_MODE_INFO": 0,
                "ENGINEER_BYPASS_OFF": 0,
                "ENGINEER_BYPASS_ON": 1,
                "TAMPER_BYPASS_ON": 2,
                }[device.bypass_mode]
            }

        property var hasTamper: {
            if (["22", "23", "24", "25", "2a", "2b", "2c", "40", "41", "0b", "0c", "1d", "1e", "1f", "12", "17", "26", "27", "29", "42", "44", "4c", "4d"].includes(device.obj_type)) return false
            return true
        }

        anchors {
            horizontalCenter: parent.horizontalCenter
            top: parent.top
            topMargin: 30
        }

        combobox.onActivated: {
            if (currentIndex == 1) {
                Popups.text_popup(tr.device_is_bypassed, tr.device_is_bypassed_description)
            }

            if (currentIndex == 2) {
                Popups.text_popup(tr.warning, tr.bypass_tamper_on_description)
            }
        }
    }

    Item {
        id: infoBody
        width: parent.width
        height: {
            return bypassInfo.lineCount * bypassInfo.font.pixelSize + 40
        }

        anchors {
            horizontalCenter: parent.horizontalCenter
            top: bypassModeField.bottom
            topMargin: 12
        }

        DS3.Text {
            id: bypassInfo

            width: parent.width - 40

            style: ui.ds3.text.body.SRegular
            wrapMode: Text.WordWrap
            horizontalAlignment: Text.AlignHCenter
            text: tr.bypass_info
            opacity: 0.5
            anchors.centerIn: parent
        }
    }

    DS3.ButtonContained {
        width: parent.width - sideMargin * 2

        anchors {
            bottom: parent.bottom
            bottomMargin: sideMargin
            horizontalCenter: parent.horizontalCenter
        }

        text: tr.save

        onClicked: {
            var bypass_sygnals = [19, 20, 21]
            app.hub_management_module.device_command(device, bypass_sygnals[bypassModeField.currentIndex])
        }
    }

    Connections {
        target: app

        onAltActionSuccess: {
            popup.width = 360
            testLoader.setSource("")
        }
    }
}
