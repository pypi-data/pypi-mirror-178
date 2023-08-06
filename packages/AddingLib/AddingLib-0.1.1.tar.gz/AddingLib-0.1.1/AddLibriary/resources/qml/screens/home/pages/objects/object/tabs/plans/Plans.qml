import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/animations/" as Anime
import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/qml/screens/home/pages/parts/"
import "qrc:/resources/js/popups.js" as Popups



Rectangle {
    id: planTab

    property bool isEditable: facility.editable_sections.includes("MEDIA")

    color: ui.colors.black
    property var currentMediaIndex: -1

    Anime.ClickAnimation { id: click }

    onCurrentMediaIndexChanged: {
        if (currentMediaIndex == -1) {
            planViewLoader.setSource("")
            return
        }
        planViewLoader.setSource("qrc:/resources/qml/screens/home/pages/objects/object/tabs/plans/SliderPlans.qml", {"tabs": planTab , "grid": gridPhotosPlans})
    }

    FocusScopePlans {
        id: focusArea
    }

    ColumnLayout {
        anchors.fill: parent
        spacing: 1

        Rectangle {
            color: ui.colors.dark3
            Layout.fillWidth: true
            Layout.minimumHeight: 48
            Layout.maximumHeight: 48

            RowLayout {
                id: rowLayout
                height: 48
                spacing: 8
                anchors {
                    bottom: parent.bottom
                    left: parent.left
                    leftMargin: 8
                }

                property var currentTab: allTBtn

                PanelTab {
                    id: allTBtn
                    text: tr.scenario_trigger_all
                    objectName: "allTBtn"
                    selected: rowLayout.currentTab == allTBtn
                    Layout.alignment: Qt.AlignVCenter
                    Custom.HandMouseArea {
                        anchors.fill: parent
                        onClicked: {
                            rowLayout.currentTab = allTBtn
                            planTab.currentMediaIndex = -1
                            facility.proxy_facility_media.set_filter("ALL")
                        }
                    }
                }

                PanelTab {
                    id: drivingDirectionsBtn
                    text: tr.a911_driving_directions
                    objectName: "drivingDirectionsBtn"
                    selected: rowLayout.currentTab == drivingDirectionsBtn
                    Layout.alignment: Qt.AlignVCenter
                    Custom.HandMouseArea {
                        anchors.fill: parent
                        onClicked: {
                            rowLayout.currentTab = drivingDirectionsBtn
                            planTab.currentMediaIndex = -1
                            facility.proxy_facility_media.set_filter("ROAD_MAP")
                        }
                    }
                }

                PanelTab {
                    id: floorPlansBtn
                    text: tr.a911_building_plans
                    objectName: "floorPlansBtn"
                    selected: rowLayout.currentTab == floorPlansBtn
                    Layout.alignment: Qt.AlignVCenter
                    Custom.HandMouseArea {
                        anchors.fill: parent
                        onClicked: {
                            rowLayout.currentTab = floorPlansBtn
                            planTab.currentMediaIndex = -1
                            facility.proxy_facility_media.set_filter("FLOOR_PLAN")
                        }
                    }
                }
            }
        }

        RowLayout {
            Layout.fillWidth: true
            Layout.fillHeight: true
            spacing: 8

            Rectangle {
                id: imagesArea
                color: "#1E1E1E"
                Layout.fillWidth: true
                Layout.minimumWidth: 512
                Layout.fillHeight: true


                GridView {
                    id: gridPhotosPlans
                    anchors.fill: parent
                    cellWidth: 128
                    cellHeight: 144
                    model: facility.proxy_facility_media
                    clip: true

                    delegate: Rectangle {
                        id: imageCell
                        width: 128
                        height: 144
                        color: {
                            if (currentMediaIndex == index) return ui.colors.green3
                            if (imageRect.containsMouse) return ui.colors.dark2
                            return "transparent"
                        }
                        property var visibleEditIcon: false


                        Item {
                            id: schemeImageItem
                            width: 112
                            height: 112
                            anchors {
                                top: parent.top
                                topMargin: 4
                                horizontalCenter: parent.horizontalCenter
                            }

                            Image {
                                fillMode: Image.PreserveAspectFit
                                source: url ? url["128x128"] : ""
                                anchors.fill: parent
                            }
                        }

                        Item {
                            width: parent.width
                            anchors {
                                top: schemeImageItem.bottom
                                topMargin: 4
                                bottom: parent.bottom
                                bottomMargin: 4
                            }

                            Custom.FontText {
                                text: media ? media.caption : ""
                                width: parent.width - 8
                                height: contentHeight
                                anchors.centerIn: parent
                                color: currentMediaIndex == index ? ui.colors.dark3 : ui.colors.light3
                                font.pixelSize: 12
                                maximumLineCount: 1
                                elide: Text.ElideRight
                                textFormat: Text.PlainText
                                verticalAlignment: Text.AlignVCenter
                                horizontalAlignment: Text.AlignHCenter
                            }
                        }

                        Custom.HandMouseArea {
                            id: imageRect
                            anchors.fill: parent
                            preventStealing: true
                            onClicked: {
                                currentMediaIndex = index
                            }
                            onEntered: visibleEditIcon = true
                            onExited: visibleEditIcon = false
                        }

                        IconContexMenu {
                            id: iconMenu
                            visible: planTab.isEditable && (visibleEditIcon || contextMenu.opened)
                            MouseArea {
                                id: mouseIconEditMenu
                                anchors.fill: parent
                                acceptedButtons: Qt.LeftButton | Qt.RightButton
                                preventStealing: true
                                onClicked: {
                                    contextMenu.popup()
                                }
                                onPressAndHold: {
                                    if (mouse.source === Qt.MouseEventNotSynthesized)
                                        contextMenu.popup()
                                }
                                EditMenu {
                                    id: contextMenu
                                    model: gridPhotosPlans.model
                                    indexMenu: index
                                }
                            }
                        }
                    }
                    footer: Item {
                        id: buttonItem
                        width: 300
                        height: 80
                        visible: planTab.isEditable

                        Custom.Button {
                            anchors.centerIn: buttonItem
                            width: 240
                            height: 40
                            text: tr.a911_add_photo
                            transparent: true
                            focusPolicy: Qt.NoFocus

                            anchors {
                                leftMargin: 30
                                verticalCenter: parent.verticalCenter
                            }
                            onClicked: Popups.upload_facility_media()
                        }
                    }
                }
            }

            Rectangle {
                Layout.minimumWidth: 496
                Layout.fillHeight: true
                Layout.fillWidth: true
                color: ui.colors.dark4
                Custom.EmptySpaceLogo {}
                Loader {
                    id: planViewLoader
                    anchors.fill: parent
                    Custom.HandMouseArea {
                        id: hoverArea
                        anchors.fill: parent
                        cursorShape: Qt.ArrowCursor
                        preventStealing: true
                    }
                }

                Rectangle {
                    id: leftArrow
                    width: 48
                    height: 48
                    radius: height / 2
                    color: ui.colors.dark3
                    opacity: 0.8
                    visible: (hoverArea.containsMouse || leftArrowArea.containsMouse || rightArrowArea.containsMouse) && currentMediaIndex != -1


                    anchors {
                        verticalCenter: parent.verticalCenter
                        left: parent.left
                        leftMargin: 8
                    }

                    Image {
                        sourceSize.width: 48
                        sourceSize.height: 48
                        anchors.centerIn: parent
                        source: "qrc:/resources/images/icons/gallery-left.svg"
                    }

                    Custom.HandMouseArea {
                        id: leftArrowArea
                        onClicked: {
                            click.animate(leftArrow)
                            focusArea.Keys.leftPressed(true)
                        }
                    }
                }

                Rectangle {
                    id: rightArrow
                    width: 48
                    height: 48
                    radius: height / 2
                    color: ui.colors.dark3
                    visible:  (hoverArea.containsMouse || leftArrowArea.containsMouse || rightArrowArea.containsMouse) && currentMediaIndex != -1

                    anchors {
                        verticalCenter: parent.verticalCenter
                        right: parent.right
                        rightMargin: 16
                    }

                    Image {
                        sourceSize.width: 48
                        sourceSize.height: 48
                        anchors.centerIn: parent
                        source: "qrc:/resources/images/icons/gallery-right.svg"
                    }

                    Custom.HandMouseArea {
                        id: rightArrowArea
                        onClicked: {
                            click.animate(rightArrow)
                            focusArea.Keys.rightPressed(true)
                        }
                    }
                }
            }
        }
    }
    onVisibleChanged: {
        if (!visible) {
            currentMediaIndex = -1
        }
    }

    Component.onCompleted: {
        if (!facility.id) return

        app.facility_media_module.start_facility_media_stream()
        focusArea.forceActiveFocus()
    }

    Connections {
        target: appCompany.current_facility ? appCompany.current_facility.facility_media : null

        onFacilityMediaDeleted: {
            planTab.currentMediaIndex = -1
        }

        onFacilityMediaUpdated: {
           planTab.currentMediaIndex = -1
        }
    }
}

