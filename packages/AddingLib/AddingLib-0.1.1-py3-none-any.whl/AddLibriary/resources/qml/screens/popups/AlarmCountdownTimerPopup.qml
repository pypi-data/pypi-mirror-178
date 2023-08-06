import QtQuick 2.12
import QtQuick.Controls 2.2

import "qrc:/resources/qml/components/"
import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/qml/components/desktop/" as CustomDesktop


AjaxPopup {
    id: popup

    width: 384
    height: 486

    modal: true
    focus: true

    closePolicy: Popup.CloseOnEscape | Popup.NoAutoClose

    property var text: ""
    property var timerTime: 3

    function pad(num, size) { return ('000000000' + num).substr(-size); }

    property var action: "PANIC"
    property var ignoreAlarms: false
    property var incidentItem: null

    Rectangle {
        anchors.fill: parent
        color: ui.colors.dark3
        radius: 10

        Custom.PopupHeader {
            id: header

            width: parent.width
            height: 88
            radius: parent.radius
            title: tr.alarm
            anchors.top: parent.top
            headerTitle.anchors.leftMargin: 32

            closeArea.onClicked: {
                popup.close()
            }

            Rectangle {
                width: parent.width - 32
                height: 1
                color: ui.colors.white
                opacity: 0.1
                anchors {
                    right: parent.right
                    bottom: parent.bottom
                }
            }
        }

        Item {
            id: bodyItem
            width: parent.width

            anchors {
                top: header.bottom
                bottom: buttonItem.top
            }

            CustomDesktop.AjaxTimeCircle {
                id: timeCircle

                anchors.centerIn: parent

                animationDuration: 1000
                easingType: Easing.Linear
                size: parent.height * 0.7
                colorCircle: ui.colors.dark4
                colorBackground: ui.colors.red1
                arcBegin: 0
                arcEnd: 360
                lineWidth: 12
                showBackground: true
            }

            Text {
                id: textCircle

                font.family: roboto.name
                font.pixelSize: 32
                color: ui.colors.red1
                text: "3"
                anchors.centerIn: timeCircle
            }

            Timer {
                id: actionTimer

                running: true
                interval: 1000
                repeat: true
                triggeredOnStart: true

                onTriggered: {
                    textCircle.text = pad(timerTime, 1)
                    timerTime -= 1

                    if (timerTime > -1) {
                        timeCircle.arcBegin += 120
                        return
                    }

                    actionTimer.stop()
                    app.hub_management_module.perform_security_action(popup.action, popup.ignoreAlarms, popup.incidentItem)

                    popup.close()
                }
            }
        }

        Item {
            id: buttonItem
            width: parent.width
            height: 88
            anchors.bottom: parent.bottom

            Rectangle {
                width: parent.width - 32
                height: 1
                color: ui.colors.white
                opacity: 0.1
                anchors.right: parent.right
            }

            Item {
                width: parent.width - 64
                height: 48

                anchors.centerIn: parent

                Custom.Button {
                    width: parent.width
                    text: tr.cancel
                    color: ui.colors.red1
                    transparent: true
                    anchors.centerIn: parent

                    onClicked:{
                        popup.close()
                    }
                }
            }
        }
    }
}