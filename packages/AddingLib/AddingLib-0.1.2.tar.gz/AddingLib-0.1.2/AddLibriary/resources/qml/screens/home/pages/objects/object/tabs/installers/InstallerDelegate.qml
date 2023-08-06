import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13

import "qrc:/resources/js/popups.js" as Popups
import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/qml/screens/home/pages/events/parts" as Parts
import "qrc:/resources/qml/components/911/DS3" as DS3

Rectangle {
    property var header: installersTable.headerItem

    width: header.width
    height: 56

    color: ui.colors.dark1

    Rectangle {
        width: parent.width
        height: 1

        anchors.bottom: parent.bottom

        color: ui.colors.black

    }

    RowLayout {
        height: 55

        spacing: 0

        Item {
            Layout.fillHeight: true
            Layout.minimumWidth: header.headerRow.children[0].width
            Layout.maximumWidth: header.headerRow.children[0].width
        }

        Item {
            clip: true
            Layout.fillHeight: true
            Layout.minimumWidth: header.headerRow.children[1].width
            Layout.maximumWidth: header.headerRow.children[1].width

            Custom.FontText {
                width: parent.width - 24

                anchors {
                    left: parent.left
                    leftMargin: 12
                    verticalCenter: parent.verticalCenter
                }

                text: installer ? installer.first_name + " " + installer.last_name : ""
                maximumLineCount: 2
                color: ui.colors.light3
                font.pixelSize: 16
                wrapMode: Text.Wrap
                elide: Text.ElideRight
                textFormat: Text.PlainText
                horizontalAlignment: Text.AlignLeft
                verticalAlignment: Text.AlignVCenter
            }
        }

        Parts.TableDivider { isHeader: false }

        Item {
            clip: true
            Layout.fillHeight: true
            Layout.minimumWidth: header.headerRow.children[3].width
            Layout.maximumWidth: header.headerRow.children[3].width

            Custom.FontText {
                width: parent.width - 24

                anchors {
                    left: parent.left
                    leftMargin: 12
                    verticalCenter: parent.verticalCenter
                }

                text: installer ? installer.email : ""
                maximumLineCount: 2
                color: ui.colors.middle1
                font.pixelSize: 14
                wrapMode: Text.Wrap
                elide: Text.ElideRight
                textFormat: Text.PlainText
                horizontalAlignment: Text.AlignLeft
                verticalAlignment: Text.AlignVCenter
            }
        }

        Parts.TableDivider { isHeader: false }

        Item {
            visible: !!permissions && permissions.access == "PARTIAL"
            clip: true
            Layout.fillHeight: true
            Layout.minimumWidth: header.headerRow.children[5].width
            Layout.maximumWidth: header.headerRow.children[5].width

            DS3.Icon {
                id: countdownIcon

                anchors.verticalCenter: parent.verticalCenter

                source: "qrc:/resources/images/icons/a-settings-icon.svg"
                color: ui.ds3.figure.base

                DS3.MouseArea {
                    onClicked: {
                        Popups.installer_access_popup(parent, facility.id, installer.employee_id, "facility")
                    }
                }
            }

            DS3.Countdown {
                anchors {
                    verticalCenter: parent.verticalCenter
                    left: countdownIcon.right
                    leftMargin: 4
                }

                clip: true

                endTimestamp: {
                    if (!permissions) {
                        return tr.no_pro_permissions
                    } else if (permissions.access == "PERMANENT" || permissions.access == "READONLY") {
                        return 0
                    } else {
                        return Math.round(Date.now() / 1000 + parseInt(permissions.delta))
                    }
                }
            }
        }

        Item {
            visible: !!permissions && permissions.access != "PARTIAL"
            clip: true
            Layout.fillHeight: true
            Layout.minimumWidth: header.headerRow.children[5].width

            Image {
                sourceSize.width: 40
                sourceSize.height: 40

                anchors {
                    left: parent.left
                    verticalCenter: parent.verticalCenter
                }

                source: "qrc:/resources/images/icons/a-settings-icon.svg"

                Custom.HandMouseArea {
                    onClicked: {
                        Popups.installer_access_popup(parent, facility.id, installer.employee_id, "facility")
                    }
                }
            }

            Custom.FontText {
                id: permissionText

                width: parent.width - 56

                anchors {
                    left: parent.left
                    leftMargin: 44
                    verticalCenter: parent.verticalCenter
                }

                maximumLineCount: 2
                font.pixelSize: 14
                wrapMode: Text.Wrap
                elide: Text.ElideRight
                textFormat: Text.PlainText
                horizontalAlignment: Text.AlignLeft
                verticalAlignment: Text.AlignVCenter
                color: {
                    if (!permissions) return ui.colors.light3
                    if (permissions.access == "PERMANENT") return ui.colors.green1
                    if (permissions.access == "READONLY") return ui.colors.light3
                    return ui.colors.light3
                }

                text: {
                    if (!permissions) return tr.no_pro_permissions
                    if (permissions.access == "PERMANENT") return tr.permanent_access
                    if (permissions.access == "READONLY") return tr.no_pro_permissions
                    return tr.no_pro_permissions
                }
            }
        }

        Parts.TableDivider { isHeader: false }

        Item {
            clip: true
            Layout.fillHeight: true
            Layout.minimumWidth: header.headerRow.children[7].width
            Layout.maximumWidth: header.headerRow.children[7].width

            Image {
                sourceSize.width: 24
                sourceSize.height: 24

                anchors.centerIn: parent

                source: "qrc:/resources/images/icons/control-a-minus-button.svg"

                Custom.HandMouseArea {
                    onClicked: {
                        var insertData = {
                            "employee": installer ? installer.first_name + " " + installer.last_name : "",
                            "facility": facility && facility.data && facility.data.facility_general_info ? facility.data.facility_general_info.name : "",
                        }

                        Popups.delete_installer({"facility_id": facility.id, "employee_id": installer.employee_id}, installersBody.reloadModel, "facility", insertData)
                    }
                }
            }
        }
    }
}
