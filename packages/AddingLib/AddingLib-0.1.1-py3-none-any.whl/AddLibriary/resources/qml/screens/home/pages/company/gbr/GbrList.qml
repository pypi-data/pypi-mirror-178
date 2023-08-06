import QtQuick 2.12
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/" as Custom


Rectangle {
    id: gbrListTopLevel
    color: companyStack.color
    Layout.alignment: Qt.AlignBottom | Qt.AlignLeft
    Layout.fillHeight: true
    Layout.fillWidth: true
    Layout.rightMargin: infoGbrComponent.visible ? 0 : 8
    Layout.minimumHeight: {
        var height = gbrLayout.height - panel.height - 1
//        if (height > scrollView.contentHeight) return scrollView.contentHeight
        return height
    }
    Layout.maximumHeight: Layout.minimumHeight

    property alias gbrData: gbrData

    ScrollView {
        id: scrollView
        anchors.fill: parent
        clip: true


        ScrollBar.horizontal.policy: {
            if (gbrData.width > scrollView.width) {
                return ScrollBar.AlwaysOn
            }
            return ScrollBar.AlwaysOff
        }
        Flickable {
            id: flick
            contentWidth: gbrData.width
            contentHeight: gbrListTopLevel.height

            ListView {
                id: gbrData
                width: headerItem.width
                height: parent.height
                property var ownCurrentIndex: -1
                headerPositioning: ListView.OverlayHeader
                boundsBehavior: Flickable.StopAtBounds

                Component.onCompleted: {
                    model = appCompany.filtered_fast_response_teams_model
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
                        if (gbrData.contentHeight > gbrData.height) {
                            return ScrollBar.AlwaysOn
                        }
                        return ScrollBar.AlwaysOff
                    }
                }

                Connections {
                    target: infoGbrComponent

                    onCurrentObjectChanged: {
                        if (!infoGbrComponent.currentObject) gbrData.ownCurrentIndex = -1
                    }
                }
                header: HeaderGBR {}
                delegate: Item {
                    width: parent.width
                    height: 57
                    property var header: gbrData.headerItem

                    Custom.HandMouseArea {
                        anchors.fill: parent
                        onClicked: {
                            gbrData.ownCurrentIndex = index
                            infoGbrComponent.currentObject = fast_response_team
                        }
                    }

                    Custom.RoundedRect {
                        width: parent.width
                        height: parent.height - 1
                        radius: 10
                        color: gbrData.ownCurrentIndex == index ? "transparent" : ui.colors.dark1
                        bottomRightCorner: gbrData.ownCurrentIndex - index == 1
                        topRightCorner: {
                            if (gbrData.ownCurrentIndex < 0) return false
                            return index - gbrData.ownCurrentIndex == 1
                        }

                        RowLayout {
                            spacing: 4
                            anchors.fill: parent

                            Item {
                                id: nameItem
                                clip: true

                                Layout.minimumWidth: header.headerRow.children[1].width
                                Layout.maximumWidth: header.headerRow.children[1].width
                                Layout.minimumHeight: parent.height
                                Layout.maximumHeight: parent.height
                                Item {
                                    id: userImageItem
                                    width: 50
                                    height: 50
                                    Custom.UserImage {
                                        width: 38
                                        height: 38
                                        imageSource: Object.keys(fast_response_team.photos).length !== 0 ? fast_response_team.photos["64x64"] : ""
                                        userName: fast_response_team ? fast_response_team.data.name : ""
                                        anchors.centerIn: parent
                                    }
                                    anchors {
                                        left: parent.left
                                        leftMargin: 12
                                    }
                                }
                                Custom.FontText {
                                    text: fast_response_team.data.name
                                    width: parent.width
                                    maximumLineCount: 2
                                    color: ui.colors.white
                                    font.pixelSize: 16
                                    wrapMode: Text.WordWrap
                                    elide: Text.ElideRight
                                    textFormat: Text.AutoText

                                    anchors {
                                        verticalCenter: parent.verticalCenter
                                        left: userImageItem.right
                                        leftMargin: 4
                                    }
                                }
                            }

                            Item {
                                id: phoneItem
                                clip: true
                                Layout.minimumWidth: header.headerRow.children[3].width
                                Layout.maximumWidth: header.headerRow.children[3].width
                                Layout.minimumHeight: parent.height
                                Layout.maximumHeight: parent.height

                                Custom.FontText {
                                    text: {
                                        if (!fast_response_team.data.phone_numbers.length) return tr.a911_unknown
                                        return fast_response_team.data.phone_numbers[0].number
                                    }
                                    width: parent.width
                                    color: ui.colors.white
                                    opacity: 0.6
                                    font.pixelSize: 14
                                    wrapMode: Text.WordWrap
                                    elide: Text.ElideRight
                                    textFormat: Text.AutoText

                                    anchors {
                                        verticalCenter: parent.verticalCenter
                                        left: parent.left
                                        leftMargin: 8
                                    }
                                }
                            }

                            Item {
                                id: carItem
                                clip: true
                                Layout.minimumWidth: header.headerRow.children[5].width
                                Layout.maximumWidth: header.headerRow.children[5].width
                                Layout.minimumHeight: parent.height
                                Layout.maximumHeight: parent.height

                                Custom.FontText {
                                    text: {
                                        if(!fast_response_team.data.vehicle.registration_number || !fast_response_team.data.vehicle.description) {
                                            return fast_response_team.data.vehicle.registration_number +  fast_response_team.data.vehicle.description
                                        }
                                        return fast_response_team.data.vehicle.registration_number + ", " + fast_response_team.data.vehicle.description
                                    }
                                    width: parent.width
                                    color: ui.colors.white
                                    font.pixelSize: 14
                                    wrapMode: Text.WordWrap
                                    elide: Text.ElideRight
                                    textFormat: Text.AutoText

                                    anchors {
                                        verticalCenter: parent.verticalCenter
                                        left: parent.left
                                        leftMargin: 8
                                    }
                                }
                            }

                            Item {
                                id: toggleItem
                                Layout.alignment: Qt.AlignRight
                                Layout.minimumHeight: parent.height
                                Layout.maximumHeight: parent.height
                                Layout.minimumWidth: header.headerRow.children[7].width
                                Layout.maximumWidth: header.headerRow.children[7].width

                                enabled: companyAccess.RRU_ADJUST

                                Item {
                                    anchors.fill: parent
                                    Rectangle {
                                        width: 1
                                        height: parent.height - 24
                                        color: companyStack.color
                                        anchors {
                                            verticalCenter: parent.verticalCenter
                                            left: parent.left
                                        }
                                    }

                                    Custom.Toggle {
                                        checked: fast_response_team.data.active
                                        anchors {
                                            centerIn: parent
                                            horizontalCenterOffset: 5
                                        }

                                        mouseArea.onClicked: {
                                            var data = {"id": fast_response_team.id, "active": !checked}
                                            app.fast_response_team_module.set_fast_response_team_status(data)
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }

            Custom.RoundedRect {
               anchors {
                   left: parent.left
                   right: parent.right
                   bottom: parent.bottom
               }
                height: parent.height - gbrData.contentHeight

                color: ui.colors.dark3

                Custom.EmptySpaceLogo {
                    visible: {
                        return gbrData.model.length == 0
                    }

                }

                radius: 10
                topRightCorner: {
                    if (appCompany.filtered_fast_response_teams_model.length == 0 || gbrList.gbrData.ownCurrentIndex == -1) return false
                    return appCompany.filtered_fast_response_teams_model.length - 1 == gbrList.gbrData.ownCurrentIndex
                }
            }
        }
    }
}
