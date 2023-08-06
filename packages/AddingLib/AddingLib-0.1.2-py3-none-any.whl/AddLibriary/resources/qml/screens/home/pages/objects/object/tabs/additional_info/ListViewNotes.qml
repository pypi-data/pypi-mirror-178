import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/js/popups.js" as Popups
import "qrc:/resources/qml/screens/home/pages/parts/"
import "qrc:/resources/qml/screens/home/pages/objects/parts/"

Item {
    id: notesTab

    property bool isEditable: facility.editable_sections.includes("NOTES")

    RowLayout {
        spacing: 8
        anchors.fill: parent

        Rectangle {
            Layout.fillWidth: true
            Layout.fillHeight: true
            color: ui.colors.dark3

            ListView {
                id: notes
                anchors.fill: parent
                clip: true
                property var currentIndex: -1

                boundsBehavior: Flickable.StopAtBounds

                onCurrentIndexChanged: {
                    if (notes.currentIndex == -1) {
                        loader.source = ""
                    }
                }

//                property var currentObject: null

                model: facility.sorted_notes

                property var toFirst: true

                delegate: NotesDelegate {}

                footer: Rectangle {
                    width: parent.width
                    height: 72
                    color: ui.colors.black
                    visible: notesTab.isEditable

                    Custom.RoundedRect {
                        width: parent.width
                        height: parent.height

                        color: ui.colors.dark3
                        radius: 10
                        topRightCorner: notes.currentIndex == notes.model.length - 1 && notes.model.length != 0

                        Custom.Button {
                            id: addNote

                            width: parent.width - 32
                            anchors.centerIn: parent
                            text: tr.a911_add_note
                            transparent: true

                            onClicked: {
                               Popups.add_facility_note()
                            }
                        }
                    }
                }
            }
        }

        Rectangle {
            Layout.fillWidth: true
            Layout.fillHeight: true
            color: ui.colors.dark3

            Loader {
                id: loader
                anchors.fill: parent
            }

            Custom.EmptySpaceLogo {
                size: parent.width / 2
                visible: loader.source == ""
            }
        }
    }
}