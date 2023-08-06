import QtQuick 2.12
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/desktop/"
import "qrc:/resources/qml/components/911/" as Custom


Menu {
    id: installerAccess

    x: - width - 8
    width: 250
    height: 280

    modal: false
    focus: true

    property var facilityId: ""
    property var employeeId: ""

    property var mode: null

    onClosed: {
        installerAccess.destroy()
    }

    background: Item {}

    contentItem: Rectangle {
        anchors.fill: parent
        color: ui.colors.dark3
        radius: 10

        Column {
            width: parent.width
            anchors {
                top: parent.top
                topMargin: 20
            }

            Repeater {
                id: accessRepeater
                model: ["NO_ACCESS", "1_HOUR", "2_HOURS", "4_HOURS", "8_HOURS", "PERMANENT_ACCESS"]

                delegate: Rectangle {
                    width: parent.width
                    height: 40
                    color: ui.colors.black

                    Rectangle {
                        width: parent.width
                        height: parent.height - 1
                        color: ui.colors.dark2

                        Custom.FontText {
                            maximumLineCount: 1
                            color: ui.colors.light3
                            font.pixelSize: 14
                            wrapMode: Text.NoWrap
                            elide: Text.ElideRight
                            textFormat: Text.PlainText
                            horizontalAlignment: Text.AlignLeft
                            verticalAlignment: Text.AlignVCenter
                            anchors {
                                left: parent.left
                                leftMargin: 16
                                verticalCenter: parent.verticalCenter
                            }

                            text: {
                                if (modelData == "NO_ACCESS") return tr.no_pro_permissions
                                if (modelData == "1_HOUR") return "1 " + tr.hour
                                if (modelData == "2_HOURS") return "2 " + tr.hours
                                if (modelData == "4_HOURS") return "4 " + tr.hours
                                if (modelData == "8_HOURS") return "8 " + tr.hours
                                if (modelData == "PERMANENT_ACCESS") return tr.permanent_access
                                return ""
                            }
                        }

                        Image {
                            sourceSize.width: 24
                            sourceSize.height: 24
                            source: "qrc:/resources/images/icons/connect.svg"
                            visible: delegArea.containsMouse

                            anchors {
                                right: parent.right
                                rightMargin: 16
                                verticalCenter: parent.verticalCenter
                            }
                        }

                        Custom.HandMouseArea {
                            id: delegArea

                            onClicked: {
                                var settings = {
                                    "facility_id": installerAccess.facilityId,
                                    "employee_id": installerAccess.employeeId
                                }

                                settings["permission"] = modelData == "NO_ACCESS" ? ["READ"] : ["READ", "WRITE"]
                                settings["expiration_date_to_edit"] = modelData

                                if (mode == "employee") {
                                    app.installers_module.save_facilities_permission_for_employee(settings)
                                } else {
                                    app.installers_module.save_employees_permission_for_facility(settings)
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    Connections {
        target: app.installers_module

        onSaveEmployeesPermissionForFacilitySuccess: {
            installerAccess.close()
        }

        onSaveFacilitiesPermissionForEmployeeSuccess: {
            installerAccess.close()
        }
    }
}
