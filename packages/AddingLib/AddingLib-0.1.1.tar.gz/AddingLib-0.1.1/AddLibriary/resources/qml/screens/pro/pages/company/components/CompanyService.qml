import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/" as Custom


Rectangle {
    id: companyService

    width: parent.width
    height: originalHeight

    clip: true
    radius: 10
    color: "transparent"

    signal toggle()

    border {
        width: 2
        color: {
            if (selected) return ui.colors.green1
            return companyService.comingSoon ? ui.colors.dark1 : ui.colors.middle4
        }
    }

    property var selected: false
    property var title: ""
    property var reasons: []
    property var comingSoon: false

    property var originalHeight: {
        var mainHeight = companyServiceTitle.height + reasonsColumn.height + 12 + 40
        return companyService.comingSoon ? mainHeight + comingSoonTitle.height + 16 : mainHeight
    }

    Item {
        width: parent.width - 32
        height: companyService.originalHeight - 40

        anchors {
            top: parent.top
            topMargin: 16
            horizontalCenter: parent.horizontalCenter
        }

        Image {
            source: "qrc:/resources/images/pro/company/selected.svg"
            sourceSize.width: 24
            sourceSize.height: 20

            visible: companyService.selected

            anchors {
                top: parent.top
                topMargin: 2
                left: parent.left
            }
        }

        Rectangle {
            width: 24
            height: 24
            radius: 4
            color: "transparent"

            visible: !companyService.selected && enabled

            border {
                width: 2
                color: companyService.comingSoon ? ui.colors.middle4 : ui.colors.middle1
            }

            anchors {
                top: parent.top
                left: parent.left
            }
        }

        Item {
            id: companyServiceTitle

            width: parent.width - 56
            height: companyServiceTitleText.lineCount > 1 ? companyServiceTitleText.contentHeight : 24

            anchors {
                top: parent.top
                left: parent.left
                leftMargin: 56
            }

            Custom.FontText {
                id: companyServiceTitleText

                text: companyService.title
                color: companyService.comingSoon ? ui.colors.nonessential : ui.colors.light3

                font.pixelSize: 16
                wrapMode: Text.Wrap
                textFormat: Text.PlainText
                verticalAlignment: Text.AlignVCenter

                anchors.fill: parent
            }
        }

        Column {
            id: reasonsColumn

            width: parent.width - 42
            spacing: 4

            anchors {
                top: companyServiceTitle.bottom
                topMargin: 12
                left: parent.left
                leftMargin: 42
            }

            Repeater {
                model: companyService.reasons
                delegate: Item {
                    width: reasonsColumn.width
                    height: reasonText.contentHeight

                    Custom.FontText {
                        id: reasonMarker

                        text: "•"
                        color: companyService.comingSoon ? ui.colors.nonessential : ui.colors.middle1

                        font.pixelSize: 12
                        wrapMode: Text.Wrap
                        textFormat: Text.PlainText
                        verticalAlignment: Text.AlignVCenter

                        anchors {
                            top: parent.top
                            left: parent.left
                        }
                    }

                    Custom.FontText {
                        id: reasonText

                        text: modelData
                        color: companyService.comingSoon ? ui.colors.nonessential : ui.colors.middle1

                        font.pixelSize: 12
                        wrapMode: Text.Wrap
                        textFormat: Text.PlainText
                        verticalAlignment: Text.AlignVCenter

                        anchors {
                            top: parent.top
                            left: reasonMarker.right
                            leftMargin: 6
                            right: parent.right
                        }
                    }
                }
            }
        }

        Item {
            id: comingSoonTitle

            clip: true
            width: parent.width - 56
            height: companyService.comingSoon ? 24 : 0
            visible: companyService.comingSoon

            anchors {
                top: reasonsColumn.bottom
                topMargin: 16
                left: parent.left
                leftMargin: 56
            }

            Custom.FontText {
                id: comingSoonTitleText

                text: tr.function_coming_soon
                color: ui.colors.light3

                font.pixelSize: 14
                wrapMode: Text.Wrap
                textFormat: Text.PlainText
                verticalAlignment: Text.AlignVCenter

                anchors.fill: parent
            }
        }
    }

    Custom.HandMouseArea {
        onClicked: toggle()
    }
}
