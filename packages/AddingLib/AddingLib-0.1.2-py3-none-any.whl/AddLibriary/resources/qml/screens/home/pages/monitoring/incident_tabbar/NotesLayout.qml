import QtQuick 2.12
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/" as Custom


Rectangle {

    color: "transparent"
//    Layout.fillWidth: true
//    Layout.fillHeight: true
    width: parent.width
    height: parent.height

    Custom.EmptySpaceLogo {
        size: parent.width / 4
        visible: notesList.model ? notesList.model.length == 0 : true
    }

    ListView {
        id: notesList

        width: parent.width - 16
        height: parent.height - 44
        clip: true
        spacing: 8

        anchors {
            left: parent.left
            leftMargin: 16
            verticalCenter: parent.verticalCenter
        }

        ScrollBar.vertical: Custom.ScrollBar {
            parent: notesList
            anchors {
                top: parent.top
                right: parent.right
                bottom: parent.bottom
            }

            policy: {
                if (notesList.contentHeight > notesList.height) {
                    return ScrollBar.AlwaysOn
                }
                return ScrollBar.AlwaysOff
            }
        }

        model: incident.sorted_notes

        delegate: Item {
            width: notesList.width
            height: noteItem.height + 13
            
            Rectangle {
                color: "transparent"
                anchors.fill: parent
            }

            Rectangle {
                id: marker

                width: 8
                height: 8
                radius: 4
                color: ui.colors.dark1

                anchors {
                    top: parent.top
                    topMargin: 12
                    right: noteItem.left
                    rightMargin: 12

                }
            }

            Rectangle {
                id: noteItem

                color: "transparent"
                width: parent.width - 25
                height: noteText.contentHeight

                anchors {
                    left: marker.right
                    leftMargin: 12
                }

                Custom.FontText {
                    id: noteText
                    width: parent.width

                    text: expiration_date ? tr.a911_to + ` ${expiration_date} ${model.text}` : model.text
                    color: ui.colors.light2
                    font.weight: Font.Light
                    wrapMode: Text.Wrap
                    horizontalAlignment: Text.AlignLeft
                    lineHeight: 1.23
                    leftPadding: 0
                    rightPadding: 8

                    anchors.verticalCenter: parent.verticalCenter
                    anchors {
                        top: parent.top
                        topMargin: 8
                    }
                }
            }

            Rectangle {
                visible: index != notesList.count - 1 ? true : false
                width: parent.width - 18
                height: 1

                color: ui.colors.dark1
                anchors {
                    top: noteItem.bottom
                    topMargin: 16
                    right: parent.right
                }
            }
        }
    }

    Component.onCompleted: {
        app.facility_note_module.start_stream_object_notes("", incident.id)
    }
}