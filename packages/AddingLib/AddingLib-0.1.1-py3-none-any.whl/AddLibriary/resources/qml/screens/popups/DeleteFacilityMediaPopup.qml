import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/qml/components/desktop/"


AjaxPopup {
    id: deleteImageMediaPopup
    objectName: "deleteImageMediaPopup"
    width: 360
    height: 168
    closePolicy: Popup.CloseOnEscape
    modal: true
    focus: true
    anchors.centerIn: parent

    property var media: null

    background: Rectangle {
        color: ui.colors.black
        opacity: 0.6
        width: application.width
        height: application.height
        x: 0 - parent.x
        y: 0 - parent.y
    }
    contentItem:  Rectangle {
        id: body
        clip: true
        color:  ui.colors.dark3
        radius: 8
        anchors.fill: parent

        Custom.FontText {
            text: tr.a911_delete_photo
            width: parent.width
            color: ui.colors.light3
            font.pixelSize: 16
            wrapMode: Text.WordWrap
            horizontalAlignment: Text.AlignLeft
            anchors {
                left: parent.left
                leftMargin: 28
                top: parent.top
                topMargin: 33
            }
        }
        Rectangle {
            width: 328
            height: 1
            color: ui.colors.dark1
            anchors {
                bottom: body.bottom
                bottomMargin: 80
                right: body.right
            }
        }
        Item {
            width: 300
            height: 46
            anchors {
                bottom: parent.bottom
                bottomMargin: 20
                horizontalCenter: parent.horizontalCenter
            }
            Item {
               width: 140
               height: 46
               anchors {
                   left: parent.left
                   verticalCenter: parent.verticalCenter
               }
               Custom.Button{
                   width: 136
                   height: 40
                   anchors.centerIn: parent
                   text: tr.cancel
                   color: ui.colors.light1
                   transparent: true
                   onClicked: deleteImageMediaPopup.close()
               }
            }
            Item {
               width: 140
               height: 46
               anchors {
                   right: parent.right
                   verticalCenter: parent.verticalCenter
               }
               Custom.Button {
                    id: deleteButton
                    width: 136
                    height: 40
                    anchors.centerIn: parent
                    text: tr.delete
                    color: ui.colors.red1
                    transparent: true
                    onClicked: {
                        deleteButton.enabled = false
                        app.facility_media_module.delete_facility_media({"id": media.id, "facility_id": media.facility_id})
                    }
                    Connections {
                        target: app
                        onActionSuccess: {
                            deleteButton.enabled = true
                            deleteImageMediaPopup.close()
                        }

                        onActionFailed: deleteButton.enabled = true
                    }
               }
            }
        }
    }
}