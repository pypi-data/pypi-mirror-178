import QtQuick 2.7
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.3
import QtGraphicalEffects 1.12

import "qrc:/resources/qml/components/desktop/"
import "qrc:/resources/qml/screens/home/pages/objects/object/managements/views"
import "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/parts/"
import "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/users/"

import "qrc:/resources/js/desktop/popups.js" as Popups
import "qrc:/resources/qml/components/911/DS3/" as DS3

Rectangle {
    anchors.fill: parent
    color: ui.backgrounds.base
    radius: 12

    property var sideMargin: 24
    property var isLeft: none

    DS3.NavBarModal {
        id: bar

        headerText: isLeft ? tr.left_side : tr.right_side
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

    View {
        id: view

        width: parent.width

        anchors {
            top: bar.bottom
            bottom: saveButton.top
        }

        Column {
            spacing: 8
            width: {
                return view.width - 10
            }
            Image {
                width: 128
                height: 128
                anchors.horizontalCenter: parent.horizontalCenter
                source: {
                    if (isLeft) {
                        if (detection.checked) {
                            return "qrc:/resources/images/desktop/delegates/dco/DCOLeftOnLarge.png"
                        } else {return "qrc:/resources/images/desktop/delegates/dco/DCOLeftOffLarge.png"}
                    } else {
                        if (detection.checked) {
                            return "qrc:/resources/images/desktop/delegates/dco/DCORightOnLarge.png"
                        } else {return "qrc:/resources/images/desktop/delegates/dco/DCORightOffLarge.png"}
                    }
                }
            }

            AjaxSettingsSwitch {
                id: detection
                text: isLeft ? tr.detection_left : tr.detection_right
                height: 32

                checked: isLeft ? device.detection_left : device.detection_right

                enabled: devEnable

                area.onClicked: {
                    checked = !checked
                }
            }
            AjaxSettingsCombobox {
                id: sensitivity
                miniText: isLeft ? tr.sensitivity_left : tr.sensitivity_right
                enabled: devEnable & detection.checked

                model: [tr.low, tr.normal, tr.high]
                currentIndex: isLeft ? device.left_motion_sensitivity : device.right_motion_sensitivity
            }

            AjaxSettingsSwitch {
                id: alwaysActive
                text: isLeft ? tr.always_active_left : tr.always_active_right
                height: 32

                enabled: devEnable & detection.checked
                checked: isLeft ? device.left_motion_always_active : device.right_motion_always_active

                area.onClicked: {
                    checked = !checked
                }
            }

            AjaxSettingsSwitch {
                id: antimasking
                text: isLeft ? tr.anti_masking_left : tr.anti_masking_right
                height: 32

                checked: isLeft ? device.left_motion_antimasking : device.right_motion_antimasking

                enabled: devEnable

                area.onClicked: {
                    checked = !checked
                }
            }

        }

    }

    DS3.ButtonContained {
        id: saveButton

        width: parent.width - sideMargin * 2

        anchors {
            bottom: parent.bottom
            bottomMargin: sideMargin
            horizontalCenter: parent.horizontalCenter
        }

        text: tr.save

        onClicked: {
            var settings = {
                "_params": {"special_signal": "saveDCOSensorSuccess"},
            }

            if (isLeft) {
                settings["left_motion_allowed"] = detection.checked
                settings["left_motion_sensitivity"] = parseInt(sensitivity.currentIndex)
                settings["left_motion_always_active"] = alwaysActive.checked
                settings["left_motion_antimasking"] = antimasking.checked
            } else {
                settings["right_motion_allowed"] = detection.checked
                settings["right_motion_sensitivity"] = parseInt(sensitivity.currentIndex)
                settings["right_motion_always_active"] = alwaysActive.checked
                settings["right_motion_antimasking"] = antimasking.checked
            }

            Popups.please_wait_popup()
            app.hub_management_module.apply_update(management, device, settings)
        }
    }

//    Connections {
//        target: client
//
//        onActionSuccess: {
//            popup.width = 400
//            currentIndex = -1
//        }
//    }
}


