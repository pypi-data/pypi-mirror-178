import QtQuick 2.12
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.13
import QtQuick.Layouts 1.13

import "qrc:/resources/js/popups.js" as Popups
import "qrc:/resources/qml/components/911/" as Custom


Rectangle {
    id: workplacesListTopLevel
    color: companyStack.color
    Layout.alignment: Qt.AlignBottom | Qt.AlignLeft
    Layout.fillHeight: true
    Layout.fillWidth: true
    Layout.rightMargin: infoWorkplacesComponent.visible ? 0 : 8
    Layout.minimumHeight: {
        var height = workplacesLayout.height - panel.height - 1
//        if (height > scrollView.contentHeight) return scrollView.contentHeight
        return height
    }
    Layout.maximumHeight: Layout.minimumHeight

    property alias workplacesData: workplacesData

    Custom.BlockLoading {
        minTime: 300
        customOpacity: 0.5
        startSignals: [app.workplaces_module.getWorkplaces]
        stopSignals: [app.workplaces_module.getWorkplacesSuccess, app.workplaces_module.getWorkplacesFailed]
    }

    ScrollView {
        id: scrollView
        anchors.fill: parent
        clip: true

        ScrollBar.horizontal.policy: {
            if (workplacesData.width > scrollView.width) {
                return ScrollBar.AlwaysOn
            }
            return ScrollBar.AlwaysOff
        }

        Flickable {
            id: flick
            contentWidth: workplacesData.width
            contentHeight: workplacesListTopLevel.height

            ListView {
                id: workplacesData
                width: headerItem.width
                height: parent.height
                boundsBehavior: Flickable.StopAtBounds
                headerPositioning: ListView.OverlayHeader

                property var ownCurrentIndex: -1

                Component.onCompleted: {
                    model = appCompany.filtered_workplaces_model
                }

                ScrollBar.vertical: Custom.ScrollBar {
                    parent: scrollView
                    anchors {
                        top: parent.top
                        topMargin: 32
                        right: parent.right
                        bottom: parent.bottom
                    }

                    policy: {
                        if (workplacesData.contentHeight > workplacesData.height) {
                            return ScrollBar.AlwaysOn
                        }
                        return ScrollBar.AlwaysOff
                    }
                }

                Connections {
                    target: infoWorkplacesComponent

                    onCurrentObjectChanged: {
                        if (!infoWorkplacesComponent.currentObject) workplacesData.ownCurrentIndex = -1
                    }
                }

                header: HeaderWorkplaces {}

                delegate: Item {
                    width: parent.width
                    height: 57
                    property var header: workplacesData.headerItem

                    Custom.HandMouseArea {
                        anchors.fill: parent
                        onClicked: {
                            workplacesData.ownCurrentIndex = index
                            infoWorkplacesComponent.currentObject = [employee, workplace]
                        }
                    }

                    Connections {
                        target: app.workplaces_module

                        onUpdateWorkplaceSuccess: {
                            if (workplacesData.ownCurrentIndex != index) return
                            infoWorkplacesComponent.currentObject = [employee, workplace]
                        }
                    }

                    Custom.RoundedRect {
                        width: parent.width
                        height: parent.height - 1
                        radius: 10
                        color: workplacesData.ownCurrentIndex == index ? "transparent" : ui.colors.dark1
                        bottomRightCorner: workplacesData.ownCurrentIndex - index == 1
                        topRightCorner: {
                            if (workplacesData.ownCurrentIndex < 0) return false
                            return index - workplacesData.ownCurrentIndex == 1
                        }

                        RowLayout {
                            spacing: 4
                            anchors.fill: parent

                            Item {
                                clip: true
                                Layout.fillHeight: true
                                Layout.minimumWidth: header.headerRow.children[1] ? header.headerRow.children[1].width : 0
                                Layout.maximumWidth: Layout.minimumWidth

                                Custom.FontText {
                                    text: employee && employee.data && employee.data.email ? employee.data.email : ui.empty
                                    color: ui.colors.light3
                                    width: parent.width - 16
                                    font.pixelSize: 14
                                    wrapMode: Text.Wrap
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

                            Item {
                                clip: true
                                Layout.fillHeight: true
                                Layout.minimumWidth: header.headerRow.children[3] ? header.headerRow.children[3].width : 0
                                Layout.maximumWidth: Layout.minimumWidth

                                Custom.FontText {
                                    text: workplace && workplace.machine_id ? workplace.machine_id : ui.empty
                                    color: ui.colors.middle1
                                    width: parent.width - 16
                                    font.pixelSize: 14
                                    wrapMode: Text.Wrap
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

                            Item {
                                clip: true
                                Layout.fillHeight: true
                                Layout.minimumWidth: header.headerRow.children[5] ? header.headerRow.children[5].width : 0
                                Layout.maximumWidth: Layout.minimumWidth

                                Custom.FontText {
                                    text: workplace && workplace.name ? workplace.name : ui.empty
                                    color: ui.colors.middle1
                                    width: parent.width - 16
                                    font.pixelSize: 14
                                    wrapMode: Text.Wrap
                                    elide: Text.ElideRight
                                    textFormat: Text.PlainText
                                    maximumLineCount: 2
                                    anchors {
                                        left: parent.left
                                        leftMargin: 12
                                        verticalCenter: parent.verticalCenter
                                    }
                                }
                            }

                            Item {
                                clip: true
                                Layout.fillHeight: true
                                Layout.minimumWidth: header.headerRow.children[7] ? header.headerRow.children[7].width : 0
                                Layout.maximumWidth: Layout.minimumWidth

                                Rectangle {
                                    width: 6
                                    height: 6
                                    radius: height / 2
                                    anchors {
                                        left: parent.left
                                        leftMargin: 12
                                        verticalCenter: parent.verticalCenter
                                    }

                                    color: {
                                        if (!workplace) return "transparent"
                                        if (workplace.connection_status == "ONLINE") return ui.colors.green1
                                        if (workplace.connection_status == "OFFLINE") return ui.colors.red1
                                        if (workplace.connection_status == "LOGGED_OUT") return ui.colors.light3
                                        return "transparent"
                                    }
                                }

                                Custom.FontText {
                                    color: ui.colors.middle1
                                    width: parent.width - 16
                                    font.pixelSize: 14
                                    wrapMode: Text.Wrap
                                    elide: Text.ElideRight
                                    textFormat: Text.PlainText
                                    maximumLineCount: 2
                                    anchors {
                                        left: parent.left
                                        leftMargin: workplace && ["ONLINE", "OFFLINE", "LOGGED_OUT"].includes(workplace.connection_status) ? 24 : 12
                                        verticalCenter: parent.verticalCenter
                                    }

                                    text: {
                                        if (!workplace) return ui.empty
                                        if (workplace.connection_status == "ONLINE") return tr.online
                                        if (workplace.connection_status == "OFFLINE") return tr.offline
                                        if (workplace.connection_status == "LOGGED_OUT") return tr.logged_out_workplaces
                                        return ui.empty
                                    }
                                }
                            }

                            Item {
                                clip: true
                                Layout.fillHeight: true
                                Layout.minimumWidth: header.headerRow.children[9] ? header.headerRow.children[9].width : 0
                                Layout.maximumWidth: Layout.minimumWidth

                                Item {
                                    anchors.fill: parent
                                    visible: workplace && workplace.verificationStatus == "VERIFIED" ? true : false

                                    Rectangle {
                                        width: 1
                                        height: parent.height - 24
                                        color: companyStack.color
                                        anchors {
                                            left: parent.left
                                            verticalCenter: parent.verticalCenter
                                        }
                                    }

                                    Custom.Toggle {
                                        checked: workplace && workplace.activityStatus == "ON" ? true : false
                                        enabled: true
                                        anchors {
                                            centerIn: parent
                                            horizontalCenterOffset: 5
                                        }

                                        mouseArea.onClicked: {
                                            var settings = {}
                                            settings["id"] = workplace.id
                                            settings["activityStatus"] = checked ? "OFF" : "ON"

                                            app.workplaces_module.set_workplace_activity_status(settings)
                                        }
                                    }
                                }

                                Item {
                                    anchors.fill: parent
                                    visible: workplace && workplace.verificationStatus == "UNVERIFIED" ? true : false

                                    Rectangle {
                                        width: 24
                                        height: 24
                                        radius: height / 2
                                        color: ui.colors.dark3
                                        anchors.centerIn: parent

                                        Image {
                                            sourceSize.width: 24
                                            sourceSize.height: 24
                                            source: workplace && workplace.machine_id ? "qrc:/resources/images/icons/a-plus-icon-green.svg" : "qrc:/resources/images/icons/a-plus-icon-red.svg"
                                            anchors.centerIn: parent
                                        }

                                        Custom.HandMouseArea {
                                            onClicked: {
                                                if (!workplace || !workplace.machine_id) {
                                                    Popups.text_popup(tr.information, tr.without_machine_id)
                                                    return
                                                }

                                                Popups.create_workplace_popup(workplace)
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }

            Custom.RoundedRect {
                color: ui.colors.dark3
                radius: 10
                height: parent.height - workplacesData.contentHeight
                anchors {
                    left: parent.left
                    right: parent.right
                    bottom: parent.bottom
                }

                topRightCorner: {
                    if (appCompany.filtered_workplaces_model.length == 0 || workplacesData.ownCurrentIndex == -1) return false
                    return appCompany.filtered_workplaces_model.length - 1 == workplacesData.ownCurrentIndex
                }

                Custom.EmptySpaceLogo {
                    visible: workplacesData.model.length == 0
                }
            }
        }
    }
}