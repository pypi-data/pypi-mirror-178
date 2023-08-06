import QtQuick 2.12
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.3

import "qrc:/resources/qml/components/desktop/"
import "qrc:/resources/qml/screens/home/pages/objects/object/popups/"
import "qrc:/resources/js/popups.js" as Popups


AjaxPopup {
    id: popup
    width: application.width
    height: application.height

    focus: true
    modal: false

    closePolicy: Popup.CloseOnEscape | Popup.CloseOnPressOutside

    background: Item {}

    MouseArea {
        anchors.fill: parent
        onClicked: {
            popup.close()
        }
    }

    Rectangle {
        id: rect
        radius: 8
        width: 180
        height: 165
        color: "#0f0f0f"
        opacity: 0.99
        border.width: 0.1
        border.color: "#1a1a1a"

        x: application.width - width - 162
        y: 62
        
        Column {
            anchors.fill: parent
            spacing: 0

            Item {
                width: rect.width
                height: 32

                MouseArea {
                    anchors.fill: parent
                    hoverEnabled: true
                    onEntered: {
                        permAccessText.color = "#60e3ab"
                    }

                    onExited: {
                        permAccessText.color = "#fdfdfd"
                    }

                    onClicked: {
                        popup.close()
                        client.request_hub_access(0)
                    }
                }

                Text {
                    id: permAccessText
                    anchors.centerIn: parent
                    text: tr.permanent_access
                    font.family: roboto.name
                    font.pixelSize: 12
                    color: ui.colors.light1
                    opacity: 0.7
                }
            }

            Rectangle {
                width: rect.width
                height: 1
                opacity: 0.1
            }

            Item {
                width: rect.width
                height: 32

                MouseArea {
                    anchors.fill: parent
                    hoverEnabled: true
                    onEntered: {
                        oneHourText.color = "#60e3ab"
                    }

                    onExited: {
                        oneHourText.color = "#fdfdfd"
                    }

                    onClicked: {
                        popup.close()
                        client.request_hub_access(1)
                    }
                }

                Text {
                    id: oneHourText
                    anchors.centerIn: parent
                    text: "1 " + tr.hrs
                    font.family: roboto.name
                    font.pixelSize: 12
                    color: ui.colors.light1
                    opacity: 0.7
                }
            }

            Rectangle {
                width: rect.width
                height: 1
                opacity: 0.1
            }

            Item {
                width: rect.width
                height: 32

                MouseArea {
                    anchors.fill: parent
                    hoverEnabled: true
                    onEntered: {
                        twoHourText.color = "#60e3ab"
                    }

                    onExited: {
                        twoHourText.color = "#fdfdfd"
                    }

                    onClicked: {
                        popup.close()
                        client.request_hub_access(2)
                    }
                }

                Text {
                    id: twoHourText
                    anchors.centerIn: parent
                    text: "2 " + tr.hrs
                    font.family: roboto.name
                    font.pixelSize: 12
                    color: ui.colors.light1
                    opacity: 0.7
                }
            }

            Rectangle {
                width: rect.width
                height: 1
                opacity: 0.1
            }

            Item {
                width: rect.width
                height: 32

                MouseArea {
                    anchors.fill: parent
                    hoverEnabled: true
                    onEntered: {
                        fourHourText.color = "#60e3ab"
                    }

                    onExited: {
                        fourHourText.color = "#fdfdfd"
                    }

                    onClicked: {
                        popup.close()
                        client.request_hub_access(4)
                    }
                }

                Text {
                    id: fourHourText
                    anchors.centerIn: parent
                    text: "4 " + tr.hrs
                    font.family: roboto.name
                    font.pixelSize: 12
                    color: ui.colors.light1
                    opacity: 0.7
                }
            }

            Rectangle {
                width: rect.width
                height: 1
                opacity: 0.1
            }

            Item {
                width: rect.width
                height: 32

                MouseArea {
                    anchors.fill: parent
                    hoverEnabled: true
                    onEntered: {
                        eightHourText.color = "#60e3ab"
                    }

                    onExited: {
                        eightHourText.color = "#fdfdfd"
                    }

                    onClicked: {
                        popup.close()
                        client.request_hub_access(8)
                    }
                }

                Text {
                    id: eightHourText
                    anchors.centerIn: parent
                    text: "8 " + tr.hrs
                    font.family: roboto.name
                    font.pixelSize: 12
                    color: ui.colors.light1
                    opacity: 0.7
                }
            }
        }
    }
}