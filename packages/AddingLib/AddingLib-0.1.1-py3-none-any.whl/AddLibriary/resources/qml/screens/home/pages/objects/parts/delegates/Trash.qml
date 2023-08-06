import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/qml/screens/home/pages/events/parts"
import "qrc:/resources/qml/screens/home/pages/objects/parts"


Rectangle {
    id: trashDeleg
    width: header.width
    color: ui.colors.dark1
    height: 48

    property var selected: false
    property var hubId: hub_id ? hub_id : ""

    property var header: objectsTable.headerItem

    Rectangle {
        width: parent.width
        height: 1
        color: ui.colors.black
        anchors.bottom: parent.bottom
    }

    ObjectMouseArea {}

    RowLayout {
        spacing: 0
        height: 48

        Item {
            Layout.fillHeight: true
            Layout.minimumWidth: header.headerRow.children[0] ? header.headerRow.children[0].width : 0
            Layout.maximumWidth: Layout.minimumWidth

            Image {
                sourceSize.width: 32
                sourceSize.height: 40
                source: trashDeleg.selected ? "qrc:/resources/images/facilities/a-badge-green.svg" : "qrc:/resources/images/facilities/a-badge-default.svg"
                anchors {
                    right: parent.right
                    rightMargin: 4
                    verticalCenter: parent.verticalCenter
                }

                Custom.HandMouseArea {
                    onClicked: {
                        trashDeleg.selected = !trashDeleg.selected
                        trashFooter.countSelected()
                    }
                }
            }
        }

        TableDivider { isHeader: false }

        Item {
            clip: true
            Layout.fillHeight: true
            Layout.minimumWidth: header.headerRow.children[2] ? header.headerRow.children[2].width : 0
            Layout.maximumWidth: Layout.minimumWidth

            Custom.FontText {
                text: number ? number : ui.empty
                color: ui.colors.light3
                width: parent.width - 16
                font.pixelSize: 14
                wrapMode: Text.WordWrap
                elide: Text.ElideRight
                textFormat: Text.PlainText
                maximumLineCount: 1
                anchors {
                    left: parent.left
                    leftMargin: 12
                    verticalCenter: parent.verticalCenter
                }
            }
        }

        TableDivider { isHeader: false }

        Item {
            clip: true
            Layout.fillHeight: true
            Layout.minimumWidth: header.headerRow.children[4] ? header.headerRow.children[4].width : 0
            Layout.maximumWidth: Layout.minimumWidth

            Custom.FontText {
                text: name ? name : ui.empty
                color: ui.colors.light1
                font.pixelSize: 16
                width: parent.width - 16
                wrapMode: Text.WordWrap
                elide: Text.ElideRight
                textFormat: Text.PlainText
                maximumLineCount: 1
                anchors {
                    left: parent.left
                    leftMargin: 12
                    verticalCenter: parent.verticalCenter
                }
            }
        }

        TableDivider { isHeader: false }

        Item {
            clip: true
            Layout.fillHeight: true
            Layout.minimumWidth: header.headerRow.children[6] ? header.headerRow.children[6].width : 0
            Layout.maximumWidth: Layout.minimumWidth

            Custom.FontText {
                text: address ? address : ui.empty
                color: ui.colors.middle1
                font.pixelSize: 14
                width: parent.width - 16
                wrapMode: Text.WordWrap
                elide: Text.ElideRight
                textFormat: Text.PlainText
                maximumLineCount: 2
                anchors {
                    left: parent.left
                    leftMargin: 12
                    verticalCenter: parent.verticalCenter
                }
            }
        }

        TableDivider { isHeader: false }

        Item {
            clip: true
            Layout.fillHeight: true
            Layout.minimumWidth: header.headerRow.children[8] ? header.headerRow.children[8].width : 0
            Layout.maximumWidth: Layout.minimumWidth

            Custom.FontText {
                text: hub_id ? hub_id : ui.empty
                color: ui.colors.light3
                width: parent.width - 16
                font.pixelSize: 14
                wrapMode: Text.WordWrap
                elide: Text.ElideRight
                textFormat: Text.PlainText
                maximumLineCount: 1
                anchors {
                    left: parent.left
                    leftMargin: 12
                    verticalCenter: parent.verticalCenter
                }
            }
        }

        TableDivider { isHeader: false }

        Item {
            clip: true
            Layout.fillHeight: true
            Layout.minimumWidth: header.headerRow.children[10] ? header.headerRow.children[10].width : 0
            Layout.maximumWidth: Layout.minimumWidth

            Custom.FontText {
                id: removeAfter
                color: removeAfter.date ? ui.colors.red1 : ui.colors.middle1
                width: parent.width - 16
                font.pixelSize: 14
                wrapMode: Text.WordWrap
                elide: Text.ElideRight
                textFormat: Text.PlainText
                maximumLineCount: 2
                anchors {
                    left: parent.left
                    leftMargin: 12
                    verticalCenter: parent.verticalCenter
                }

                property var date: {
                    if (!object) return null
                    if (!object.scheduled_removal) return null
                    if (!object.scheduled_removal.seconds) return null

                    return util.get_timedelta_by_timestamp(object.scheduled_removal)
                }

                text: {
                    if (!removeAfter.date) return ui.empty

                    var trueDate = ""
                    if (removeAfter.date.days) {
                        trueDate += removeAfter.date.days + " " + tr.days + " "
                    }
                    if (removeAfter.date.hours) {
                        trueDate += removeAfter.date.hours + " " + tr.hrs + " "
                    }
                    if (removeAfter.date.minutes) {
                        trueDate += removeAfter.date.minutes + " " + tr.mins + " "
                    }
                    return trueDate
                }
            }
        }
    }
}