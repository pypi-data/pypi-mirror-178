import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13

import "qrc:/resources/js/popups.js" as Popups
import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/qml/screens/home/pages/parts/"
import "qrc:/resources/qml/screens/home/pages/objects/parts/"


Rectangle {
    id: editNote

    color: ui.colors.dark3

    property var model: null
    property var addNote: false
    property var currentIndex: notes.currentIndex

    function get_current_date() {
        var today = new Date();
        /*if (today.getFullYear() < 1970) {
            today.setFullYear(today.getFullYear() + 100)
            console.log("ERROR :: YEAR PROBLEM, NEW DATE IS ", today)
        }*/
        var date = today.toLocaleDateString(application.locale, application.shortDateFormat)
        return date
    }

    ScrollView {
        id: noteEditScroll

        anchors.fill: parent
        anchors.bottomMargin: 72
        clip: true

        ColumnLayout {
            id: column
            width: noteEditScroll.width
            spacing: 0

            Rectangle {
                Layout.fillWidth: true
                Layout.preferredHeight: 112

                visible: !addNote
                color: "transparent"

                Custom.Button {
                    id: editNoteButton

                    width: parent.width - 224
                    color: ui.colors.white
                    anchors {
                        top: parent.top
                        right: parent.right
                        rightMargin: 16
                        topMargin: 16
                    }
                    text: tr.cancel
                    transparent: true

                    onClicked: {
                        loader.setSource("qrc:/resources/qml/screens/home/pages/objects/object/tabs/additional_info/NoteView.qml", {"model": model})
                    }
                }
            }

            Delimiter {
                visible: !addNote
            }

            Item {
                Layout.fillWidth: true
                Layout.preferredHeight: editDescription.height + 32 + (editDescription.valueText.valid ? 0 : 20)

                Custom.TextAreaEdit {
                    id: editDescription

                    width: parent.width - 48
                    distance: 10
                    valueText.maximumLength: 200
                    valueText.control.wrapMode: Text.Wrap
                    valueText.control.horizontalAlignment: Text.AlignLeft
                    valueText.preferredHeight: 80
                    valueText.height: valueText.control.contentHeight + 24 < valueText.preferredHeight ? valueText.preferredHeight : valueText.control.contentHeight + 24
                    valueText.control.height: valueText.control.contentHeight + 24 < valueText.preferredHeight - 8 ? valueText.preferredHeight - 8 : valueText.control.contentHeight + 24

                    anchors.centerIn: parent
                    key: tr.a911_note_text
                    value: model ? model.text : ""


                    Connections {
                        target: app.facility_note_module
                        onNotesErrors: {
                            if (result["3"]) {
                                editDescription.valueText.valid = false
                                editDescription.valueText.error = result["3"].message
                            }
                        }
                    }
                }
            }

            Item {
                Layout.fillWidth: true
                Layout.preferredHeight: 56

                Rectangle {

                    width: parent.width - 48
                    height: 40
                    radius: 10
                    color: ui.colors.dark1
                    anchors.horizontalCenter: parent.horizontalCenter

                    Custom.FontText {
                        width: parent.width
                        text: tr.a911_valid_until_2
                        color: ui.colors.white
                        font.weight: Font.Bold

                        anchors {
                            verticalCenter: parent.verticalCenter
                            left: parent.left
                            leftMargin: 16
                        }
                    }

                    Custom.Toggle {
                        id: noteToggle

                        checked: model && model.expiration_date ? model.expiration_date : false

                        anchors {
                            verticalCenter: parent.verticalCenter
                            right: parent.right
                            rightMargin: 6
                        }

                        mouseArea.onClicked: {
                            checked = !checked
                            if (!checked) {
                                autoDeleteNote.autoDel = false
                            }
                        }
                    }
                }
            }

            Item {
                id: dataItem

                Layout.fillWidth: true
                Layout.preferredHeight: 120

                enabled: noteToggle.checked
                opacity: enabled ? 1 : 0.2

                Item {
                    id: dateBlock
                    width: parent.width
                    height: 40

                    property var trueDate: null

                    Rectangle{
                        width: parent.width - 48
                        height: parent.height
                        radius: 10
                        color: ui.colors.dark1
                        anchors.horizontalCenter: parent.horizontalCenter

                        Custom.FontText {
                            id: dateField
                            width: parent.width - 24
                            height: 20
                            color: ui.colors.white
                            opacity: 0.9
                            font.pixelSize: 14
                            horizontalAlignment: Text.AlignLeft
                            verticalAlignment: Text.AlignVCenter
                            anchors {
                                left: parent.left
                                leftMargin: 16
                                verticalCenter: parent.verticalCenter
                            }

                            text: {
                                if (model && model.timestamp) {
                                    var date = new Date(model.timestamp * 1000)
                                    return date.toLocaleDateString(application.locale, application.shortDateFormat)
                                }
                                return get_current_date()
                            }

                            onTextChanged: {
                                dateBlock.trueDate = Date.fromLocaleDateString(application.locale, dateField.text, application.shortDateFormat)
                            }

                            Connections {
                                target: tr

                                onTranslation_changed: {
                                    if (!dateBlock.trueDate) return
                                    dateField.text = dateBlock.trueDate.toLocaleDateString(application.locale, application.shortDateFormat)
                                }
                            }
                        }

                        Custom.Triangle {
                            rotation: -90
                            anchors {
                                right: parent.right
                                rightMargin: 12
                                verticalCenter: parent.verticalCenter
                            }
                        }

                        Custom.HandMouseArea {
                            id: dateArea

                            onClicked: {
                                function action(date) {
                                    dateField.text = date.toLocaleDateString(application.locale, application.shortDateFormat)
                                }
                                var selectedDate = Date.fromLocaleDateString(application.locale, dateField.text, application.shortDateFormat)
                                var allowFuture = true
                                var allowPast = false
                                Popups.calendar_popup(action, selectedDate, allowFuture, allowPast)
                            }
                        }

                    }
                }

                Item {
                    width: parent.width
                    height: 40

                    anchors {
                        top: dateBlock.bottom
                        topMargin: 16
                    }

                    Image {
                        id: autoDeleteNote

                        sourceSize.width: 32
                        sourceSize.height: 40
                        source: autoDel ? "qrc:/resources/images/facilities/a-badge-green.svg" : "qrc:/resources/images/facilities/a-badge-default.svg"

                        anchors {
                            top: parent.top
                            left: parent.left
                            leftMargin: 24
                        }

                        property var autoDel: {
                            if (!model) return false
                            return noteToggle.checked && model.remove_on_expiration
                        }

                    }

                    Custom.FontText {
                        color: ui.colors.white
                        text: tr.a911_delete_automatically
                        anchors {
                            top: parent.top
                            topMargin: 12
                            left: autoDeleteNote.right
                            leftMargin: 8
                        }
                    }

                    Custom.HandMouseArea {
                        onClicked: {
                            autoDeleteNote.autoDel = !autoDeleteNote.autoDel
                        }
                    }
                }
            }


            Delimiter {}
        }
    }

     Item {
        width: parent.width
        height: 72
        anchors.bottom: parent.bottom

        Custom.Button {
            id: saveChangesNote
            width: parent.width - 48
            anchors.centerIn: parent
            text: tr.save_scenario

            onClicked: {
                var note_info = {}
                note_info["text"] = editDescription.valueText.control.text
                note_info["remove_on_expiration"] = autoDeleteNote.autoDel

                if (noteToggle.checked) {
                    var dateNote = dateField.text
                    dateNote = Date.fromLocaleString(application.locale, dateNote, application.shortDateFormat)
                    dateNote.setHours(23, 59, 59, 999)
                    dateNote = dateNote.getTime() / 1000

                    note_info["expiration_date"] = dateNote
                }

                if (addNote) {
                    app.facility_note_module.create_facility_note(note_info)
                    return
                }
                app.facility_note_module.update_facility_note(currentIndex, note_info)

            }
        }
    }

    Connections {
        target: facility.notes

        onActionSuccess: {
            if(addNote) return
            loader.setSource("qrc:/resources/qml/screens/home/pages/objects/object/tabs/additional_info/NoteView.qml", {"model": model})
        }
    }
}