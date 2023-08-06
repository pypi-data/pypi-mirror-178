import QtQuick 2.12
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/desktop/"
import "qrc:/resources/qml/components/911/" as Custom


AjaxPopup {
    id: popup
    objectName: "hubsAvailabilityPopup"
    width: 328
    height: header.height + body.height + 10
    closePolicy: Popup.NoAutoClose

    modal: true
    focus: true

    anchors.centerIn: parent

    property var result: []

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
            title: tr.availability_of_hubs
            anchors.top: parent.top
            headerTitle.anchors.leftMargin: 32

            closeArea.onClicked: {
                popup.close()
            }

            Rectangle {
                width: parent.width
                height: 1
                color: ui.colors.black
                anchors.bottom: parent.bottom
            }
        }

        Item {
            id: body
            width: parent.width
            height: listView.height
            anchors.top: header.bottom

            Custom.EmptySpaceLogo {
                size: width / 2
                visible: listView.model.length == 0
            }

            ListView {
                id: listView
                width: parent.width
                height: 424
                clip: true
                spacing: 0
                boundsBehavior: Flickable.StopAtBounds
                headerPositioning: ListView.OverlayHeader

                model: popup.result.result

                ScrollBar.vertical: Custom.ScrollBar {
                    id: control
                    parent: listView
                    anchors {
                        top: parent.top
                        right: parent.right
                        bottom: parent.bottom
                    }

                    policy: {
                        if (listView.contentHeight > listView.height) {
                            return ScrollBar.AlwaysOn
                        }
                        return ScrollBar.AlwaysOff
                    }
                }

                header: Rectangle {
                    width: parent.width
                    height: 33
                    color: ui.colors.dark2

                    Rectangle {
                        width: parent.width
                        height: 1
                        color: ui.colors.black
                        anchors.bottom: parent.bottom
                    }

                    Item {
                        width: parent.width / 2
                        height: parent.height
                        anchors.left: parent.left

                        Custom.FontText {
                            width: parent.width
                            height: parent.height
                            text: tr.object_number
                            color: ui.colors.middle1
                            font.pixelSize: 12
                            verticalAlignment: Text.AlignVCenter
                            horizontalAlignment: Text.AlignHCenter
                            elide: Text.ElideRight
                            textFormat: Text.PlainText
                            wrapMode: Text.WordWrap
                            maximumLineCount: 1
                            anchors.centerIn: parent
                        }
                    }

                    Item {
                        width: parent.width / 2
                        height: parent.height
                        anchors.right: parent.right

                        Custom.FontText {
                            width: parent.width - 16
                            height: parent.height
                            text: "%"
                            color: ui.colors.middle1
                            font.pixelSize: 12
                            verticalAlignment: Text.AlignVCenter
                            horizontalAlignment: Text.AlignHCenter
                            elide: Text.ElideRight
                            textFormat: Text.PlainText
                            wrapMode: Text.WordWrap
                            maximumLineCount: 1
                            anchors.centerIn: parent
                        }
                    }
                }

                delegate: Rectangle {
                    width: parent.width
                    height: 49
                    color: ui.colors.dark1

                    Rectangle {
                        width: parent.width
                        height: 1
                        color: ui.colors.black
                        anchors.bottom: parent.bottom
                    }

                    Item {
                        width: parent.width / 2
                        height: parent.height
                        anchors.left: parent.left

                        Custom.FontText {
                            width: parent.width - 16
                            height: parent.height
                            text: modelData.registration_number
                            color: ui.colors.light3
                            font.pixelSize: 14
                            verticalAlignment: Text.AlignVCenter
                            horizontalAlignment: Text.AlignHCenter
                            elide: Text.ElideRight
                            textFormat: Text.PlainText
                            wrapMode: Text.WordWrap
                            maximumLineCount: 1
                            anchors.centerIn: parent
                        }
                    }

                    Item {
                        width: parent.width / 2
                        height: parent.height
                        anchors.right: parent.right

                        Custom.FontText {
                            width: parent.width
                            height: parent.height
                            text: modelData.availability_percent
                            color: ui.colors.light3
                            font.pixelSize: 14
                            verticalAlignment: Text.AlignVCenter
                            horizontalAlignment: Text.AlignHCenter
                            elide: Text.ElideRight
                            textFormat: Text.PlainText
                            wrapMode: Text.WordWrap
                            maximumLineCount: 1
                            anchors.centerIn: parent
                        }
                    }
                }
            }
        }
    }
}