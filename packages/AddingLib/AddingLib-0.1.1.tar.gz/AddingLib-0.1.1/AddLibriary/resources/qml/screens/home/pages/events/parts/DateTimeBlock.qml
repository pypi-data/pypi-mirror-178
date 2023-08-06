import QtQuick 2.12
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/animations/" as Anime
import "qrc:/resources/qml/components/911/" as Custom


Item {
    id: dateTimeItem
    width: parent.width
    height: 136

    property var text: ""
    property var date: ""
    property var time: ""
    property var trueDate: null
    property var checked: dateTimeToggle.checked

    property alias dateArea: dateArea
    property alias timeField: timeField
    property alias dateTimeToggle: dateTimeToggle
    property alias dateFieldErrorHighlight: dateFieldErrorHighlight

    Anime.ClickAnimation { id: click }

    onDateChanged: {
        dateTimeItem.trueDate = Date.fromLocaleDateString(application.locale, dateTimeItem.date, application.shortDateFormat)
    }

    Connections {
        target: tr

        onTranslation_changed: {
            if (!dateTimeItem.trueDate) return
            dateTimeItem.date = dateTimeItem.trueDate.toLocaleDateString(application.locale, application.shortDateFormat)
        }
    }

    Rectangle {
        id: dateTimeHeader
        width: parent.width
        height: 40
        color: ui.colors.dark1
        anchors.top: parent.top

        Custom.FontText {
            text: dateTimeItem.text
            width: parent.width - 64
            color: ui.colors.middle1
            font.pixelSize: 16
            font.weight: Font.Light
            wrapMode: Text.WordWrap
            anchors {
                left: parent.left
                leftMargin: 16
                verticalCenter: parent.verticalCenter
            }
        }

        Custom.Toggle {
            id: dateTimeToggle

            checked: false
            anchors {
                right: parent.right
                verticalCenter: parent.verticalCenter
            }

            mouseArea.onClicked: {
                checked = !checked
            }
        }

        Rectangle {
            width: parent.width
            height: 1
            color: ui.colors.black
            anchors.bottom: parent.bottom
        }
    }

    Item {
        id: dateTimeBody
        width: parent.width
        height: 96
        enabled: dateTimeToggle.checked
        opacity: enabled ? 1 : 0.6
        anchors.top: dateTimeHeader.bottom

        Item {
            id: dateItem
            width: 160
            height: 80
            anchors {
                top: parent.top
                left: parent.left
                leftMargin: 16
            }

            Custom.FontText {
                text: tr.a911_date
                width: parent.width
                color: ui.colors.white
                opacity: 0.8
                font.pixelSize: 14
                font.weight: Font.Light
                wrapMode: Text.WordWrap
                anchors {
                    top: parent.top
                    topMargin: 12
                    left: parent.left
                }
            }

            Rectangle {
                id: dateFieldErrorHighlight
                width: parent.width
                height: 40
                radius: 10
                color: ui.colors.dark1
                border.width: 0
                border.color: ui.colors.red1
                anchors {
                    left: parent.left
                    bottom: parent.bottom
                }

                Custom.FontText {
                    width: parent.width - 24
                    text: dateTimeItem.date
                    height: 20
                    color: ui.colors.white
                    opacity: 0.9
                    font.pixelSize: 14
                    verticalAlignment: Text.AlignVCenter
                    anchors {
                        left: parent.left
                        leftMargin: 16
                        verticalCenter: parent.verticalCenter
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

                    onClicked: {
                        timeField.background.border.width = 0
                        dateFieldErrorHighlight.border.width = 0
                    }
                }
            }
        }

        Item {
            id: timeItem
            width: 96
            height: 80
            anchors {
                top: parent.top
                right: parent.right
                rightMargin: 16
            }

            property var incField: timeField.control.cursorPosition < 2 ? "hours" : "minutes"

            Custom.FontText {
                text: tr.a911_time
                width: parent.width
                color: ui.colors.white
                opacity: 0.8
                font.pixelSize: 14
                font.weight: Font.Light
                wrapMode: Text.WordWrap
                anchors {
                    top: parent.top
                    topMargin: 12
                    left: parent.left
                }
            }

            Custom.TextField {
                id: timeField
                width: parent.width - 28
                height: 40
                placeHolderText: "00:00"
                control.leftPadding: 16
                control.text: dateTimeItem.time
                background.radius: 10
                background.color: ui.colors.dark1
                background.border.color: ui.colors.red1
                background.height: height
                control.inputMask: "00:00"
                control.validator: RegExpValidator { regExp: /^(0[0-9 ]|1[0-9 ]|2[0-3 ]|  ):[0-5 ][0-9 ]$/ }
                anchors {
                    left: parent.left
                    bottom: parent.bottom
                    bottomMargin: -4
                }

                Keys.onUpPressed: {
                    upArea.clicked(true)
                }

                Keys.onDownPressed: {
                    downArea.clicked(true)
                }

                control.onTextChanged: {
                    timeField.background.border.width = 0
                    dateFieldErrorHighlight.border.width = 0
                }
            }

            Item {
                width: 12
                height: 6
                anchors {
                    right: parent.right
                    rightMargin: 4
                    verticalCenter: timeField.verticalCenter
                    verticalCenterOffset: -10
                }

                Custom.Triangle {
                    id: upTriangle
                    rotation: 180
                    anchors.centerIn: parent
                }

                Custom.HandMouseArea {
                    id: upArea
                    onClicked: {
                        click.animate(upTriangle)

                        var currentCursorPosition = timeField.control.cursorPosition
                        var data = {
                            "time": timeField.control.text,
                            "value": 1,
                            "field": timeItem.incField,
                        }
                        timeField.control.text = util.increment_time(data)
                        timeField.control.cursorPosition = currentCursorPosition
                        dateTimeItem.time = timeField.control.text
                    }
                }
            }

            Item {
                width: 12
                height: 6
                anchors {
                    right: parent.right
                    rightMargin: 4
                    verticalCenter: timeField.verticalCenter
                    verticalCenterOffset: 4
                }

                Custom.Triangle {
                    id: downTriangle
                    rotation: 0
                    anchors.centerIn: parent
                }

                Custom.HandMouseArea {
                    id: downArea
                    onClicked: {
                        click.animate(downTriangle)

                        var currentCursorPosition = timeField.control.cursorPosition
                        var data = {
                            "time": timeField.control.text,
                            "value": -1,
                            "field": timeItem.incField,
                        }
                        timeField.control.text = util.increment_time(data)
                        timeField.control.cursorPosition = currentCursorPosition
                        dateTimeItem.time = timeField.control.text
                    }
                }
            }
        }
    }
}