import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13

import "qrc:/resources/js/popups.js" as Popups
import "qrc:/resources/qml/components/911/" as Custom


Rectangle {
    id: syncedStatus
    Layout.minimumWidth: timeRect.width + 16
    Layout.maximumWidth: timeRect.width + 16
    Layout.fillHeight: true
    color: "transparent"
    visible: !app.synced

    Rectangle {
        id: timeRect
        width: panicText.width + 56
        height: parent.height - 24
        radius: height / 2
        color: ui.colors.dark4
        anchors.verticalCenter: parent.verticalCenter

        Image {
            id: panicIcon
            sourceSize.width: 24
            sourceSize.height: 24
            source: "qrc:/resources/images/icons/panic.svg"
            anchors {
                left: parent.left
                leftMargin: 8
                verticalCenter: parent.verticalCenter
            }
        }

        Custom.FontText {
            id: panicText
            text: tr.attention_time_synchronization_911
            color: ui.colors.red1
            font.pixelSize: 14
            width: contentWidth
            height: parent.height
            wrapMode: Text.NoWrap
            verticalAlignment: Text.AlignVCenter
            anchors {
                left: panicIcon.right
                leftMargin: 8
                verticalCenter: parent.verticalCenter
            }

            Connections {
                target: tr

                onTranslation_changed: {
                    // not repainting (wtf?)
                    panicText.text = ""
                    panicText.text = tr.attention_time_synchronization_911
                }
            }
        }

        Custom.HandMouseArea {
            id: panicArea
            onClicked: {
                Popups.time_sync_popup()
            }
        }
    }
}