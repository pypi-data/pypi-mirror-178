import QtQuick 2.12
import QtQuick.Controls 2.2

import "qrc:/resources/qml/components/desktop/"
import "qrc:/resources/qml/screens/home/pages/objects/object/popups/"
import "qrc:/resources/js/desktop/popups.js" as Popups


AjaxPopup {
    id: popup
    width: 360
    height: 410

    modal: true
    focus: true

    closePolicy: Popup.CloseOnEscape | Popup.NoAutoClose

    property var room_id: null

    Rectangle {
        width: 360
        height: 410
        color: "#252525"

        radius: 3
        border.width: 1
        border.color: "#1a1a1a"

        AjaxPopupCloseHeader {
            id: closeItem
            label: tr.add_room
        }

        Text {
            id: infoLabel
            text: tr.name_and_photo_can_be_changed_anytime_from_room_settings_screen
            width: parent.width - 24
            horizontalAlignment: Text.AlignHCenter
            wrapMode: Text.WordWrap
            color: ui.colors.light1
            font.family: roboto.name
            font.pixelSize: 12
            opacity: 0.5

            anchors {
                top: closeItem.bottom
                topMargin: 34
                horizontalCenter: parent.horizontalCenter
            }
        }

        ImageRectNew {
            id: imageRect
            uploadAvailable: true
            sourceImage: "WRONG"
            anchors {
                top: infoLabel.bottom
                topMargin: 48
                horizontalCenter: parent.horizontalCenter
            }

            property var imageData: null
            property var trueUrl: null

            onImageDataChanged: {
                if (imageData) {
                    app.process_image(imageData, "room")
                }
            }

            uploadArea.onClicked: {
                imageFileDialog.target = imageRect
                imageFileDialog.isRounded = true
                imageFileDialog.open()
            }

            deleteArea.onClicked: {
                sourceImage = "WRONG"
                trueUrl = null
            }
        }

        AjaxSettingsTextField {
            id: roomNameField

            miniText: tr.room_name

            width: popup.width - 64

            field.onActiveFocusChanged: {
                if (!valid) {
                    valid = true
                }
            }

            field.focus: true

            field.onTextChanged: {
                roomNameField.field.text = util.validator(field.text, 24)
                return
            }

            anchors {
                top: imageRect.bottom
                topMargin: 32
                horizontalCenter: parent.horizontalCenter
            }

            Keys.onEnterPressed: {
                addRoomArea.clicked(true)
            }

            Keys.onReturnPressed: {
                addRoomArea.clicked(true)
            }
        }

        MouseArea {
            id: addRoomArea
            width: parent.width
            height: 48
            hoverEnabled: true
            cursorShape: Qt.PointingHandCursor

            Text {
                anchors.centerIn: parent
                text: tr.add_room
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
                var roomName = roomNameField.field.text.trim()
                if (!roomName) {
                    roomNameField.field.focus = false
                    roomNameField.field.valid = false
                    Popups.text_popup(tr.information, tr.please_fill_in_all_of_the_required_fields)
                    return
                }
                var imagePresent = imageRect.trueUrl ? true : false
                Popups.please_wait_popup()
                app.hub_management_module.add_room(hub, roomName)
            }
        }
    }

    Connections {
        target: app
        onActionSuccess: {
            popup.close()
        }
    }

    Connections {
        target: app
        onNewImageReady: {
            imageRect.sourceImage = data["path"]
        }
    }

    Connections {
        target: app.hub_management_module
        onAddRoomSuccess: {
            if (imageRect.imageData) {
                var settings = {}
                settings["url"] = imageRect.sourceImage
                settings["hub_id"] = hub.hub_id
                settings["room_id"] = room.room_id
                app.hub_management_module.upload_room_photo(settings)
            }
        }
    }
}