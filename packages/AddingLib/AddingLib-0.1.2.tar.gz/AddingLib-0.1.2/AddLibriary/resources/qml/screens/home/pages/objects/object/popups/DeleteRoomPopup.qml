import QtQuick 2.12
import QtQuick.Controls 2.2

import "qrc:/resources/qml/components/desktop/"
import "qrc:/resources/qml/screens/home/pages/objects/object/popups/"
import "qrc:/resources/js/desktop/popups.js" as Popups


AjaxPopup {
    id: popup
    width: 336
    height: 430

    modal: true
    focus: true

    closePolicy: Popup.CloseOnEscape | Popup.NoAutoClose

    property var room: null

    Rectangle {
        width: 336
        height: 430
        color: "#252525"

        radius: 3
        border.width: 1
        border.color: "#1a1a1a"

        AjaxPopupCloseHeader {
            id: closeItem
            label: tr.delete_room
        }

        ImageRectNew {
            id: imageRect
            uploadAvailable: false
            sourceImage: room.small_image_link
            anchors {
                top: closeItem.bottom
                topMargin: 64
                horizontalCenter: parent.horizontalCenter
            }
        }

        Text {
            id: roomNameLabel
            text: room.name
            color: ui.colors.light1
            font.family: roboto.name
            font.pixelSize: 14
            anchors {
                top: imageRect.bottom
                topMargin: 16
                horizontalCenter: parent.horizontalCenter
            }
        }

        Text {
            id: infoLabel
            width: parent.width - 24
            text: util.insert(tr.you_are_about_to_delete_room_all_settings_will_be_erased_continue, [room.name])
            horizontalAlignment: Text.AlignHCenter
            wrapMode: Text.WordWrap
            color: ui.colors.light1
            font.family: roboto.name
            font.pixelSize: 12
            opacity: 0.6
            anchors {
                top: roomNameLabel.bottom
                topMargin: 32
                horizontalCenter: parent.horizontalCenter
            }
        }

        AjaxSaveCancel {
            anchors.bottom: parent.bottom

            saveText: tr.delete

            cancelArea.onClicked: {
                popup.close()
            }

            saveArea.onClicked: {
                Popups.please_wait_popup()
                app.hub_management_module.delete_room(hub, room.room_id)
            }
        }

    }

    Connections {
        target: app
        onActionSuccess: {
            popup.close()
        }
        onActionFailed: {
            popup.close()
        }
    }
}