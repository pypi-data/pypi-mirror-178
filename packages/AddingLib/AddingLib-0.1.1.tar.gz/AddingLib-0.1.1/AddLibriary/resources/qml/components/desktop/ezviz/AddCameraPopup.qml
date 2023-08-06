import QtQuick 2.12
import QtQuick.Controls 2.2

import "qrc:/resources/qml/components/desktop/"
import "qrc:/resources/js/popups.js" as Popups


AjaxPopup {
    id: popup
    width: 300
    height: 240

    modal: true
    focus: true

    closePolicy: Popup.CloseOnEscape | Popup.NoAutoClose

    Rectangle {
        width: parent.width
        height: parent.height
        color: "#252525"

        radius: 3
        border.width: 1
        border.color: "#1a1a1a"

        AjaxPopupCloseHeader {
            id: closeItem
            label: tr.add_camera
        }


        AjaxTextField {
            id: cameraIdField
            placeholderText: tr.device_id
            width: popup.width - 64
            maximumLength: 9
            focus: true
            validator: RegExpValidator { regExp: /^([0-9a-zA-Z]{9})$/ }

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
                cameraIdField.text = util.validator(text, 9)
            }

            Keys.onEnterPressed: {
                addDeviceArea.clicked(true)
            }

            Keys.onReturnPressed: {
                addDeviceArea.clicked(true)
            }
        }

        AjaxTextField {
            id: cameraCodeField
            placeholderText: tr.verification_code
            width: popup.width - 64
            echoMode: TextInput.Password

            onActiveFocusChanged: {
                if (!valid) {
                    valid = true
                }
            }

            anchors {
                top: cameraIdField.bottom
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
                var cameraId = cameraIdField.text.trim()
                var cameraCode = cameraCodeField.text.trim()

                if (!cameraId || !cameraCode) {
                    if (!cameraId) {
                        cameraIdField.focus = false
                        cameraIdField.valid = false
                    }

                    if (!cameraCode) {
                        cameraCodeField.focus = false
                        cameraCodeField.valid = false
                    }

                    Popups.text_popup(tr.information, tr.please_fill_in_all_of_the_required_fields)
                    return
                }

                if (!cameraIdField.acceptableInput) {
                    cameraIdField.focus = false
                    cameraIdField.valid = false
                    Popups.text_popup(tr.information, tr.bad_device_id)
                    return
                }

                ezviz.add_camera(cameraId, cameraCode)
            }
        }
    }

    Connections {
        target: ezviz

        onEzvizActionSuccess: {
            popup.close()
        }
    }
}
