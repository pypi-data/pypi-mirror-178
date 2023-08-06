import QtQuick 2.12
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.13

import QtQuick.Controls 1.4 as OldControls
import QtQuick.Controls.Styles 1.4 as OldStyles

import "qrc:/resources/qml/components/desktop/"
import "qrc:/resources/qml/components/911/" as Custom


AjaxPopup {
    id: popup
    objectName: "calendarPopup"
    width: 360
    height: 420
    closePolicy: Popup.CloseOnEscape | Popup.CloseOnPressOutside

    modal: true
    focus: true

    anchors.centerIn: parent

    property var action: null
    property var selectedDate: null
    property var allowFuture: null
    property var allowPast: null
    property var minimumDate: null
    property var maximumDate: null

    background: Rectangle {
        color: ui.colors.black
        opacity: 0.6
        width: application.width
        height: application.height
        x: 0 - parent.x
        y: 0 - parent.y
    }

    contentItem: Rectangle {
        anchors.fill: parent
        color: ui.colors.dark3
        radius: 8

        OldControls.Calendar {
            id: calendar
            width: parent.width
            height: parent.width
            anchors.top: parent.top

            dayOfWeekFormat: Locale.ShortFormat
            locale: application.locale
            frameVisible: false
            selectedDate: {
                if (popup.selectedDate) return popup.selectedDate
                var t = new Date()
                /*if (t.getFullYear() < 1970) {
                    t.setFullYear(t.getFullYear() + 100)
                    console.log("ERROR :: YEAR PROBLEM, NEW DATE IS ", t)
                }*/
                return t
            }

            Component.onCompleted: {
                var t = new Date()
                /*if (t.getFullYear() < 1970) {
                    t.setFullYear(t.getFullYear() + 100)
                    console.log("ERROR :: YEAR PROBLEM, NEW DATE IS ", t)
                }*/

                if (popup.maximumDate) {
                    calendar.maximumDate = popup.maximumDate
                } else if (!popup.allowFuture) {
                    calendar.maximumDate = t
                }

                if (popup.minimumDate) {
                    calendar.minimumDate = popup.minimumDate
                } else if (!popup.allowPast) {
                    calendar.minimumDate = t
                }
            }

            style: Custom.CalendarStyle {}
        }

        Item {
            id: actionPanel
            width: parent.width
            anchors {
                top: calendar.bottom
                bottom: parent.bottom
            }

            Item {
                id: todayButton
                width: parent.width / 2
                height: parent.height
                anchors.left: parent.left

                Custom.FontText {
                    text: tr.a911_today
                    width: parent.width - 36
                    color: ui.colors.green1
                    font.pixelSize: 14
                    font.family: roboto.name
                    font.weight: Font.Light
                    wrapMode: Text.WordWrap
                    verticalAlignment: Text.AlignVCenter
                    horizontalAlignment: Text.AlignHCenter
                    anchors.centerIn: parent
                }

                Custom.HandMouseArea {
                    onClicked: {
                        var t = new Date()
                        /*if (t.getFullYear() < 1970) {
                            t.setFullYear(t.getFullYear() + 100)
                            console.log("ERROR :: YEAR PROBLEM, NEW DATE IS ", t)
                        }*/
                        calendar.selectedDate = t
                    }
                }
            }

            Rectangle {
                width: 1
                height: parent.height - 16
                color: ui.colors.white
                opacity: 0.1
                anchors.centerIn: parent
            }

            Item {
                id: selectButton
                width: parent.width / 2
                height: parent.height
                anchors.right: parent.right

                Custom.FontText {
                    text: tr.confirm
                    width: parent.width - 36
                    color: ui.colors.green1
                    font.pixelSize: 14
                    font.family: roboto.name
                    font.weight: Font.Light
                    wrapMode: Text.WordWrap
                    verticalAlignment: Text.AlignVCenter
                    horizontalAlignment: Text.AlignHCenter
                    anchors.centerIn: parent
                }

                Custom.HandMouseArea {
                    onClicked: {
                        popup.action(calendar.selectedDate)
                        popup.close()
                    }
                }
            }
        }
    }
}
