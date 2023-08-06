import QtQuick 2.12
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/desktop/"
import "qrc:/resources/qml/components/911/" as Custom


AjaxPopup {
    id: popup
    objectName: "scheduleMenuPopup"
    width: 192 + 16 + parent.width
    height: listView.height + 16
    closePolicy: Popup.CloseOnPressOutside

    focus: true
    modal: true

    anchors.centerIn: null

    x: -208
    y: -8

    onClosed: {
        if (!popup.parent) return
        popup.parent.updateModel()
    }

    background: Item {}

    contentItem: Item {
        anchors.fill: parent

        MouseArea {
            anchors.fill: parent
            onClicked: {
                popup.close()
            }
        }

        Rectangle {
            id: comboView
            width: 192
            height: popup.height
            color: ui.colors.dark2
            radius: 10

            MouseArea {
                anchors.fill: parent
            }

            ListView {
                id: listView
                width: parent.width
                height: contentHeight
                spacing: 0
                interactive: false
                anchors {
                    top: parent.top
                    topMargin: 8
                }

                model: ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"]

                function updateWeekdays() {
                    var temp = []
                    for (var i = 0; i < 7; i++) {
                        if (listView.itemAtIndex(i).daySelected) {
                            temp = temp.concat([listView.itemAtIndex(i).dayName])
                        }
                    }
                    popup.parent.trueWeekdays = temp
                }

                delegate: Rectangle {
                    width: parent.width
                    height: 41
                    color: ui.colors.dark1

                    property var dayName: modelData
                    property alias daySelected: badgeImage.selected

                    Custom.FontText {
                        width: parent.width - 64
                        height: parent.height
                        text: {
                            var temp = application.locale.dayName(popup.parent.weekdaysData[modelData], Locale.LongFormat)
                            return temp.charAt(0).toUpperCase() + temp.slice(1)
                        }
                        color: ui.colors.white
                        opacity: 0.9
                        font.pixelSize: 14
                        horizontalAlignment: Text.AlignLeft
                        verticalAlignment: Text.AlignVCenter
                        anchors {
                            left: parent.left
                            leftMargin: 16
                            verticalCenter: parent.verticalCenter
                        }
                    }

                    Image {
                        id: badgeImage
                        sourceSize.width: 32
                        sourceSize.height: 40
                        source: selected ? greenBadge : defaultBadge
                        anchors {
                            right: parent.right
                            rightMargin: 16
                            verticalCenter: parent.verticalCenter
                        }

                        property var selected: popup.parent.trueWeekdays.includes(modelData)
                        property var greenBadge: "qrc:/resources/images/facilities/a-badge-green.svg"
                        property var defaultBadge: "qrc:/resources/images/facilities/a-badge-default.svg"
                    }

                    Rectangle {
                        width: parent.width
                        height: 1
                        color: ui.colors.black
                        anchors.bottom: parent.bottom
                    }

                    Custom.HandMouseArea {
                        onClicked: {
                            badgeImage.selected = !badgeImage.selected
                            listView.updateWeekdays()
                        }
                    }
                }
            }
        }

        Rectangle {
            width: popup.parent.width
            height: 40
            radius: 10
            color: ui.colors.dark1
            anchors {
                top: parent.top
                topMargin: 8
                left: comboView.right
                leftMargin: 16
            }

            MouseArea {
                anchors.fill: parent
            }

            Custom.FontText {
                width: parent.width - 24
                height: parent.height
                text: popup.parent.weekdaysText
                color: ui.colors.white
                opacity: 0.9
                font.pixelSize: 14
                horizontalAlignment: Text.AlignLeft
                verticalAlignment: Text.AlignVCenter
                anchors {
                    left: parent.left
                    leftMargin: 16
                    verticalCenter: parent.verticalCenter
                }
            }
        }
    }
}
