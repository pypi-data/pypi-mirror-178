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
                        id: onArmActionCombobox
                        miniText: tr.react_to_arming_desktop
                        model: [tr.no_change, tr.enabled, tr.disabled]

                        enabled: devEnable

                        currentIndex: {
                            if (device.arming_actions == 0) {
                                return 0
                            }
                            if (device.arming_actions & 2) {
                                return 1
                            }
                            if (device.arming_actions & 4) {
                                return 2
                            }
                            return 0
                        }
                    }
                    AjaxSettingsCombobox {
                        id: onDisarmActionCombobox

                        miniText: tr.react_to_disarming_desktop
                        model: [tr.no_change, tr.enabled, tr.disabled]

                        enabled: devEnable

                        currentIndex: {
                            if (device.arming_actions == 0) {
                                return 0
                            }
                            if (device.arming_actions & 8) {
                                return 1
                            }
                                if (device.arming_actions & 16) {
                                return 2
                            }
                            return 0
                        }
                    }
                    AjaxSettingsSwitch {
                        id: nightModeReaction

                        height: 32

                        text: tr.react_on_perimetral_arming_disarming
                        visible: (hub.firmware_version_dec >= 206000)
                        enabled: devEnable && (onArmActionCombobox.currentIndex != 0 || onDisarmActionCombobox.currentIndex != 0)
                        checked: device.perimeter_protection_group

                        area.onClicked: {
                            checked = !checked
                        }
                    }
                    Settings.CurrentProtection { id: currentProtection }
                    Settings.VoltageProtection { id: voltageProtection }

                    TestSignalLevelNav {}
                    Bypass {}
                    ManualNav {}

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

                    var settings = {
                        "common_part": {
                            "name": {"name": deviceName.atomInput.text.trim()},
                        },
                    }
                    if (roomsCombobox.currentIndex >= 0) {
                        settings["common_part"]["room_id"] = rooms.get_room(roomsCombobox.currentIndex).id
                    }

                    if (nightModeReaction.enabled) {
                        settings["perimeter_protection_group"] = nightModeReaction.checked
                    }

                    var armingActions = 0
                    if (onArmActionCombobox.currentIndex != 0) {
                        armingActions += Math.pow(2, onArmActionCombobox.currentIndex)
                    }
                    if (onDisarmActionCombobox.currentIndex != 0) {
                        armingActions += Math.pow(2, onDisarmActionCombobox.currentIndex + 2)
                    }

                    settings["arming_actions"] = armingActions
                    settings["current_protection"] = currentProtection.checked
                    settings["voltage_protection"] = voltageProtection.checked

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