import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/qml/screens/home/pages/parts/"
import "qrc:/resources/qml/screens/home/pages/objects/parts/"


Rectangle {
    width: notes.width
    height: content.height

    color: ui.colors.black

    MouseArea {
        id: dragArea

        property var ix: index
        property var xNotesIndex: server_index
        property var possibleXNotesIndex: -1
        property bool held: false

        anchors.fill: parent

        DropArea {
            anchors { fill: parent; margins: 10 }

            onEntered: {
                if (drag.source.ix != index) {
                    drag.source.possibleXNotesIndex = server_index
                    notes.model.moveRow(drag.source.ix, index)
                }
            }
        }

        Rectangle {
            id: content

            width: parent.width
            height: 97

            Drag.active: dragArea.held
            Drag.source: dragArea
            Drag.hotSpot.x: width / 2
            Drag.hotSpot.y: height / 2

            color: {
                if (notes.currentIndex == index) return ui.colors.black
                return dragArea.held ? ui.colors.black : "transparent"
            }
            Behavior on color { ColorAnimation { duration: 100 } }

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

                    ParentChange { target: content; parent: notes }
                    PropertyChanges { target: content; x: -4; color: ui.colors.dark1 }
                    AnchorChanges {
                        target: content
                        anchors { horizontalCenter: undefined; verticalCenter: undefined }
                    }
                }
            ]

            Custom.HandMouseArea {
                onClicked: {
                    loader.setSource("qrc:/resources/qml/screens/home/pages/objects/object/tabs/additional_info/NoteView.qml", {"model": model})
                    notes.currentIndex = index
                }
            }

            Component.onCompleted: {
                if (notes.toFirst && (index == 0)) {
                    notes.currentIndex = index
                    loader.setSource("qrc:/resources/qml/screens/home/pages/objects/object/tabs/additional_info/NoteView.qml", {"model": model})
                    notes.toFirst = false
                }
            }

            Custom.RoundedRect {
                width: parent.width
                height: 96
                color: {
                    if (dragArea.held) return ui.colors.dark2
                    return notes.currentIndex == index ? ui.colors.black : ui.colors.dark1
                }
                radius: 10

                topRightCorner: {
                    if (notes.currentIndex == -1) return false
                    return notes.currentIndex == index - 1
                }
                bottomRightCorner: {
                    if (notes.currentIndex == -1) return false
                    return notes.currentIndex == index + 1
                }

                Item {
                    anchors.fill: parent

                    Rectangle {
                        id: noteCircle
                        width: 32
                        height: 32
                        radius: 16

                        anchors.verticalCenter: parent.verticalCenter
                        anchors.left: parent.left
                        anchors.leftMargin: 16

                        color: ui.colors.dark4

                        Custom.FontText {
                            anchors.centerIn: parent
                            text: index + 1
                            color: ui.colors.middle3
                        }
                    }

                    Custom.TextFieldStatic {
                        id: noteTab
                        width: parent.width - 120
                        anchors {
                            left: parent.left
                            leftMargin: 64
                            verticalCenter: parent.verticalCenter

                        }

                        key: {
                            if (!timestamp) return tr.a911_without_date
                            var date = new Date(timestamp * 1000)
                            date = date.toLocaleDateString(application.locale, application.shortDateFormat)
                            return tr.a911_to + " " + date
                        }
                        value: text

                        keyText {
                            width: undefined
                            wrapMode: Text.NoWrap
                        }

                        valueText {
                            maximumLineCount: 2
                            textFormat: Text.PlainText
                            elide: Text.ElideRight
                            lineHeight: 1.23
                            leftPadding: 0
                            rightPadding: 16
                        }

                        Image {
                            anchors.left: parent.keyText.right
                            anchors.leftMargin: 8
                            sourceSize.width: 16
                            sourceSize.height: 16
                            source: timestamp ? "qrc:/resources/images/icons/clock.svg": ""
                        }
                    }

                    Item {
                        width: 40
                        height: 20

                        visible: notesTab.isEditable

                        anchors {
                            verticalCenter: parent.verticalCenter
                            right: parent.right
                            rightMargin: 24
                        }

                        Custom.DragIcon {
                            anchors.centerIn: parent
                        }
                        
                        Custom.HandMouseArea {
                            anchors.fill: parent

                            pressAndHoldInterval: 100

                            drag.target: dragArea.held ? content : undefined
                            drag.axis: Drag.YAxis

                            onPressAndHold: {
                                notes.currentIndex = -1
                                dragArea.held = true
                                loader.source = ""
                            }

                            onReleased: {
                                dragArea.held = false
                                app.facility_note_module.re_index_notes(facility.id, dragArea.xNotesIndex, dragArea.possibleXNotesIndex)
                                dragArea.possibleXNotesIndex = -1
                            }
                        }
                    }
                }
            }
        }
    }
}