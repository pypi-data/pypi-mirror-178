import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13

import "qrc:/resources/js/popups.js" as Popups
import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/qml/screens/home/pages/parts/"
import "qrc:/resources/qml/screens/home/pages/objects/parts/"


Rectangle {
    id: viewNote

    color: ui.colors.dark3

    property var currentIndex: notes.currentIndex
    property var model: null

    ScrollView {
        id: noteViewScroll
        anchors.fill: parent
        anchors.bottomMargin: 72
        clip: true

        ColumnLayout {
            id: column
            width: noteViewScroll.width
            spacing: 0

            Rectangle {
                Layout.fillWidth: true
                Layout.preferredHeight: 112
                color: "transparent"
                visible: notesTab.isEditable

                Custom.Button {
                    id: editNoteButton

                    width: parent.width - 176
                    anchors {
                        top: parent.top
                        topMargin: 16
                        right: parent.right
                        rightMargin: 16
                    }
                    text: tr.edit
                    transparent: true

                    onClicked: {
                        loader.setSource("qrc:/resources/qml/screens/home/pages/objects/object/tabs/additional_info/EditNote.qml", {"model": model})
                    }
                }
            }

            Delimiter {
                visible: notesTab.isEditable
            }

            Item {
                Layout.preferredHeight: noteDescription.height + 32
                Layout.fillWidth: true

                Custom.TextFieldStatic {
                    id: noteDescription

                    width: parent.width - 48
                    anchors {
                        top: parent.top
                        topMargin: 16
                        horizontalCenter: parent.horizontalCenter
                    }

                    key: tr.a911_note_text
                    valueText.wrapMode: Text.Wrap
                    value: model ? model.text : ""
//                    valueText.linkAt: console.log(x, y)
                }
            }

            Delimiter {}

             Item {
                id: noteEstimate

                Layout.fillWidth: true
                Layout.preferredHeight: 126

                visible: model && model.expiration_date ? true : false

                Custom.TextFieldStatic {
                    id: dateInfo

                    anchors {
                        top: parent.top
                        left: parent.left
                        topMargin: 16
                        leftMargin: 24
                    }
                    key: tr.a911_valid_until_2
                    value: {
                        if (model && model.timestamp) {
                            var date = new Date(model.timestamp * 1000)
                            return date.toLocaleDateString(application.locale, application.shortDateFormat)
                        }
                        return ""
                    }
                }


                Item {
                    width: parent.width
                    height: 40

                    visible: model ? model.remove_on_expiration : false

                    anchors {
                        bottom: parent.bottom
                        bottomMargin: 16
                        left: parent.left
                        leftMargin: 24
                    }
                    Custom.FontText {
                        width: parent.width

                        color: ui.colors.white
                        text: tr.a911_delete_automatically
                        anchors {
                           verticalCenter: parent.verticalCenter
                           left: parent.left
                           leftMargin: 42
                        }
                    }

                    Image{
                        sourceSize.width: 32
                        sourceSize.height: 40
                        source: "qrc:/resources/images/icons/a-info-badge.svg"
                    }
                }
            }

            Delimiter {
                visible: model ? model.remove_on_expiration : false
            }
        }
    }

    Item {
        width: viewNote.width
        height: 72
        anchors.bottom: viewNote.bottom
        visible: notesTab.isEditable

        Custom.Button {
            id: deleteNote

            width: parent.width - 48
            anchors.centerIn: parent
            text: tr.a911_delete_note
            transparent: true
            color: ui.colors.red1

            onClicked: {
                var deleted_note_info = {}

                deleted_note_info["id"] = model.note["id"]
                deleted_note_info["facility_id"] = facility.id

                function task() {
                    app.facility_note_module.delete_facility_note(deleted_note_info)
                }

                Popups.confirmation_deletion_popup(task)
            }
        }
    }

    Connections {
        target: facility.notes

        onActionSuccess: {
            notes.currentIndex = -1
            loader.source = ""
        }
    }
}