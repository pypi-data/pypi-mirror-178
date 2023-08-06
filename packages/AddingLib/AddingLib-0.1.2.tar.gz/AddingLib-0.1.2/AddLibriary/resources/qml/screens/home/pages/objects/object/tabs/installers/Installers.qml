import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13

import "qrc:/resources/js/popups.js" as Popups
import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/qml/screens/home/pages/parts/"


Rectangle {
    id: installersBody
    clip: true
    color: ui.colors.black

    signal reloadModel()

    onReloadModel: {
        if (!facility.id) return
        app.installers_module.get_employees_permission_for_facility({"facility_id": facility.id})
    }

    ColumnLayout {
        anchors.fill: parent
        spacing: 1

        Rectangle {
            color: ui.colors.dark3
            Layout.minimumHeight: 48
            Layout.maximumHeight: 48
            Layout.fillWidth: true

            Custom.FontText {
                text: tr.installer_access
                color: ui.colors.light3
                width: parent.width / 2 - 18
                height: parent.height / 2
                font.pixelSize: 14
                wrapMode: Text.Wrap
                elide: Text.ElideRight
                textFormat: Text.PlainText
                maximumLineCount: 1
                verticalAlignment: Text.AlignVCenter
                horizontalAlignment: Text.AlignLeft
                anchors {
                    top: parent.top
                    topMargin: 3
                    left: parent.left
                    leftMargin: 18
                }
            }

            Custom.FontText {
                text: tr.installers + ":  " + installersTable.model.length
                color: ui.colors.middle4
                width: parent.width / 2 - 18
                height: parent.height / 2
                font.pixelSize: 12
                wrapMode: Text.Wrap
                elide: Text.ElideRight
                textFormat: Text.PlainText
                maximumLineCount: 1
                verticalAlignment: Text.AlignVCenter
                horizontalAlignment: Text.AlignLeft
                anchors {
                    left: parent.left
                    leftMargin: 18
                    bottom: parent.bottom
                    bottomMargin: 1
                }
            }

            Item {
                id: reloadButtonItem
                width: refreshIcon.width + refreshText.width + 4
                height: 32

                anchors {
                    right: addButtonItem.left
                    rightMargin: 24
                    verticalCenter: parent.verticalCenter
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
                        installersBody.reloadModel()
                    }
                }
            }

            Item {
                id: addButtonItem
                width: 136
                height: 40

                anchors {
                    right: parent.right
                    rightMargin: 8
                    verticalCenter: parent.verticalCenter
                }

                Custom.Button {
                    width: parent.width
                    text: tr.assign_new_object
                    transparent: true
                    color: ui.colors.green1
                    anchors.centerIn: parent
                    backgroundItem.implicitHeight: down ? 32 : 36

                    onClicked: {
                        Popups.add_installer_popup(facility)
                    }
                }
            }
        }

        ScrollView {
            id: scrollView
            clip: true
            Layout.fillWidth: true
            Layout.fillHeight: true

            ScrollBar.horizontal.policy: {
                if (installersTable.width > scrollView.width) {
                    return ScrollBar.AlwaysOn
                }
                return ScrollBar.AlwaysOff
            }

            Flickable {
                contentWidth: installersTable.width
                contentHeight: scrollView.height

                ListView {
                    id: installersTable
                    clip: true
                    spacing: 0
                    width: headerItem.width
                    height: parent.height

                    headerPositioning: ListView.OverlayHeader
                    boundsBehavior: Flickable.StopAtBounds

                    model: facility ? facility.filtered_installers_model : []

                    header: Header {}
                    delegate: InstallerDelegate {}

                    Custom.EmptySpaceLogo {
                        visible: installersTable.model.length == 0
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
                }
            }
        }
    }

    Custom.BlockLoading {
        id: installersLoader
        minTime: 300
        startSignals: [app.installers_module.getEmployeesPermissionForFacility]
        stopSignals: [app.installers_module.getEmployeesPermissionForFacilitySuccess, app.installers_module.getEmployeesPermissionForFacilityFailed]
    }

    Connections {
        target: objectView

        onCurrentTabIndexChanged: {
            if (currentTabIndex == 7) installersBody.reloadModel()
        }
    }

    Connections {
        target: app.installers_module

        onSaveEmployeesPermissionForFacilitySuccess: {
            installersBody.reloadModel()
        }
    }

    Component.onCompleted: {
        if (currentTabIndex == 7) installersBody.reloadModel()
    }
}
