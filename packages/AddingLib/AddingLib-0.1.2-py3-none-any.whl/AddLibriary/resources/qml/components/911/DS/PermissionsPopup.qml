import QtQuick 2.13
import QtQuick.Controls 2.12

import "qrc:/resources/qml/components/911/DS" as DS


Popup {
    id: popup

    signal choosen(string choice, var duration)

    onChoosen: {
        application.debug("Permission popup -> ".concat(choice))
        close()
    }

    width: 260

    focus: true
    padding: 0
    topPadding: 16
    bottomPadding: 16
    closePolicy: Popup.CloseOnEscape | Popup.CloseOnPressOutside
    x: parent.width - width
    y: parent.height + 8
    enter: Transition {
        NumberAnimation { property: "opacity"; from: 0.0; to: 1.0; duration: 200 }
    }
    exit: Transition {
        NumberAnimation { property: "opacity"; from: 1.0; to: 0.0; duration: 200 }
    }
    background: Rectangle {
        color: ui.backgrounds.high
        radius: 8
    }

    contentItem: Column {
        id: contentContainer

        width: parent.width

        anchors.centerIn: parent

        property var choices: {
            "ONE_HOUR": {text: tr.request_access_hour_desktop, duration: 3600},
            "TWO_HOURS": {text: "2 " + tr.hrs, duration: 7200},
            "FOUR_HOURS": {text: "4 " + tr.hrs, duration: 14400},
            "EIGHT_HOURS": {text: "8 " + tr.hrs, duration: 28800},
            "PERMANENT": {text: tr.permanent_access, duration: 'PERMANENT'},
        }

        Repeater {
            model: Object.keys(contentContainer.choices)

            Rectangle {
                width: parent.width
                height: 40

                color: ui.backgrounds[area.containsMouse ? "high" : "highest"]

                DS.TextBodyMRegular {
                    width: parent.width - 24

                    anchors.centerIn: parent

                    text: contentContainer.choices[modelData].text
                }

                Rectangle {
                    width: parent.width
                    height: 1

                    anchors.bottom: parent.bottom

                    color: ui.backgrounds.base
                }

                DS.MouseArea {
                    id: area

                    onClicked: choosen(modelData, contentContainer.choices[modelData].duration)
                }
            }
        }
    }

    Connections {
        target: app.login_module

        onLogoutSignal: {
            popup.close()
        }
    }
}
