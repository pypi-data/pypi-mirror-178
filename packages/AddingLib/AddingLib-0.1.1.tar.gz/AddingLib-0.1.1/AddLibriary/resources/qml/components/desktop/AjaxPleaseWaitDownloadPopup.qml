import QtQuick 2.12
import QtQuick.Controls 2.2

import "qrc:/resources/js/popups.js" as Popups


AjaxPopup {
    id: popup
    width: 320
    height: 200

    modal: true
    focus: true

    closePolicy: Popup.NoAutoClose

    property int progress: updater.percents

    Rectangle {
        width: 320
        height: 230
        anchors.fill: parent
        color: ui.colors.dark2
        radius: 10

        SequentialAnimation {
            running: opened
            loops: Animation.Infinite
            NumberAnimation {
                target: logoIco;
                property: "anchors.verticalCenterOffset";
                to: -20;
                duration: 1000;
                easing.type: Easing.OutInQuart
            }
            NumberAnimation {
                target: logoIco;
                property: "anchors.verticalCenterOffset";
                to: 20;
                duration: 1000;
                easing.type: Easing.OutInQuart
            }
        }

        Column {
            anchors.fill: parent

            Item {
                width: parent.width
                height: 3

                Rectangle {
                    id: topLine
                    anchors.centerIn: parent
                    width: 0
                    height: 1
                }
            }

            Item {
                width: parent.width
                height: 120

                Image {
                    id: logoIco
                    sourceSize.width: 96
                    sourceSize.height: 96
                    source: "qrc:/resources/images/icons/a-logo-pro.svg"
                    anchors {
                        verticalCenter: parent.verticalCenter
                        horizontalCenter: parent.horizontalCenter
                    }
                }
            }

            Item {
                width: parent.width
                height: 48

                Text {
                    text: tr.request_send
                    color: ui.colors.white
                    font.family: roboto.name
                    font.pixelSize: 14
                    anchors.centerIn: parent
                }
            }

            Item {
                width: parent.width
                height: 30
                visible: false

                ProgressBar {
                    id: control
                    from: 0
                    value: progress
                    to: 100
                    padding: 2
                    width: parent.width - 64
                    anchors.centerIn: parent

                    background: Rectangle {
                        implicitWidth: parent.width
                        implicitHeight: 4
                        color: ui.colors.white
                        radius: 3
                        opacity: 0.1
                    }

                    contentItem: Item {
                        implicitWidth: parent.width
                        implicitHeight: 4

                        Rectangle {
                            width: control.visualPosition * parent.width
                            height: parent.height
                            radius: 2
                            color: ui.colors.green1

                            Behavior on width {
                                NumberAnimation { duration: 200 }
                            }
                        }
                    }
                }
            }
        }
    }

    Connections {
        target: updater

        onInstallationDone: {
            popup.close()
        }

        onInstallationFailed: {
            popup.close()
        }
    }
}

