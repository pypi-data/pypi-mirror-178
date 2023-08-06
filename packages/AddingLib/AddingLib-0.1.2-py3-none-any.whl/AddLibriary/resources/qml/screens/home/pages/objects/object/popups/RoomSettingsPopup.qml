import QtQuick 2.12
import QtQuick.Controls 2.2


import "qrc:/resources/qml/components/desktop/"
import "qrc:/resources/qml/screens/home/pages/objects/object/managements/views"
import "qrc:/resources/qml/screens/home/pages/objects/object/popups/"

import "qrc:/resources/js/desktop/popups.js" as Popups


AjaxPopup {
    id: popup
    width: 360
    height: 440

    closePolicy: Popup.CloseOnEscape | Popup.NoAutoClose

    property var room: null
    property var devEnable: true

    Rectangle {
        width: 360
        height: 440
        color: "#252525"

        radius: 3
        border.width: 1
        border.color: "#1a1a1a"

        AjaxPopupCloseHeader {
            id: closeItem
            label: room.name
        }

        ImageRectNew {
            id: imageRect

            property var isUploadAvailable: {
                if (!hub) return false
                if (!hub.online) return false
                if (hub.state == "ARMED" || hub.state == "NIGHT_MODE") return false
                return true
            }

            uploadAvailable: isUploadAvailable
            sourceImage: room.small_image_link
            enabled: devEnable
            anchors {
                top: closeItem.bottom
                topMargin: 32
                horizontalCenter: parent.horizontalCenter
            }

            property var imageData: null

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
                var settings = {}
                settings["hub_id"] = hub.hub_id
                settings["room_id"] = room.room_id
                app.hub_management_module.delete_room_photo(settings)
            }
        }

        AjaxSettingsTextField {
            id: roomNameField

            miniText: tr.room_name
            field.text: room.name
            enabled: devEnable
            width: popup.width - 64
            anchors {
                top: imageRect.bottom
                topMargin: 32
                horizontalCenter: parent.horizontalCenter
            }

            anchors {
                top: imageRect.bottom
                topMargin: 32
                horizontalCenter: parent.horizontalCenter
            }

            field.focus: true

            Keys.onEnterPressed: {
                saveCancel.saveArea.clicked(true)
            }

            Keys.onReturnPressed: {
                saveCancel.saveArea.clicked(true)
            }

            field.onActiveFocusChanged: {
                if (!valid) {
                    valid = true
                }
            }

            field.onTextChanged: {
                roomNameField.field.text = util.validator(field.text, 24)
                return
            }
        }

        AjaxButton {
            text: tr.delete_room
            opacity: devEnable ? 1 : 0.3
            enabled: devEnable
            width: 200
            color: ui.colors.light1

            anchors {
                top: roomNameField.bottom
                topMargin: 48
                horizontalCenter: parent.horizontalCenter
            }

            onClicked: {
                Popups.room_delete_popup(room)
            }
        }

        AjaxSaveCancel {
            id: saveCancel
            anchors.bottom: parent.bottom
            saveArea.enabled: devEnable

            cancelArea.onClicked: {
                popup.close()
            }

            saveArea.onClicked: {
                var roomName = roomNameField.field.text.trim()
                if (!roomName) {
                    roomNameField.field.focus = false
                    roomNameField.field.valid = false
                    Popups.text_popup(tr.information, tr.please_fill_in_all_of_the_required_fields)
                    return
                }

                Popups.please_wait_popup()
                app.hub_management_module.apply_update(management, room, {"name": {"name": roomName}})
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
            var settings = {}
            settings["url"] = data["path"]
            settings["hub_id"] = hub.hub_id
            settings["room_id"] = room.room_id
            app.hub_management_module.upload_room_photo(settings)
        }
    }
}
