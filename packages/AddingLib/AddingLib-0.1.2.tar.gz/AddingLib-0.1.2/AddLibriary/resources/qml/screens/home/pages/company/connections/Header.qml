import QtQuick 2.12
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/qml/screens/home/pages/events/parts"


Rectangle {
    Layout.alignment: Qt.AlignTop | Qt.AlignLeft
    color: ui.colors.dark2
    Layout.fillWidth: true
    Layout.minimumHeight: 32
    Layout.maximumHeight: 32
    Layout.rightMargin: 8
    Layout.topMargin: 2

    RowLayout {
        anchors.fill: parent

        Item {
            Layout.minimumWidth: parent.width / 30 * 3 - 1
            Layout.maximumWidth: parent.width / 30 * 3 - 1
            Layout.minimumHeight: parent.height
            Layout.maximumHeight: parent.height
            Layout.leftMargin: 12

            Custom.FontText {
                text: tr.binding_911
                width: parent.width
                maximumLineCount: 2
                color: ui.colors.middle1
                font.pixelSize: 12
                wrapMode: Text.WordWrap
                elide: Text.ElideRight
                textFormat: Text.AutoText

                anchors {
                    verticalCenter: parent.verticalCenter
                    left: parent.left
                }
            }
        }

        Rectangle {
            color:  ui.colors.dark1
            Layout.minimumHeight: parent.height - 12
            Layout.maximumHeight: parent.height - 12
            Layout.minimumWidth: 1
            Layout.maximumWidth: 1
        }

        Item {
            Layout.minimumWidth: parent.width / 30 * 4 - 1
            Layout.maximumWidth: parent.width / 30 * 4 - 1
            Layout.minimumHeight: parent.height
            Layout.maximumHeight: parent.height

            Custom.FontText {
                text: tr.a911_hub_id
                width: parent.width
                maximumLineCount: 2
                color: ui.colors.middle1
                font.pixelSize: 12
                wrapMode: Text.WordWrap
                elide: Text.ElideRight
                textFormat: Text.AutoText

                anchors {
                    verticalCenter: parent.verticalCenter
                    left: parent.left
                }
            }
        }

        Rectangle {
            color:  ui.colors.dark1
            Layout.minimumHeight: parent.height - 12
            Layout.maximumHeight: parent.height - 12
            Layout.minimumWidth: 1
            Layout.maximumWidth: 1
        }

        Item {
            Layout.minimumWidth: parent.width / 30 * 3 - 1
            Layout.maximumWidth: parent.width / 30 * 3 - 1
            Layout.minimumHeight: parent.height
            Layout.maximumHeight: parent.height

            Custom.FontText {
                text: tr.a911_binding_status
                width: parent.width
                color: ui.colors.middle1
                font.pixelSize: 12
                wrapMode: Text.WordWrap
                elide: Text.ElideRight
                textFormat: Text.AutoText

                anchors {
                    verticalCenter: parent.verticalCenter
                    left: parent.left
                }
            }
        }

        Rectangle {
            color:  ui.colors.dark1
            Layout.minimumHeight: parent.height - 12
            Layout.maximumHeight: parent.height - 12
            Layout.minimumWidth: 1
            Layout.maximumWidth: 1
        }

        Item {
            Layout.alignment: Qt.AlignLeft
            Layout.minimumWidth: parent.width / 30 * 4 - 1
            Layout.maximumWidth: parent.width / 30 * 4 - 1
            Layout.minimumHeight: parent.height
            Layout.maximumHeight: parent.height

            Custom.FontText {
                text: tr.account_number
                width: parent.width
                color: ui.colors.middle1
                font.pixelSize: 12
                wrapMode: Text.WordWrap
                elide: Text.ElideRight
                textFormat: Text.AutoText
                horizontalAlignment: Text.AlignLeft

                anchors {
                    verticalCenter: parent.verticalCenter
                    left: parent.left
                }
            }
        }

        Rectangle {
            color:  ui.colors.dark1
            Layout.minimumHeight: parent.height - 12
            Layout.maximumHeight: parent.height - 12
            Layout.minimumWidth: 1
            Layout.maximumWidth: 1
        }

        Item {
            Layout.alignment: Qt.AlignRight
            Layout.minimumHeight: parent.height
            Layout.maximumHeight: parent.height
            Layout.minimumWidth: parent.width / 30 * 16 - 1
            Layout.maximumWidth: parent.width / 30 * 16 - 1

            Custom.FontText {
                text: tr.object_name
                width: parent.width
                color: ui.colors.middle1
                font.pixelSize: 12
                wrapMode: Text.WordWrap
                elide: Text.ElideRight
                textFormat: Text.AutoText
                horizontalAlignment: Text.AlignLeft

                anchors {
                    verticalCenter: parent.verticalCenter
                    left: parent.left
                }
            }
        }
    }
}