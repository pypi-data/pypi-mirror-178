import QtQuick 2.13
import QtQuick.Controls 2.12

import "qrc:/resources/qml/components/911/DS3" as DS3
import "qrc:/resources/qml/components/911/DS3/popups" as DS3Popups
import 'qrc:/resources/js/desktop/popups.js' as Popups
import "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/settings/" as Settings


DS3Popups.PopupStep {
    id: chimesSettingsPopupStep

    property var sideMargin: 24
    property var isLeft: none

    Component.onDestruction: {
        device.dataChanged()
    }

    height: maxStepHeight

    sidePadding: 24

    title: device.view_name  //    title: isLeft ? tr.left_side : tr.right_side

    Column {
        width: parent.width

        DS3.Spacing {
            height: 24
        }

        Image {
            width: 375
            height: 200
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

        DS3.Spacing {
            height: 24
        }

        DS3.SettingsContainer {
            DS3.SettingsSwitch {
                id: detection

                title: isLeft ? tr.detection_left : tr.detection_right
                checked: isLeft ? device.detection_left : device.detection_right
            }

            DS3.SettingsPickerTitleSecondary {
                id: sensitivity

                atomTitle.title: isLeft ? tr.sensitivity_left : tr.sensitivity_right
                model: [tr.low, tr.normal, tr.high]
                currentIndex: isLeft ? device.left_motion_sensitivity : device.right_motion_sensitivity
                visible: devEnable & detection.checked
            }

            DS3.SettingsSwitch {
                id: alwaysActive

                title: isLeft ? tr.always_active_left : tr.always_active_right
                checked: isLeft ? device.left_motion_always_active : device.right_motion_always_active
                visible: devEnable & detection.checked
            }
        }

        DS3.Spacing {
            height: 24
        }

        DS3.SettingsContainer {
            DS3.SettingsSwitch {
                id: antimasking

                title: isLeft ? tr.anti_masking_left : tr.anti_masking_right
                checked: isLeft ? device.left_motion_antimasking : device.right_motion_antimasking
            }
        }
    }

    DS3.ChangesChecker {
        id: changesChecker

        listeningValues: [
            detection.checked,
            sensitivity.currentIndex,
            alwaysActive.checked,
            antimasking.checked
        ]
    }

    footer: DS3.ButtonBar {
        id: saveButton

        width: parent.width

        button.text: tr.save
        enabled: changesChecker.hasChanges
        hasBackground: true

        button.onClicked: {
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
            changesChecker.changeInitialValues()
        }
    }
}