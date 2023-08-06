import QtQuick 2.12
import QtQuick.Controls 2.2

import "qrc:/resources/qml/components/desktop/"
import "qrc:/resources/qml/screens/home/pages/objects/object/popups/"
import "qrc:/resources/js/popups.js" as Popups
import "qrc:/resources/js/desktop/popups.js" as DesktopPopups


AjaxPopup {
    id: popup
    width: 360
    height: cameraCodeField.visible ? 316 + cameraCodeField.height + 10 : 316

    modal: true
    focus: true

    closePolicy: Popup.CloseOnEscape | Popup.NoAutoClose

    property var roomIndex: null
    property var camType: null
    property var info: null
    property var selectedDevice: null

    onSelectedDeviceChanged: {
        if (!popup.selectedDevice) {
            chooseCamera.text = ""
            cameraCodeField.visible = false
            return
        }

        if (popup.selectedDevice.isEncrypt == 1) {
            cameraCodeField.visible = true
        } else {
            cameraCodeField.visible = false
        }

        if (popup.selectedDevice.type == "camera") {
            chooseCamera.text = popup.selectedDevice.channelName
            return
        }
        if (popup.selectedDevice.type == "device") {
            chooseCamera.text = popup.selectedDevice.deviceName
            return
        }
        chooseCamera.text = ""
    }

    Rectangle {
        width: popup.width
        height: popup.height
        color: "#252525"

        radius: 3
        border.width: 1
        border.color: "#1a1a1a"

        AjaxPopupCloseHeader {
            id: closeItem
            label: tr.add_camera
        }

        Image {
            id: hikLogo
            source: {
                if (camType == 5) return "qrc:/resources/images/defaults/safire-logo.png"
                return "qrc:/resources/images/defaults/hikvision-logo.png"
            }
            anchors {
                top: closeItem.bottom
                topMargin: camType == 5 ? 4 : -15
                horizontalCenter: parent.horizontalCenter
            }
        }

        AjaxTextField {
            id: cameraNameField
            placeholderText: tr.name
            width: popup.width - 64
            maximumLength: 24
            focus: true

            onActiveFocusChanged: {
                if (!valid) {
                    valid = true
                }
            }

            anchors {
                top: hikLogo.bottom
                topMargin: 26
                horizontalCenter: parent.horizontalCenter
            }

            onTextChanged: {
                cameraNameField.text = util.validator(text, 24)
            }

            Image {
                source: "qrc:/resources/images/icons/ic-popup-info@2x.png"

                anchors {
                    right: parent.right
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
            id: roomsCombobox
            width: popup.width
            miniText: tr.room
            model: rooms.room_names
            currentIndex: roomIndex
            anchors {
                top: cameraNameField.bottom
                topMargin: 12
                horizontalCenter: parent.horizontalCenter
            }

            func: function() {
                addDeviceArea.clicked(true)
            }
        }

        AjaxTextField {
            id: chooseCamera
            placeholderText: tr.camera
            width: popup.width - 64
            readOnly: true
            text: ""

            anchors {
                top: roomsCombobox.bottom
                topMargin: 4
                horizontalCenter: parent.horizontalCenter
            }

            Image {
                sourceSize.width: 34
                sourceSize.height: 34
                source: "qrc:/resources/images/icons/ic-menu-camera.png"

                anchors {
                    right: parent.right
                    rightMargin: -6
                    verticalCenter: parent.verticalCenter
                }
            }

            MouseArea {
                id: chooseCameraArea
                anchors.fill: parent
                hoverEnabled: true
                cursorShape: Qt.PointingHandCursor

                onClicked: {
                    if (!chooseCamera.valid) chooseCamera.valid = true
                    Popups.choose_hikvision_safire_camera_popup(info)
                }
            }
        }

        AjaxTextField {
            id: cameraCodeField
            placeholderText: tr.verification_code
            width: popup.width - 64
            echoMode: TextInput.Password
            visible: false
            text: ""

            onActiveFocusChanged: {
                if (!valid) {
                    valid = true
                }
            }

            anchors {
                top: chooseCamera.bottom
                topMargin: 12
                horizontalCenter: parent.horizontalCenter
            }

            Keys.onEnterPressed: {
                addDeviceArea.clicked(true)
            }

            Keys.onReturnPressed: {
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
                text: tr.add_camera
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
                var cameraName = cameraNameField.text.trim()
                var cameraDevice = chooseCamera.text.trim()
                var cameraCode = cameraCodeField.text.trim()

                if (!cameraName || !cameraDevice || (cameraCodeField.visible && !cameraCode)) {
                    if (!cameraName) {
                        cameraNameField.focus = false
                        cameraNameField.valid = false
                    }

                    if (!cameraDevice) {
                        chooseCamera.focus = false
                        chooseCamera.valid = false
                    }

                    if (cameraCodeField.visible && !cameraCode) {
                        cameraCodeField.focus = false
                        cameraCodeField.valid = false
                    }

                    Popups.text_popup(tr.information, tr.please_fill_in_all_of_the_required_fields)
                    return
                }

                if (roomsCombobox.currentIndex >= 0) {
                        var room = rooms.get_room(roomsCombobox.currentIndex)
                        settings["room_id"] = room.id
                     }

                DesktopPopups.please_wait_popup()
                client.add_hikvision_safire_camera(popup.selectedDevice, camType, cameraName, room_id, cameraCode)
            }
        }
    }

    Connections {
        target: client
        onActionSuccess: {
            popup.close()
        }
    }

    Connections {
        target: hubScreen

        onHikvisionSafireCamSelected: {
            popup.selectedDevice = data
        }
    }
}