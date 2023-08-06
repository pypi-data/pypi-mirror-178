import QtQuick 2.12
import QtQuick.Controls 2.2
import QtGraphicalEffects 1.12

import "qrc:/resources/qml/components/desktop/"
import "qrc:/resources/qml/screens/home/pages/objects/object/popups/"
import "qrc:/resources/js/popups.js" as Popups
import "qrc:/resources/js/desktop/popups.js" as DesktopPopups
import "qrc:/resources/qml/components/911/" as Custom


AjaxPopup {
    id: popup

    width: 384
    height: {
        let groupsColumnHeight = 0
        if (hub && hub.groups_enabled) {
            groupsColumnHeight = groupsColumn.height
        }

        return header.height
            + spacerLine.height + 18
            + deviceNameColumn.height
            + wireInputColumn.height
            + roomsColumn.height
            + groupsColumnHeight
            + spacerLineBottom.height
            + 24 + 42 + 24
    }

    modal: true
    focus: true

    closePolicy: Popup.CloseOnEscape | Popup.NoAutoClose

    property int roomIndex: 0
    property var mtr_device: ""

    Rectangle {
        width: 384
        height: popup.height
        color: ui.colors.dark3

        radius: 8

        Custom.PopupHeader {
            id: header
            width: parent.width
            height: 88
            radius: parent.radius
            title: tr.add_wire_device
            anchors.top: parent.top

            closeArea.onClicked: {
                popup.close()
            }
        }

        Rectangle {
            id: spacerLine

            width: parent.width - 32
            height: 1
            color: ui.colors.dark1
            anchors {
                top: header.bottom
                right: parent.right
            }
        }

        Column {
            id: deviceNameColumn

            width: popup.width - 64
            spacing: 18

            anchors {
                top: spacerLine.bottom
                topMargin: 18
                horizontalCenter: parent.horizontalCenter
            }

            Text {
                width: parent.width
                height: contentHeight

                anchors.left: parent.left

                text: tr.name

                color: ui.colors.middle1
                font.family: roboto.name
                font.pixelSize: 14
                wrapMode: Text.Wrap

            }

            Custom.TextField {
                id: deviceNameField

                width: parent.width
                color: ui.colors.dark2

                placeHolderText: tr.name
                control.validator: RegExpValidator { regExp: /^([a-zA-Z0-9!""#$%&'()*+,-./:;<=>?@[\]^_`{|}~\s]){24}|([!""#$%&'()*+,-./:;<=>?@[\]^_`{|}~а-яіїґєa-zA-ZА-ЯІЇЄҐ0-9\s]){12}$/ }

                Image {
                    id: infoIcon

                    source: "qrc:/resources/images/desktop/icons/ic-popup-info@2x.png"

                    anchors {
                        right: parent.right
                        top: parent.top
                        rightMargin: 6
                        topMargin: 6
                    }
                    MouseArea {
                        anchors.fill: parent
                        onClicked: Popups.text_popup(tr.information, tr.the_name_can_contain_letters)
                    }
                }

                ColorOverlay {
                    anchors.fill: infoIcon
                    source: infoIcon
                    color: ui.colors.green1
                }
            }

            Item {
                width: parent.width
                height: 4
            }
        }

        Column {
            id: wireInputColumn

            width: popup.width - 64
            spacing: 18

            anchors {
                top: deviceNameColumn.bottom
                horizontalCenter: parent.horizontalCenter
            }

            Text {
                width: parent.width
                height: contentHeight

                anchors.left: parent.left

                text: tr.wire_input

                color: ui.colors.middle1
                font.family: roboto.name
                font.pixelSize: 14
                wrapMode: Text.Wrap
            }

            Custom.ComboBox {
                id: wireInputCombobox

                width: popup.width - 64
                popup.height: Math.min(130, model.length * 40 + 6)

                model: mtr_device.wired_inputs.map((elem) => `${tr.input} ${elem}`)
                currentIndex: 0
            }
            Item {
                width: parent.width
                height: 4
            }
        }

        Column {
            id: roomsColumn

            width: popup.width - 64
            spacing: 18

            anchors {
                top: wireInputColumn.bottom
                horizontalCenter: parent.horizontalCenter
            }

            Text {
                width: parent.width
                height: contentHeight

                anchors.left: parent.left

                text: tr.room

                color: ui.colors.middle1
                font.family: roboto.name
                font.pixelSize: 14
                wrapMode: Text.Wrap
            }

            Custom.ComboBox {
                id: roomsCombobox

                width: popup.width - 64
                model: rooms.room_names
                currentIndex: roomIndex
                textLabel.textFormat: Text.PlainText
            }
            Item {
                width: parent.width
                height: 4
            }
        }

        Column {
            id: groupsColumn

            width: popup.width - 64
            spacing: 18

            anchors {
                top: roomsColumn.bottom
                horizontalCenter: parent.horizontalCenter
            }

            visible: hub.groups_enabled

            Text {
                width: parent.width
                height: contentHeight

                anchors.left: parent.left

                text: tr.group

                visible: hub.groups_enabled

                color: ui.colors.middle1
                font.family: roboto.name
                font.pixelSize: 14
                wrapMode: Text.Wrap
            }

            Custom.ComboBox  {
                id: groupsCombobox

                width: popup.width - 64
                model: groups.group_names
                currentIndex: 0
                textLabel.textFormat: Text.PlainText
                visible: hub.groups_enabled
            }

            Item {
                width: parent.width
                height: 4
            }
        }

        Rectangle {
            id: spacerLineBottom

            width: parent.width - 32
            height: 1

            color: ui.colors.dark1
            anchors {
                top: hub.groups_enabled ? groupsColumn.bottom : roomsColumn.bottom
                right: parent.right
            }
        }

        Custom.Button {
            id: addWireInputMTDeviceButton

            width: 320
            text: tr.add_device
            transparent: true
            color: deviceNameField.control.text ? ui.colors.green1 : ui.colors.middle4

            anchors {
                top: spacerLineBottom.bottom
                horizontalCenter: parent.horizontalCenter
                topMargin: 24
            }
            onClicked: {
                var deviceName = deviceNameField.control.text.trim()
                var wiredDeviceId = mtr_device.wired_inputs[wireInputCombobox.currentIndex].toString(16).padStart(2, "0") + mtr_device.device_id.slice(2)

                if (!deviceName) {
                    Popups.text_popup(tr.information, tr.please_fill_in_all_of_the_required_fields)
                    return
                }

                var room = rooms.get_room(roomsCombobox.currentIndex)

                var group = null
                if (hub.groups_enabled) {
                    if (groupsCombobox.model.length) {
                        var group = groups.get(groupsCombobox.currentIndex)
                    } else {
                        Popups.text_popup(tr.information, tr.please_add_at_least_one_group_first)
                        return
                    }
                }
                DesktopPopups.please_wait_popup()
                app.hub_management_module.reg_device(mtr_device, room.room_id, group, wiredDeviceId, deviceName)
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
