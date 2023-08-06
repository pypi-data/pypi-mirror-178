import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13

import "qrc:/resources/js/popups.js" as Popups
import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/qml/screens/home/pages/events/parts"
import "qrc:/resources/qml/screens/home/pages/objects/parts"


Rectangle {
    width: header.width
    color: ui.colors.dark1
    height: 48

    property var header: objectsTable.headerItem

    Rectangle {
        width: parent.width
        height: 1
        color: ui.colors.black
        anchors.bottom: parent.bottom
    }

    ObjectMouseArea {}

    RowLayout {
        spacing: 0
        height: 48

        Item {
            Layout.fillHeight: true
            Layout.minimumWidth: header.headerRow.children[0] ? header.headerRow.children[0].width : 0
            Layout.maximumWidth: Layout.minimumWidth

            Custom.FontText {
                text: hub_id ? hub_id : ui.empty
                color: ui.colors.light3
                width: parent.width - 16
                font.pixelSize: 14
                wrapMode: Text.WordWrap
                elide: Text.ElideRight
                textFormat: Text.PlainText
                maximumLineCount: 1
                anchors {
                    left: parent.left
                    leftMargin: 12
                    verticalCenter: parent.verticalCenter
                }
            }
        }

        TableDivider { isHeader: false }

        Item {
            clip: true
            Layout.fillHeight: true
            Layout.minimumWidth: header.headerRow.children[2] ? header.headerRow.children[2].width : 0
            Layout.maximumWidth: Layout.minimumWidth

            Custom.FontText {
                text: {
                    if (!object) return ui.empty
                    if (!object.binding_initiator) return ui.empty
                    if (!object.binding_initiator.first_name && !object.binding_initiator.first_name) return ui.empty

                    var displayName = ""
                    if (object.binding_initiator.first_name) {
                        displayName += object.binding_initiator.first_name + " "
                    }
                    if (object.binding_initiator.last_name) {
                        displayName += object.binding_initiator.last_name
                    }
                    return displayName
                }
                color: ui.colors.light3
                font.pixelSize: 16
                width: parent.width - 16
                wrapMode: Text.WordWrap
                elide: Text.ElideRight
                textFormat: Text.PlainText
                maximumLineCount: 1
                anchors {
                    left: parent.left
                    leftMargin: 12
                    verticalCenter: parent.verticalCenter
                }
            }
        }

        TableDivider { isHeader: false }

        Item {
            clip: true
            Layout.fillHeight: true
            Layout.minimumWidth: header.headerRow.children[4] ? header.headerRow.children[4].width : 0
            Layout.maximumWidth: Layout.minimumWidth

            Custom.FontText {
                text: {
                    if (!object) return ui.empty
                    if (!object.binding_initiator) return ui.empty
                    if (!object.binding_initiator.email) return ui.empty

                    return object.binding_initiator.email
                }
                color: ui.colors.light3
                font.pixelSize: 14
                width: parent.width - 16
                wrapMode: Text.WordWrap
                elide: Text.ElideRight
                textFormat: Text.PlainText
                maximumLineCount: 1
                anchors {
                    left: parent.left
                    leftMargin: 12
                    verticalCenter: parent.verticalCenter
                }
            }
        }

        TableDivider { isHeader: false }

        Item {
            clip: true
            Layout.fillHeight: true
            Layout.minimumWidth: header.headerRow.children[6] ? header.headerRow.children[6].width : 0
            Layout.maximumWidth: Layout.minimumWidth

            Custom.FontText {
                id: createdDate
                color: ui.colors.middle1
                font.pixelSize: 14
                width: parent.width - 16
                wrapMode: Text.WordWrap
                elide: Text.ElideRight
                textFormat: Text.PlainText
                maximumLineCount: 2
                anchors {
                    left: parent.left
                    leftMargin: 12
                    verticalCenter: parent.verticalCenter
                }

                property var date: {
                    if (!object) return ui.empty
                    if (!object.binding_initiator) return ui.empty
                    if (!object.binding_initiator.request_date) return ui.empty
                    if (!object.binding_initiator.request_date.seconds) return ui.empty

                    return new Date(object.binding_initiator.request_date.seconds * 1000)
                }

                text: {
                    if (!createdDate.date) return ui.empty
                    return createdDate.date.toLocaleString(application.locale, application.shortDateTimeFormat)
                }
            }
        }

        TableDivider { isHeader: false }

        Item {
            clip: true
            Layout.fillHeight: true
            Layout.minimumWidth: header.headerRow.children[8] ? header.headerRow.children[8].width : 0
            Layout.maximumWidth: Layout.minimumWidth

            Item {
                width: 72
                height: 24
                anchors.centerIn: parent

                Rectangle {
                    width: 24
                    height: width
                    radius: height / 2
                    color: ui.colors.dark3
                    visible: hub_id ? true : false
                    anchors.left: parent.left

                    enabled: companyAccess.OBJECTS_MONITORING_REQUEST_FROM_USER_APPROVE
                    opacity: enabled ? 1 : 0.3

                    Image {
                        sourceSize.width: 20
                        sourceSize.height: 20
                        source: "qrc:/resources/images/icons/connect.svg"
                        anchors.centerIn: parent
                    }

                    Custom.HandMouseArea {
                        onClicked: {
                            var settings = {}

                            settings["hub_id"] = hub_id ? hub_id : ""
                            settings["registration_number"] = number ? number : ""
                            settings["name"] = name ? name : ""
                            settings["facility_id"] = object.facility_id ? object.facility_id : ""

                            Popups.create_911_channel_popup(settings)
                        }
                    }
                }

                Rectangle {
                    width: 24
                    height: width
                    radius: height / 2
                    color: ui.colors.dark3
                    visible: hub_id ? true : false
                    anchors.right: parent.right

                    enabled: companyAccess.OBJECT_MONITORING_DELETE
                    opacity: enabled ? 1 : 0.3

                    Image {
                        sourceSize.width: 20
                        sourceSize.height: 20
                        source: "qrc:/resources/images/icons/disconnect.svg"
                        anchors.centerIn: parent
                    }

                    Custom.HandMouseArea {
                        onClicked: app.bindings_module.reject_monitoring_application(hub_id ? hub_id : "")
                    }
                }
            }
        }
    }
}