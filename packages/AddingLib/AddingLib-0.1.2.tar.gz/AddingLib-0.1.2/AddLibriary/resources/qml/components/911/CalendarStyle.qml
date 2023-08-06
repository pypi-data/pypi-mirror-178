import QtQuick 2.12
import QtQuick.Controls 2.2

import QtQuick.Controls 1.4 as OldControls
import QtQuick.Controls.Styles 1.4 as OldStyles

import "qrc:/resources/qml/components/911/" as Custom


OldStyles.CalendarStyle {
    id: style
    gridVisible: false
    property var now: {
        var t = new Date()
        /*if (t.getFullYear() < 1970) {
            t.setFullYear(t.getFullYear() + 100)
            console.log("ERROR :: YEAR PROBLEM, NEW DATE IS ", t)
        }*/
        return t
    }
    property var maxDate: control.maximumDate
    property var minDate: control.minimumDate

    navigationBar: Custom.RoundedRect {
        width: calendar.width
        height: 60
        radius: 8
        color:  ui.colors.dark3
        topLeftCorner: true
        topRightCorner: true

        Rectangle {
            width: 40
            height: width
            radius: height / 2
            color: leftArrowArea.containsPress ?  ui.colors.dark2 : "transparent"
            opacity: enabled ? 1 : 0.5
            enabled: {
                var currentMonth = style.minDate.getFullYear() * 12 + style.minDate.getMonth() + 1
                var monthCount = control.visibleYear * 12 + control.visibleMonth + 1
                return currentMonth < monthCount
            }
            anchors {
                left: parent.left
                leftMargin: 8
                verticalCenter: parent.verticalCenter
            }

            Image {
                source: "qrc:/resources/images/icons/left-arrow-white.svg"
                sourceSize.width: 10
                sourceSize.height: 18
                anchors {
                    centerIn: parent
                    horizontalCenterOffset: -1
                }
            }

            Custom.HandMouseArea {
                id: leftArrowArea
                onClicked: {
                    control.showPreviousMonth()
                }
            }
        }

        Custom.FontText {
            text: styleData.title
            width: parent.width - 96
            color:  ui.colors.white
            font.pixelSize: 20
            font.styleName: roboto.name
            font.capitalization: Font.Capitalize
            wrapMode: Text.WordWrap
            verticalAlignment: Text.AlignVCenter
            horizontalAlignment: Text.AlignHCenter
            anchors.centerIn: parent
        }

        Rectangle {
            width: 40
            height: width
            radius: height / 2
            color: rightArrowArea.containsPress ?  ui.colors.dark2 : "transparent"
            opacity: enabled ? 1 : 0.5
            enabled: {
                var currentMonth = style.maxDate.getFullYear() * 12 + style.maxDate.getMonth() + 1
                var monthCount = control.visibleYear * 12 + control.visibleMonth + 1
                return currentMonth > monthCount
            }
            anchors {
                right: parent.right
                rightMargin: 8
                verticalCenter: parent.verticalCenter
            }

            Image {
                source: "qrc:/resources/images/icons/right-arrow-white.svg"
                sourceSize.width: 10
                sourceSize.height: 18
                anchors {
                    centerIn: parent
                    horizontalCenterOffset: 1
                }
            }

            Custom.HandMouseArea {
                id: rightArrowArea
                onClicked: {
                    control.showNextMonth()
                }
            }
        }
    }

    dayOfWeekDelegate: Item {
        height: 60

        Custom.FontText {
            text: Qt.locale().dayName(styleData.dayOfWeek, Locale.ShortFormat)
            width: parent.width
            color:  ui.colors.white
            font.pixelSize: 14
            opacity: 0.5
            font.weight: Font.Light
            font.capitalization: Font.Capitalize
            wrapMode: Text.WordWrap
            verticalAlignment: Text.AlignVCenter
            horizontalAlignment: Text.AlignHCenter
            anchors.centerIn: parent
        }
    }

    dayDelegate: Item {
        anchors.fill: parent

        property var today: {
            return (style.now.getMonth() == styleData.date.getMonth()) && (style.now.getFullYear() == styleData.date.getFullYear())  && (style.now.getDate() == styleData.date.getDate())
        }

        Rectangle {
            width: 36
            height: width
            radius: width / 2
            anchors.centerIn: parent
            color: {
                if (styleData.selected) return ui.colors.green1
                if (today) return ui.colors.dark1
                return "transparent"
            }
        }

        Custom.FontText {
            text: styleData.date.getDate()
            width: parent.width
            color: styleData.selected ?  ui.colors.dark3 : ui.colors.white
            font.pixelSize: 16
            opacity: (!styleData.visibleMonth && !styleData.selected) || (styleData.date > control.maximumDate) || (styleData.date < control.minimumDate) ? 0.5 : 1
            font.weight: Font.Light
            wrapMode: Text.WordWrap
            verticalAlignment: Text.AlignVCenter
            horizontalAlignment: Text.AlignHCenter
            anchors.centerIn: parent
        }
    }

    background: Rectangle {
        width: 360
        height: width
        radius: 8
        color:  ui.colors.dark3
    }
}