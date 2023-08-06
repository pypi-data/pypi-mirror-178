import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/animations/" as Anime
import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/qml/components/desktop/"


AjaxPopup {
    id: popup
    objectName: "removeImmediately"
    width: 360
    height: 120 + moveText.height

    modal: true
    focus: true

    closePolicy: Popup.CloseOnEscape

    anchors.centerIn: parent

    property var facility: null
    property var mode: null

    background: Rectangle {
        color: ui.colors.black
        opacity: 0.6
        width: application.width
        height: application.height
        x: 0 - parent.x
        y: 0 - parent.y
    }

    contentItem: Rectangle {
        id: body
        clip: true
        color:  ui.colors.dark3
        radius: 8
        anchors.fill: parent

        Custom.FontText {
            id: moveText
            text: tr.a911_delete_object_permanently
            width: parent.width - 64
            height: contentHeight
            color: ui.colors.light3
            font.pixelSize: 16
            wrapMode: Text.WordWrap
            horizontalAlignment: Text.AlignLeft
            anchors {
                top: parent.top
                topMargin: 24
                horizontalCenter: parent.horizontalCenter
            }
        }

        Item {
            width: parent.width
            height: 80
            anchors.bottom: parent.bottom

            Rectangle {
                width: parent.width - 32
                height: 1
                color: ui.colors.white
                opacity: 0.1
                anchors {
                    top: parent.top
                    right: parent.right
                }
            }

            Anime.SharinganLoader {
                id: anim
                radius: 13
                color: ui.colors.red1
                useCircle: true
                visible: !popup.enabled
                anchors.centerIn: parent
                anchors.verticalCenterOffset: -4
            }

            Item {
                width: 136
                height: 40
                visible: popup.enabled
                anchors {
                    left: parent.left
                    leftMargin: 32
                    verticalCenter: parent.verticalCenter
                }

                Custom.Button {
                    width: parent.width
                    text: tr.cancel
                    color: ui.colors.white
                    transparent: true
                    anchors.centerIn: parent

                    onClicked: {
                        popup.close()
                    }
                }
            }

            Item {
                width: 136
                height: 40
                visible: popup.enabled
                anchors {
                    right: parent.right
                    rightMargin: 32
                    verticalCenter: parent.verticalCenter
                }

                Custom.Button {
                    width: parent.width
                    text: tr.a911_delete_popup
                    color: ui.colors.red1
                    transparent: true
                    anchors.centerIn: parent

                    onClicked: {
                        popup.enabled = false

                        var settings = {}

                        settings["hub_id"] = facility.hub_id

                        if (popup.mode == "facility") {
                            app.facility_module.remove_channel_911(settings)
                        } else {
                            app.bindings_module.remove_channel_911(settings)
                        }
                    }
                }
            }
        }
    }

    Connections {
        target: app.facility_module

        onRemoveChannel911Success: {
            popup.close()
        }

        onRemoveChannel911Failed: {
            popup.close()
        }
    }

    Connections {
        target: app.bindings_module

        onRemoveChannel911Success: {
            popup.close()
        }

        onRemoveChannel911Failed: {
            popup.close()
        }
    }
}