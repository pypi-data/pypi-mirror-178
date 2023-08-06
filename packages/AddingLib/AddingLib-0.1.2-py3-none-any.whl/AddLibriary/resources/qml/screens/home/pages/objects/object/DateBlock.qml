import QtQuick 2.12
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/" as Custom


Item {
    id: topLevel
    width: parent.width
    height: 68

    signal clearField()

    property var text: ""
    property var date: ""
    property var valid: true
    property var trueDate: null
    property var timezoneMode: false

    property alias dateArea: dateArea
    property alias clearImage: clearImage

    onDateChanged: {
        if (topLevel.timezoneMode) return
        topLevel.trueDate = Date.fromLocaleDateString(application.locale, topLevel.date, application.shortDateFormat)
    }

    Connections {
        target: tr

        onTranslation_changed: {
            if (!topLevel.trueDate) return
            if (topLevel.timezoneMode) return
            topLevel.date = topLevel.trueDate.toLocaleDateString(application.locale, application.shortDateFormat)
        }
    }

    Custom.FontText {
        text: topLevel.text
        width: parent.width
        color: ui.colors.white
        opacity: 0.5
        font.pixelSize: 14
        font.weight: Font.Light
        wrapMode: Text.WordWrap
        horizontalAlignment: Text.AlignLeft
        anchors {
            top: parent.top
            topMargin: 4
            left: parent.left
        }
    }

    Rectangle {
        width: parent.width
        height: 40
        radius: 10
        color: ui.colors.dark1
        border.color: ui.colors.red3
        border.width: topLevel.valid ? 0 : 1
        anchors {
            left: parent.left
            bottom: parent.bottom
        }

        Custom.FontText {
            width: parent.width - 24
            height: 20
            color: ui.colors.white
            opacity: topLevel.date ? 0.9 : 0.4
            font.pixelSize: 14
            horizontalAlignment: Text.AlignLeft
            verticalAlignment: Text.AlignVCenter
            anchors {
                left: parent.left
                leftMargin: 16
                verticalCenter: parent.verticalCenter
            }

            text: {
                if (topLevel.date) return topLevel.date
                return topLevel.timezoneMode ? tr.hub_time_zone_default : tr.a911_not_chosen + "..."
            }
        }

        Custom.Triangle {
            rotation: -90
            anchors {
                right: parent.right
                rightMargin: 12
                verticalCenter: parent.verticalCenter
            }
        }

        Custom.HandMouseArea {
            id: dateArea
        }

        Image {
            id: clearImage
            opacity: 0.8
            visible: topLevel.date
            source: "qrc:/resources/images/icons/a-delete-button.svg"
            sourceSize.width: 32
            sourceSize.height: 32
            anchors {
                right: parent.right
                rightMargin: 24
                verticalCenter: parent.verticalCenter
            }

            Custom.HandMouseArea {
                onClicked: {
                    topLevel.date = ""
                    clearField()
                }
            }
        }
    }
}