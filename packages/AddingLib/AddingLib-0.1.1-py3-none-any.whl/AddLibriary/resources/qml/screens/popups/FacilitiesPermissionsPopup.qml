import QtQuick 2.12
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.13
import QtGraphicalEffects 1.13

import "qrc:/resources/js/popups.js" as Popups
import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/qml/components/desktop/"
import "qrc:/resources/qml/screens/home/pages/events/parts"


AjaxPopup {
    id: popup
    objectName: "facilitiesPermissionsPopup"
    width: parent.width - 464
    height: parent.height - 136 > 632 ? parent.height - 136 : 632
    closePolicy: Popup.NoAutoClose

    modal: true
    focus: true

    anchors.centerIn: parent

    signal reloadModel()

    onReloadModel: {
        if (!employee.id) return
        app.installers_module.get_facilities_permissions_for_employee({"employee_id": employee.id})
    }

    property var employee: null

    property var assignedCount: appCompany.assigned_facilities.length

    onOpened: {
        popup.reloadModel()
    }

    onClosed: {
        appCompany.filtered_assigned_facilities.set_filter("")
    }

    Timer {
        id: facilitiesTimer
        repeat: true
        running: true
        interval: 1000

        onTriggered: {
            // timer logic
            appCompany.assigned_facilities.update_all()
        }
    }

    background: Rectangle {
        color: "black"
        opacity: 0.6
        width: application.width
        height: application.height
        x: 0 - parent.x
        y: 0 - parent.y
    }

    contentItem: Rectangle {
        anchors.fill: parent
        color: ui.colors.dark3
        radius: 8

        Custom.PopupHeader {
            id: header
            width: parent.width
            height: 88
            radius: parent.radius
            anchors.top: parent.top
            headerTitle.anchors.leftMargin: 32

            title: popup.assignedCount ? tr.assigned_object + "  (" + popup.assignedCount + ")" : tr.assigned_object

            closeArea.onClicked: {
                popup.close()
            }

            Custom.FontText {
                color: ui.colors.middle1
                width: parent.width / 2
                height: 16
                font.pixelSize: 12
                wrapMode: Text.Wrap
                elide: Text.ElideMiddle
                textFormat: Text.PlainText
                maximumLineCount: 2
                verticalAlignment: Text.AlignVCenter
                horizontalAlignment: Text.AlignHCenter
                anchors {
                    top: parent.top
                    topMargin: 56
                    horizontalCenter: parent.horizontalCenter
                }

                text: {
                    var tmpName = ""
                    var tmpEmail = ""
                    var tmpDiv = "  •  "

                    if (!popup.employee) return ui.empty + tmpDiv + ui.empty
                    if (!popup.employee.data) return ui.empty + tmpDiv + ui.empty

                    tmpName = popup.employee.data.first_name + " " + popup.employee.data.last_name
                    tmpName = tmpName && tmpName != " " ? tmpName : ui.empty

                    tmpEmail = popup.employee.data.email
                    tmpEmail = tmpEmail ? tmpEmail : ui.empty

                    return tmpName + tmpDiv + tmpEmail
                }
            }
        }

        Item {
            width: 288
            height: 48
            anchors {
                top: header.bottom
                left: parent.left
                leftMargin: 32
            }

            Custom.SearchField {
                width: parent.width
                height: 40
                anchors.centerIn: parent
                placeHolderText: tr.search_via_object

                onSearchStarted: {
                    appCompany.filtered_assigned_facilities.set_filter(data)
                }
            }
        }

        Item {
            width: refreshIcon.width + refreshText.width + 4
            height: 48

            anchors {
                top: header.bottom
                right: assignButtonItem.left
                rightMargin: 24
            }

            Image {
                id: refreshIcon
                sourceSize.width: 16
                sourceSize.height: 16
                source: "qrc:/resources/images/desktop/button_icons/refresh.svg"
                anchors {
                    left: parent.left
                    verticalCenter: parent.verticalCenter
                }

                RotationAnimator {
                    id: refreshAnim
                    target: refreshIcon
                    from: 0
                    to: 360
                    duration: 500
                }
            }

            Custom.FontText {
                id: refreshText
                width: contentWidth
                height: contentHeight
                text: tr.Refresh_button_desktop
                color: ui.colors.green1
                font.bold: true
                font.pixelSize: 14
                verticalAlignment: Text.AlignVCenter
                anchors {
                    right: parent.right
                    verticalCenter: parent.verticalCenter
                }
            }

            Custom.HandMouseArea {
                onClicked: {
                    refreshAnim.start()
                    popup.reloadModel()
                }
            }
        }

        Item {
            id: assignButtonItem
            width: 136
            height: 48
            anchors {
                top: header.bottom
                right: parent.right
                rightMargin: 32
            }

            Custom.Button {
                id: assignButton
                width: parent.width
                text: tr.assign_new_object
                transparent: true
                color: ui.colors.green1
                loading_background_color: ui.colors.dark3
                anchors.centerIn: parent
                backgroundItem.implicitHeight: down ? 32 : 36

                onClicked: {
                    Popups.add_installer_facility_popup(employee)
                }
            }
        }

        Rectangle {
            id: tableItem
            width: parent.width - 64
            color: ui.colors.dark4

            anchors {
                top: header.bottom
                topMargin: 64
                bottom: parent.bottom
                bottomMargin: 32
                horizontalCenter: parent.horizontalCenter
            }

            ScrollView {
                id: scrollView
                clip: true
                anchors.fill: parent

                ScrollBar.horizontal.policy: {
                    if (facilitiesTable.width > scrollView.width) {
                        return ScrollBar.AlwaysOn
                    }
                    return ScrollBar.AlwaysOff
                }

                Flickable {
                    contentWidth: facilitiesTable.width
                    contentHeight: scrollView.height

                    ListView {
                        id: facilitiesTable
                        clip: true
                        spacing: 0
                        width: headerItem.width
                        height: parent.height

                        headerPositioning: ListView.OverlayHeader
                        boundsBehavior: Flickable.StopAtBounds

                        model: appCompany ? appCompany.filtered_assigned_facilities : []

                        Custom.EmptySpaceLogo {
                            visible: facilitiesTable.model.length == 0
                        }

                        ScrollBar.vertical: Custom.ScrollBar {
                            id: control
                            parent: scrollView
                            anchors {
                                top: parent.top
                                topMargin: 32
                                right: parent.right
                                bottom: parent.bottom
                            }
                        }

                        header: Rectangle {
                            id: topLevel
                            width: stableWidth + additionalCell.Layout.maximumWidth
                            height: 34
                            z: 3
                            color: ui.colors.black

                            property var stableWidth: {
                                var s = 0
                                for (var i = 0; i < headerRow.children.length - 1; i++ ) {
                                    s += headerRow.children[i].width
                                }
                                return s
                            }

                            property alias headerRow: headerRow

                            Rectangle {
                                width: parent.width
                                height: parent.height - 1
                                color: ui.colors.dark2
                                anchors.top: parent.top

                                RowLayout {
                                    id: headerRow
                                    spacing: 0
                                    height: parent.height

                                    Item {
                                        Layout.fillHeight: true
                                        Layout.minimumWidth: 0
                                        Layout.maximumWidth: 0
                                    }

                                    HeaderCell {
                                        text: tr.number
                                        Layout.preferredWidth: tableItem.width * 0.2
                                    }

                                    TableDivider {}

                                    HeaderCell {
                                        text: tr.object_name
                                        Layout.preferredWidth: tableItem.width * 0.25
                                    }

                                    TableDivider {}

                                    HeaderCell {
                                        text: tr.a911_hub_id
                                        Layout.preferredWidth: tableItem.width * 0.15
                                    }

                                    TableDivider {}

                                    HeaderCell {
                                        text: tr.permissions
                                        Layout.preferredWidth: tableItem.width * 0.25
                                    }

                                    TableDivider {}

                                    HeaderCell {
                                        id: additionalCell
                                        text: ""
                                        Layout.maximumWidth: {
                                            if (tableItem.width - topLevel.stableWidth < 72) return 72
                                            return tableItem.width - topLevel.stableWidth
                                        }
                                        Layout.minimumWidth: Layout.maximumWidth
                                    }
                                }
                            }
                        }

                        delegate: Rectangle {
                            width: header.width
                            color: ui.colors.dark1
                            height: 56

                            property var header: facilitiesTable.headerItem

                            Rectangle {
                                width: parent.width
                                height: 1
                                color: ui.colors.black
                                anchors.bottom: parent.bottom
                            }

                            RowLayout {
                                spacing: 0
                                height: 55

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
                                        text: facility ? facility.registration_number : ""
                                        width: parent.width - 24
                                        maximumLineCount: 2
                                        color: ui.colors.middle1
                                        font.pixelSize: 14
                                        wrapMode: Text.Wrap
                                        elide: Text.ElideRight
                                        textFormat: Text.PlainText
                                        horizontalAlignment: Text.AlignLeft
                                        verticalAlignment: Text.AlignVCenter
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
                                    Layout.minimumWidth: header.headerRow.children[3].width
                                    Layout.maximumWidth: header.headerRow.children[3].width

                                    Custom.FontText {
                                        text: facility ? facility.name : ""
                                        width: parent.width - 24
                                        maximumLineCount: 2
                                        color: ui.colors.light3
                                        font.pixelSize: 16
                                        wrapMode: Text.Wrap
                                        elide: Text.ElideRight
                                        textFormat: Text.PlainText
                                        horizontalAlignment: Text.AlignLeft
                                        verticalAlignment: Text.AlignVCenter
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
                                    Layout.minimumWidth: header.headerRow.children[5].width
                                    Layout.maximumWidth: header.headerRow.children[5].width

                                    Custom.FontText {
                                        text: facility ? facility.hub_id : ""
                                        width: parent.width - 24
                                        maximumLineCount: 2
                                        color: ui.colors.light3
                                        font.pixelSize: 14
                                        wrapMode: Text.Wrap
                                        elide: Text.ElideRight
                                        textFormat: Text.PlainText
                                        horizontalAlignment: Text.AlignLeft
                                        verticalAlignment: Text.AlignVCenter
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
                                    Layout.minimumWidth: header.headerRow.children[7].width
                                    Layout.maximumWidth: header.headerRow.children[7].width

                                    Image {
                                        sourceSize.width: 40
                                        sourceSize.height: 40
                                        source: "qrc:/resources/images/icons/a-settings-icon.svg"
                                        anchors {
                                            left: parent.left
                                            verticalCenter: parent.verticalCenter
                                        }

                                        Custom.HandMouseArea {
                                            onClicked: {
                                                Popups.installer_access_popup(parent, facility.facility_id, employee.id, "employee")
                                            }
                                        }
                                    }

                                    Custom.FontText {
                                        id: permissionText
                                        width: parent.width - 56
                                        maximumLineCount: 2
                                        font.pixelSize: 14
                                        wrapMode: Text.Wrap
                                        elide: Text.ElideRight
                                        textFormat: Text.PlainText
                                        horizontalAlignment: Text.AlignLeft
                                        verticalAlignment: Text.AlignVCenter
                                        anchors {
                                            left: parent.left
                                            leftMargin: 44
                                            verticalCenter: parent.verticalCenter
                                        }

                                        color: {
                                            if (!permissions) return ui.colors.light3
                                            if (permissions.access == "PERMANENT") return ui.colors.green1
                                            if (permissions.access == "PARTIAL") return ui.colors.red1
                                            if (permissions.access == "READONLY") return ui.colors.light3
                                            return ui.colors.light3
                                        }

                                        text: {
                                            if (!permissions) return tr.no_pro_permissions
                                            if (permissions.access == "PERMANENT") return tr.permanent_access
                                            if (permissions.access == "PARTIAL") return util.format_timedelta(permissions.delta)
                                            if (permissions.access == "READONLY") return tr.no_pro_permissions
                                            return tr.no_pro_permissions
                                        }
                                    }
                                }

                                TableDivider { isHeader: false }

                                Item {
                                    clip: true
                                    Layout.fillHeight: true
                                    Layout.minimumWidth: header.headerRow.children[9].width
                                    Layout.maximumWidth: header.headerRow.children[9].width

                                    Image {
                                        sourceSize.width: 24
                                        sourceSize.height: 24
                                        source: "qrc:/resources/images/icons/control-a-minus-button.svg"
                                        anchors.centerIn: parent

                                        Custom.HandMouseArea {
                                            onClicked: {
                                                var insertData = {
                                                    "employee": employee && employee.data ? employee.data.first_name + " " + employee.data.last_name : "",
                                                    "facility": facility ? facility.name : "",
                                                }

                                                Popups.delete_installer({"facility_id": facility.facility_id, "employee_id": employee.id}, popup.reloadModel, "employee", insertData)
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }

            Custom.BlockLoading {
                id: facilitiesLoader
                minTime: 300
                startSignals: [app.installers_module.getFacilitiesPermissionsForEmployee]
                stopSignals: [app.installers_module.getFacilitiesPermissionsForEmployeeSuccess, app.installers_module.getFacilitiesPermissionsForEmployeeFailed]
            }
        }
    }

    Connections {
        target: app.installers_module

        onSaveFacilitiesPermissionForEmployeeSuccess: {
            popup.reloadModel()
        }
    }
}
