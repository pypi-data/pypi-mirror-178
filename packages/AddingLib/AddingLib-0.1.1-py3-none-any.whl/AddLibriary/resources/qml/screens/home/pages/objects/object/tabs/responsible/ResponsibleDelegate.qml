import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13


import "qrc:/resources/qml/components/911/" as Custom


MouseArea {
    id: dragArea
    property var ix: index
    property var xPersonIndex: person_index
    property var possibleXPersonIndex: -1
    property bool held: false

    width: listView.width
    height: 56

    DropArea {
        anchors { fill: parent; margins: 10 }

        onEntered: {
            if (drag.source.ix != index) {
                drag.source.possibleXPersonIndex = person_index
                listView.model.moveRow(drag.source.ix, index)
            }
        }
    }

    Rectangle {
        id: content

        color: {
            if (currentResponsibleIndex == index) return ui.colors.black
            return dragArea.held ? ui.colors.black : "transparent"
        }
        Behavior on color { ColorAnimation { duration: 100 } }

        Drag.active: dragArea.held
        Drag.source: dragArea
        Drag.hotSpot.x: width / 2
        Drag.hotSpot.y: height / 2

        states: [
            State {
                when: !dragArea.held

                ParentChange { target: content; parent: dragArea }
                AnchorChanges {
                    target: content
                    anchors { horizontalCenter: dragArea.horizontalCenter; verticalCenter: dragArea.verticalCenter }
                }
            },
            State {
                when: dragArea.held

                ParentChange { target: content; parent: listView }
                PropertyChanges { target: content; x: -4; color: ui.colors.dark2 }
                AnchorChanges {
                    target: content
                    anchors { horizontalCenter: undefined; verticalCenter: undefined }
                }
            }
        ]

        width: listView.width
        height: 56

        Custom.HandMouseArea {
            onClicked: {
                currentResponsibleObject = person
                currentResponsibleIndex = index
            }
        }

        Custom.RoundedRect {
            width: parent.width
            height: 56

            radius: 10

            color: {
                if (dragArea.held) return ui.colors.dark2
                return currentResponsibleIndex == index ? ui.colors.black : ui.colors.dark1
            }

            topRightCorner: {
                if (currentResponsibleIndex == -1) return false
                return currentResponsibleIndex == index - 1
            }
            bottomRightCorner: {
                if (currentResponsibleIndex == -1) return false
                return currentResponsibleIndex == index + 1
            }

            RowLayout {
                anchors.fill: parent

                Item {
                    Layout.minimumWidth: 56
                    Layout.maximumWidth: 56
                    Layout.minimumHeight: 56
                    Layout.maximumHeight: 56

                    Custom.UserImage {
                        width: 32
                        height: 32
                        imageSource: ""
                        userName: person ? person.first_name + " " + person.last_name : ""
                        anchors.centerIn: parent
                        fontSize: 12
                    }
                }

                Custom.FontText {
                    Layout.preferredWidth: 180
                    Layout.fillWidth: true
                    Layout.minimumHeight: 56
                    Layout.maximumHeight: 56

                    text: person ? person.first_name + " " + person.last_name : ""
                    color: ui.colors.light3
                    font.pixelSize: 16
                    verticalAlignment: Text.AlignVCenter
                    elide: Text.ElideRight
                    textFormat: Text.PlainText
                }

                Custom.FontText {
                    Layout.preferredWidth: 160
                    Layout.fillWidth: true
                    Layout.minimumHeight: 56
                    Layout.maximumHeight: 56

                    text: person && person.phone_numbers[0] ? person.phone_numbers[0].number : ""
                    color: ui.colors.middle1
                    font.pixelSize: 14
                    verticalAlignment: Text.AlignVCenter
                    elide: Text.ElideRight
                    textFormat: Text.PlainText
                }

                Custom.FontText {
                    Layout.preferredWidth: 160
                    Layout.fillWidth: true
                    Layout.minimumHeight: 56
                    Layout.maximumHeight: 56

                    text: person && person.email_addresses[0] ? person.email_addresses[0].email : ""
                    color: ui.colors.light3
                    font.pixelSize: 14
                    verticalAlignment: Text.AlignVCenter
                    elide: Text.ElideRight
                    textFormat: Text.PlainText
                }

                Item {
                    Layout.minimumWidth: 56
                    Layout.maximumWidth: 56
                    Layout.fillHeight: true
                    visible: responsibleTab.isEditable

                    Custom.DragIcon {
                        anchors.centerIn: parent
                    }

                    Custom.HandMouseArea {
                        anchors.fill: parent

                        pressAndHoldInterval: 100

                        drag.target: held ? content : undefined
                        drag.axis: Drag.YAxis

                        onPressAndHold: {
                            currentResponsibleObject = null
                            currentResponsibleIndex = -1
                            held = true
                        }
                        onReleased: {
                            held = false
                            app.responsible_person_module.re_index_responsible_persons(facility.id, xPersonIndex, possibleXPersonIndex)
                            possibleXPersonIndex = -1
                        }
                    }
                }
            }
        }
    }
}