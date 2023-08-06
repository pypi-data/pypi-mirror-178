import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/qml/screens/home/pages/parts/"
import "qrc:/resources/qml/screens/home/pages/objects/parts/"


Rectangle {
    id: additionalInfo
    color: ui.colors.black

    property var currentNotesIndex: 0

    ColumnLayout {
        anchors.fill: parent
        spacing: 1

        Header {
            Layout.minimumHeight: 48
            Layout.maximumHeight: 48
            Layout.fillWidth: true
        }

        Item {
            Layout.fillWidth: true
            Layout.fillHeight: true

            RowLayout {
                id: info
                anchors.fill: parent

                spacing: 8

                Sidebar {
                    Layout.minimumWidth: parent.width / 3
                    Layout.maximumWidth: parent.width / 3
                    Layout.fillHeight: true
                }

                StackLayout {
                    Layout.fillWidth: true
                    Layout.fillHeight: true

                    currentIndex: currentNotesIndex

                    Item {
                        ListViewNotes {
                            anchors.fill: parent
                        }
                    }

                    Rectangle {
                        color: ui.colors.dark3

                        Loader {
                            id: loader
                            anchors.fill: parent
                            source: "qrc:/resources/qml/screens/home/pages/objects/object/tabs/additional_info/AdditionalView.qml"
                        }
                    }
                }
            }
        }

    }

    Component.onCompleted: {
        if (!facility.id) return

        app.facility_note_module.start_stream_object_notes(facility.id, "")
    }
}
