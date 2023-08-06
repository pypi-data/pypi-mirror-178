import QtQuick 2.7
import QtQuick.Controls 2.2

import "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/service/advanced_settings"
import "qrc:/resources/js/desktop/popups.js" as Popups
import "qrc:/resources/qml/components/911/DS3" as DS3
import "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/service/advanced_settings/parts" as Parts


Rectangle {
    id: wizardBeepDevicesScreen

    property var devices_model: management.filtered_devices_for_post_alarm_indication
    property var verifying: management.filtered_devices_for_post_alarm_indication.confirming()
    property var sideMargin: 24

    property var devices_len: {
        return devices_model.length
    }

    function get_devices() {
        var devices = []
        for(var child in devicesView.contentItem.children) {
            let deviceItem = devicesView.contentItem.children[child]
            if (deviceItem.objectName == "delegate") {
                var dev = devices_model.get(deviceItem.indexRef)
                var choice = deviceItem.checked
                var old = deviceItem.old_state
                devices.push([dev.obj_type, dev.device_id, choice])
            }
        }
        return devices
    }

    function getResultSelectDevices(arr1, arr2) {
        let result = arr1.filter((elem) => arr2.every((sub) => (elem[1] != sub[1] || elem[2] != sub[2])))
        return result
    }
    
    Component.onCompleted: {
        if (lastScreen == 7) {
            // delete this screen from array if changed pd complient status
            let array = serviceSettings.notCompliantWizardScreens
            let index = array.indexOf(tr.beep_on_delay_pd)

            if (index != -1) {
                array.splice(index, 1)
            }
            lastScreen += 1
        }
    }

    Connections {
        target: app

        onAltActionSuccess: {
            if (serviceSettings.isWizard) {
                advancedSettingsLoader.setSource("qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/service/wizard/FinalWizardScreen.qml")
            } else {
                advancedSettingsLoader.setSource("")
            }
        }
    }

    color: ui.ds3.bg.base

    DS3.MouseArea {
        cursorShape: Qt.ArrowCursor
    }
    
    DS3.NavBarModal {
        id: wizardBeepDevicesBar

        headerText: tr.beep_on_delay_pd
        showBackArrow: true
        showCloseIcon: false
        isRound: false

        onBackAreaClicked: {
            if (serviceSettings.isWizard) {
                advancedSettingsLoader.setSource("qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/service/advanced_settings/ArmingDisarmingFlow.qml")
            } else {
                advancedSettingsLoader.setSource("")
            }
        }
    }

    DS3.InfoContainer {
        anchors {
            top: wizardBeepDevicesBar.bottom
            topMargin: 24
            horizontalCenter: parent.horizontalCenter
        }

        imageType: DS3.InfoContainer.ImageType.PlugImage
        imageSource: "qrc:/resources/images/Athena/PD_compliant/NoDevices.svg"
        descComponent.text: tr.no_devices_for_beep
        visible: !devices_model.length
    }

    DS3.ScrollView {
        anchors {
            fill: undefined
            top: wizardBeepDevicesBar.bottom
            bottom: nextButton.top
            left: parent.left
            right: parent.right
        }

        width: parent.width

        padding: sideMargin
        visible: devices_len

        DS3.SettingsContainer {
            width: parent.width

            anchors.horizontalCenter: parent.horizontalCenter

            DS3.CommentImportant {
                atomTitle.title: tr.beep_on_delay_pd_info
            }
        }
        
        DS3.Spacing {
            height: 4
        }
        
        DS3.Text {
            width: parent.width
            
            text: tr.select_at_least_one_pd_device
            style: ui.ds3.text.body.MRegular
            color: ui.ds3.figure.attention
            visible: {
                let count = 0

                for (let i = 0; i < wizardBeepDevicesScreen.verifying.length; i++) {
                    if (wizardBeepDevicesScreen.verifying[i][2] == true) {
                        count += 1
                    }
                }

                nextButton.hasComment = !count
                return !count
            }
        }

        DS3.Spacing {
            height: 24
        }

        DS3.SettingsContainer {
            width: parent.width

            anchors.horizontalCenter: parent.horizontalCenter

            SelectDevicesView {
                id: devicesView

                selectDevicesRect: wizardBeepDevicesScreen
                devicesModel: devices_model
                getDevices: get_devices
            }
        }

        DS3.Spacing {
            height: 4
        }

        DS3.Text {
            width: parent.width

            text: tr.beep_when_arming_sirens_info
            style: ui.ds3.text.body.MRegular
            color: ui.ds3.figure.secondary
        }
    }

    Parts.ButtonNextCancelPD {
        id: nextButton

        enabled: devEnable
        stepAmount: 10
        currentStep: 8
        hasStepper: serviceSettings.isWizard
        commentText: tr.settings_are_not_PD6662_compliant
        commentColor: ui.ds3.figure.attention
        commentIcon: "qrc:/resources/images/Athena/common_icons/Info-Grey-S.svg"
        hasComment: {
            let count = 0

            for (let i = 0; i < wizardBeepDevicesScreen.verifying.length; i++) {
                if (wizardBeepDevicesScreen.verifying[i][2] == true) {
                    count += 1
                }
            }

            if (serviceSettings.isWizard &&
                (!count || !devices_len)) return true
            return false
        }

        button.onClicked: {
            Popups.please_wait_popup()

            var data = []
            var selectedDevices = get_devices()
            var beepDevices = getResultSelectDevices(selectedDevices, management.filtered_devices_for_post_alarm_indication.beep_when_arming())

             for (let dev of beepDevices) {
                let device_info = {}
                device_info["type"] = dev[0]
                device_info["id"] = dev[1]
                device_info["beep_on_delay"] = dev[2]

                data.push(device_info)
            }

            // if screen not compliant with PD
            if (nextButton.hasComment) {
                serviceSettings.notCompliantWizardScreens.push(tr.beep_on_delay_pd)
            }

            app.hub_management_module.update_objects_settings(data, {"emit_alt_signal": true})
        }
    }
}

