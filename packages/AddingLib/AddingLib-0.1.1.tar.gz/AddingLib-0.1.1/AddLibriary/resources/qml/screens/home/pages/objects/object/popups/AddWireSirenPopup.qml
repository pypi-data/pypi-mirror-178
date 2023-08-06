import QtQuick 2.12
import QtQuick.Controls 2.2

import "qrc:/resources/qml/components/desktop/"
import "qrc:/resources/qml/screens/home/pages/objects/object/popups/"
import "qrc:/resources/js/popups.js" as Popups
import "qrc:/resources/js/desktop/popups.js" as DesktopPopups
import "qrc:/resources/qml/components/911/" as Custom

AjaxPopup {
    id: popup
    width: 360
    height: 400

    modal: true
    focus: true

    closePolicy: Popup.CloseOnEscape | Popup.NoAutoClose

    property int roomIndex: 0

    property var management: null
    property var hub: management.devices.hub

    Rectangle {
        width: 360
        height: 330
        color: "#252525"

        radius: 3
        border.width: 1
        border.color: "#1a1a1a"

        AjaxPopupCloseHeader {
            id: closeItem
            fontSize: 16
            label: tr.add_wire_siren
        }

        AjaxSettingsTextField {
            id: deviceNameField

            miniText: tr.name

            width: popup.width - 64

            field.onActiveFocusChanged: {
                if (!valid) {
                    valid = true
                }
            }

            field.focus: true

            field.onTextChanged: {
                deviceNameField.field.text = util.validator(field.text, 24)
                return
            }

            anchors {
                top: closeItem.bottom
                topMargin: 32
                horizontalCenter: parent.horizontalCenter
            }

            Image {
                source: "qrc:/resources/images/desktop/icons/ic-popup-info@2x.png"

                anchors {
                    right: parent.right
                    rightMargin: 32
                    verticalCenter: parent.verticalCenter
                }

                MouseArea {
                    anchors.fill: parent
                    onClicked: Popups.text_popup(tr.information, tr.the_name_can_contain_letters)
                }
            }

            Keys.onEnterPressed: {
                addDeviceArea.clicked(true)
            }

            Keys.onReturnPressed: {
                addDeviceArea.clicked(true)
            }
        }

        AjaxSettingsCombobox {
            id: deviceNumberCombobox

            width: popup.width - 64
            miniText: ""
            model: popup.management.devices.wire_sirens_model
            currentIndex: 0
            visible: false
            height: 0
            anchors {
                top: deviceNameField.bottom
                topMargin: 8
                horizontalCenter: parent.horizontalCenter
            }

            func: function() {
                addDeviceArea.clicked(true)
            }
        }

        AjaxSettingsCombobox {
            id: roomsCombobox

            width: popup.width - 64
            miniText: tr.room
            model: popup.management.rooms.room_names
            currentIndex: roomIndex
            anchors {
                top: deviceNumberCombobox.bottom
                topMargin: 8
                horizontalCenter: parent.horizontalCenter
            }

            func: function() {
                addDeviceArea.clicked(true)
            }
        }

        AjaxSettingsCombobox {
            id: groupsCombobox

            width: popup.width - 64
            miniText: tr.group
            model: popup.management.groups.group_names
            currentIndex: 0
            visible: popup.hub.groups_enabled
            anchors {
                top: roomsCombobox.bottom
                topMargin: 8
                horizontalCenter: parent.horizontalCenter
            }

            func: function() {
                addDeviceArea.clicked(true)
            }
        }

        MouseArea {
            id: addDeviceArea

            width: parent.width
            height: 48
            hoverEnabled: true
            cursorShape: Qt.PointingHandCursor

            Text {
                anchors.centerIn: parent
                text: tr.add
                color: ui.colors.green1
                font.family: roboto.name
                font.pixelSize: 14
            }

            Rectangle {
                width: parent.width
                height: 1
                color: ui.colors.light1
                opacity: 0.05

                anchors {
                    bottom: parent.top
                }
            }

            anchors {
                bottom: parent.bottom
            }

            onClicked: {
                var deviceName = deviceNameField.field.text.trim()
                if (!deviceName) {
                    deviceNameField.field.focus = false
                    deviceNameField.field.valid = false
                    Popups.text_popup(tr.information, tr.please_fill_in_all_of_the_required_fields)
                    return
                }

                var settings = {
                    "name": {"name": deviceNameField.field.text.trim()},
                    "enabled": true,
                }

                if (roomsCombobox.currentIndex >= 0) {
                    var room = popup.management.rooms.get_room(roomsCombobox.currentIndex)
                    settings["room_id"] = room.id
                }

                if (popup.hub.groups_enabled) {
                    if (!groupsCombobox.model.length) {
                        Popups.text_popup(tr.information, tr.please_add_at_least_one_group_first)
                        return
                    }
                    var group = popup.management.groups.get(groupsCombobox.currentIndex)
                    settings["group_id"] = group.group_id
                } else {
                    settings["group_id"] = "00000000"
                }

                var device = null
                device = popup.management.devices.available_wire_sirens[deviceNumberCombobox.currentIndex]
                device = popup.management.devices.get_by_id(device)

                DesktopPopups.please_wait_popup()
                app.hub_management_module.apply_update(popup.management, device, settings)
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