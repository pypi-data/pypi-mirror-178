import QtQuick 2.12
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/desktop/"
import "qrc:/resources/qml/components/911/" as Custom


AjaxPopup {
    id: popup
    width: 360
    height: 170
    closePolicy: Popup.CloseOnEscape

    property var task: null
    property var popup_text: null

    modal: true
    focus: true

    anchors.centerIn: parent

    background: Rectangle {
        color: "black"
        opacity: 0.6
        width: application.width
        height: application.height
        x: 0 - parent.x
        y: 0 - parent.y
    }

    contentItem: Rectangle {
        anchors.fill: parent
        color: ui.colors.dark3
        clip: true

        Column {
            anchors.fill: parent
            anchors.margins: 32

            Custom.FontText {
                width: parent.width
                height: 64
                text: {
                    if (popup_text) return popup_text
                    return tr.a911_confirm_delete
                }
                color: ui.colors.light1
                font.pixelSize: 16
            }
            Rectangle {
                width: popup.width
                height: 1
                color: ui.colors.dark1
            }
            RowLayout {
                width: parent.width
                height: 72

                Item {
                    Layout.preferredWidth: parent.width / 2
                    Layout.fillHeight: true

                    Custom.Button {
                        width: 136
                        height: 40
                        transparent: true
                        color: ui.colors.white
                        text: tr.cancel
                        anchors.centerIn: parent
                        onClicked: {
                            popup.close()
                        }
                    }
                }

                Item {
                    Layout.preferredWidth: parent.width / 2
                    Layout.fillHeight: true

                    Custom.Button {
                        width: 126
                        height: 40
                        transparent: true
                        color: ui.colors.red1
                        text: tr.delete
                        anchors.centerIn: parent

                        onClicked: {
                            popup.task()
                        }
                    }
                }
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
