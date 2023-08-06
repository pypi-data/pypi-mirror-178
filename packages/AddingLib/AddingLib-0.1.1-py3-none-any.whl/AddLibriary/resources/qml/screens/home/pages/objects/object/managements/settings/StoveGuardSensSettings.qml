import QtQuick 2.7
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.3
import QtGraphicalEffects 1.12

import "qrc:/resources/qml/components/desktop/"
import "qrc:/resources/qml/screens/home/pages/objects/object/managements/views"
import "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/parts/"

import "qrc:/resources/js/desktop/popups.js" as Popups
import "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/settings/" as Settings

AjaxPopup {
    id: popup

    width: 360
    height: {
        if (view.contentHeight + 100 + 96 > application.height) {
            return maxPopupHeight
        }
        return view.contentHeight + 50 + 96
    }

    property var device: null
    property var devEnable: hub.online && device.online
    property var switchDevices: hub.get_stoveguard_switches()
    property alias testLoader: rightPanelCanvas.testLoader

    Behavior on width {
        NumberAnimation { duration: 200 }
    }

    closePolicy: Popup.CloseOnEscape | Popup.NoAutoClose

    onClosed: {
        popup.width = 360
    }

    Item {
        id: s

        width: popup.width
        height: popup.height

        RightPanelCanvas {
            id: rightPanelCanvas
        }

        Rectangle {
            width: 360
            height: parent.height

            anchors.left: parent.left
            color: "#0f0f0f"
            border.width: 1
            border.color: "#1f1f1f"

            AjaxPopupCloseHeader {
                id: closeItem

                label: device.info_name
            }

            View {
                id: view

                width: parent.width

                anchors {
                    top: closeItem.bottom
                    bottom: saveCancel.top
                }


                Column {
                    id: column

                    width: view.width
                    spacing: 5

                    DeviceImage {}
                    Settings.Name { id: deviceName }
                    Settings.Room { id: roomsCombobox }


                    AjaxSettingsCombobox {
                        id: switchNumberCombobox

                        miniText: "switchNumber"
                        model: switchDevices.names
//                        visible: switchDevices != []

                        enabled: devEnable

                        currentIndex: switchDevices.indexes.indexOf(device.switch_number)
                    }


                    AjaxSettingsCombobox {
                        id: cookingTimeOutCombobox

                        miniText: "cookingTimeOut"
                        model: [0, 1, 2, 3, 4, 5, 6, 7, 8]

                        enabled: devEnable

                        currentIndex: device.cooking_timeout
                    }

                    AjaxSettingsCombobox {
                        id: sensitivityLevelCombobox

                        miniText: "sensitivityLevel"
                        model: [0, 1, 2, 3, 4, 5, 6, 7]

                        enabled: devEnable

                        currentIndex: device.sensitivity_level
                    }

                    AjaxSettingsCombobox {
                        id: manualSensitivityCombobox

                        miniText: "manualSensitivity"
                        model: [tr.auto, tr.set_up_manually]

                        enabled: devEnable

                        currentIndex: device.manual_sensitivity
                    }

                    AjaxSettingsSwitch {
                        id: flameAlarmSwitch

                        height: 32

                        text: "flameAlarm"
                        visible: true
                        enabled: devEnable
                        checked: device.flame_alarm

                        area.onClicked: {
                            checked = !checked
                        }
                    }

                    AjaxSettingsSwitch {
                        id: buzzerSwitch

                        height: 32

                        text: "buzzer"
                        visible: true
                        enabled: devEnable
                        checked: device.buzzer

                        area.onClicked: {
                            checked = !checked
                        }
                    }

                    AjaxSettingsSwitch {
                        id: blindControlSwitch

                        height: 32

                        text: "blindControl"
                        visible: true
                        enabled: devEnable
                        checked: device.blind_control

                        area.onClicked: {
                            checked = !checked
                        }
                    }

                    TestSignalLevelNav {}
                    Bypass {}

                    Delete {}
                }
            }

            AjaxSaveCancel {
                id: saveCancel

                width: parent.width
                height: 48

                saveArea.enabled: devEnable
                anchors.bottom: parent.bottom
                saveArea.onClicked: {
                    console.log("ERROR: Missing prototype, save action not available.")
                    return

                    if (!deviceName.atomInput.text.trim()) {
                        Popups.text_popup(tr.information, tr.the_name_field_cannot_be_blank)
                        return
                    }

                    if (switchNumberCombobox.currentIndex == -1) {
                        Popups.text_popup(tr.information, tr.please_fill_in_all_of_the_required_fields)
                        return
                    }

                    var settings = {
                        "common_part": {
                            "name": {"name": deviceName.atomInput.text.trim()},
                        },
                    }
                    if (roomsCombobox.currentIndex >= 0) {
                        settings["common_part"]["room_id"] = rooms.get_room(roomsCombobox.currentIndex).id
                    }

                    settings["switch_number"] = popup.switchDevices.indexes[switchNumberCombobox.currentIndex]
                    settings["cooking_timeout"] = cookingTimeOutCombobox.currentIndex
                    settings["sensitivity_level"] = sensitivityLevelCombobox.currentIndex
                    settings["manual_sensitivity"] = manualSensitivityCombobox.currentIndex

                    settings["flame_alarm"] = flameAlarmSwitch.checked
                    settings["buzzer"] = buzzerSwitch.checked
                    settings["blind_control"] = blindControlSwitch.checked

                    app.hub_management_module.apply_update(management, device, settings)
                }

                cancelArea.onClicked: {
                    popup.close()
                }
            }
        }
    }

    Connections {
        target: app
        onActionSuccess: {
            popup.close()
        }
    }
}
