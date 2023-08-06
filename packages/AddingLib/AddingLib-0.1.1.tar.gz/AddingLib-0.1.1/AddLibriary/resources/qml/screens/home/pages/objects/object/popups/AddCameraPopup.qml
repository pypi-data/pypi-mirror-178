import QtQuick 2.12
import QtQuick.Controls 2.2

import "qrc:/resources/qml/components/desktop/"
import "qrc:/resources/qml/screens/home/pages/objects/object/popups/"
import "qrc:/resources/js/popups.js" as Popups
import "qrc:/resources/js/desktop/popups.js" as PopupsDesk


AjaxPopup {
    id: popup
    width: 360
    height: 280

    modal: true
    focus: true

    closePolicy: Popup.CloseOnEscape | Popup.NoAutoClose

    property var roomIndex: null
    property var rooms

    Rectangle {
        width: 360
        height: 280
        color: "#252525"

        radius: 3
        border.width: 1
        border.color: "#1a1a1a"

        AjaxPopupCloseHeader {
            id: closeItem
            label: tr.add_camera
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
                top: closeItem.bottom
                topMargin: 32
                horizontalCenter: parent.horizontalCenter
            }

            onTextChanged: {
                cameraNameField.text = util.validator(text, 24)
            }

            Image {
                source: "qrc:/resources/images/desktop/icons/ic-popup-info@2x.png"

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

        AjaxTextField {
            id: cameraUrlField
            placeholderText: tr.stream_url
            width: popup.width - 64
            validator: RegExpValidator { regExp: /^([a-zA-Z0-9!""#$%&'()*+,-./:;<=>?@[\]^_`{|}~])*$/ }

            onActiveFocusChanged: {
                if (!valid) {
                    valid = true
                }
            }

            anchors {
                top: cameraNameField.bottom
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

        AjaxSettingsCombobox {
            id: roomsCombobox
            width: popup.width
            miniText: tr.room
            model: rooms.room_names
            currentIndex: roomIndex
            anchors {
                top: cameraUrlField.bottom
                topMargin: 12
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
                var cameraUrl = cameraUrlField.text.trim()

                if (!cameraName || !cameraUrl) {
                    if (!cameraName) {
                        cameraNameField.focus = false
                        cameraNameField.valid = false
                    }

                    if (!cameraUrl) {
                        cameraUrlField.focus = false
                        cameraUrlField.valid = false
                    }

                    Popups.text_popup(tr.information, tr.please_fill_in_all_of_the_required_fields)
                    return
                }

                var room_id = rooms.get(roomsCombobox.currentIndex).room_id
                PopupsDesk.please_wait_popup()
                app.hub_management_module.add_rtsp_camera(cameraName, cameraUrl, room_id)
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