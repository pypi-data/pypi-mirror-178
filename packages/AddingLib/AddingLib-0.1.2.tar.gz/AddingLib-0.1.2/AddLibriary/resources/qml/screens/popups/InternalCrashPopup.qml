import QtQuick 2.12
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.13
import QtQml.Models 2.14
import QtGraphicalEffects 1.12

import "qrc:/resources/qml/components/desktop/"
import "qrc:/resources/qml/components/911/" as Custom


AjaxPopup {
    id: popup
    objectName: "internalCrashPopup"
    width: 384
    height: 536
    closePolicy: Popup.NoAutoClose

    modal: true
    focus: true

    anchors.centerIn: parent

    property var selectedStatus: null

    background: Rectangle {
        color: "black"
        opacity: 0.6
        width: application.width
        height: application.height
        x: 0 - parent.x
        y: 0 - parent.y
    }

    contentItem: Rectangle {
        radius: 10
        color: ui.colors.dark3
        anchors.fill: parent

        Custom.PopupHeader {
            id: header
            width: parent.width
            height: 88
            radius: parent.radius
            title: "Crash Test"
            anchors.top: parent.top
            headerTitle.anchors.leftMargin: 32

            closeArea.onClicked: {
                popup.close()
            }

            Rectangle {
                width: parent.width - 32
                height: 1
                color: ui.colors.middle1
                opacity: 0.1
                anchors {
                    right: parent.right
                    bottom: parent.bottom
                }
            }
        }

        Item {
            id: body

            clip: true
            width: parent.width
            height: 312

            anchors {
                top: header.bottom
                topMargin: 24
            }

            Item {
                width: parent.width - 64
                height: parent.height

                anchors.centerIn: parent

                ListView {
                    clip: true
                    spacing: 5
                    boundsBehavior: Flickable.StopAtBounds
                    anchors.fill: parent

                    model: [
                        "OK",                   // 0
                        "CANCELLED",            // 1
                        "UNKNOWN",              // 2
                        "INVALID_ARGUMENT",     // 3
                        "DEADLINE_EXCEEDED",    // 4
                        "NOT_FOUND",            // 5
                        "ALREADY_EXISTS",       // 6
                        "PERMISSION_DENIED",    // 7
                        "RESOURCE_EXHAUSTED",   // 8
                        "FAILED_PRECONDITION",  // 9
                        "ABORTED",              // 10
                        "OUT_OF_RANGE",         // 11
                        "UNIMPLEMENTED",        // 12
                        "INTERNAL",             // 13
                        "UNAVAILABLE",          // 14
                        "DATA_LOSS",            // 15
                        "UNAUTHENTICATED",      // 16
                    ]

                    ScrollBar.vertical: Custom.ScrollBar {}

                    delegate: Item {
                        width: parent.width
                        height: 48

                        Rectangle {
                            width: parent.width
                            height: parent.height

                            radius: 8
                            color: ui.colors.dark1

                            Custom.FontText {
                                text: modelData
                                color: ui.colors.middle1
                                width: parent.width - 16
                                font.pixelSize: 14
                                font.bold: true
                                wrapMode: Text.Wrap
                                elide: Text.ElideRight
                                textFormat: Text.PlainText
                                maximumLineCount: 1
                                anchors {
                                    left: parent.left
                                    leftMargin: 12
                                    verticalCenter: parent.verticalCenter
                                }
                            }

                            Image {
                                id: badgeImage

                                sourceSize.width: 40
                                sourceSize.height: 40
                                source: "qrc:/resources/images/icons/a-selected-bage-green.svg"

                                visible: popup.selectedStatus == modelData

                                anchors {
                                    right: parent.right
                                    verticalCenter: parent.verticalCenter
                                }
                            }
                        }

                        Custom.HandMouseArea {
                            onClicked: {
                                popup.selectedStatus = modelData
                            }
                        }
                    }
                }
            }
        }

        Item {
            id: btnSaveItem
            width: parent.width
            height: 88
            anchors {
                top: body.bottom
                topMargin: 24
            }

            Rectangle {
                width: parent.width - 32
                height: 1
                color: ui.colors.middle1
                opacity: 0.1
                anchors.right: parent.right
            }

            Custom.Button {
                id: btnSave
                width: parent.width - 64
                text: tr.send
                enabledCustom: popup.selectedStatus
                anchors.centerIn: parent

                onClicked: {
                    app.create_error_event(popup.selectedStatus)
                }
            }
        }
    }

    Connections {
        target: app

        onActionFailed: {
            btnSave.loading = false
            popup.enabled = true
        }

        onActionSuccess: {
            popup.close()
        }
    }
}
