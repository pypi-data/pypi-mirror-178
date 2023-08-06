import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/qml/screens/home/pages/objects/parts"


Rectangle {
    color: ui.colors.black

    ColumnLayout {
        anchors.fill: parent
        spacing: 0

        Rectangle {
            Layout.fillWidth: true
            Layout.minimumHeight: 64
            Layout.maximumHeight: 64
            color: ui.colors.black

            Custom.RoundedRect {
                radius: 10
                bottomRightCorner: currentObjectIndex == 0
                color: ui.colors.dark4
                anchors.fill: parent

                Image {
                    sourceSize.width: 24
                    sourceSize.height: 24

                    anchors {
                        verticalCenter: parent.verticalCenter
                        left: parent.left
                        leftMargin: 16
                    }

                    source: "qrc:/resources/images/icons/back.svg"

                    Custom.HandMouseArea {
                        anchors.fill: parent

                        onClicked: {
                            currentObjectIndex = -1
                        }
                    }
                }
            }
        }

        Rectangle {
            Layout.fillWidth: true
            Layout.minimumHeight: smallObjectsList.contentHeight
            Layout.maximumHeight: parent.height - 64
            color: ui.colors.black

            ListView {
                id: smallObjectsList
                clip: true
                spacing: 0
                width: parent.width
                height: parent.height
                boundsBehavior: Flickable.StopAtBounds

                model: appCompany.filtered_objects_model

                Component.onCompleted: {
                    smallObjectsList.positionViewAtIndex(currentObjectIndex, ListView.Beginning)
                }

                ScrollBar.vertical: Custom.ScrollBar {
                    id: control
                    parent: smallObjectsList

                    property var lastPosition: 0.0
                    property var direction: 0   // 0 - up, 1 - down
                    property var prevAB: 0

                    onPositionChanged: {
                        if (control.position - control.lastPosition > 0) {
                            control.direction = 1
                        } else {
                            control.direction = 0
                        }
                        control.lastPosition = control.position

                        var a = 1 - (control.position + control.size)
                        var b = 1 - (control.position + control.size/2)

                        if (a/b < 0.4 && control.direction == 1) {
                            if (prevAB >= 0.4) {
                                app.facility_module.get_category(currentMode, false)
                            }
                            if (control.pressed && control.lastPosition) {
                                control.position = control.lastPosition
                            }
                        }

                        control.prevAB = a/b
                    }
                }

                delegate: Rectangle {
                    width: smallObjectsList.width
                    height: 49
                    color: ui.colors.black

                    ObjectMouseArea {}

                    Custom.RoundedRect {
                        width: smallObjectsList.width
                        height: 48
                        radius: 10
                        color: index == currentObjectIndex ? ui.colors.black : ui.colors.dark1
                        topRightCorner: index - 1 == currentObjectIndex
                        bottomRightCorner: index + 1 == currentObjectIndex

                        RowLayout {
                            clip: true
                            width: parent.width - 24
                            height: parent.height
                            anchors.right: parent.right

                            Item {
                                clip: true
                                Layout.fillHeight: true
                                Layout.minimumWidth: parent.width / 2

                                Custom.FontText {
                                    text: {
                                        if (number) return number
                                        if (hub_id) return hub_id
                                        return ui.empty
                                    }
                                    color: ui.colors.light3
                                    font.pixelSize: 14
                                    anchors {
                                        left: parent.left
                                        verticalCenter: parent.verticalCenter
                                    }
                                }
                            }

                            Item {
                                clip: true
                                Layout.fillHeight: true
                                Layout.minimumWidth: parent.width / 2

                                Custom.FontText {
                                    text: {
                                        if (name) return name
                                        if (object.hub_name) return object.hub_name
                                        if (hub_id) return hub_id
                                        return ui.empty
                                    }
                                    color: ui.colors.light1
                                    font.pixelSize: 16
                                    width: parent.width - 16
                                    elide: Text.ElideRight
                                    textFormat: Text.PlainText
                                    anchors {
                                        left: parent.left
                                        verticalCenter: parent.verticalCenter
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }

        Rectangle {
            Layout.fillWidth: true
            Layout.fillHeight: true
            color: ui.colors.black

            Custom.RoundedRect {
                color: ui.colors.dark4
                radius: 10
                topRightCorner: currentObjectIndex == smallObjectsList.model.length - 1
                anchors.fill: parent

                Custom.EmptySpaceLogo {
                    size: parent.width / 2
                    visible: smallObjectsList.model.length == 0
                    anchors {
                        horizontalCenter: parent.horizontalCenter
                        verticalCenter: parent.verticalCenter
                        verticalCenterOffset: -32
                    }
                }
            }
        }
    }
}