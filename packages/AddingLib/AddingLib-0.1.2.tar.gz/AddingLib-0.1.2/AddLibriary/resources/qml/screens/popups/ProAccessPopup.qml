import QtQuick 2.12
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/desktop/"
import "qrc:/resources/qml/components/911/" as Custom


Menu {
    id: proAccess

    x: - width - 8
    width: 220
    height: 240

    modal: false
    focus: true

    property var hub: null

    onClosed: {
        proAccess.destroy()
    }

    background: Item {}

    contentItem: Rectangle {
        anchors.fill: parent
        color: ui.colors.dark2
        radius: 10

        Column {
            width: parent.width
            anchors {
                top: parent.top
                topMargin: 20
            }

            Repeater {
                id: accessRepeater
                model: ["1_HOUR", "2_HOURS", "4_HOURS", "8_HOURS", "PERMANENT_ACCESS"]

                delegate: Rectangle {
                    width: parent.width
                    height: 40
                    color: ui.colors.black

                    Rectangle {
                        width: parent.width
                        height: parent.height - 1
                        color: ui.colors.dark1

                        Custom.FontText {
                            maximumLineCount: 1
                            color: ui.colors.light3
                            font.pixelSize: 14
                            wrapMode: Text.NoWrap
                            elide: Text.ElideRight
                            textFormat: Text.PlainText
                            horizontalAlignment: Text.AlignLeft
                            verticalAlignment: Text.AlignVCenter
                            anchors {
                                left: parent.left
                                leftMargin: 16
                                verticalCenter: parent.verticalCenter
                            }

                            text: {
                                if (modelData == "1_HOUR") return "1 " + tr.hour
                                if (modelData == "2_HOURS") return "2 " + tr.hours
                                if (modelData == "4_HOURS") return "4 " + tr.hours
                                if (modelData == "8_HOURS") return "8 " + tr.hours
                                if (modelData == "PERMANENT_ACCESS") return tr.permanent_access
                                return ""
                            }
                        }

                        Image {
                            sourceSize.width: 24
                            sourceSize.height: 24
                            source: "qrc:/resources/images/icons/connect.svg"
                            visible: delegArea.containsMouse

                            anchors {
                                right: parent.right
                                rightMargin: 16
                                verticalCenter: parent.verticalCenter
                            }
                        }

                        Custom.HandMouseArea {
                            id: delegArea

                            onClicked: {
                                app.hub_management_module.profi_hub_access_request(hub, modelData)
                            }
                        }
                    }
                }
            }
        }
    }

    Connections {
        target: app

        onActionSuccess: {
            proAccess.close()
        }

        onActionFailed: {
            proAccess.close()
        }
    }
}
