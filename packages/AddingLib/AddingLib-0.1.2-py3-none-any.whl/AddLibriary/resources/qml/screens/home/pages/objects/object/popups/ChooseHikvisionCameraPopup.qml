import QtQuick 2.12
import QtQuick.Controls 2.2

import "qrc:/resources/qml/components/desktop/"
import "qrc:/resources/qml/screens/hub/" as Hub


AjaxPopup {
    id: popup
    width: 320
    height: {
        if (devicesView.contentHeight + 200 + 10 > application.height) {
            return application.height - 200
        }
        return devicesView.contentHeight + 10
    }

    modal: true
    focus: true

    property var info: null

    Rectangle {
        width: popup.width
        height: popup.height
        color: "#1a1a1a" //"#252525"

        border.width: 1
        border.color: "#1a1a1a"
        radius: 3

        ListView {
            id: devicesView
            clip: true
            spacing: 6
            boundsBehavior: Flickable.StopAtBounds
            anchors {
                top: parent.top
                topMargin: 4
                left: parent.left
                right: parent.right
                bottom: parent.bottom
                bottomMargin: 4
            }

            ScrollBar.vertical: ScrollBar {
                id: control
                policy: {
                    if (devicesView.contentHeight < devicesView.height) {
                        return ScrollBar.AlwaysOff
                    }
                    return ScrollBar.AlwaysOn
                }

                anchors {
                    top: devicesView.top
                    right: devicesView.right
                    bottom: devicesView.bottom
                }

                contentItem: Rectangle {
                    implicitWidth: 2
                    implicitHeight: 100
                    radius: width / 2
                    color: control.pressed ? "#81e889" : "#9e9e9e"
                    opacity: 0.6
                }

                background: Rectangle {
                    implicitWidth: 2
                    implicitHeight: 100
                    color: "#575757"
                }
            }

            model: info

            delegate: Item {
                width: parent.width
                height: 68 + 70 * modelData.cameras.length

                property var devModelData: modelData

                Item {
                    id: mainDevice
                    width: parent.width
                    height: 68
                    anchors {
                        top: parent.top
                        horizontalCenter: parent.horizontalCenter
                    }

                    Item {
                        width: parent.width - 8
                        height: parent.height
                        anchors {
                            verticalCenter: parent.verticalCenter
                            right: parent.right
                            rightMargin: 4
                        }

                        HikvisionDeviceDelegate {
                            height: parent.height
                            device: modelData
                            main: true
                            color: mainArea.containsMouse ? "#373737" : "#272727"
                            anchors {
                                left: parent.left
                                right: parent.right
                                rightMargin: control.policy == ScrollBar.AlwaysOff ? 0 : 2
                            }

                            MouseArea {
                                id: mainArea
                                anchors.fill: parent
                                hoverEnabled: true
                                cursorShape: Qt.PointingHandCursor

                                onClicked: {
                                    hikvisionSafireCamSelected(modelData)
                                    popup.close()
                                }
                            }
                        }
                    }
                }

                ListView {
                    spacing: 2
                    clip: true
                    width: parent.width
                    anchors {
                        top: mainDevice.bottom
                        topMargin: 2
                        horizontalCenter: parent.horizontalCenter
                        bottom: parent.bottom
                    }

                    model: parent.devModelData.cameras

                    delegate: Item {
                        width: parent.width
                        height: 68

                        Rectangle {
                            width: 4
                            height: 4
                            radius: 2
                            color: notMainArea.containsMouse ? "#60e3ab" : "#fdfdfd"
                            opacity: notMainArea.containsMouse ? 1 : 0.4
                            anchors {
                                verticalCenter: parent.verticalCenter
                                left: parent.left
                                leftMargin: 12
                            }
                        }

                        Item {
                            width: parent.width - 28
                            height: parent.height
                            anchors {
                                verticalCenter: parent.verticalCenter
                                right: parent.right
                                rightMargin: 4
                            }

                            HikvisionDeviceDelegate {
                                height: parent.height
                                device: modelData
                                main: false
                                color: notMainArea.containsMouse ? "#373737" : "#272727"
                                anchors {
                                    left: parent.left
                                    right: parent.right
                                    rightMargin: control.policy == ScrollBar.AlwaysOff ? 0 : 2
                                }

                                MouseArea {
                                    id: notMainArea
                                    anchors.fill: parent
                                    hoverEnabled: true
                                    cursorShape: Qt.PointingHandCursor

                                    onClicked: {
                                        hikvisionSafireCamSelected(modelData)
                                        popup.close()
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}