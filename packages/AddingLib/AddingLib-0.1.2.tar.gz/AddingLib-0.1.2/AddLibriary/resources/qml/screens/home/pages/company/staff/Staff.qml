import QtQuick 2.12
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/" as Custom


Rectangle {
    id: staff
    color: companyStack.color

    property var ownCurrentIndex: -1

//    property var accessibleRoles: []
//    property var uiRoles: []

    RowLayout {
        anchors.fill: parent
        spacing: 8

        Item {
            Layout.alignment: Qt.AlignTop | Qt.AlignLeft
            Layout.fillWidth: true
            Layout.fillHeight: true

            ColumnLayout {
                id: staffLayout
                anchors.fill: parent
                spacing: 0

                Panel {
                    id: panel
                }

                StaffList {
                    id: staffList
                }
            }

            Rectangle {
                anchors.fill: parent
                color: ui.colors.black
                opacity: 0.5
                visible: infoStaffComponent.editMode

                Custom.HandMouseArea {
                    cursorShape: Qt.ArrowCursor
                }
            }
        }

        Info {
            id: infoStaffComponent
        }
    }
}

//    Component.onCompleted: {
//        if (!companyAccess.COMPANY_EMPLOYEES) return
//
//        accessibleRoles = app.employee_module.get_employees_accessible_roles()
//        uiRoles = app.roles_to_ui(accessibleRoles)
////        TODO: Remove then
////        uiRoles =[
////            "OWNER",
////            "SENIOR_CMS_ENGINEER",
////            "CMS_ENGINEER",
////            "HEAD_OF_INSTALLERS",
////            "INSTALLER",
////            "HEAD_OF_OPERATORS",
////            "OPERATOR",
////            "RAPID_RESPONSE_TEAM",
////            "PRO"
////        ]
//    }
//
//    Connections {
//        target: tr
//
//        onTranslation_changed: {
//            if (!companyAccess.COMPANY_EMPLOYEES) return
//
//            staff.accessibleRoles = app.employee_module.get_employees_accessible_roles()
//            staff.uiRoles = app.roles_to_ui(accessibleRoles)
//        }
//    }
//}