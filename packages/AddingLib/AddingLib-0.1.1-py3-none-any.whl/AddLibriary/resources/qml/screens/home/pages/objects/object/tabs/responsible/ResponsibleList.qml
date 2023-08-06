import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13

import "qrc:/resources/js/popups.js" as Popups
import "qrc:/resources/qml/components/911/" as Custom


Rectangle {
    color: ui.colors.black

    ColumnLayout {
        clip: true
        spacing: 0
        anchors.fill: parent

        ListView {
            id: listView
            Layout.fillWidth: true
            Layout.minimumHeight: listView.contentHeight
            Layout.maximumHeight: parent.height
            boundsBehavior: Flickable.StopAtBounds

            model: facility.filtered_responsible_persons
            spacing: 1

            move: moveDisplaced
            moveDisplaced: Transition {
                NumberAnimation { properties: "y"; duration: 150 }
            }

            delegate: ResponsibleDelegate {}

            footer: Rectangle {
                width: parent.width
                height: visible ? 72 : 0
                color: ui.colors.black

                visible: responsibleTab.isEditable

                Custom.RoundedRect {
                    width: parent.width
                    height: parent.height

                    color: ui.colors.dark3
                    radius: 10

                    topRightCorner: currentResponsibleIndex == listView.model.length - 1 && listView.model.length != 0

                    Item {
                        width: 296
                        height: 48
                        anchors {
                            top: parent.top
                            topMargin: 16
                            left: parent.left
                            leftMargin: 16
                        }

                        Custom.Button {
                            width: parent.width
                            text: tr.a911_to_add_responsible_person
                            transparent: true
                            anchors.centerIn: parent

                            visible: responsibleTab.isEditable

                            onClicked: {
                                Popups.add_responsible_person_popup()
                            }
                        }
                    }

                    Rectangle {
                        width: listView.width
                        height: listView.model.length != 0 ? 1 : 0
                        color: ui.colors.black
                    }
                }
            }
        }

        Custom.RoundedRect {
            z: listView.z - 1
            color: ui.colors.dark3
            radius: 8
            Layout.fillWidth: true
            Layout.minimumHeight: parent.height
            Layout.maximumHeight: parent.height
        }
    }
}